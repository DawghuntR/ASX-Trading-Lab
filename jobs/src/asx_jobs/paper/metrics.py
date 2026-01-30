"""Portfolio performance metrics calculation."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from asx_jobs.database import Database
from asx_jobs.logging import get_logger

logger = get_logger(__name__)


@dataclass
class PortfolioMetrics:
    """Computed portfolio performance metrics."""

    account_id: int
    account_name: str
    start_date: str
    end_date: str
    initial_value: float
    final_value: float
    total_return: float
    total_return_pct: float
    max_drawdown: float
    max_drawdown_pct: float
    max_drawdown_date: str | None
    peak_value: float
    peak_date: str | None
    trading_days: int
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    avg_win: float
    avg_loss: float
    profit_factor: float
    avg_exposure: float
    current_exposure: float


@dataclass
class EquityPoint:
    """Single point on the equity curve."""

    date: str
    total_value: float
    cash_balance: float
    positions_value: float
    daily_pnl: float
    daily_return: float
    cumulative_return: float
    drawdown: float
    drawdown_pct: float


class PortfolioAnalyzer:
    """Analyzes portfolio performance from paper trading data."""

    def __init__(self, db: Database) -> None:
        """Initialize portfolio analyzer.

        Args:
            db: Database client.
        """
        self._db = db
        logger.info("portfolio_analyzer_initialized")

    def compute_metrics(self, account_id: int) -> PortfolioMetrics:
        """Compute performance metrics for an account.

        Args:
            account_id: Paper trading account ID.

        Returns:
            PortfolioMetrics with all computed values.
        """
        account = self._db.get_paper_account(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")

        snapshots = self._db.get_portfolio_snapshots(account_id, limit=500)
        snapshots.reverse()  # Oldest first

        if not snapshots:
            return self._empty_metrics(account)

        initial_value = float(account["initial_balance"])
        final_value = float(snapshots[-1]["total_value"])

        equity_curve = self._build_equity_curve(snapshots, initial_value)
        drawdown_info = self._calculate_drawdown(equity_curve)
        trade_stats = self._calculate_trade_stats(account_id)
        exposure_stats = self._calculate_exposure(equity_curve, initial_value)

        total_return = final_value - initial_value
        total_return_pct = total_return / initial_value if initial_value > 0 else 0

        return PortfolioMetrics(
            account_id=account_id,
            account_name=account["name"],
            start_date=snapshots[0]["snapshot_date"],
            end_date=snapshots[-1]["snapshot_date"],
            initial_value=initial_value,
            final_value=final_value,
            total_return=total_return,
            total_return_pct=total_return_pct,
            max_drawdown=drawdown_info["max_drawdown"],
            max_drawdown_pct=drawdown_info["max_drawdown_pct"],
            max_drawdown_date=drawdown_info["max_drawdown_date"],
            peak_value=drawdown_info["peak_value"],
            peak_date=drawdown_info["peak_date"],
            trading_days=len(snapshots),
            total_trades=trade_stats["total_trades"],
            winning_trades=trade_stats["winning_trades"],
            losing_trades=trade_stats["losing_trades"],
            win_rate=trade_stats["win_rate"],
            avg_win=trade_stats["avg_win"],
            avg_loss=trade_stats["avg_loss"],
            profit_factor=trade_stats["profit_factor"],
            avg_exposure=exposure_stats["avg_exposure"],
            current_exposure=exposure_stats["current_exposure"],
        )

    def get_equity_curve(
        self, account_id: int, limit: int = 365
    ) -> list[EquityPoint]:
        """Get the equity curve for an account.

        Args:
            account_id: Account ID.
            limit: Maximum number of points.

        Returns:
            List of EquityPoint objects.
        """
        account = self._db.get_paper_account(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")

        snapshots = self._db.get_portfolio_snapshots(account_id, limit=limit)
        snapshots.reverse()  # Oldest first

        if not snapshots:
            return []

        initial_value = float(account["initial_balance"])
        return self._build_equity_curve(snapshots, initial_value)

    def _build_equity_curve(
        self, snapshots: list[dict[str, Any]], initial_value: float
    ) -> list[EquityPoint]:
        """Build equity curve from snapshots.

        Args:
            snapshots: List of portfolio snapshots (oldest first).
            initial_value: Initial portfolio value.

        Returns:
            List of EquityPoint objects.
        """
        curve: list[EquityPoint] = []
        peak_value = initial_value

        for snap in snapshots:
            total_value = float(snap["total_value"])
            cash_balance = float(snap["cash_balance"])
            positions_value = float(snap["positions_value"])
            daily_pnl = float(snap.get("daily_pnl") or 0)
            daily_return = float(snap.get("daily_return") or 0)

            cumulative_return = (total_value - initial_value) / initial_value if initial_value > 0 else 0

            if total_value > peak_value:
                peak_value = total_value

            drawdown = peak_value - total_value
            drawdown_pct = drawdown / peak_value if peak_value > 0 else 0

            curve.append(
                EquityPoint(
                    date=snap["snapshot_date"],
                    total_value=total_value,
                    cash_balance=cash_balance,
                    positions_value=positions_value,
                    daily_pnl=daily_pnl,
                    daily_return=daily_return,
                    cumulative_return=cumulative_return,
                    drawdown=drawdown,
                    drawdown_pct=drawdown_pct,
                )
            )

        return curve

    def _calculate_drawdown(
        self, equity_curve: list[EquityPoint]
    ) -> dict[str, Any]:
        """Calculate drawdown statistics.

        Args:
            equity_curve: List of equity points.

        Returns:
            Dictionary with drawdown statistics.
        """
        if not equity_curve:
            return {
                "max_drawdown": 0.0,
                "max_drawdown_pct": 0.0,
                "max_drawdown_date": None,
                "peak_value": 0.0,
                "peak_date": None,
            }

        max_drawdown = 0.0
        max_drawdown_pct = 0.0
        max_drawdown_date = None
        peak_value = equity_curve[0].total_value
        peak_date = equity_curve[0].date

        for point in equity_curve:
            if point.total_value > peak_value:
                peak_value = point.total_value
                peak_date = point.date

            if point.drawdown > max_drawdown:
                max_drawdown = point.drawdown
                max_drawdown_pct = point.drawdown_pct
                max_drawdown_date = point.date

        return {
            "max_drawdown": max_drawdown,
            "max_drawdown_pct": max_drawdown_pct,
            "max_drawdown_date": max_drawdown_date,
            "peak_value": peak_value,
            "peak_date": peak_date,
        }

    def _calculate_trade_stats(self, account_id: int) -> dict[str, Any]:
        """Calculate trade-level statistics.

        Args:
            account_id: Account ID.

        Returns:
            Dictionary with trade statistics.
        """
        orders = self._db.get_paper_orders(account_id, status="filled", limit=1000)

        sell_orders = [o for o in orders if o["order_side"] == "sell"]

        if not sell_orders:
            return {
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "win_rate": 0.0,
                "avg_win": 0.0,
                "avg_loss": 0.0,
                "profit_factor": 0.0,
            }

        positions = self._db.get_paper_positions(account_id, include_closed=True)
        position_map = {p["instrument_id"]: p for p in positions}

        wins = []
        losses = []

        for order in sell_orders:
            instrument_id = order["instrument_id"]
            fill_price = float(order.get("filled_avg_price") or 0)
            quantity = int(order["quantity"])

            pos = position_map.get(instrument_id)
            if pos:
                avg_entry = float(pos["avg_entry_price"])
                pnl = (fill_price - avg_entry) * quantity

                if pnl > 0:
                    wins.append(pnl)
                elif pnl < 0:
                    losses.append(abs(pnl))

        total_trades = len(wins) + len(losses)
        winning_trades = len(wins)
        losing_trades = len(losses)

        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        avg_win = sum(wins) / len(wins) if wins else 0
        avg_loss = sum(losses) / len(losses) if losses else 0

        total_wins = sum(wins)
        total_losses = sum(losses)
        profit_factor = total_wins / total_losses if total_losses > 0 else float("inf") if total_wins > 0 else 0

        return {
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": win_rate,
            "avg_win": avg_win,
            "avg_loss": avg_loss,
            "profit_factor": profit_factor,
        }

    def _calculate_exposure(
        self, equity_curve: list[EquityPoint], initial_value: float
    ) -> dict[str, float]:
        """Calculate exposure statistics.

        Args:
            equity_curve: List of equity points.
            initial_value: Initial portfolio value.

        Returns:
            Dictionary with exposure statistics.
        """
        if not equity_curve:
            return {
                "avg_exposure": 0.0,
                "current_exposure": 0.0,
            }

        exposures = []
        for point in equity_curve:
            if point.total_value > 0:
                exposure = point.positions_value / point.total_value
            else:
                exposure = 0.0
            exposures.append(exposure)

        avg_exposure = sum(exposures) / len(exposures) if exposures else 0
        current_exposure = exposures[-1] if exposures else 0

        return {
            "avg_exposure": avg_exposure,
            "current_exposure": current_exposure,
        }

    def _empty_metrics(self, account: dict[str, Any]) -> PortfolioMetrics:
        """Create empty metrics for an account with no data.

        Args:
            account: Account record.

        Returns:
            PortfolioMetrics with zero values.
        """
        initial = float(account["initial_balance"])
        return PortfolioMetrics(
            account_id=account["id"],
            account_name=account["name"],
            start_date="",
            end_date="",
            initial_value=initial,
            final_value=initial,
            total_return=0.0,
            total_return_pct=0.0,
            max_drawdown=0.0,
            max_drawdown_pct=0.0,
            max_drawdown_date=None,
            peak_value=initial,
            peak_date=None,
            trading_days=0,
            total_trades=0,
            winning_trades=0,
            losing_trades=0,
            win_rate=0.0,
            avg_win=0.0,
            avg_loss=0.0,
            profit_factor=0.0,
            avg_exposure=0.0,
            current_exposure=0.0,
        )

    def format_report(self, metrics: PortfolioMetrics) -> str:
        """Format metrics as a readable report.

        Args:
            metrics: Computed portfolio metrics.

        Returns:
            Formatted string report.
        """
        lines = [
            f"Portfolio Performance Report",
            f"=" * 50,
            f"Account: {metrics.account_name} (ID: {metrics.account_id})",
            f"Period: {metrics.start_date} to {metrics.end_date}",
            f"",
            f"Returns",
            f"-" * 30,
            f"Initial Value:    ${metrics.initial_value:>15,.2f}",
            f"Final Value:      ${metrics.final_value:>15,.2f}",
            f"Total Return:     ${metrics.total_return:>15,.2f}",
            f"Total Return %:   {metrics.total_return_pct*100:>15.2f}%",
            f"",
            f"Risk Metrics",
            f"-" * 30,
            f"Max Drawdown:     ${metrics.max_drawdown:>15,.2f}",
            f"Max Drawdown %:   {metrics.max_drawdown_pct*100:>15.2f}%",
            f"Peak Value:       ${metrics.peak_value:>15,.2f}",
            f"",
            f"Trade Statistics",
            f"-" * 30,
            f"Total Trades:     {metrics.total_trades:>15}",
            f"Winning Trades:   {metrics.winning_trades:>15}",
            f"Losing Trades:    {metrics.losing_trades:>15}",
            f"Win Rate:         {metrics.win_rate*100:>15.2f}%",
            f"Avg Win:          ${metrics.avg_win:>15,.2f}",
            f"Avg Loss:         ${metrics.avg_loss:>15,.2f}",
            f"Profit Factor:    {metrics.profit_factor:>15.2f}",
            f"",
            f"Exposure",
            f"-" * 30,
            f"Avg Exposure:     {metrics.avg_exposure*100:>15.2f}%",
            f"Current Exposure: {metrics.current_exposure*100:>15.2f}%",
            f"Trading Days:     {metrics.trading_days:>15}",
        ]
        return "\n".join(lines)
