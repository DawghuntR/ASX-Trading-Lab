"""Paper trading engine for managing accounts, orders, and positions."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from asx_jobs.database import Database
from asx_jobs.logging import get_logger

logger = get_logger(__name__)


@dataclass
class OrderResult:
    """Result of order submission."""

    order_id: int
    success: bool
    message: str


@dataclass
class ExecutionResult:
    """Result of order execution."""

    order_id: int
    filled: bool
    fill_price: float | None
    fill_quantity: int
    message: str


class PaperTradingEngine:
    """Engine for paper trading operations.

    Manages accounts, order submission, and position tracking.
    Uses EOD (end-of-day) prices for order fills.
    """

    def __init__(self, db: Database) -> None:
        """Initialize paper trading engine.

        Args:
            db: Database client.
        """
        self._db = db
        logger.info("paper_trading_engine_initialized")

    def create_account(
        self,
        name: str,
        initial_balance: float = 100000.0,
    ) -> int:
        """Create a new paper trading account.

        Args:
            name: Account name (must be unique).
            initial_balance: Starting cash balance.

        Returns:
            Account ID.

        Raises:
            ValueError: If account name already exists.
        """
        existing = self._db.get_paper_account_by_name(name)
        if existing:
            raise ValueError(f"Account '{name}' already exists")

        account_id = self._db.create_paper_account(name, initial_balance)
        logger.info(
            "paper_account_created",
            account_id=account_id,
            name=name,
            initial_balance=initial_balance,
        )
        return account_id

    def get_account(self, account_id: int) -> dict[str, Any] | None:
        """Get account details.

        Args:
            account_id: Account ID.

        Returns:
            Account record or None.
        """
        return self._db.get_paper_account(account_id)

    def get_account_by_name(self, name: str) -> dict[str, Any] | None:
        """Get account by name.

        Args:
            name: Account name.

        Returns:
            Account record or None.
        """
        return self._db.get_paper_account_by_name(name)

    def list_accounts(self) -> list[dict[str, Any]]:
        """List all active paper accounts.

        Returns:
            List of account records.
        """
        return self._db.get_all_paper_accounts()

    def submit_order(
        self,
        account_id: int,
        symbol: str,
        side: str,
        quantity: int,
        order_type: str = "market",
        limit_price: float | None = None,
        notes: str | None = None,
    ) -> OrderResult:
        """Submit a paper trading order.

        Args:
            account_id: Account ID.
            symbol: Stock symbol.
            side: 'buy' or 'sell'.
            quantity: Number of shares.
            order_type: 'market' or 'limit'.
            limit_price: Limit price (required for limit orders).
            notes: Optional notes.

        Returns:
            OrderResult with order ID and status.
        """
        if side not in ("buy", "sell"):
            return OrderResult(0, False, f"Invalid side: {side}")

        if quantity <= 0:
            return OrderResult(0, False, "Quantity must be positive")

        if order_type == "limit" and limit_price is None:
            return OrderResult(0, False, "Limit price required for limit orders")

        account = self._db.get_paper_account(account_id)
        if not account:
            return OrderResult(0, False, f"Account {account_id} not found")

        instrument = self._db.get_instrument_by_symbol(symbol)
        if not instrument:
            return OrderResult(0, False, f"Symbol {symbol} not found")

        if side == "sell":
            position = self._db.get_paper_position(account_id, instrument["id"])
            if not position or position["quantity"] < quantity:
                available = position["quantity"] if position else 0
                return OrderResult(
                    0, False, f"Insufficient position: have {available}, need {quantity}"
                )

        order_id = self._db.submit_paper_order(
            account_id=account_id,
            instrument_id=instrument["id"],
            order_side=side,
            quantity=quantity,
            order_type=order_type,
            limit_price=limit_price,
            notes=notes,
        )

        logger.info(
            "paper_order_submitted",
            order_id=order_id,
            account_id=account_id,
            symbol=symbol,
            side=side,
            quantity=quantity,
            order_type=order_type,
        )

        return OrderResult(order_id, True, "Order submitted")

    def cancel_order(self, order_id: int) -> bool:
        """Cancel a pending order.

        Args:
            order_id: Order ID.

        Returns:
            True if cancelled, False if not found or already filled.
        """
        orders = self._db.get_pending_paper_orders()
        if not any(o["id"] == order_id for o in orders):
            return False

        self._db.cancel_paper_order(order_id)
        logger.info("paper_order_cancelled", order_id=order_id)
        return True

    def get_positions(self, account_id: int) -> list[dict[str, Any]]:
        """Get all open positions for an account.

        Args:
            account_id: Account ID.

        Returns:
            List of position records.
        """
        return self._db.get_paper_positions(account_id)

    def get_orders(
        self, account_id: int, status: str | None = None
    ) -> list[dict[str, Any]]:
        """Get orders for an account.

        Args:
            account_id: Account ID.
            status: Optional status filter.

        Returns:
            List of order records.
        """
        return self._db.get_paper_orders(account_id, status)

    def get_portfolio_value(self, account_id: int) -> dict[str, Any]:
        """Calculate current portfolio value.

        Args:
            account_id: Account ID.

        Returns:
            Dictionary with cash, positions_value, total_value, positions.
        """
        account = self._db.get_paper_account(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")

        positions = self._db.get_paper_positions(account_id)
        positions_value = 0.0
        position_details = []

        for pos in positions:
            latest_price = self._db.get_latest_price_for_instrument(
                pos["instrument_id"]
            )
            current_price = latest_price["close"] if latest_price else pos["avg_entry_price"]

            market_value = current_price * pos["quantity"]
            unrealized_pnl = (current_price - pos["avg_entry_price"]) * pos["quantity"]

            positions_value += market_value
            position_details.append(
                {
                    "instrument_id": pos["instrument_id"],
                    "symbol": pos["instruments"]["symbol"] if pos.get("instruments") else None,
                    "quantity": pos["quantity"],
                    "avg_entry_price": pos["avg_entry_price"],
                    "current_price": current_price,
                    "market_value": market_value,
                    "unrealized_pnl": unrealized_pnl,
                    "unrealized_pnl_pct": unrealized_pnl / (pos["avg_entry_price"] * pos["quantity"])
                    if pos["quantity"] > 0
                    else 0,
                }
            )

        total_value = account["cash_balance"] + positions_value

        return {
            "account_id": account_id,
            "cash_balance": account["cash_balance"],
            "positions_value": positions_value,
            "total_value": total_value,
            "initial_balance": account["initial_balance"],
            "total_return": (total_value - account["initial_balance"])
            / account["initial_balance"],
            "positions": position_details,
        }

    def update_position_prices(self, account_id: int) -> int:
        """Update all position prices with latest market data.

        Args:
            account_id: Account ID.

        Returns:
            Number of positions updated.
        """
        positions = self._db.get_paper_positions(account_id)
        updated = 0

        for pos in positions:
            latest_price = self._db.get_latest_price_for_instrument(
                pos["instrument_id"]
            )
            if latest_price:
                self._db.upsert_paper_position(
                    account_id=account_id,
                    instrument_id=pos["instrument_id"],
                    quantity=pos["quantity"],
                    avg_entry_price=pos["avg_entry_price"],
                    current_price=latest_price["close"],
                    realized_pnl=pos["realized_pnl"],
                )
                updated += 1

        return updated

    def create_snapshot(self, account_id: int, snapshot_date: str) -> int:
        """Create a portfolio snapshot for a specific date.

        Args:
            account_id: Account ID.
            snapshot_date: Date for snapshot (YYYY-MM-DD).

        Returns:
            Snapshot ID.
        """
        portfolio = self.get_portfolio_value(account_id)

        prev_snapshot = self._db.get_latest_portfolio_snapshot(account_id)
        daily_pnl = None
        daily_return = None

        if prev_snapshot:
            daily_pnl = portfolio["total_value"] - prev_snapshot["total_value"]
            if prev_snapshot["total_value"] > 0:
                daily_return = daily_pnl / prev_snapshot["total_value"]

        positions_data = {
            str(p["instrument_id"]): {
                "symbol": p["symbol"],
                "quantity": p["quantity"],
                "avg_entry_price": p["avg_entry_price"],
                "current_price": p["current_price"],
                "market_value": p["market_value"],
            }
            for p in portfolio["positions"]
        }

        snapshot_id = self._db.create_portfolio_snapshot(
            account_id=account_id,
            snapshot_date=snapshot_date,
            cash_balance=portfolio["cash_balance"],
            positions_value=portfolio["positions_value"],
            total_value=portfolio["total_value"],
            daily_pnl=daily_pnl,
            daily_return=daily_return,
            positions_snapshot=positions_data,
        )

        logger.info(
            "portfolio_snapshot_created",
            account_id=account_id,
            snapshot_date=snapshot_date,
            total_value=portfolio["total_value"],
        )

        return snapshot_id
