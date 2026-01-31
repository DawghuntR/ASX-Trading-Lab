"""Breakout Strategy.

Buy when price breaks above the N-day high. Exit using a trailing stop,
fixed stop loss, or time-based exit.

This strategy attempts to capture momentum when stocks break out of
consolidation patterns.
"""

from dataclasses import dataclass
from typing import Any

from asx_jobs.backtest.strategy import SignalType, Strategy, StrategyConfig, StrategySignal


@dataclass
class BreakoutConfig(StrategyConfig):
    """Configuration for breakout strategy.

    Attributes:
        lookback_days: Number of days to look back for high.
        trailing_stop_pct: Trailing stop percentage from peak.
        stop_loss_pct: Initial stop loss percentage.
        max_holding_days: Maximum days to hold.
        min_breakout_pct: Minimum percentage above prior high.
        require_volume_confirmation: Require above-average volume on breakout.
        volume_multiplier: Volume must be this times average.
        min_price: Minimum stock price to consider.
    """

    lookback_days: int = 20
    trailing_stop_pct: float = 5.0
    stop_loss_pct: float = 3.0
    max_holding_days: int = 20
    min_breakout_pct: float = 1.0
    require_volume_confirmation: bool = True
    volume_multiplier: float = 1.5
    min_price: float = 0.50


class BreakoutStrategy(Strategy):
    """Breakout strategy.

    Entry: Buy when today's close exceeds the highest close of the
           past N days by at least min_breakout_pct, optionally
           with volume confirmation.

    Exit: Sell when:
      - Price drops trailing_stop_pct from the highest price since entry
      - Price drops stop_loss_pct from entry (initial stop)
      - Holding period exceeds max_holding_days
    """

    def __init__(
        self,
        lookback_days: int = 20,
        trailing_stop_pct: float = 5.0,
        stop_loss_pct: float = 3.0,
        max_holding_days: int = 20,
        min_breakout_pct: float = 1.0,
        require_volume_confirmation: bool = True,
        volume_multiplier: float = 1.5,
        min_price: float = 0.50,
    ) -> None:
        """Initialize the strategy.

        Args:
            lookback_days: Days to look back for the high.
            trailing_stop_pct: Trailing stop percentage.
            stop_loss_pct: Initial stop loss percentage.
            max_holding_days: Maximum holding period.
            min_breakout_pct: Minimum breakout percentage.
            require_volume_confirmation: Require volume confirmation.
            volume_multiplier: Volume must exceed average by this factor.
            min_price: Minimum stock price filter.
        """
        config = BreakoutConfig(
            name="Breakout",
            version="1.0.0",
            description=(
                f"Buy {lookback_days}-day breakout, exit with {trailing_stop_pct}% trailing stop"
            ),
            lookback_days=lookback_days,
            trailing_stop_pct=trailing_stop_pct,
            stop_loss_pct=stop_loss_pct,
            max_holding_days=max_holding_days,
            min_breakout_pct=min_breakout_pct,
            require_volume_confirmation=require_volume_confirmation,
            volume_multiplier=volume_multiplier,
            min_price=min_price,
        )
        super().__init__(config)
        self._config = config
        self._peak_prices: dict[int, float] = {}

    def get_parameters(self) -> dict[str, Any]:
        """Get strategy parameters."""
        return {
            "lookback_days": self._config.lookback_days,
            "trailing_stop_pct": self._config.trailing_stop_pct,
            "stop_loss_pct": self._config.stop_loss_pct,
            "max_holding_days": self._config.max_holding_days,
            "min_breakout_pct": self._config.min_breakout_pct,
            "require_volume_confirmation": self._config.require_volume_confirmation,
            "volume_multiplier": self._config.volume_multiplier,
            "min_price": self._config.min_price,
        }

    def on_start(self, start_date: str, end_date: str) -> None:
        """Reset tracking state."""
        self._peak_prices = {}

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
            if instrument_id in self._peak_prices:
                self._peak_prices[instrument_id] = max(
                    self._peak_prices[instrument_id], current_price
                )
            else:
                self._peak_prices[instrument_id] = current_price

            return self._check_exit(instrument_id, symbol, bar, position)
        else:
            if instrument_id in self._peak_prices:
                del self._peak_prices[instrument_id]

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

        if len(history) < self._config.lookback_days:
            return None

        lookback_prices = history[: self._config.lookback_days]
        highest_high = max(h["high"] or h["close"] for h in lookback_prices)

        breakout_pct = ((current_price - highest_high) / highest_high) * 100

        if breakout_pct < self._config.min_breakout_pct:
            return None

        if self._config.require_volume_confirmation:
            current_volume = bar.get("volume", 0)
            if not current_volume:
                return None

            historical_volumes = [h.get("volume", 0) for h in lookback_prices if h.get("volume")]
            if not historical_volumes:
                return None

            avg_volume = sum(historical_volumes) / len(historical_volumes)
            if current_volume < avg_volume * self._config.volume_multiplier:
                return None

        self._peak_prices[instrument_id] = current_price

        return StrategySignal(
            signal_type=SignalType.BUY,
            instrument_id=instrument_id,
            symbol=symbol,
            price=current_price,
            reason=f"Breakout: {breakout_pct:.1f}% above {self._config.lookback_days}-day high",
            metadata={
                "breakout_pct": breakout_pct,
                "prior_high": highest_high,
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

        pnl_from_entry = ((current_price - entry_price) / entry_price) * 100

        if pnl_from_entry <= -self._config.stop_loss_pct:
            return StrategySignal(
                signal_type=SignalType.SELL,
                instrument_id=instrument_id,
                symbol=symbol,
                price=current_price,
                reason=f"Stop loss hit: {pnl_from_entry:.1f}%",
                metadata={"pnl_pct": pnl_from_entry, "exit_type": "stop_loss"},
            )

        peak_price = self._peak_prices.get(instrument_id, entry_price)
        drawdown_from_peak = ((peak_price - current_price) / peak_price) * 100

        if drawdown_from_peak >= self._config.trailing_stop_pct:
            return StrategySignal(
                signal_type=SignalType.SELL,
                instrument_id=instrument_id,
                symbol=symbol,
                price=current_price,
                reason=f"Trailing stop hit: {drawdown_from_peak:.1f}% from peak",
                metadata={
                    "pnl_pct": pnl_from_entry,
                    "peak_price": peak_price,
                    "drawdown_pct": drawdown_from_peak,
                    "exit_type": "trailing_stop",
                },
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
                        "pnl_pct": pnl_from_entry,
                        "holding_days": holding_days,
                        "exit_type": "time_stop",
                    },
                )
        except (ValueError, TypeError):
            pass

        return None
