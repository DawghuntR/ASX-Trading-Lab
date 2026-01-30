"""Volatility Spike Signal Engine.

Implements Feature 017 - Signal Engine: Volatility Spike Watcher.
Detects abnormal daily range (volatility) compared to recent averages.
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

from asx_jobs.database import Database
from asx_jobs.jobs.base import BaseJob, JobResult
from asx_jobs.logging import get_logger

logger = get_logger(__name__)


@dataclass
class VolatilityConfig:
    """Configuration for volatility spike detection."""

    atr_window: int = 14
    spike_multiplier: float = 2.0
    strong_spike_multiplier: float = 3.0
    min_price: float = 0.01
    min_atr: float = 0.001


class VolatilitySpikeSignalJob(BaseJob):
    """Generate volatility spike signals for all instruments."""

    def __init__(
        self,
        db: Database,
        config: VolatilityConfig | None = None,
        signal_date: date | None = None,
    ) -> None:
        """Initialize the signal engine.

        Args:
            db: Database client.
            config: Signal configuration.
            signal_date: Date to generate signals for (defaults to today).
        """
        self.db = db
        self.config = config or VolatilityConfig()
        self.signal_date = signal_date or date.today()

    @property
    def name(self) -> str:
        return "volatility_spike_signals"

    def run(self) -> JobResult:
        """Execute volatility spike signal generation."""
        started_at = datetime.now()
        signals_generated = 0
        failed = 0
        errors: list[str] = []

        instruments = self.db.get_all_active_instruments()
        logger.info(
            "signal_job_started",
            job=self.name,
            instruments_count=len(instruments),
            signal_date=self.signal_date.isoformat(),
        )

        for instrument in instruments:
            try:
                signal = self._process_instrument(instrument)
                if signal:
                    self.db.insert_signal(signal)
                    signals_generated += 1
            except Exception as e:
                failed += 1
                errors.append(f"{instrument['symbol']}: {str(e)}")
                logger.warning(
                    "signal_generation_failed",
                    symbol=instrument["symbol"],
                    error=str(e),
                )

        completed_at = datetime.now()

        logger.info(
            "signal_job_completed",
            job=self.name,
            signals_generated=signals_generated,
            failed=failed,
            duration_seconds=(completed_at - started_at).total_seconds(),
        )

        return JobResult(
            job_name=self.name,
            success=failed < len(instruments),
            started_at=started_at,
            completed_at=completed_at,
            records_processed=signals_generated,
            records_failed=failed,
            error_message="; ".join(errors[:10]) if errors else None,
            metadata={
                "instruments_count": len(instruments),
                "signal_date": self.signal_date.isoformat(),
            },
        )

    def _process_instrument(
        self, instrument: dict[str, Any]
    ) -> dict[str, Any] | None:
        """Process a single instrument for volatility signals.

        Args:
            instrument: Instrument record.

        Returns:
            Signal record if triggered, None otherwise.
        """
        instrument_id = instrument["id"]

        prices = self.db.get_price_history(
            instrument_id=instrument_id,
            days=self.config.atr_window + 5,
        )

        if len(prices) < self.config.atr_window + 1:
            return None

        latest = prices[0]

        if latest["close"] is None or latest["close"] < self.config.min_price:
            return None

        today_range = self._calc_true_range(latest, prices[1])
        if today_range is None:
            return None

        atr = self._calc_atr(prices[1:], self.config.atr_window)
        if atr is None or atr < self.config.min_atr:
            return None

        range_ratio = today_range / atr

        if range_ratio < self.config.spike_multiplier:
            return None

        strength = self._determine_strength(range_ratio)

        return {
            "instrument_id": instrument_id,
            "signal_date": self.signal_date.isoformat(),
            "signal_type": "volatility_spike",
            "direction": "neutral",
            "strength": strength,
            "trigger_price": latest["close"],
            "trigger_reason": (
                f"Daily range {range_ratio:.1f}x above "
                f"{self.config.atr_window}-day ATR"
            ),
            "metrics": {
                "true_range": round(today_range, 4),
                "atr": round(atr, 4),
                "range_ratio": round(range_ratio, 2),
                "atr_window": self.config.atr_window,
                "high": latest.get("high"),
                "low": latest.get("low"),
                "close": latest["close"],
            },
        }

    def _calc_true_range(
        self,
        current: dict[str, Any],
        previous: dict[str, Any],
    ) -> float | None:
        """Calculate true range for current bar.

        True Range = max(
            high - low,
            abs(high - previous_close),
            abs(low - previous_close)
        )
        """
        high = current.get("high")
        low = current.get("low")
        prev_close = previous.get("close")

        if high is None or low is None or prev_close is None:
            return None

        return max(
            high - low,
            abs(high - prev_close),
            abs(low - prev_close),
        )

    def _calc_atr(
        self,
        prices: list[dict[str, Any]],
        window: int,
    ) -> float | None:
        """Calculate Average True Range over window.

        Args:
            prices: Price history (most recent first).
            window: Number of periods for ATR.

        Returns:
            ATR value or None if insufficient data.
        """
        if len(prices) < window + 1:
            return None

        true_ranges: list[float] = []
        for i in range(window):
            tr = self._calc_true_range(prices[i], prices[i + 1])
            if tr is not None:
                true_ranges.append(tr)

        if len(true_ranges) < window // 2:
            return None

        return sum(true_ranges) / len(true_ranges)

    def _determine_strength(self, range_ratio: float) -> str:
        """Determine signal strength based on range ratio."""
        if range_ratio >= self.config.strong_spike_multiplier:
            return "strong"
        elif range_ratio >= (
            self.config.spike_multiplier + self.config.strong_spike_multiplier
        ) / 2:
            return "medium"
        else:
            return "weak"
