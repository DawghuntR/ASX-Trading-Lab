"""Job run tracking and data quality monitoring.

This module provides observability capabilities for the ASX Jobs Runner:
- Persists job execution metadata to the database
- Monitors data quality and detects issues
- Enables visibility into system health
"""

from datetime import datetime
from typing import Any

from asx_jobs.database import Database
from asx_jobs.jobs.base import JobResult
from asx_jobs.logging import get_logger

logger = get_logger(__name__)


class JobRunTracker:
    """Tracks job execution metadata in the database."""

    def __init__(self, db: Database) -> None:
        """Initialize the job run tracker.

        Args:
            db: Database client for persistence.
        """
        self.db = db

    def record_job_run(self, result: JobResult) -> int:
        """Record a completed job run to the database.

        Args:
            result: JobResult from an executed job.

        Returns:
            The ID of the created job_runs record.
        """
        status = self._determine_status(result)
        run_date = result.started_at.strftime("%Y-%m-%d")

        data = {
            "job_name": result.job_name,
            "run_date": run_date,
            "started_at": result.started_at.isoformat(),
            "completed_at": result.completed_at.isoformat(),
            "status": status,
            "records_processed": result.records_processed,
            "records_failed": result.records_failed,
            "duration_seconds": round(result.duration_seconds, 2),
            "error_message": result.error_message,
            "metadata": result.metadata or {},
        }

        try:
            response = self.db.client.table("job_runs").insert(data).execute()
            run_id = int(response.data[0]["id"])
            logger.info(
                "job_run_recorded",
                job_name=result.job_name,
                run_id=run_id,
                status=status,
            )
            return run_id
        except Exception as e:
            logger.error(
                "job_run_record_failed",
                job_name=result.job_name,
                error=str(e),
            )
            raise

    def _determine_status(self, result: JobResult) -> str:
        """Determine the job status based on execution result.

        Args:
            result: JobResult to evaluate.

        Returns:
            Status string: 'success', 'partial_failure', or 'failure'.
        """
        if not result.success:
            return "failure"
        if result.records_failed > 0:
            return "partial_failure"
        return "success"

    def get_last_successful_run(self, job_name: str) -> dict[str, Any] | None:
        """Get the most recent successful run for a job.

        Args:
            job_name: Name of the job to query.

        Returns:
            Job run record or None if no successful runs found.
        """
        try:
            result = (
                self.db.client.table("job_runs")
                .select("*")
                .eq("job_name", job_name)
                .eq("status", "success")
                .order("run_date", desc=True)
                .order("started_at", desc=True)
                .limit(1)
                .execute()
            )
            if result.data:
                return dict(result.data[0])
            return None
        except Exception as e:
            logger.error(
                "get_last_successful_run_failed",
                job_name=job_name,
                error=str(e),
            )
            return None

    def get_recent_runs(
        self, job_name: str | None = None, days: int = 7, limit: int = 100
    ) -> list[dict[str, Any]]:
        """Get recent job runs.

        Args:
            job_name: Optional filter by job name.
            days: Number of days to look back.
            limit: Maximum number of records to return.

        Returns:
            List of job run records.
        """
        try:
            start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            start_date = start_date.replace(
                day=start_date.day - days if start_date.day > days else 1
            )

            query = (
                self.db.client.table("job_runs")
                .select("*")
                .gte("run_date", start_date.strftime("%Y-%m-%d"))
                .order("run_date", desc=True)
                .order("started_at", desc=True)
                .limit(limit)
            )

            if job_name:
                query = query.eq("job_name", job_name)

            result = query.execute()
            return [dict(r) for r in result.data]
        except Exception as e:
            logger.error("get_recent_runs_failed", error=str(e))
            return []


