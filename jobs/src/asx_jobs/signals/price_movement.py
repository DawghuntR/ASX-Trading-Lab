"""Price Movement Signal Engine.

Implements Feature 016 - Signal Engine: Price Movement Tracker.
Detects significant price movements, momentum, and unusual volume.
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

from asx_jobs.database import Database
from asx_jobs.jobs.base import BaseJob, JobResult
from asx_jobs.logging import get_logger

logger = get_logger(__name__)


@dataclass
class PriceMovementConfig:
    """Configuration for price movement detection."""
    
    daily_change_threshold: float = 5.0
    five_day_change_threshold: float = 10.0
    volume_spike_multiplier: float = 2.0
    volume_baseline_days: int = 20
    min_price: float = 0.01
    lookback_days: int = 30


class PriceMovementSignalJob(BaseJob):
    """Generate price movement signals for all instruments."""

    def __init__(
        self,
        db: Database,
        config: PriceMovementConfig | None = None,
        signal_date: date | None = None,
    ) -> None:
        """Initialize the signal engine.

        Args:
            db: Database client.
            config: Signal configuration.
            signal_date: Date to generate signals for (defaults to today).
        """
        self.db = db
        self.config = config or PriceMovementConfig()
        self.signal_date = signal_date or date.today()

    @property
    def name(self) -> str:
        return "price_movement_signals"

    def run(self) -> JobResult:
        """Execute price movement signal generation."""
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
                count = self._process_instrument(instrument)
                signals_generated += count
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

    def _process_instrument(self, instrument: dict[str, Any]) -> int:
        """Process a single instrument for signals.

        Args:
            instrument: Instrument record.

        Returns:
            Number of signals generated.
        """
        symbol = instrument["symbol"]
        instrument_id = instrument["id"]

        prices = self.db.get_price_history(
            instrument_id=instrument_id,
            days=self.config.lookback_days,
        )

        if len(prices) < 2:
            return 0

        signals_count = 0
        latest = prices[0]
        previous = prices[1]

        if latest["close"] < self.config.min_price:
            return 0

        daily_change = self._calc_daily_change(latest, previous)
        if daily_change is not None:
            signal = self._check_daily_movement(
                instrument_id, symbol, latest, daily_change
            )
            if signal:
                self.db.insert_signal(signal)
                signals_count += 1

        if len(prices) >= 6:
            five_day_change = self._calc_multi_day_change(prices, 5)
            if five_day_change is not None:
                signal = self._check_momentum(
                    instrument_id, symbol, latest, five_day_change
                )
                if signal:
                    self.db.insert_signal(signal)
                    signals_count += 1

        if len(prices) >= self.config.volume_baseline_days:
            volume_ratio = self._calc_volume_ratio(
                prices, self.config.volume_baseline_days
            )
            if volume_ratio is not None:
                signal = self._check_volume_spike(
                    instrument_id, symbol, latest, volume_ratio
                )
                if signal:
                    self.db.insert_signal(signal)
                    signals_count += 1

        return signals_count

    def _calc_daily_change(
        self, latest: dict[str, Any], previous: dict[str, Any]
    ) -> float | None:
        """Calculate daily percentage change."""
        if previous["close"] is None or previous["close"] == 0:
            return None
        return ((latest["close"] - previous["close"]) / previous["close"]) * 100

    def _calc_multi_day_change(
        self, prices: list[dict[str, Any]], days: int
    ) -> float | None:
        """Calculate multi-day percentage change."""
        if len(prices) < days + 1:
            return None
        baseline = prices[days]["close"]
        if baseline is None or baseline == 0:
            return None
        return ((prices[0]["close"] - baseline) / baseline) * 100

    def _calc_volume_ratio(
        self, prices: list[dict[str, Any]], baseline_days: int
    ) -> float | None:
        """Calculate volume ratio vs baseline average."""
        if len(prices) < baseline_days:
            return None

        today_volume = prices[0].get("volume", 0)
        if today_volume is None or today_volume == 0:
            return None

        baseline_volumes: list[int] = []
        for p in prices[1:baseline_days + 1]:
            vol = p.get("volume")
            if vol is not None and vol > 0:
                baseline_volumes.append(vol)

        if not baseline_volumes:
            return None

        avg_volume = sum(baseline_volumes) / len(baseline_volumes)
        if avg_volume == 0:
            return None

        return today_volume / avg_volume

    def _check_daily_movement(
        self,
        instrument_id: int,
        symbol: str,
        price: dict[str, Any],
        change_pct: float,
    ) -> dict[str, Any] | None:
        """Check for significant daily price movement."""
        threshold = self.config.daily_change_threshold

        if abs(change_pct) < threshold:
            return None

        direction = "up" if change_pct > 0 else "down"
        strength = self._calc_strength(abs(change_pct), threshold, threshold * 3)

        return {
            "instrument_id": instrument_id,
            "signal_date": self.signal_date.isoformat(),
            "signal_type": "price_movement",
            "direction": direction,
            "strength": strength,
            "trigger_price": price["close"],
            "trigger_reason": f"Daily change {change_pct:+.1f}% exceeds {threshold}% threshold",
            "metrics": {
                "daily_change_pct": round(change_pct, 2),
                "close": price["close"],
                "volume": price.get("volume"),
            },
        }

    def _check_momentum(
        self,
        instrument_id: int,
        symbol: str,
        price: dict[str, Any],
        change_pct: float,
    ) -> dict[str, Any] | None:
        """Check for significant 5-day momentum."""
        threshold = self.config.five_day_change_threshold

        if abs(change_pct) < threshold:
            return None

        direction = "up" if change_pct > 0 else "down"
        strength = self._calc_strength(abs(change_pct), threshold, threshold * 2)

        return {
            "instrument_id": instrument_id,
            "signal_date": self.signal_date.isoformat(),
            "signal_type": "momentum",
            "direction": direction,
            "strength": strength,
            "trigger_price": price["close"],
            "trigger_reason": f"5-day change {change_pct:+.1f}% exceeds {threshold}% threshold",
            "metrics": {
                "five_day_change_pct": round(change_pct, 2),
                "close": price["close"],
            },
        }

    def _check_volume_spike(
        self,
        instrument_id: int,
        symbol: str,
        price: dict[str, Any],
        volume_ratio: float,
    ) -> dict[str, Any] | None:
        """Check for unusual volume."""
        multiplier = self.config.volume_spike_multiplier

        if volume_ratio < multiplier:
            return None

        strength = self._calc_strength(volume_ratio, multiplier, multiplier * 3)

        return {
            "instrument_id": instrument_id,
            "signal_date": self.signal_date.isoformat(),
            "signal_type": "volume_spike",
            "direction": "neutral",
            "strength": strength,
            "trigger_price": price["close"],
            "trigger_reason": f"Volume {volume_ratio:.1f}x above {self.config.volume_baseline_days}-day average",
            "metrics": {
                "volume_ratio": round(volume_ratio, 2),
                "volume": price.get("volume"),
                "baseline_days": self.config.volume_baseline_days,
            },
        }

    def _calc_strength(
        self, value: float, low_threshold: float, high_threshold: float
    ) -> str:
        """Calculate signal strength based on thresholds."""
        if value >= high_threshold:
            return "strong"
        elif value >= (low_threshold + high_threshold) / 2:
            return "medium"
        else:
            return "weak"
