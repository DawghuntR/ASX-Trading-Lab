"""Mean Reversion Strategy.

Buy when a stock drops for N consecutive days, sell after a target bounce
or after a maximum holding period.

This strategy assumes that stocks tend to revert to their mean after
short-term pullbacks.
"""

from dataclasses import dataclass
from typing import Any

from asx_jobs.backtest.strategy import SignalType, Strategy, StrategyConfig, StrategySignal


@dataclass
class MeanReversionConfig(StrategyConfig):
    """Configuration for mean reversion strategy.

    Attributes:
        consecutive_down_days: Number of consecutive down days before buying.
        target_bounce_pct: Target profit percentage to exit.
        max_holding_days: Maximum days to hold before forced exit.
        stop_loss_pct: Stop loss percentage (positive number).
        min_drop_pct: Minimum total drop over the down days.
        min_price: Minimum stock price to consider.
        min_volume: Minimum average volume to consider.
    """

    consecutive_down_days: int = 3
    target_bounce_pct: float = 2.0
    max_holding_days: int = 10
    stop_loss_pct: float = 5.0
    min_drop_pct: float = 3.0
    min_price: float = 0.10
    min_volume: int = 100000


class MeanReversionStrategy(Strategy):
    """Mean reversion strategy.

    Entry: Buy when stock drops for N consecutive days with total
           drop exceeding min_drop_pct.

    Exit: Sell when:
      - Price bounces target_bounce_pct from entry (profit target)
      - Price drops stop_loss_pct from entry (stop loss)
      - Holding period exceeds max_holding_days (time stop)
    """

    def __init__(
        self,
        consecutive_down_days: int = 3,
        target_bounce_pct: float = 2.0,
        max_holding_days: int = 10,
        stop_loss_pct: float = 5.0,
        min_drop_pct: float = 3.0,
        min_price: float = 0.10,
        min_volume: int = 100000,
    ) -> None:
        """Initialize the strategy.

        Args:
            consecutive_down_days: Days of consecutive drops before entry.
            target_bounce_pct: Profit target percentage.
            max_holding_days: Maximum holding period.
            stop_loss_pct: Stop loss percentage.
            min_drop_pct: Minimum total drop to trigger entry.
            min_price: Minimum stock price filter.
            min_volume: Minimum average volume filter.
        """
        config = MeanReversionConfig(
            name="Mean Reversion",
            version="1.0.0",
            description=(
                f"Buy after {consecutive_down_days} consecutive down days, "
                f"exit at {target_bounce_pct}% profit or {max_holding_days} days"
            ),
            consecutive_down_days=consecutive_down_days,
            target_bounce_pct=target_bounce_pct,
            max_holding_days=max_holding_days,
            stop_loss_pct=stop_loss_pct,
            min_drop_pct=min_drop_pct,
            min_price=min_price,
            min_volume=min_volume,
        )
        super().__init__(config)
        self._config = config

    def get_parameters(self) -> dict[str, Any]:
        """Get strategy parameters."""
        return {
            "consecutive_down_days": self._config.consecutive_down_days,
            "target_bounce_pct": self._config.target_bounce_pct,
            "max_holding_days": self._config.max_holding_days,
            "stop_loss_pct": self._config.stop_loss_pct,
            "min_drop_pct": self._config.min_drop_pct,
            "min_price": self._config.min_price,
            "min_volume": self._config.min_volume,
        }

    def on_bar(
        self,
        instrument_id: int,
        symbol: str,
        bar: dict[str, Any],
        history: list[dict[str, Any]],
        position: dict[str, Any] | None,
    ) -> StrategySignal | None:
        """Process a bar and generate signals."""
        current_price = bar["close"]

        if position:
            return self._check_exit(instrument_id, symbol, bar, position)
        else:
            return self._check_entry(instrument_id, symbol, bar, history)

    def _check_entry(
        self,
        instrument_id: int,
        symbol: str,
        bar: dict[str, Any],
        history: list[dict[str, Any]],
    ) -> StrategySignal | None:
        """Check for entry conditions.

        Args:
            instrument_id: Instrument ID.
            symbol: Ticker symbol.
            bar: Current bar.
            history: Historical bars.

        Returns:
            Buy signal if conditions met, None otherwise.
        """
        current_price = bar["close"]

        if current_price < self._config.min_price:
            return None

        required_history = self._config.consecutive_down_days + 1
        if len(history) < required_history:
            return None

        if self._config.min_volume > 0:
            volumes = [h.get("volume", 0) for h in history[:20] if h.get("volume")]
            if volumes:
                avg_volume = sum(volumes) / len(volumes)
                if avg_volume < self._config.min_volume:
                    return None

        down_days = 0
        prices = [bar["close"]] + [h["close"] for h in history[:self._config.consecutive_down_days]]

        for i in range(len(prices) - 1):
            if prices[i] < prices[i + 1]:
                down_days += 1
            else:
                break

        if down_days < self._config.consecutive_down_days:
            return None

        start_price = history[self._config.consecutive_down_days - 1]["close"]
        total_drop_pct = ((start_price - current_price) / start_price) * 100

        if total_drop_pct < self._config.min_drop_pct:
            return None

        return StrategySignal(
            signal_type=SignalType.BUY,
            instrument_id=instrument_id,
            symbol=symbol,
            price=current_price,
            reason=f"Mean reversion: {down_days} down days, -{total_drop_pct:.1f}% drop",
            metadata={
                "down_days": down_days,
                "total_drop_pct": total_drop_pct,
                "entry_price": current_price,
            },
        )

    def _check_exit(
        self,
        instrument_id: int,
        symbol: str,
        bar: dict[str, Any],
        position: dict[str, Any],
    ) -> StrategySignal | None:
        """Check for exit conditions.

        Args:
            instrument_id: Instrument ID.
            symbol: Ticker symbol.
            bar: Current bar.
            position: Current position info.

        Returns:
            Sell signal if exit conditions met, None otherwise.
        """
        current_price = bar["close"]
        entry_price = position["entry_price"]
        entry_date = position["entry_date"]
        current_date = bar["trade_date"]

        pnl_pct = ((current_price - entry_price) / entry_price) * 100

        if pnl_pct >= self._config.target_bounce_pct:
            return StrategySignal(
                signal_type=SignalType.SELL,
                instrument_id=instrument_id,
                symbol=symbol,
                price=current_price,
                reason=f"Profit target hit: {pnl_pct:.1f}%",
                metadata={"pnl_pct": pnl_pct, "exit_type": "profit_target"},
            )

        if pnl_pct <= -self._config.stop_loss_pct:
            return StrategySignal(
                signal_type=SignalType.SELL,
                instrument_id=instrument_id,
                symbol=symbol,
                price=current_price,
                reason=f"Stop loss hit: {pnl_pct:.1f}%",
                metadata={"pnl_pct": pnl_pct, "exit_type": "stop_loss"},
            )

        try:
            from datetime import datetime

            entry_dt = datetime.strptime(entry_date, "%Y-%m-%d")
            current_dt = datetime.strptime(current_date, "%Y-%m-%d")
            holding_days = (current_dt - entry_dt).days

            if holding_days >= self._config.max_holding_days:
                return StrategySignal(
                    signal_type=SignalType.SELL,
                    instrument_id=instrument_id,
                    symbol=symbol,
                    price=current_price,
                    reason=f"Time stop: {holding_days} days",
                    metadata={
                        "pnl_pct": pnl_pct,
                        "holding_days": holding_days,
                        "exit_type": "time_stop",
                    },
                )
        except (ValueError, TypeError):
            pass

        return None