class DataQualityMonitor:
    """Monitors data quality and records issues."""

    def __init__(self, db: Database) -> None:
        """Initialize the data quality monitor.

        Args:
            db: Database client for queries and persistence.
        """
        self.db = db
        self.tracker = JobRunTracker(db)

    def record_issue(
        self,
        check_type: str,
        severity: str,
        affected_count: int,
        affected_symbols: list[str],
        description: str,
        details: dict[str, Any] | None = None,
    ) -> int:
        """Record a data quality issue.

        Args:
            check_type: Type of check (e.g., 'stale_data', 'missing_snapshot').
            severity: Issue severity ('info', 'warning', 'error').
            affected_count: Number of affected records.
            affected_symbols: List of affected ticker symbols.
            description: Human-readable description of the issue.
            details: Additional context as JSON.

        Returns:
            The ID of the created record.
        """
        data = {
            "check_date": datetime.now().strftime("%Y-%m-%d"),
            "check_type": check_type,
            "severity": severity,
            "affected_count": affected_count,
            "affected_symbols": affected_symbols,
            "description": description,
            "details": details or {},
        }

        try:
            response = self.db.client.table("data_quality_checks").insert(data).execute()
            issue_id = int(response.data[0]["id"])
            logger.info(
                "data_quality_issue_recorded",
                check_type=check_type,
                severity=severity,
                affected_count=affected_count,
                issue_id=issue_id,
            )
            return issue_id
        except Exception as e:
            logger.error(
                "data_quality_issue_record_failed",
                check_type=check_type,
                error=str(e),
            )
            raise

    def check_stale_data(self, days_threshold: int = 7) -> dict[str, Any]:
        """Check for symbols without recent price data.

        Args:
            days_threshold: Number of days without data to consider stale.

        Returns:
            Dictionary with check results including count and symbols.
        """
        try:
            result = (
                self.db.client.table("v_stale_data_check")
                .select("symbol, days_since_update, staleness_status")
                .or_("staleness_status.eq.stale,staleness_status.eq.never")
                .execute()
            )

            stale_symbols = [row["symbol"] for row in result.data]
            count = len(stale_symbols)

            if count > 0:
                self.record_issue(
                    check_type="stale_data",
                    severity="warning" if count < 50 else "error",
                    affected_count=count,
                    affected_symbols=stale_symbols[:100],
                    description=f"{count} symbols without price data for {days_threshold}+ days",
                    details={"days_threshold": days_threshold},
                )

            logger.info(
                "stale_data_check_completed",
                stale_count=count,
            )

            return {
                "check_type": "stale_data",
                "count": count,
                "symbols": stale_symbols,
            }
        except Exception as e:
            logger.error("stale_data_check_failed", error=str(e))
            return {"check_type": "stale_data", "count": 0, "symbols": [], "error": str(e)}

    def check_missing_today_snapshot(self) -> dict[str, Any]:
        """Check for active symbols missing today's price snapshot.

        Returns:
            Dictionary with check results.
        """
        try:
            today = datetime.now().strftime("%Y-%m-%d")

            active_instruments = self.db.get_all_active_instruments()
            active_ids = {inst["id"] for inst in active_instruments}
            symbol_map = {inst["id"]: inst["symbol"] for inst in active_instruments}

            prices_today = (
                self.db.client.table("daily_prices")
                .select("instrument_id")
                .eq("trade_date", today)
                .execute()
            )
            ids_with_prices = {row["instrument_id"] for row in prices_today.data}

            missing_ids = active_ids - ids_with_prices
            missing_symbols = [symbol_map[id_] for id_ in missing_ids if id_ in symbol_map]

            count = len(missing_symbols)

            if count > 0 and count < len(active_ids) * 0.9:
                self.record_issue(
                    check_type="missing_snapshot",
                    severity="warning",
                    affected_count=count,
                    affected_symbols=missing_symbols[:100],
                    description=f"{count} active symbols missing today's price snapshot",
                    details={"check_date": today},
                )

            logger.info(
                "missing_snapshot_check_completed",
                missing_count=count,
                total_active=len(active_ids),
            )

            return {
                "check_type": "missing_snapshot",
                "count": count,
                "symbols": missing_symbols,
            }
        except Exception as e:
            logger.error("missing_snapshot_check_failed", error=str(e))
            return {"check_type": "missing_snapshot", "count": 0, "symbols": [], "error": str(e)}

    def check_price_quality(self, days: int = 7) -> dict[str, Any]:
        """Check for abnormal or invalid price values.

        Args:
            days: Number of days to check.

        Returns:
            Dictionary with check results.
        """
        try:
            result = (
                self.db.client.table("v_price_quality_issues")
                .select("symbol, issue_type, trade_date")
                .execute()
            )

            issues = result.data
            count = len(issues)
            affected_symbols = list(set(row["symbol"] for row in issues))

            if count > 0:
                issue_types: dict[str, int] = {}
                for issue in issues:
                    issue_type = issue["issue_type"]
                    issue_types[issue_type] = issue_types.get(issue_type, 0) + 1

                self.record_issue(
                    check_type="abnormal_prices",
                    severity="error" if count > 10 else "warning",
                    affected_count=count,
                    affected_symbols=affected_symbols[:100],
                    description=f"{count} price records with data quality issues",
                    details={"issue_breakdown": issue_types},
                )

            logger.info(
                "price_quality_check_completed",
                issues_found=count,
            )

            return {
                "check_type": "abnormal_prices",
                "count": count,
                "symbols": affected_symbols,
            }
        except Exception as e:
            logger.error("price_quality_check_failed", error=str(e))
            return {"check_type": "abnormal_prices", "count": 0, "symbols": [], "error": str(e)}

    def run_all_checks(self) -> dict[str, Any]:
        """Run all data quality checks.

        Returns:
            Dictionary with all check results.
        """
        logger.info("data_quality_checks_started")

        results: dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
        }

        results["checks"]["stale_data"] = self.check_stale_data()
        results["checks"]["missing_snapshot"] = self.check_missing_today_snapshot()
        results["checks"]["price_quality"] = self.check_price_quality()

        checks: dict[str, dict[str, Any]] = results["checks"]
        total_issues = sum(check.get("count", 0) for check in checks.values())
        results["total_issues"] = total_issues

        logger.info(
            "data_quality_checks_completed",
            total_issues=total_issues,
        )

        return results

    def get_unresolved_issues(self, limit: int = 100) -> list[dict[str, Any]]:
        """Get all unresolved data quality issues.

        Args:
            limit: Maximum number of issues to return.

        Returns:
            List of unresolved issue records.
        """
        try:
            result = (
                self.db.client.table("data_quality_checks")
                .select("*")
                .is_("resolved_at", "null")
                .order("check_date", desc=True)
                .limit(limit)
                .execute()
            )
            return [dict(r) for r in result.data]
        except Exception as e:
            logger.error("get_unresolved_issues_failed", error=str(e))
            return []

    def resolve_issue(self, issue_id: int) -> bool:
        """Mark a data quality issue as resolved.

        Args:
            issue_id: ID of the issue to resolve.

        Returns:
            True if successful, False otherwise.
        """
        try:
            self.db.client.table("data_quality_checks").update(
                {"resolved_at": datetime.now().isoformat()}
            ).eq("id", issue_id).execute()
            logger.info("data_quality_issue_resolved", issue_id=issue_id)
            return True
        except Exception as e:
            logger.error(
                "data_quality_issue_resolve_failed",
                issue_id=issue_id,
                error=str(e),
            )
            return False
