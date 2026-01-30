"""Risk rules and metrics for paper trading."""

from dataclasses import dataclass, field
from typing import Any

from asx_jobs.database import Database
from asx_jobs.logging import get_logger

logger = get_logger(__name__)


@dataclass
class RiskLimits:
    """Configurable risk limits for paper trading."""

    max_total_exposure: float = 0.95
    max_position_concentration: float = 0.20
    max_drawdown_pct: float = 0.20
    max_losing_streak: int = 5
    min_cash_reserve: float = 0.05

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RiskLimits":
        """Create RiskLimits from a dictionary."""
        return cls(
            max_total_exposure=data.get("max_total_exposure", 0.95),
            max_position_concentration=data.get("max_position_concentration", 0.20),
            max_drawdown_pct=data.get("max_drawdown_pct", 0.20),
            max_losing_streak=data.get("max_losing_streak", 5),
            min_cash_reserve=data.get("min_cash_reserve", 0.05),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "max_total_exposure": self.max_total_exposure,
            "max_position_concentration": self.max_position_concentration,
            "max_drawdown_pct": self.max_drawdown_pct,
            "max_losing_streak": self.max_losing_streak,
            "min_cash_reserve": self.min_cash_reserve,
        }


@dataclass
class RiskViolation:
    """A detected risk rule violation."""

    rule: str
    severity: str
    current_value: float
    limit_value: float
    message: str


@dataclass
class PositionRisk:
    """Risk metrics for a single position."""

    instrument_id: int
    symbol: str
    quantity: int
    market_value: float
    concentration_pct: float
    unrealized_pnl: float
    unrealized_pnl_pct: float


@dataclass
class RiskMetrics:
    """Computed risk metrics for a portfolio."""

    account_id: int
    account_name: str
    total_value: float
    cash_balance: float
    positions_value: float
    total_exposure: float
    cash_reserve_pct: float
    current_drawdown: float
    current_drawdown_pct: float
    peak_value: float
    losing_streak: int
    position_risks: list[PositionRisk] = field(default_factory=list)
    violations: list[RiskViolation] = field(default_factory=list)
    is_compliant: bool = True


