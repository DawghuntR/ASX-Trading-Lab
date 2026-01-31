"""News Reaction Analytics Job.

Implements Feature 022 - News Reaction Analytics (1D).
Computes 1-day price reaction metrics following ASX announcements.
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any

from asx_jobs.database import Database
from asx_jobs.jobs.base import BaseJob, JobResult
from asx_jobs.logging import get_logger

logger = get_logger(__name__)


@dataclass
class ReactionConfig:
    """Configuration for reaction metrics computation."""

    positive_threshold_pct: float = 1.0
    negative_threshold_pct: float = -1.0
    strong_threshold_pct: float = 5.0
    lookback_days: int = 90
    max_gap_days: int = 5


@dataclass
class ReactionMetrics:
    """Computed reaction metrics for an announcement."""

    announcement_id: int
    instrument_id: int
    announcement_date: str
    announcement_close: float | None
    announcement_volume: int | None
    next_day_date: str | None
    next_day_open: float | None
    next_day_close: float | None
    next_day_high: float | None
    next_day_low: float | None
    next_day_volume: int | None
    return_1d: float | None
    return_1d_pct: float | None
    gap_open_pct: float | None
    intraday_range_pct: float | None
    volume_change_pct: float | None
    reaction_direction: str
    reaction_strength: str
    document_type: str | None
    sensitivity: str | None
    headline: str


class ComputeReactionsJob(BaseJob):
    """Compute 1-day price reactions for announcements."""

    def __init__(
        self,
        db: Database,
        config: ReactionConfig | None = None,
        lookback_date: date | None = None,
    ) -> None:
        """Initialize the reactions computation job.

        Args:
            db: Database client.
            config: Reaction configuration.
            lookback_date: Compute reactions for announcements after this date.
        """
        self.db = db
        self.config = config or ReactionConfig()
        self.lookback_date = lookback_date or (
            date.today() - timedelta(days=self.config.lookback_days)
        )

    @property
    def name(self) -> str:
        return "compute_reactions"

    def run(self) -> JobResult:
        """Execute reaction metrics computation."""
        started_at = datetime.now()
        reactions_computed = 0
        failed = 0
        errors: list[str] = []

        announcements = self._get_unprocessed_announcements()
        logger.info(
            "reactions_job_started",
            job=self.name,
            announcements_count=len(announcements),
            lookback_date=self.lookback_date.isoformat(),
        )

        if not announcements:
            logger.info("no_announcements_to_process")
            return JobResult(
                job_name=self.name,
                success=True,
                started_at=started_at,
                completed_at=datetime.now(),
                records_processed=0,
                records_failed=0,
                metadata={"message": "No unprocessed announcements found"},
            )

        instrument_ids = list({a["instrument_id"] for a in announcements})
        prices_by_instrument = self._fetch_price_data(instrument_ids)

        for announcement in announcements:
            try:
                metrics = self._compute_reaction(announcement, prices_by_instrument)
                if metrics:
                    self._save_reaction(metrics)
                    reactions_computed += 1
            except Exception as e:
                failed += 1
                errors.append(f"Announcement {announcement['id']}: {str(e)}")
                logger.warning(
                    "reaction_computation_failed",
                    announcement_id=announcement["id"],
                    error=str(e),
                )

        completed_at = datetime.now()

        logger.info(
            "reactions_job_completed",
            job=self.name,
            reactions_computed=reactions_computed,
            failed=failed,
            duration_seconds=(completed_at - started_at).total_seconds(),
        )

        return JobResult(
            job_name=self.name,
            success=failed < len(announcements) // 2,
            started_at=started_at,
            completed_at=completed_at,
            records_processed=reactions_computed,
            records_failed=failed,
            error_message="; ".join(errors[:10]) if errors else None,
            metadata={
                "announcements_count": len(announcements),
                "lookback_date": self.lookback_date.isoformat(),
            },
        )

    def _get_unprocessed_announcements(self) -> list[dict[str, Any]]:
        """Get announcements that haven't had reactions computed yet."""
        result = (
            self.db.client.table("announcements")
            .select("*")
            .gte("announced_at", self.lookback_date.isoformat())
            .order("announced_at", desc=True)
            .execute()
        )

        announcement_ids = [a["id"] for a in result.data]
        if not announcement_ids:
            return []

        existing = (
            self.db.client.table("announcement_reactions")
            .select("announcement_id")
            .in_("announcement_id", announcement_ids)
            .execute()
        )
        processed_ids = {r["announcement_id"] for r in existing.data}

        unprocessed: list[dict[str, Any]] = [
            a for a in result.data if a["id"] not in processed_ids  # type: ignore[misc]
        ]
        return unprocessed

    def _fetch_price_data(self, instrument_ids: list[int]) -> dict[int, list[dict[str, Any]]]:
        """Fetch price data for all relevant instruments."""
        start_date = (self.lookback_date - timedelta(days=10)).isoformat()
        end_date = (date.today() + timedelta(days=1)).isoformat()

        return self.db.get_all_price_history_range(
            start_date=start_date,
            end_date=end_date,
            instrument_ids=instrument_ids,
        )

    def _compute_reaction(
        self,
        announcement: dict[str, Any],
        prices_by_instrument: dict[int, list[dict[str, Any]]],
    ) -> ReactionMetrics | None:
        """Compute reaction metrics for a single announcement."""
        instrument_id = announcement["instrument_id"]
        announced_at = announcement["announced_at"]

        if isinstance(announced_at, str):
            announcement_dt = datetime.fromisoformat(announced_at.replace("Z", "+00:00"))
        else:
            announcement_dt = announced_at

        announcement_date = announcement_dt.date()
        announcement_date_str = announcement_date.isoformat()

        prices = prices_by_instrument.get(instrument_id, [])
        if not prices:
            return None

        prices_by_date = {p["trade_date"]: p for p in prices}

        announcement_price = prices_by_date.get(announcement_date_str)
        if not announcement_price:
            for i in range(1, 4):
                check_date = (announcement_date - timedelta(days=i)).isoformat()
                if check_date in prices_by_date:
                    announcement_price = prices_by_date[check_date]
                    break

        if not announcement_price:
            return None

        next_day_price = None
        for i in range(1, self.config.max_gap_days + 1):
            check_date = (announcement_date + timedelta(days=i)).isoformat()
            if check_date in prices_by_date:
                next_day_price = prices_by_date[check_date]
                break

        if not next_day_price:
            return None

        return self._calculate_metrics(announcement, announcement_price, next_day_price)

    def _calculate_metrics(
        self,
        announcement: dict[str, Any],
        announcement_price: dict[str, Any],
        next_day_price: dict[str, Any],
    ) -> ReactionMetrics:
        """Calculate reaction metrics from price data."""
        ann_close = float(announcement_price["close"]) if announcement_price["close"] else None
        ann_volume = int(announcement_price.get("volume") or 0)

        next_open = float(next_day_price.get("open") or 0) if next_day_price.get("open") else None
        next_close = float(next_day_price["close"]) if next_day_price["close"] else None
        next_high = float(next_day_price.get("high") or 0) if next_day_price.get("high") else None
        next_low = float(next_day_price.get("low") or 0) if next_day_price.get("low") else None
        next_volume = int(next_day_price.get("volume") or 0)

        return_1d = None
        return_1d_pct = None
        gap_open_pct = None
        intraday_range_pct = None
        volume_change_pct = None

        if ann_close and next_close:
            return_1d = next_close - ann_close
            return_1d_pct = (return_1d / ann_close) * 100

        if ann_close and next_open:
            gap_open_pct = ((next_open - ann_close) / ann_close) * 100

        if next_open and next_high and next_low and next_open > 0:
            intraday_range_pct = ((next_high - next_low) / next_open) * 100

        if ann_volume and ann_volume > 0 and next_volume:
            volume_change_pct = ((next_volume - ann_volume) / ann_volume) * 100

        direction = self._determine_direction(return_1d_pct)
        strength = self._determine_strength(return_1d_pct)

        announced_at = announcement["announced_at"]
        if isinstance(announced_at, str):
            announcement_dt = datetime.fromisoformat(announced_at.replace("Z", "+00:00"))
            announcement_date_str = announcement_dt.date().isoformat()
        else:
            announcement_date_str = announced_at.date().isoformat()

        return ReactionMetrics(
            announcement_id=announcement["id"],
            instrument_id=announcement["instrument_id"],
            announcement_date=announcement_date_str,
            announcement_close=ann_close,
            announcement_volume=ann_volume if ann_volume > 0 else None,
            next_day_date=next_day_price["trade_date"],
            next_day_open=next_open,
            next_day_close=next_close,
            next_day_high=next_high,
            next_day_low=next_low,
            next_day_volume=next_volume if next_volume > 0 else None,
            return_1d=return_1d,
            return_1d_pct=return_1d_pct,
            gap_open_pct=gap_open_pct,
            intraday_range_pct=intraday_range_pct,
            volume_change_pct=volume_change_pct,
            reaction_direction=direction,
            reaction_strength=strength,
            document_type=announcement.get("document_type"),
            sensitivity=announcement.get("sensitivity"),
            headline=announcement["headline"],
        )

    def _determine_direction(self, return_pct: float | None) -> str:
        """Determine reaction direction based on return percentage."""
        if return_pct is None:
            return "neutral"
        if return_pct >= self.config.positive_threshold_pct:
            return "positive"
        if return_pct <= self.config.negative_threshold_pct:
            return "negative"
        return "neutral"

    def _determine_strength(self, return_pct: float | None) -> str:
        """Determine reaction strength based on return percentage."""
        if return_pct is None:
            return "weak"
        abs_return = abs(return_pct)
        if abs_return >= self.config.strong_threshold_pct:
            return "strong"
        if abs_return >= self.config.positive_threshold_pct * 2:
            return "medium"
        return "weak"

    def _save_reaction(self, metrics: ReactionMetrics) -> None:
        """Save reaction metrics to database."""
        data = {
            "announcement_id": metrics.announcement_id,
            "instrument_id": metrics.instrument_id,
            "announcement_date": metrics.announcement_date,
            "announcement_close": metrics.announcement_close,
            "announcement_volume": metrics.announcement_volume,
            "next_day_date": metrics.next_day_date,
            "next_day_open": metrics.next_day_open,
            "next_day_close": metrics.next_day_close,
            "next_day_high": metrics.next_day_high,
            "next_day_low": metrics.next_day_low,
            "next_day_volume": metrics.next_day_volume,
            "return_1d": metrics.return_1d,
            "return_1d_pct": metrics.return_1d_pct,
            "gap_open_pct": metrics.gap_open_pct,
            "intraday_range_pct": metrics.intraday_range_pct,
            "volume_change_pct": metrics.volume_change_pct,
            "reaction_direction": metrics.reaction_direction,
            "reaction_strength": metrics.reaction_strength,
            "document_type": metrics.document_type,
            "sensitivity": metrics.sensitivity,
            "headline": metrics.headline,
        }

        self.db.client.table("announcement_reactions").upsert(
            data, on_conflict="announcement_id"
        ).execute()
