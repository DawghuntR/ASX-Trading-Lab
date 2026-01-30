"""Job orchestrator for running all daily jobs."""

from dataclasses import dataclass
from datetime import datetime

from asx_jobs.config import Config
from asx_jobs.database import Database
from asx_jobs.jobs.base import JobResult
from asx_jobs.jobs.compute_reactions import ComputeReactionsJob
from asx_jobs.jobs.ingest_announcements import IngestAnnouncementsJob
from asx_jobs.jobs.ingest_prices import BackfillPricesJob, IngestPricesJob
from asx_jobs.jobs.ingest_symbols import IngestSymbolsJob
from asx_jobs.logging import get_logger
from asx_jobs.observability import DataQualityMonitor, JobRunTracker
from asx_jobs.providers.yahoo import YahooFinanceProvider
from asx_jobs.signals.price_movement import PriceMovementSignalJob
from asx_jobs.signals.volatility import VolatilitySpikeSignalJob

logger = get_logger(__name__)


@dataclass
class OrchestratorResult:
    """Result of orchestrator execution."""

    started_at: datetime
    completed_at: datetime
    jobs_run: int
    jobs_succeeded: int
    jobs_failed: int
    results: list[JobResult]

    @property
    def success(self) -> bool:
        return self.jobs_failed == 0

    @property
    def duration_seconds(self) -> float:
        return (self.completed_at - self.started_at).total_seconds()