class RiskManager:
    """Manages risk rules and metrics for paper trading accounts."""

    def __init__(self, db: Database, limits: RiskLimits | None = None) -> None:
        """Initialize risk manager.

        Args:
            db: Database client.
            limits: Risk limits configuration. Uses defaults if not provided.
        """
        self._db = db
        self._limits = limits or RiskLimits()
        logger.info("risk_manager_initialized", limits=self._limits.to_dict())

    @property
    def limits(self) -> RiskLimits:
        """Get current risk limits."""
        return self._limits

    def set_limits(self, limits: RiskLimits) -> None:
        """Update risk limits.

        Args:
            limits: New risk limits.
        """
        self._limits = limits
        logger.info("risk_limits_updated", limits=limits.to_dict())

    def compute_risk_metrics(self, account_id: int) -> RiskMetrics:
        """Compute risk metrics for an account.

        Args:
            account_id: Paper trading account ID.

        Returns:
            RiskMetrics with all computed values and violations.
        """
        account = self._db.get_paper_account(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")

        positions = self._db.get_paper_positions(account_id)
        snapshots = self._db.get_portfolio_snapshots(account_id, limit=100)

        cash_balance = float(account["cash_balance"])
        positions_value = self._calculate_positions_value(positions)
        total_value = cash_balance + positions_value

        total_exposure = positions_value / total_value if total_value > 0 else 0
        cash_reserve_pct = cash_balance / total_value if total_value > 0 else 1.0

        drawdown_info = self._calculate_drawdown(snapshots, total_value, float(account["initial_balance"]))
        losing_streak = self._calculate_losing_streak(account_id)
        position_risks = self._calculate_position_risks(positions, total_value)

        metrics = RiskMetrics(
            account_id=account_id,
            account_name=account["name"],
            total_value=total_value,
            cash_balance=cash_balance,
            positions_value=positions_value,
            total_exposure=total_exposure,
            cash_reserve_pct=cash_reserve_pct,
            current_drawdown=drawdown_info["drawdown"],
            current_drawdown_pct=drawdown_info["drawdown_pct"],
            peak_value=drawdown_info["peak_value"],
            losing_streak=losing_streak,
            position_risks=position_risks,
        )

        metrics.violations = self._check_violations(metrics)
        metrics.is_compliant = len(metrics.violations) == 0

        logger.info(
            "risk_metrics_computed",
            account_id=account_id,
            total_exposure=total_exposure,
            drawdown_pct=drawdown_info["drawdown_pct"],
            losing_streak=losing_streak,
            violations=len(metrics.violations),
        )

        return metrics

    def _calculate_positions_value(self, positions: list[dict[str, Any]]) -> float:
        """Calculate total market value of positions."""
        total = 0.0
        for pos in positions:
            quantity = int(pos["quantity"])
            current_price = float(pos.get("current_price") or pos["avg_entry_price"])
            total += quantity * current_price
        return total

    def _calculate_drawdown(
        self, snapshots: list[dict[str, Any]], current_value: float, initial_value: float
    ) -> dict[str, float]:
        """Calculate current drawdown from peak."""
        if not snapshots:
            return {
                "drawdown": 0.0,
                "drawdown_pct": 0.0,
                "peak_value": max(current_value, initial_value),
            }

        peak_value = initial_value
        for snap in snapshots:
            snap_value = float(snap["total_value"])
            if snap_value > peak_value:
                peak_value = snap_value

        if current_value > peak_value:
            peak_value = current_value

        drawdown = peak_value - current_value
        drawdown_pct = drawdown / peak_value if peak_value > 0 else 0

        return {
            "drawdown": drawdown,
            "drawdown_pct": drawdown_pct,
            "peak_value": peak_value,
        }

    def _calculate_losing_streak(self, account_id: int) -> int:
        """Calculate current losing streak from recent trades."""
        orders = self._db.get_paper_orders(account_id, status="filled", limit=50)
        sell_orders = [o for o in orders if o["order_side"] == "sell"]

        if not sell_orders:
            return 0

        positions = self._db.get_paper_positions(account_id, include_closed=True)
        position_map = {p["instrument_id"]: p for p in positions}

        streak = 0
        for order in sell_orders:
            instrument_id = order["instrument_id"]
            fill_price = float(order.get("filled_avg_price") or 0)
            quantity = int(order["quantity"])

            pos = position_map.get(instrument_id)
            if pos:
                avg_entry = float(pos["avg_entry_price"])
                pnl = (fill_price - avg_entry) * quantity

                if pnl < 0:
                    streak += 1
                else:
                    break

        return streak

    def _calculate_position_risks(
        self, positions: list[dict[str, Any]], total_value: float
    ) -> list[PositionRisk]:
        """Calculate risk metrics for each position."""
        risks = []

        for pos in positions:
            quantity = int(pos["quantity"])
            avg_entry = float(pos["avg_entry_price"])
            current_price = float(pos.get("current_price") or avg_entry)
            market_value = quantity * current_price

            concentration = market_value / total_value if total_value > 0 else 0
            unrealized_pnl = (current_price - avg_entry) * quantity
            unrealized_pnl_pct = (current_price - avg_entry) / avg_entry if avg_entry > 0 else 0

            symbol = "N/A"
            if pos.get("instruments"):
                symbol = pos["instruments"].get("symbol", "N/A")

            risks.append(
                PositionRisk(
                    instrument_id=pos["instrument_id"],
                    symbol=symbol,
                    quantity=quantity,
                    market_value=market_value,
                    concentration_pct=concentration,
                    unrealized_pnl=unrealized_pnl,
                    unrealized_pnl_pct=unrealized_pnl_pct,
                )
            )

        risks.sort(key=lambda x: x.concentration_pct, reverse=True)
        return risks

    def _check_violations(self, metrics: RiskMetrics) -> list[RiskViolation]:
        """Check for risk rule violations."""
        violations = []

        if metrics.total_exposure > self._limits.max_total_exposure:
            violations.append(
                RiskViolation(
                    rule="max_total_exposure",
                    severity="warning",
                    current_value=metrics.total_exposure,
                    limit_value=self._limits.max_total_exposure,
                    message=f"Total exposure {metrics.total_exposure*100:.1f}% exceeds limit of {self._limits.max_total_exposure*100:.1f}%",
                )
            )

        if metrics.cash_reserve_pct < self._limits.min_cash_reserve:
            violations.append(
                RiskViolation(
                    rule="min_cash_reserve",
                    severity="warning",
                    current_value=metrics.cash_reserve_pct,
                    limit_value=self._limits.min_cash_reserve,
                    message=f"Cash reserve {metrics.cash_reserve_pct*100:.1f}% below minimum of {self._limits.min_cash_reserve*100:.1f}%",
                )
            )

        if metrics.current_drawdown_pct > self._limits.max_drawdown_pct:
            violations.append(
                RiskViolation(
                    rule="max_drawdown",
                    severity="critical",
                    current_value=metrics.current_drawdown_pct,
                    limit_value=self._limits.max_drawdown_pct,
                    message=f"Drawdown {metrics.current_drawdown_pct*100:.1f}% exceeds limit of {self._limits.max_drawdown_pct*100:.1f}%",
                )
            )

        if metrics.losing_streak >= self._limits.max_losing_streak:
            violations.append(
                RiskViolation(
                    rule="max_losing_streak",
                    severity="warning",
                    current_value=float(metrics.losing_streak),
                    limit_value=float(self._limits.max_losing_streak),
                    message=f"Losing streak of {metrics.losing_streak} trades meets/exceeds limit of {self._limits.max_losing_streak}",
                )
            )

        for pos_risk in metrics.position_risks:
            if pos_risk.concentration_pct > self._limits.max_position_concentration:
                violations.append(
                    RiskViolation(
                        rule="max_position_concentration",
                        severity="warning",
                        current_value=pos_risk.concentration_pct,
                        limit_value=self._limits.max_position_concentration,
                        message=f"Position {pos_risk.symbol} concentration {pos_risk.concentration_pct*100:.1f}% exceeds limit of {self._limits.max_position_concentration*100:.1f}%",
                    )
                )

        return violations

    def check_order_risk(
        self, account_id: int, symbol: str, side: str, quantity: int, estimated_price: float
    ) -> tuple[bool, list[str]]:
        """Check if a proposed order would violate risk rules.

        Args:
            account_id: Account ID.
            symbol: Stock symbol.
            side: Order side ('buy' or 'sell').
            quantity: Number of shares.
            estimated_price: Estimated fill price.

        Returns:
            Tuple of (is_allowed, list of warning messages).
        """
        if side == "sell":
            return True, []

        account = self._db.get_paper_account(account_id)
        if not account:
            return False, ["Account not found"]

        positions = self._db.get_paper_positions(account_id)
        cash_balance = float(account["cash_balance"])
        positions_value = self._calculate_positions_value(positions)
        total_value = cash_balance + positions_value

        order_value = quantity * estimated_price
        warnings = []

        if order_value > cash_balance:
            return False, [f"Insufficient cash: need ${order_value:,.2f}, have ${cash_balance:,.2f}"]

        new_cash = cash_balance - order_value
        new_positions_value = positions_value + order_value
        new_total = new_cash + new_positions_value

        new_exposure = new_positions_value / new_total if new_total > 0 else 0
        if new_exposure > self._limits.max_total_exposure:
            warnings.append(
                f"Order would increase exposure to {new_exposure*100:.1f}% (limit: {self._limits.max_total_exposure*100:.1f}%)"
            )

        new_cash_reserve = new_cash / new_total if new_total > 0 else 0
        if new_cash_reserve < self._limits.min_cash_reserve:
            warnings.append(
                f"Order would reduce cash reserve to {new_cash_reserve*100:.1f}% (minimum: {self._limits.min_cash_reserve*100:.1f}%)"
            )

        existing_position_value = 0.0
        for pos in positions:
            if pos.get("instruments", {}).get("symbol") == symbol:
                qty = int(pos["quantity"])
                price = float(pos.get("current_price") or pos["avg_entry_price"])
                existing_position_value = qty * price
                break

        new_position_value = existing_position_value + order_value
        new_concentration = new_position_value / new_total if new_total > 0 else 0
        if new_concentration > self._limits.max_position_concentration:
            warnings.append(
                f"Order would increase {symbol} concentration to {new_concentration*100:.1f}% (limit: {self._limits.max_position_concentration*100:.1f}%)"
            )

        return True, warnings

    def format_report(self, metrics: RiskMetrics) -> str:
        """Format risk metrics as a readable report.

        Args:
            metrics: Computed risk metrics.

        Returns:
            Formatted string report.
        """
        status = "COMPLIANT" if metrics.is_compliant else "VIOLATIONS DETECTED"

        lines = [
            f"Risk Report",
            f"=" * 50,
            f"Account: {metrics.account_name} (ID: {metrics.account_id})",
            f"Status: {status}",
            f"",
            f"Portfolio Summary",
            f"-" * 30,
            f"Total Value:      ${metrics.total_value:>15,.2f}",
            f"Cash Balance:     ${metrics.cash_balance:>15,.2f}",
            f"Positions Value:  ${metrics.positions_value:>15,.2f}",
            f"",
            f"Risk Metrics",
            f"-" * 30,
            f"Total Exposure:   {metrics.total_exposure*100:>15.1f}% (limit: {self._limits.max_total_exposure*100:.0f}%)",
            f"Cash Reserve:     {metrics.cash_reserve_pct*100:>15.1f}% (min: {self._limits.min_cash_reserve*100:.0f}%)",
            f"Current Drawdown: {metrics.current_drawdown_pct*100:>15.1f}% (limit: {self._limits.max_drawdown_pct*100:.0f}%)",
            f"Peak Value:       ${metrics.peak_value:>15,.2f}",
            f"Losing Streak:    {metrics.losing_streak:>15} (limit: {self._limits.max_losing_streak})",
        ]

        if metrics.position_risks:
            lines.extend([
                f"",
                f"Position Concentration",
                f"-" * 30,
            ])
            for pos in metrics.position_risks[:10]:
                flag = "*" if pos.concentration_pct > self._limits.max_position_concentration else " "
                lines.append(
                    f"{flag}{pos.symbol:<7} {pos.concentration_pct*100:>6.1f}%  ${pos.market_value:>12,.2f}  P&L: {pos.unrealized_pnl_pct*100:>+6.1f}%"
                )

        if metrics.violations:
            lines.extend([
                f"",
                f"Violations ({len(metrics.violations)})",
                f"-" * 30,
            ])
            for v in metrics.violations:
                severity_marker = "!!" if v.severity == "critical" else "!"
                lines.append(f"{severity_marker} [{v.rule}] {v.message}")

        return "\n".join(lines)
