"""Supabase database client for ASX Jobs Runner."""

from datetime import datetime
from typing import Any

from supabase import Client, create_client

from asx_jobs.config import SupabaseConfig
from asx_jobs.logging import get_logger

logger = get_logger(__name__)


class Database:
    """Supabase database client wrapper."""

    def __init__(self, config: SupabaseConfig) -> None:
        """Initialize database client.

        Args:
            config: Supabase configuration.
        """
        self._client: Client = create_client(config.url, config.service_role_key)
        logger.info("database_connected", url=config.url)

    @property
    def client(self) -> Client:
        """Get the underlying Supabase client."""
        return self._client

    def upsert_instrument(
        self,
        symbol: str,
        name: str | None = None,
        sector: str | None = None,
        industry: str | None = None,
        market_cap: int | None = None,
        is_asx300: bool = False,
        metadata: dict[str, Any] | None = None,
    ) -> int:
        """Upsert an instrument record.

        Args:
            symbol: ASX ticker symbol.
            name: Company name.
            sector: GICS sector.
            industry: GICS industry.
            market_cap: Market capitalization.
            is_asx300: Whether in ASX 300 index.
            metadata: Additional metadata.

        Returns:
            Instrument ID.
        """
        data = {
            "symbol": symbol,
            "name": name,
            "sector": sector,
            "industry": industry,
            "market_cap": market_cap,
            "is_asx300": is_asx300,
            "metadata": metadata or {},
        }

        result = (
            self._client.table("instruments")
            .upsert(data, on_conflict="symbol")
            .execute()
        )

        instrument_id: int = result.data[0]["id"]
        return instrument_id

    def upsert_daily_price(
        self,
        instrument_id: int,
        trade_date: str,
        open_price: float | None,
        high: float | None,
        low: float | None,
        close: float,
        volume: int = 0,
        adjusted_close: float | None = None,
        data_source: str = "yahoo",
    ) -> int:
        """Upsert a daily price record.

        Args:
            instrument_id: Instrument foreign key.
            trade_date: Trade date (YYYY-MM-DD).
            open_price: Opening price.
            high: High price.
            low: Low price.
            close: Closing price.
            volume: Trading volume.
            adjusted_close: Adjusted closing price.
            data_source: Data provider source.

        Returns:
            Daily price record ID.
        """
        data = {
            "instrument_id": instrument_id,
            "trade_date": trade_date,
            "open": open_price,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
            "adjusted_close": adjusted_close,
            "data_source": data_source,
        }

        result = (
            self._client.table("daily_prices")
            .upsert(data, on_conflict="instrument_id,trade_date")
            .execute()
        )

        price_id: int = result.data[0]["id"]
        return price_id

    def get_instrument_by_symbol(self, symbol: str) -> dict[str, Any] | None:
        """Get an instrument by symbol.

        Args:
            symbol: ASX ticker symbol.

        Returns:
            Instrument record or None if not found.
        """
        result = (
            self._client.table("instruments")
            .select("*")
            .eq("symbol", symbol)
            .limit(1)
            .execute()
        )

        if result.data:
            return dict(result.data[0])
        return None

    def get_instrument_by_id(self, instrument_id: int) -> dict[str, Any] | None:
        """Get an instrument by ID.

        Args:
            instrument_id: Instrument database ID.

        Returns:
            Instrument record or None if not found.
        """
        result = (
            self._client.table("instruments")
            .select("*")
            .eq("id", instrument_id)
            .limit(1)
            .execute()
        )

        if result.data:
            return dict(result.data[0])
        return None

    def get_all_active_instruments(self) -> list[dict[str, Any]]:
        """Get all active instruments.

        Returns:
            List of instrument records.
        """
        result = (
            self._client.table("instruments")
            .select("*")
            .eq("is_active", True)
            .order("symbol")
            .execute()
        )

        return [dict(r) for r in result.data]

    def get_latest_price_date(self, instrument_id: int) -> str | None:
        """Get the latest price date for an instrument.

        Args:
            instrument_id: Instrument ID.

        Returns:
            Latest trade date or None if no prices.
        """
        result = (
            self._client.table("daily_prices")
            .select("trade_date")
            .eq("instrument_id", instrument_id)
            .order("trade_date", desc=True)
            .limit(1)
            .execute()
        )

        if result.data:
            return str(result.data[0]["trade_date"])
        return None

    def bulk_upsert_prices(
        self, prices: list[dict[str, Any]], batch_size: int = 100
    ) -> int:
        """Bulk upsert daily prices.

        Args:
            prices: List of price records.
            batch_size: Records per batch.

        Returns:
            Number of records upserted.
        """
        total = 0
        for i in range(0, len(prices), batch_size):
            batch = prices[i : i + batch_size]
            self._client.table("daily_prices").upsert(
                batch, on_conflict="instrument_id,trade_date"
            ).execute()
            total += len(batch)

        return total

    def get_price_history(
        self, instrument_id: int, days: int = 30
    ) -> list[dict[str, Any]]:
        """Get price history for an instrument.

        Args:
            instrument_id: Instrument ID.
            days: Number of days to fetch.

        Returns:
            List of price records (most recent first).
        """
        result = (
            self._client.table("daily_prices")
            .select("*")
            .eq("instrument_id", instrument_id)
            .order("trade_date", desc=True)
            .limit(days)
            .execute()
        )

        return [dict(r) for r in result.data]

    def insert_signal(self, signal: dict[str, Any]) -> int:
        """Insert a trading signal.

        Args:
            signal: Signal record with fields:
                - instrument_id: int
                - signal_date: str (YYYY-MM-DD)
                - signal_type: str (price_movement, momentum, volume_spike, volatility_spike)
                - direction: str (up, down, neutral)
                - strength: str (weak, medium, strong)
                - trigger_price: float
                - trigger_reason: str
                - metrics: dict

        Returns:
            Signal ID.
        """
        result = (
            self._client.table("signals")
            .upsert(
                signal,
                on_conflict="instrument_id,signal_date,signal_type",
            )
            .execute()
        )

        signal_id: int = result.data[0]["id"]
        return signal_id

    def bulk_insert_signals(
        self, signals: list[dict[str, Any]], batch_size: int = 100
    ) -> int:
        """Bulk insert trading signals.

        Args:
            signals: List of signal records.
            batch_size: Records per batch.

        Returns:
            Number of signals inserted.
        """
        total = 0
        for i in range(0, len(signals), batch_size):
            batch = signals[i : i + batch_size]
            self._client.table("signals").upsert(
                batch,
                on_conflict="instrument_id,signal_date,signal_type",
            ).execute()
            total += len(batch)

        return total

    def get_signals_for_date(
        self, signal_date: str, signal_type: str | None = None
    ) -> list[dict[str, Any]]:
        """Get signals for a specific date.

        Args:
            signal_date: Date string (YYYY-MM-DD).
            signal_type: Optional filter by signal type.

        Returns:
            List of signal records.
        """
        query = (
            self._client.table("signals")
            .select("*, instruments(symbol, name)")
            .eq("signal_date", signal_date)
        )

        if signal_type:
            query = query.eq("signal_type", signal_type)

        result = query.order("strength", desc=True).execute()

        return [dict(r) for r in result.data]

    def upsert_announcement(
        self,
        instrument_id: int,
        announced_at: str,
        headline: str,
        url: str | None = None,
        document_type: str | None = None,
        sensitivity: str = "unknown",
        pages: int | None = None,
        asx_announcement_id: str | None = None,
        content_hash: str | None = None,
    ) -> bool:
        """Upsert an announcement record.

        Args:
            instrument_id: Instrument foreign key.
            announced_at: Announcement timestamp (ISO format).
            headline: Announcement headline.
            url: URL to the announcement document.
            document_type: Type of document.
            sensitivity: Price sensitivity level.
            pages: Number of pages.
            asx_announcement_id: ASX internal ID.
            content_hash: Hash for deduplication.

        Returns:
            True if this is a new record, False if updated existing.
        """
        data = {
            "instrument_id": instrument_id,
            "announced_at": announced_at,
            "headline": headline,
            "url": url,
            "document_type": document_type,
            "sensitivity": sensitivity,
            "pages": pages,
            "asx_announcement_id": asx_announcement_id,
            "content_hash": content_hash,
        }

        existing = (
            self._client.table("announcements")
            .select("id")
            .eq("content_hash", content_hash)
            .limit(1)
            .execute()
        )

        is_new = len(existing.data) == 0

        self._client.table("announcements").upsert(
            data, on_conflict="content_hash"
        ).execute()

        return is_new

    def get_announcements_for_symbol(
        self, instrument_id: int, limit: int = 20
    ) -> list[dict[str, Any]]:
        """Get announcements for an instrument.

        Args:
            instrument_id: Instrument ID.
            limit: Maximum number of announcements.

        Returns:
            List of announcement records.
        """
        result = (
            self._client.table("announcements")
            .select("*")
            .eq("instrument_id", instrument_id)
            .order("announced_at", desc=True)
            .limit(limit)
            .execute()
        )

        return [dict(r) for r in result.data]

    def create_backtest_run(
        self,
        strategy_id: int,
        start_date: str,
        end_date: str,
        initial_capital: float = 100000.0,
        parameters: dict[str, Any] | None = None,
        name: str | None = None,
    ) -> int:
        """Create a new backtest run.

        Args:
            strategy_id: Strategy foreign key.
            start_date: Backtest start date.
            end_date: Backtest end date.
            initial_capital: Starting capital.
            parameters: Strategy parameters.
            name: Optional run name.

        Returns:
            Backtest run ID.
        """
        data = {
            "strategy_id": strategy_id,
            "start_date": start_date,
            "end_date": end_date,
            "initial_capital": initial_capital,
            "parameters": parameters or {},
            "name": name,
            "status": "running",
            "started_at": datetime.now().isoformat(),
        }

        result = self._client.table("backtest_runs").insert(data).execute()
        return int(result.data[0]["id"])

    def complete_backtest_run(
        self,
        backtest_run_id: int,
        final_capital: float,
        status: str = "completed",
        error_message: str | None = None,
    ) -> None:
        """Mark a backtest run as complete.

        Args:
            backtest_run_id: Backtest run ID.
            final_capital: Final portfolio value.
            status: Run status (completed, failed).
            error_message: Optional error message.
        """
        data: dict[str, Any] = {
            "final_capital": final_capital,
            "status": status,
            "completed_at": datetime.now().isoformat(),
        }
        if error_message:
            data["error_message"] = error_message

        self._client.table("backtest_runs").update(data).eq(
            "id", backtest_run_id
        ).execute()

    def insert_backtest_trade(
        self,
        backtest_run_id: int,
        instrument_id: int,
        entry_date: str,
        entry_price: float,
        quantity: int,
        side: str,
        exit_date: str | None = None,
        exit_price: float | None = None,
        pnl: float | None = None,
        pnl_percent: float | None = None,
        exit_reason: str | None = None,
    ) -> int:
        """Insert a backtest trade record.

        Args:
            backtest_run_id: Backtest run foreign key.
            instrument_id: Instrument foreign key.
            entry_date: Trade entry date.
            entry_price: Entry price.
            quantity: Number of shares.
            side: Trade side (buy/sell).
            exit_date: Exit date (optional).
            exit_price: Exit price (optional).
            pnl: Profit/loss amount.
            pnl_percent: Profit/loss percentage.
            exit_reason: Reason for exit.

        Returns:
            Trade ID.
        """
        data = {
            "backtest_run_id": backtest_run_id,
            "instrument_id": instrument_id,
            "entry_date": entry_date,
            "entry_price": entry_price,
            "quantity": quantity,
            "side": side,
            "exit_date": exit_date,
            "exit_price": exit_price,
            "pnl": pnl,
            "pnl_percent": pnl_percent,
            "exit_reason": exit_reason,
        }

        result = self._client.table("backtest_trades").insert(data).execute()
        return int(result.data[0]["id"])

    def bulk_insert_backtest_trades(
        self, trades: list[dict[str, Any]], batch_size: int = 100
    ) -> int:
        """Bulk insert backtest trades.

        Args:
            trades: List of trade records.
            batch_size: Records per batch.

        Returns:
            Number of trades inserted.
        """
        total = 0
        for i in range(0, len(trades), batch_size):
            batch = trades[i : i + batch_size]
            self._client.table("backtest_trades").insert(batch).execute()
            total += len(batch)

        return total

    def insert_backtest_metrics(
        self,
        backtest_run_id: int,
        metrics: dict[str, Any],
    ) -> int:
        """Insert backtest metrics.

        Args:
            backtest_run_id: Backtest run foreign key.
            metrics: Dictionary of metric values.

        Returns:
            Metrics record ID.
        """
        data = {"backtest_run_id": backtest_run_id, **metrics}

        result = self._client.table("backtest_metrics").insert(data).execute()
        return int(result.data[0]["id"])

    def get_or_create_strategy(
        self,
        name: str,
        description: str | None = None,
        version: str = "1.0.0",
        parameters: dict[str, Any] | None = None,
    ) -> int:
        """Get or create a strategy record.

        Args:
            name: Strategy name.
            description: Strategy description.
            version: Strategy version.
            parameters: Default parameters.

        Returns:
            Strategy ID.
        """
        existing = (
            self._client.table("strategies")
            .select("id")
            .eq("name", name)
            .eq("version", version)
            .limit(1)
            .execute()
        )

        if existing.data:
            return int(existing.data[0]["id"])

        data = {
            "name": name,
            "description": description,
            "version": version,
            "parameters": parameters or {},
        }

        result = self._client.table("strategies").insert(data).execute()
        return int(result.data[0]["id"])

    def get_price_history_range(
        self,
        instrument_id: int,
        start_date: str,
        end_date: str,
    ) -> list[dict[str, Any]]:
        """Get price history for a date range.

        Args:
            instrument_id: Instrument ID.
            start_date: Start date (YYYY-MM-DD).
            end_date: End date (YYYY-MM-DD).

        Returns:
            List of price records sorted by date ascending.
        """
        result = (
            self._client.table("daily_prices")
            .select("*")
            .eq("instrument_id", instrument_id)
            .gte("trade_date", start_date)
            .lte("trade_date", end_date)
            .order("trade_date", desc=False)
            .execute()
        )

        return [dict(r) for r in result.data]

    def get_all_price_history_range(
        self,
        start_date: str,
        end_date: str,
        instrument_ids: list[int] | None = None,
    ) -> dict[int, list[dict[str, Any]]]:
        """Get price history for all instruments in a date range.

        Args:
            start_date: Start date (YYYY-MM-DD).
            end_date: End date (YYYY-MM-DD).
            instrument_ids: Optional list of instrument IDs to filter.

        Returns:
            Dictionary mapping instrument_id to list of price records.
        """
        query = (
            self._client.table("daily_prices")
            .select("*")
            .gte("trade_date", start_date)
            .lte("trade_date", end_date)
            .order("trade_date", desc=False)
        )

        if instrument_ids:
            query = query.in_("instrument_id", instrument_ids)

        result = query.execute()

        prices_by_instrument: dict[int, list[dict[str, Any]]] = {}
        for row in result.data:
            inst_id = row["instrument_id"]
            if inst_id not in prices_by_instrument:
                prices_by_instrument[inst_id] = []
            prices_by_instrument[inst_id].append(dict(row))

        return prices_by_instrument

    # =========================================================================
    # Paper Trading Methods
    # =========================================================================

    def create_paper_account(
        self,
        name: str,
        initial_balance: float = 100000.0,
    ) -> int:
        """Create a new paper trading account.

        Args:
            name: Account name.
            initial_balance: Starting cash balance.

        Returns:
            Account ID.
        """
        data = {
            "name": name,
            "initial_balance": initial_balance,
            "cash_balance": initial_balance,
            "is_active": True,
        }

        result = self._client.table("paper_accounts").insert(data).execute()
        return int(result.data[0]["id"])

    def get_paper_account(self, account_id: int) -> dict[str, Any] | None:
        """Get a paper trading account by ID.

        Args:
            account_id: Account ID.

        Returns:
            Account record or None.
        """
        result = (
            self._client.table("paper_accounts")
            .select("*")
            .eq("id", account_id)
            .limit(1)
            .execute()
        )

        if result.data:
            return dict(result.data[0])
        return None

    def get_paper_account_by_name(self, name: str) -> dict[str, Any] | None:
        """Get a paper trading account by name.

        Args:
            name: Account name.

        Returns:
            Account record or None.
        """
        result = (
            self._client.table("paper_accounts")
            .select("*")
            .eq("name", name)
            .limit(1)
            .execute()
        )

        if result.data:
            return dict(result.data[0])
        return None

    def get_all_paper_accounts(self, active_only: bool = True) -> list[dict[str, Any]]:
        """Get all paper trading accounts.

        Args:
            active_only: Only return active accounts.

        Returns:
            List of account records.
        """
        query = self._client.table("paper_accounts").select("*")

        if active_only:
            query = query.eq("is_active", True)

        result = query.order("name").execute()
        return [dict(r) for r in result.data]

    def update_paper_account_balance(
        self, account_id: int, cash_balance: float
    ) -> None:
        """Update paper account cash balance.

        Args:
            account_id: Account ID.
            cash_balance: New cash balance.
        """
        self._client.table("paper_accounts").update(
            {"cash_balance": cash_balance, "updated_at": datetime.now().isoformat()}
        ).eq("id", account_id).execute()

    def submit_paper_order(
        self,
        account_id: int,
        instrument_id: int,
        order_side: str,
        quantity: int,
        order_type: str = "market",
        limit_price: float | None = None,
        stop_price: float | None = None,
        notes: str | None = None,
    ) -> int:
        """Submit a paper trading order.

        Args:
            account_id: Account ID.
            instrument_id: Instrument ID.
            order_side: 'buy' or 'sell'.
            quantity: Number of shares.
            order_type: 'market', 'limit', 'stop', 'stop_limit'.
            limit_price: Limit price (for limit orders).
            stop_price: Stop price (for stop orders).
            notes: Optional notes.

        Returns:
            Order ID.
        """
        data = {
            "account_id": account_id,
            "instrument_id": instrument_id,
            "order_side": order_side,
            "order_type": order_type,
            "quantity": quantity,
            "limit_price": limit_price,
            "stop_price": stop_price,
            "status": "pending",
            "filled_quantity": 0,
            "notes": notes,
            "submitted_at": datetime.now().isoformat(),
        }

        result = self._client.table("paper_orders").insert(data).execute()
        return int(result.data[0]["id"])

    def get_pending_paper_orders(
        self, account_id: int | None = None
    ) -> list[dict[str, Any]]:
        """Get all pending paper orders.

        Args:
            account_id: Optional account filter.

        Returns:
            List of pending order records.
        """
        query = (
            self._client.table("paper_orders")
            .select("*, instruments(symbol, name)")
            .eq("status", "pending")
        )

        if account_id:
            query = query.eq("account_id", account_id)

        result = query.order("submitted_at").execute()
        return [dict(r) for r in result.data]

    def fill_paper_order(
        self,
        order_id: int,
        filled_price: float,
        filled_quantity: int | None = None,
    ) -> None:
        """Fill a paper order.

        Args:
            order_id: Order ID.
            filled_price: Fill price.
            filled_quantity: Quantity filled (defaults to full order).
        """
        order = (
            self._client.table("paper_orders")
            .select("*")
            .eq("id", order_id)
            .single()
            .execute()
        )

        qty = filled_quantity or order.data["quantity"]
        status = "filled" if qty >= order.data["quantity"] else "partial"

        self._client.table("paper_orders").update(
            {
                "filled_quantity": qty,
                "filled_avg_price": filled_price,
                "status": status,
                "filled_at": datetime.now().isoformat(),
            }
        ).eq("id", order_id).execute()

    def cancel_paper_order(self, order_id: int) -> None:
        """Cancel a paper order.

        Args:
            order_id: Order ID.
        """
        self._client.table("paper_orders").update(
            {"status": "cancelled", "cancelled_at": datetime.now().isoformat()}
        ).eq("id", order_id).execute()

    def get_paper_orders(
        self,
        account_id: int,
        status: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Get paper orders for an account.

        Args:
            account_id: Account ID.
            status: Optional status filter.
            limit: Maximum records.

        Returns:
            List of order records.
        """
        query = (
            self._client.table("paper_orders")
            .select("*, instruments(symbol, name)")
            .eq("account_id", account_id)
        )

        if status:
            query = query.eq("status", status)

        result = query.order("submitted_at", desc=True).limit(limit).execute()
        return [dict(r) for r in result.data]

    def upsert_paper_position(
        self,
        account_id: int,
        instrument_id: int,
        quantity: int,
        avg_entry_price: float,
        current_price: float | None = None,
        realized_pnl: float = 0.0,
    ) -> int:
        """Upsert a paper trading position.

        Args:
            account_id: Account ID.
            instrument_id: Instrument ID.
            quantity: Position size (0 to close).
            avg_entry_price: Average entry price.
            current_price: Current market price.
            realized_pnl: Realized P&L from this position.

        Returns:
            Position ID.
        """
        unrealized_pnl = None
        if current_price and quantity > 0:
            unrealized_pnl = (current_price - avg_entry_price) * quantity

        data = {
            "account_id": account_id,
            "instrument_id": instrument_id,
            "quantity": quantity,
            "avg_entry_price": avg_entry_price,
            "current_price": current_price,
            "unrealized_pnl": unrealized_pnl,
            "realized_pnl": realized_pnl,
            "updated_at": datetime.now().isoformat(),
        }

        result = (
            self._client.table("paper_positions")
            .upsert(data, on_conflict="account_id,instrument_id")
            .execute()
        )
        return int(result.data[0]["id"])

    def get_paper_positions(
        self, account_id: int, include_closed: bool = False
    ) -> list[dict[str, Any]]:
        """Get paper positions for an account.

        Args:
            account_id: Account ID.
            include_closed: Include zero-quantity positions.

        Returns:
            List of position records.
        """
        query = (
            self._client.table("paper_positions")
            .select("*, instruments(symbol, name, sector)")
            .eq("account_id", account_id)
        )

        if not include_closed:
            query = query.gt("quantity", 0)

        result = query.order("instrument_id").execute()
        return [dict(r) for r in result.data]

    def get_paper_position(
        self, account_id: int, instrument_id: int
    ) -> dict[str, Any] | None:
        """Get a specific paper position.

        Args:
            account_id: Account ID.
            instrument_id: Instrument ID.

        Returns:
            Position record or None.
        """
        result = (
            self._client.table("paper_positions")
            .select("*, instruments(symbol, name)")
            .eq("account_id", account_id)
            .eq("instrument_id", instrument_id)
            .limit(1)
            .execute()
        )

        if result.data:
            return dict(result.data[0])
        return None

    def create_portfolio_snapshot(
        self,
        account_id: int,
        snapshot_date: str,
        cash_balance: float,
        positions_value: float,
        total_value: float,
        daily_pnl: float | None = None,
        daily_return: float | None = None,
        positions_snapshot: dict[str, Any] | None = None,
    ) -> int:
        """Create a portfolio snapshot.

        Args:
            account_id: Account ID.
            snapshot_date: Snapshot date (YYYY-MM-DD).
            cash_balance: Cash balance.
            positions_value: Total positions value.
            total_value: Total portfolio value.
            daily_pnl: Daily P&L.
            daily_return: Daily return percentage.
            positions_snapshot: Detailed positions data.

        Returns:
            Snapshot ID.
        """
        data = {
            "account_id": account_id,
            "snapshot_date": snapshot_date,
            "cash_balance": cash_balance,
            "positions_value": positions_value,
            "total_value": total_value,
            "daily_pnl": daily_pnl,
            "daily_return": daily_return,
            "positions_snapshot": positions_snapshot or {},
        }

        result = (
            self._client.table("portfolio_snapshots")
            .upsert(data, on_conflict="account_id,snapshot_date")
            .execute()
        )
        return int(result.data[0]["id"])

    def get_portfolio_snapshots(
        self, account_id: int, limit: int = 90
    ) -> list[dict[str, Any]]:
        """Get portfolio snapshots for an account.

        Args:
            account_id: Account ID.
            limit: Maximum records.

        Returns:
            List of snapshot records (most recent first).
        """
        result = (
            self._client.table("portfolio_snapshots")
            .select("*")
            .eq("account_id", account_id)
            .order("snapshot_date", desc=True)
            .limit(limit)
            .execute()
        )
        return [dict(r) for r in result.data]

    def get_latest_portfolio_snapshot(
        self, account_id: int
    ) -> dict[str, Any] | None:
        """Get the latest portfolio snapshot.

        Args:
            account_id: Account ID.

        Returns:
            Latest snapshot or None.
        """
        result = (
            self._client.table("portfolio_snapshots")
            .select("*")
            .eq("account_id", account_id)
            .order("snapshot_date", desc=True)
            .limit(1)
            .execute()
        )

        if result.data:
            return dict(result.data[0])
        return None

    def get_latest_price_for_instrument(
        self, instrument_id: int
    ) -> dict[str, Any] | None:
        """Get the latest price for an instrument.

        Args:
            instrument_id: Instrument ID.

        Returns:
            Latest price record or None.
        """
        result = (
            self._client.table("daily_prices")
            .select("*")
            .eq("instrument_id", instrument_id)
            .order("trade_date", desc=True)
            .limit(1)
            .execute()
        )

        if result.data:
            return dict(result.data[0])
        return None

    def get_prices_for_date(self, trade_date: str) -> list[dict[str, Any]]:
        """Get all prices for a specific date.

        Args:
            trade_date: Trade date (YYYY-MM-DD).

        Returns:
            List of price records.
        """
        result = (
            self._client.table("daily_prices")
            .select("*")
            .eq("trade_date", trade_date)
            .execute()
        )
        return [dict(r) for r in result.data]

    # =========================================================================
    # Announcement Reactions Methods
    # =========================================================================

    def get_reactions_by_type(
        self,
        document_type: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Get announcement reactions, optionally filtered by document type.

        Args:
            document_type: Optional filter by document type.
            limit: Maximum number of records.

        Returns:
            List of reaction records.
        """
        query = (
            self._client.table("announcement_reactions")
            .select("*, instruments(symbol, name)")
        )

        if document_type:
            query = query.eq("document_type", document_type)

        result = query.order("announcement_date", desc=True).limit(limit).execute()
        return [dict(r) for r in result.data]

    def get_reactions_summary_by_type(self) -> list[dict[str, Any]]:
        """Get aggregated reaction summary by document type.

        Returns:
            List of aggregated statistics by document type.
        """
        result = (
            self._client.table("announcement_reactions")
            .select("document_type, reaction_direction, return_1d_pct")
            .execute()
        )

        type_stats: dict[str, dict[str, Any]] = {}
        for row in result.data:
            doc_type = row.get("document_type") or "Unknown"
            if doc_type not in type_stats:
                type_stats[doc_type] = {
                    "document_type": doc_type,
                    "total_count": 0,
                    "positive_count": 0,
                    "negative_count": 0,
                    "neutral_count": 0,
                    "returns": [],
                }

            type_stats[doc_type]["total_count"] += 1
            direction = row.get("reaction_direction")
            if direction == "positive":
                type_stats[doc_type]["positive_count"] += 1
            elif direction == "negative":
                type_stats[doc_type]["negative_count"] += 1
            else:
                type_stats[doc_type]["neutral_count"] += 1

            if row.get("return_1d_pct") is not None:
                type_stats[doc_type]["returns"].append(float(row["return_1d_pct"]))

        summary = []
        for doc_type, stats in type_stats.items():
            returns = stats.pop("returns")
            if returns:
                stats["avg_return_pct"] = sum(returns) / len(returns)
                stats["median_return_pct"] = sorted(returns)[len(returns) // 2]
            else:
                stats["avg_return_pct"] = 0.0
                stats["median_return_pct"] = 0.0
            summary.append(stats)

        return sorted(summary, key=lambda x: x["total_count"], reverse=True)

    def get_reactions_summary_by_sensitivity(self) -> list[dict[str, Any]]:
        """Get aggregated reaction summary by price sensitivity.

        Returns:
            List of aggregated statistics by sensitivity level.
        """
        result = (
            self._client.table("announcement_reactions")
            .select("sensitivity, reaction_direction, return_1d_pct")
            .execute()
        )

        sens_stats: dict[str, dict[str, Any]] = {}
        for row in result.data:
            sensitivity = row.get("sensitivity") or "unknown"
            if sensitivity not in sens_stats:
                sens_stats[sensitivity] = {
                    "sensitivity": sensitivity,
                    "total_count": 0,
                    "positive_count": 0,
                    "negative_count": 0,
                    "neutral_count": 0,
                    "returns": [],
                }

            sens_stats[sensitivity]["total_count"] += 1
            direction = row.get("reaction_direction")
            if direction == "positive":
                sens_stats[sensitivity]["positive_count"] += 1
            elif direction == "negative":
                sens_stats[sensitivity]["negative_count"] += 1
            else:
                sens_stats[sensitivity]["neutral_count"] += 1

            if row.get("return_1d_pct") is not None:
                sens_stats[sensitivity]["returns"].append(float(row["return_1d_pct"]))

        summary = []
        for sensitivity, stats in sens_stats.items():
            returns = stats.pop("returns")
            if returns:
                stats["avg_return_pct"] = sum(returns) / len(returns)
            else:
                stats["avg_return_pct"] = 0.0
            summary.append(stats)

        return sorted(summary, key=lambda x: x["total_count"], reverse=True)

    def get_reactions_for_symbol(
        self, instrument_id: int, limit: int = 50
    ) -> list[dict[str, Any]]:
        """Get announcement reactions for a specific instrument.

        Args:
            instrument_id: Instrument ID.
            limit: Maximum number of records.

        Returns:
            List of reaction records.
        """
        result = (
            self._client.table("announcement_reactions")
            .select("*")
            .eq("instrument_id", instrument_id)
            .order("announcement_date", desc=True)
            .limit(limit)
            .execute()
        )
        return [dict(r) for r in result.data]