class JobOrchestrator:
    """Orchestrates execution of all daily jobs."""

    def __init__(self, config: Config) -> None:
        """Initialize the orchestrator.

        Args:
            config: Application configuration.
        """
        self.config = config
        self.db = Database(config.supabase)
        self.provider = YahooFinanceProvider(config.yahoo)
        self.job_tracker = JobRunTracker(self.db)
        self.quality_monitor = DataQualityMonitor(self.db)

    def run_daily(self) -> OrchestratorResult:
        """Run all daily jobs in sequence.

        Order:
        1. Ingest symbols (update instrument universe)
        2. Ingest prices (fetch latest daily bars)
        3. Ingest announcements (scrape ASX announcements)
        4. Generate price movement signals
        5. Generate volatility spike signals
        6. Run data quality checks

        Returns:
            OrchestratorResult with all job results.
        """
        started_at = datetime.now()
        results: list[JobResult] = []

        logger.info("orchestrator_started", mode="daily")

        jobs = [
            IngestSymbolsJob(
                db=self.db,
                provider=self.provider,
                fetch_metadata=False,
            ),
            IngestPricesJob(
                db=self.db,
                provider=self.provider,
                lookback_days=7,
                batch_size=self.config.yahoo.batch_size,
            ),
            IngestAnnouncementsJob(db=self.db),
            PriceMovementSignalJob(db=self.db),
            VolatilitySpikeSignalJob(db=self.db),
        ]

        for job in jobs:
            logger.info("job_starting", job=job.name)
            try:
                result = job.run()
                results.append(result)

                # Persist job run to database
                self._record_job_run(result)

                if not result.success:
                    logger.warning(
                        "job_partial_failure",
                        job=job.name,
                        failed=result.records_failed,
                    )
            except Exception as e:
                logger.error("job_exception", job=job.name, error=str(e))
                error_result = JobResult(
                    job_name=job.name,
                    success=False,
                    started_at=datetime.now(),
                    completed_at=datetime.now(),
                    error_message=str(e),
                )
                results.append(error_result)
                self._record_job_run(error_result)

        # Run data quality checks after all jobs complete
        self._run_quality_checks()

        completed_at = datetime.now()
        succeeded = sum(1 for r in results if r.success)
        failed = len(results) - succeeded

        logger.info(
            "orchestrator_completed",
            mode="daily",
            jobs_run=len(results),
            jobs_succeeded=succeeded,
            jobs_failed=failed,
            duration_seconds=(completed_at - started_at).total_seconds(),
        )

        return OrchestratorResult(
            started_at=started_at,
            completed_at=completed_at,
            jobs_run=len(results),
            jobs_succeeded=succeeded,
            jobs_failed=failed,
            results=results,
        )

    def run_backfill(self, period: str = "2y") -> OrchestratorResult:
        """Run historical backfill.

        Args:
            period: History period (e.g., '1y', '2y', '5y', 'max').

        Returns:
            OrchestratorResult with backfill results.
        """
        started_at = datetime.now()
        results: list[JobResult] = []

        logger.info("orchestrator_started", mode="backfill", period=period)

        jobs = [
            IngestSymbolsJob(
                db=self.db,
                provider=self.provider,
                fetch_metadata=True,
            ),
            BackfillPricesJob(
                db=self.db,
                provider=self.provider,
                period=period,
            ),
        ]

        for job in jobs:
            logger.info("job_starting", job=job.name)
            try:
                result = job.run()
                results.append(result)
            except Exception as e:
                logger.error("job_exception", job=job.name, error=str(e))
                results.append(
                    JobResult(
                        job_name=job.name,
                        success=False,
                        started_at=datetime.now(),
                        completed_at=datetime.now(),
                        error_message=str(e),
                    )
                )

        completed_at = datetime.now()
        succeeded = sum(1 for r in results if r.success)
        failed = len(results) - succeeded

        logger.info(
            "orchestrator_completed",
            mode="backfill",
            jobs_run=len(results),
            jobs_succeeded=succeeded,
            jobs_failed=failed,
            duration_seconds=(completed_at - started_at).total_seconds(),
        )

        return OrchestratorResult(
            started_at=started_at,
            completed_at=completed_at,
            jobs_run=len(results),
            jobs_succeeded=succeeded,
            jobs_failed=failed,
            results=results,
        )

    def run_symbols_only(self, fetch_metadata: bool = True) -> OrchestratorResult:
        """Run only symbol ingestion.

        Args:
            fetch_metadata: Whether to fetch metadata from Yahoo.

        Returns:
            OrchestratorResult.
        """
        started_at = datetime.now()

        logger.info("orchestrator_started", mode="symbols_only")

        job = IngestSymbolsJob(
            db=self.db,
            provider=self.provider,
            fetch_metadata=fetch_metadata,
        )

        result = job.run()

        completed_at = datetime.now()

        return OrchestratorResult(
            started_at=started_at,
            completed_at=completed_at,
            jobs_run=1,
            jobs_succeeded=1 if result.success else 0,
            jobs_failed=0 if result.success else 1,
            results=[result],
        )

    def run_signals(self) -> OrchestratorResult:
        """Run only signal generation jobs.

        Order:
        1. Price movement signals
        2. Volatility spike signals

        Returns:
            OrchestratorResult with signal job results.
        """
        started_at = datetime.now()
        results: list[JobResult] = []

        logger.info("orchestrator_started", mode="signals")

        jobs = [
            PriceMovementSignalJob(db=self.db),
            VolatilitySpikeSignalJob(db=self.db),
        ]

        for job in jobs:
            logger.info("job_starting", job=job.name)
            try:
                result = job.run()
                results.append(result)
                if not result.success:
                    logger.warning(
                        "job_partial_failure",
                        job=job.name,
                        failed=result.records_failed,
                    )
            except Exception as e:
                logger.error("job_exception", job=job.name, error=str(e))
                results.append(
                    JobResult(
                        job_name=job.name,
                        success=False,
                        started_at=datetime.now(),
                        completed_at=datetime.now(),
                        error_message=str(e),
                    )
                )

        completed_at = datetime.now()
        succeeded = sum(1 for r in results if r.success)
        failed = len(results) - succeeded

        logger.info(
            "orchestrator_completed",
            mode="signals",
            jobs_run=len(results),
            jobs_succeeded=succeeded,
            jobs_failed=failed,
            duration_seconds=(completed_at - started_at).total_seconds(),
        )

        return OrchestratorResult(
            started_at=started_at,
            completed_at=completed_at,
            jobs_run=len(results),
            jobs_succeeded=succeeded,
            jobs_failed=failed,
            results=results,
        )

    def run_announcements(self) -> OrchestratorResult:
        """Run only announcements ingestion job.

        Returns:
            OrchestratorResult with announcements job result.
        """
        started_at = datetime.now()

        logger.info("orchestrator_started", mode="announcements")

        job = IngestAnnouncementsJob(db=self.db)

        try:
            result = job.run()
        except Exception as e:
            logger.error("job_exception", job=job.name, error=str(e))
            result = JobResult(
                job_name=job.name,
                success=False,
                started_at=datetime.now(),
                completed_at=datetime.now(),
                error_message=str(e),
            )

        completed_at = datetime.now()

        logger.info(
            "orchestrator_completed",
            mode="announcements",
            jobs_run=1,
            jobs_succeeded=1 if result.success else 0,
            jobs_failed=0 if result.success else 1,
            duration_seconds=(completed_at - started_at).total_seconds(),
        )

        return OrchestratorResult(
            started_at=started_at,
            completed_at=completed_at,
            jobs_run=1,
            jobs_succeeded=1 if result.success else 0,
            jobs_failed=0 if result.success else 1,
            results=[result],
        )

    def run_reactions(self, lookback_days: int = 90) -> OrchestratorResult:
        """Run only reaction metrics computation job.

        Args:
            lookback_days: Number of days to look back for announcements.

        Returns:
            OrchestratorResult with reactions job result.
        """
        from datetime import date, timedelta

        started_at = datetime.now()

        logger.info("orchestrator_started", mode="reactions")

        lookback_date = date.today() - timedelta(days=lookback_days)
        job = ComputeReactionsJob(db=self.db, lookback_date=lookback_date)

        try:
            result = job.run()
        except Exception as e:
            logger.error("job_exception", job=job.name, error=str(e))
            result = JobResult(
                job_name=job.name,
                success=False,
                started_at=datetime.now(),
                completed_at=datetime.now(),
                error_message=str(e),
            )

        completed_at = datetime.now()

        logger.info(
            "orchestrator_completed",
            mode="reactions",
            jobs_run=1,
            jobs_succeeded=1 if result.success else 0,
            jobs_failed=0 if result.success else 1,
            duration_seconds=(completed_at - started_at).total_seconds(),
        )

        return OrchestratorResult(
            started_at=started_at,
            completed_at=completed_at,
            jobs_run=1,
            jobs_succeeded=1 if result.success else 0,
            jobs_failed=0 if result.success else 1,
            results=[result],
        )

    # =========================================================================
    # Observability Helper Methods
    # =========================================================================

    def _record_job_run(self, result: JobResult) -> None:
        """Record a job run to the database.

        Fails silently to avoid disrupting job execution.

        Args:
            result: JobResult to persist.
        """
        try:
            self.job_tracker.record_job_run(result)
        except Exception as e:
            logger.warning(
                "job_run_tracking_failed",
                job=result.job_name,
                error=str(e),
            )

    def _run_quality_checks(self) -> None:
        """Run data quality checks after job execution.

        Fails silently to avoid disrupting orchestration.
        """
        try:
            self.quality_monitor.run_all_checks()
        except Exception as e:
            logger.warning(
                "quality_checks_failed",
                error=str(e),
            )
