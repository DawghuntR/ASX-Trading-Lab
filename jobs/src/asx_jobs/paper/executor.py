"""End-of-day order executor for paper trading."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from asx_jobs.database import Database
from asx_jobs.logging import get_logger

logger = get_logger(__name__)


@dataclass
class FillResult:
    """Result of filling an order."""

    order_id: int
    instrument_id: int
    symbol: str
    side: str
    quantity: int
    fill_price: float
    total_value: float
    success: bool
    message: str


@dataclass
class ExecutionSummary:
    """Summary of EOD execution run."""

    execution_date: str
    orders_processed: int
    orders_filled: int
    orders_rejected: int
    total_buy_value: float
    total_sell_value: float
    fills: list[FillResult]


class EODExecutor:
    """Executes paper orders at end-of-day prices.

    This executor simulates market order fills using the daily closing price.
    Limit orders are filled if the price condition is met.
    """

    def __init__(self, db: Database) -> None:
        """Initialize EOD executor.

        Args:
            db: Database client.
        """
        self._db = db
        logger.info("eod_executor_initialized")

    def execute_orders(
        self,
        execution_date: str | None = None,
        account_id: int | None = None,
    ) -> ExecutionSummary:
        """Execute all pending orders at EOD prices.

        Args:
            execution_date: Date to use for prices (defaults to today).
            account_id: Optional account filter.

        Returns:
            ExecutionSummary with results.
        """
        if execution_date is None:
            execution_date = datetime.now().strftime("%Y-%m-%d")

        pending_orders = self._db.get_pending_paper_orders(account_id)
        prices = self._db.get_prices_for_date(execution_date)
        price_map = {p["instrument_id"]: p for p in prices}

        fills: list[FillResult] = []
        filled_count = 0
        rejected_count = 0
        total_buy = 0.0
        total_sell = 0.0

        for order in pending_orders:
            result = self._process_order(order, price_map, execution_date)
            fills.append(result)

            if result.success:
                filled_count += 1
                if result.side == "buy":
                    total_buy += result.total_value
                else:
                    total_sell += result.total_value
            else:
                rejected_count += 1

        logger.info(
            "eod_execution_complete",
            execution_date=execution_date,
            orders_processed=len(pending_orders),
            orders_filled=filled_count,
            orders_rejected=rejected_count,
        )

        return ExecutionSummary(
            execution_date=execution_date,
            orders_processed=len(pending_orders),
            orders_filled=filled_count,
            orders_rejected=rejected_count,
            total_buy_value=total_buy,
            total_sell_value=total_sell,
            fills=fills,
        )

    def _process_order(
        self,
        order: dict[str, Any],
        price_map: dict[int, dict[str, Any]],
        execution_date: str,
    ) -> FillResult:
        """Process a single order.

        Args:
            order: Order record.
            price_map: Map of instrument_id to price data.
            execution_date: Execution date.

        Returns:
            FillResult for this order.
        """
        instrument_id: int = order["instrument_id"]
        instruments_data = order.get("instruments")
        symbol: str = instruments_data["symbol"] if instruments_data else "UNKNOWN"
        order_id: int = order["id"]
        side: str = order["order_side"]
        quantity: int = order["quantity"]
        order_type: str = order["order_type"]
        limit_price_raw = order.get("limit_price")

        if instrument_id not in price_map:
            return FillResult(
                order_id=order_id,
                instrument_id=instrument_id,
                symbol=symbol,
                side=side,
                quantity=quantity,
                fill_price=0.0,
                total_value=0.0,
                success=False,
                message=f"No price data for {execution_date}",
            )

        price_data = price_map[instrument_id]
        close_price: float = float(price_data["close"])
        high_price: float = float(price_data["high"]) if price_data.get("high") else close_price
        low_price: float = float(price_data["low"]) if price_data.get("low") else close_price

        fill_price: float = close_price
        if order_type == "limit" and limit_price_raw is not None:
            limit_price: float = float(limit_price_raw)
            can_fill = self._check_limit_order(side, limit_price, high_price, low_price)
            if not can_fill:
                return FillResult(
                    order_id=order_id,
                    instrument_id=instrument_id,
                    symbol=symbol,
                    side=side,
                    quantity=quantity,
                    fill_price=0.0,
                    total_value=0.0,
                    success=False,
                    message=f"Limit price {limit_price} not reached",
                )
            fill_price = limit_price

        total_value: float = fill_price * quantity

        account = self._db.get_paper_account(order["account_id"])
        if not account:
            return FillResult(
                order_id=order_id,
                instrument_id=instrument_id,
                symbol=symbol,
                side=side,
                quantity=quantity,
                fill_price=fill_price,
                total_value=total_value,
                success=False,
                message="Account not found",
            )

        cash_balance: float = float(account["cash_balance"])

        if side == "buy":
            if cash_balance < total_value:
                return FillResult(
                    order_id=order_id,
                    instrument_id=instrument_id,
                    symbol=symbol,
                    side=side,
                    quantity=quantity,
                    fill_price=fill_price,
                    total_value=total_value,
                    success=False,
                    message=f"Insufficient cash: need {total_value:.2f}, have {cash_balance:.2f}",
                )

            new_cash = cash_balance - total_value
            self._db.update_paper_account_balance(order["account_id"], new_cash)

            position = self._db.get_paper_position(order["account_id"], instrument_id)
            if position and position["quantity"] > 0:
                pos_qty: int = int(position["quantity"])
                pos_avg: float = float(position["avg_entry_price"])
                new_qty = pos_qty + quantity
                total_cost = pos_avg * pos_qty + fill_price * quantity
                new_avg_price = total_cost / new_qty
            else:
                new_qty = quantity
                new_avg_price = fill_price

            self._db.upsert_paper_position(
                account_id=order["account_id"],
                instrument_id=instrument_id,
                quantity=new_qty,
                avg_entry_price=new_avg_price,
                current_price=close_price,
            )

        else:  # sell
            position = self._db.get_paper_position(order["account_id"], instrument_id)
            if not position or position["quantity"] < quantity:
                available = int(position["quantity"]) if position else 0
                return FillResult(
                    order_id=order_id,
                    instrument_id=instrument_id,
                    symbol=symbol,
                    side=side,
                    quantity=quantity,
                    fill_price=fill_price,
                    total_value=total_value,
                    success=False,
                    message=f"Insufficient position: need {quantity}, have {available}",
                )

            pos_qty = int(position["quantity"])
            pos_avg = float(position["avg_entry_price"])
            pos_realized = float(position.get("realized_pnl", 0) or 0)

            realized_pnl = (fill_price - pos_avg) * quantity
            new_qty = pos_qty - quantity
            new_cash = cash_balance + total_value

            self._db.update_paper_account_balance(order["account_id"], new_cash)

            if new_qty > 0:
                self._db.upsert_paper_position(
                    account_id=order["account_id"],
                    instrument_id=instrument_id,
                    quantity=new_qty,
                    avg_entry_price=pos_avg,
                    current_price=close_price,
                    realized_pnl=pos_realized + realized_pnl,
                )
            else:
                self._db.upsert_paper_position(
                    account_id=order["account_id"],
                    instrument_id=instrument_id,
                    quantity=0,
                    avg_entry_price=0.0,
                    current_price=close_price,
                    realized_pnl=pos_realized + realized_pnl,
                )

        self._db.fill_paper_order(order_id, fill_price, quantity)

        logger.info(
            "paper_order_filled",
            order_id=order_id,
            symbol=symbol,
            side=side,
            quantity=quantity,
            fill_price=fill_price,
        )

        return FillResult(
            order_id=order_id,
            instrument_id=instrument_id,
            symbol=symbol,
            side=side,
            quantity=quantity,
            fill_price=fill_price,
            total_value=total_value,
            success=True,
            message="Filled at EOD close",
        )

    def _check_limit_order(
        self,
        side: str,
        limit_price: float,
        high: float,
        low: float,
    ) -> bool:
        """Check if a limit order would have been filled.

        Args:
            side: 'buy' or 'sell'.
            limit_price: Order limit price.
            high: Day's high price.
            low: Day's low price.

        Returns:
            True if order would have filled.
        """
        if side == "buy":
            return low <= limit_price
        else:
            return high >= limit_price
