"""Daily Price Ingestion Job.

Implements Feature 012 - Yahoo Finance price data ingestion.
Implements Feature 013 - Daily Price Ingestion (OHLCV).
"""

from datetime import date, datetime, timedelta
from typing import Any

from asx_jobs.database import Database
from asx_jobs.jobs.base import BaseJob, JobResult
from asx_jobs.logging import get_logger
from asx_jobs.providers.yahoo import YahooFinanceProvider

logger = get_logger(__name__)


class IngestPricesJob(BaseJob):
    """Ingest daily prices for all active instruments."""

    def __init__(
        self,
        db: Database,
        provider: YahooFinanceProvider | None = None,
        lookback_days: int = 30,
        batch_size: int = 10,
    ) -> None:
        """Initialize the job.

        Args:
            db: Database client.
            provider: Yahoo Finance provider.
            lookback_days: Days of history to fetch for new instruments.
            batch_size: Symbols per batch for bulk download.
        """
        self.db = db
        self.provider = provider or YahooFinanceProvider()
        self.lookback_days = lookback_days
        self.batch_size = batch_size

    @property
    def name(self) -> str:
        return "ingest_prices"

    def run(self) -> JobResult:
        """Execute price ingestion for all active instruments."""
        started_at = datetime.now()
        processed = 0
        failed = 0
        errors: list[str] = []

        instruments = self.db.get_all_active_instruments()
        logger.info(
            "job_started",
            job=self.name,
            instruments_count=len(instruments),
        )

        for i in range(0, len(instruments), self.batch_size):
            batch = instruments[i : i + self.batch_size]
            batch_result = self._process_batch(batch)
            processed += batch_result["processed"]
            failed += batch_result["failed"]
            errors.extend(batch_result["errors"])

        completed_at = datetime.now()

        logger.info(
            "job_completed",
            job=self.name,
            processed=processed,
            failed=failed,
            duration_seconds=(completed_at - started_at).total_seconds(),
        )

        return JobResult(
            job_name=self.name,
            success=failed < len(instruments),
            started_at=started_at,
            completed_at=completed_at,
            records_processed=processed,
            records_failed=failed,
            error_message="; ".join(errors[:10]) if errors else None,
            metadata={"instruments_count": len(instruments)},
        )

    def _process_batch(
        self, instruments: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Process a batch of instruments.

        Args:
            instruments: List of instrument records.

        Returns:
            Dictionary with processed, failed counts and errors.
        """
        processed = 0
        failed = 0
        errors: list[str] = []

        symbols = [inst["symbol"] for inst in instruments]
        symbol_to_id = {inst["symbol"]: inst["id"] for inst in instruments}

        end_date = date.today()
        start_date = end_date - timedelta(days=self.lookback_days)

        try:
            history = self.provider.get_bulk_history(
                symbols=symbols,
                start_date=start_date,
                end_date=end_date,
            )

            for symbol, bars in history.items():
                instrument_id = symbol_to_id.get(symbol)
                if not instrument_id:
                    continue

                if not bars:
                    failed += 1
                    errors.append(f"{symbol}: no price data")
                    continue

                prices = [
                    {
                        "instrument_id": instrument_id,
                        "trade_date": bar.trade_date.isoformat(),
                        "open": bar.open,
                        "high": bar.high,
                        "low": bar.low,
                        "close": bar.close,
                        "volume": bar.volume,
                        "adjusted_close": bar.adjusted_close,
                        "data_source": "yahoo",
                    }
                    for bar in bars
                ]

                self.db.bulk_upsert_prices(prices)
                processed += len(bars)

                logger.debug(
                    "prices_ingested",
                    symbol=symbol,
                    bars_count=len(bars),
                )

        except Exception as e:
            failed += len(symbols)
            error_msg = f"batch error: {str(e)}"
            errors.append(error_msg)
            logger.error("batch_failed", error=str(e), symbols=symbols)

        return {"processed": processed, "failed": failed, "errors": errors}


class BackfillPricesJob(BaseJob):
    """Backfill historical prices for instruments.

    Implements Feature 014 - Historical Backfill (Seed Window).
    """

    def __init__(
        self,
        db: Database,
        provider: YahooFinanceProvider | None = None,
        period: str = "2y",
    ) -> None:
        """Initialize the job.

        Args:
            db: Database client.
            provider: Yahoo Finance provider.
            period: History period (e.g., '1y', '2y', '5y', 'max').
        """
        self.db = db
        self.provider = provider or YahooFinanceProvider()
        self.period = period

    @property
    def name(self) -> str:
        return "backfill_prices"

    def run(self) -> JobResult:
        """Execute historical backfill for all active instruments."""
        started_at = datetime.now()
        processed = 0
        failed = 0
        errors: list[str] = []

        instruments = self.db.get_all_active_instruments()
        logger.info(
            "job_started",
            job=self.name,
            instruments_count=len(instruments),
            period=self.period,
        )

        for instrument in instruments:
            symbol = instrument["symbol"]
            instrument_id = instrument["id"]

            try:
                bars = self.provider.get_price_history(
                    symbol=symbol,
                    period=self.period,
                )

                if not bars:
                    failed += 1
                    errors.append(f"{symbol}: no historical data")
                    continue

                prices = [
                    {
                        "instrument_id": instrument_id,
                        "trade_date": bar.trade_date.isoformat(),
                        "open": bar.open,
                        "high": bar.high,
                        "low": bar.low,
                        "close": bar.close,
                        "volume": bar.volume,
                        "adjusted_close": bar.adjusted_close,
                        "data_source": "yahoo",
                    }
                    for bar in bars
                ]

                self.db.bulk_upsert_prices(prices)
                processed += len(bars)

                logger.info(
                    "backfill_completed",
                    symbol=symbol,
                    bars_count=len(bars),
                    start=bars[0].trade_date.isoformat(),
                    end=bars[-1].trade_date.isoformat(),
                )

            except Exception as e:
                failed += 1
                errors.append(f"{symbol}: {str(e)}")
                logger.warning("backfill_failed", symbol=symbol, error=str(e))

        completed_at = datetime.now()

        logger.info(
            "job_completed",
            job=self.name,
            processed=processed,
            failed=failed,
            duration_seconds=(completed_at - started_at).total_seconds(),
        )

        return JobResult(
            job_name=self.name,
            success=failed < len(instruments),
            started_at=started_at,
            completed_at=completed_at,
            records_processed=processed,
            records_failed=failed,
            error_message="; ".join(errors[:10]) if errors else None,
            metadata={
                "instruments_count": len(instruments),
                "period": self.period,
            },
        )
