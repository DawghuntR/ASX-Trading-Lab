"""Command-line interface for ASX Jobs Runner."""

import argparse
import sys

from asx_jobs.config import load_config
from asx_jobs.logging import get_logger, setup_logging
from asx_jobs.orchestrator import JobOrchestrator


def main() -> int:
    """Main entry point for the CLI.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    parser = argparse.ArgumentParser(
        description="ASX Trading Lab Jobs Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  asx-jobs daily              Run daily ingestion + signal generation
  asx-jobs backfill --period 2y   Backfill 2 years of historical data
  asx-jobs symbols            Ingest symbols only (with metadata)
  asx-jobs symbols --no-metadata  Ingest symbols without metadata
  asx-jobs signals            Generate signals only (requires existing price data)
  asx-jobs announcements      Ingest ASX announcements only
        """,
    )

    parser.add_argument(
        "command",
        choices=["daily", "backfill", "symbols", "signals", "announcements"],
        help="Command to run",
    )

    parser.add_argument(
        "--period",
        default="2y",
        help="Backfill period (e.g., 1y, 2y, 5y, max). Default: 2y",
    )

    parser.add_argument(
        "--no-metadata",
        action="store_true",
        help="Skip fetching metadata for symbols",
    )

    parser.add_argument(
        "--env-file",
        help="Path to .env file",
    )

    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level. Default: INFO",
    )

    args = parser.parse_args()

    setup_logging(args.log_level)
    logger = get_logger("cli")

    try:
        config = load_config(args.env_file)
        config.validate()
    except ValueError as e:
        logger.error("configuration_error", error=str(e))
        print(f"Configuration error: {e}", file=sys.stderr)
        return 1

    orchestrator = JobOrchestrator(config)

    try:
        if args.command == "daily":
            result = orchestrator.run_daily()
        elif args.command == "backfill":
            result = orchestrator.run_backfill(period=args.period)
        elif args.command == "symbols":
            result = orchestrator.run_symbols_only(fetch_metadata=not args.no_metadata)
        elif args.command == "signals":
            result = orchestrator.run_signals()
        elif args.command == "announcements":
            result = orchestrator.run_announcements()
        else:
            logger.error("unknown_command", command=args.command)
            return 1

        for job_result in result.results:
            status = "SUCCESS" if job_result.success else "FAILED"
            print(
                f"[{status}] {job_result.job_name}: "
                f"{job_result.records_processed} processed, "
                f"{job_result.records_failed} failed "
                f"({job_result.duration_seconds:.1f}s)"
            )
            if job_result.error_message:
                print(f"  Errors: {job_result.error_message}")

        print(f"\nTotal: {result.jobs_succeeded}/{result.jobs_run} jobs succeeded")
        print(f"Duration: {result.duration_seconds:.1f}s")

        return 0 if result.success else 1

    except KeyboardInterrupt:
        logger.warning("interrupted")
        print("\nInterrupted by user", file=sys.stderr)
        return 130

    except Exception as e:
        logger.error("fatal_error", error=str(e), exc_info=True)
        print(f"Fatal error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
