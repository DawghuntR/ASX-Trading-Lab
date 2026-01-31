"""ASX Announcements Ingestion Job.

Implements Feature 021 - ASX Announcements Ingestion.
Fetches announcements from the ASX API and stores them in Supabase.
"""

import hashlib
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import requests

from asx_jobs.database import Database
from asx_jobs.jobs.base import BaseJob, JobResult
from asx_jobs.logging import get_logger

logger = get_logger(__name__)

ASX_API_BASE_URL = "https://asx.api.markitdigital.com/asx-research/1.0/companies"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


@dataclass
class AnnouncementRecord:
    """Parsed announcement record."""

    symbol: str
    announced_at: datetime
    headline: str
    url: str | None
    document_type: str | None
    sensitivity: str
    pages: int | None
    asx_announcement_id: str | None


@dataclass
class IngestAnnouncementsConfig:
    """Configuration for announcements ingestion."""

    request_delay: float = 0.5
    timeout: int = 30
    symbols_filter: list[str] | None = None
    batch_size: int = 50


class IngestAnnouncementsJob(BaseJob):
    """Ingest ASX announcements from the ASX API."""

    def __init__(
        self,
        db: Database,
        config: IngestAnnouncementsConfig | None = None,
    ) -> None:
        """Initialize the announcements ingestion job.

        Args:
            db: Database client.
            config: Ingestion configuration.
        """
        self.db = db
        self.config = config or IngestAnnouncementsConfig()
        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        })

    @property
    def name(self) -> str:
        return "ingest_announcements"

    def run(self) -> JobResult:
        """Execute announcements ingestion."""
        started_at = datetime.now()
        announcements_processed = 0
        announcements_new = 0
        symbols_processed = 0
        symbols_failed = 0
        errors: list[str] = []

        logger.info(
            "announcements_job_started",
            job=self.name,
        )

        try:
            instruments = self._get_instruments_to_fetch()
            total_instruments = len(instruments)
            
            logger.info(
                "fetching_announcements_for_instruments",
                total=total_instruments,
            )

            for i, instrument in enumerate(instruments):
                symbol = instrument["symbol"]
                
                try:
                    announcements = self._fetch_announcements_for_symbol(symbol)
                    symbols_processed += 1
                    
                    for ann in announcements:
                        try:
                            is_new = self._process_announcement(ann, instrument)
                            announcements_processed += 1
                            if is_new:
                                announcements_new += 1
                        except Exception as e:
                            errors.append(f"{symbol}: {str(e)}")
                            logger.warning(
                                "announcement_processing_failed",
                                symbol=symbol,
                                headline=ann.headline[:50] if ann.headline else "N/A",
                                error=str(e),
                            )
                    
                    if (i + 1) % 10 == 0:
                        logger.info(
                            "progress",
                            symbols_done=i + 1,
                            total=total_instruments,
                            new_announcements=announcements_new,
                        )
                    
                    if i < total_instruments - 1:
                        time.sleep(self.config.request_delay)
                        
                except Exception as e:
                    symbols_failed += 1
                    errors.append(f"{symbol}: fetch failed - {str(e)}")
                    logger.warning(
                        "symbol_fetch_failed",
                        symbol=symbol,
                        error=str(e),
                    )

        except Exception as e:
            logger.error("announcements_job_failed", error=str(e))
            errors.append(f"Job failed: {str(e)}")

        completed_at = datetime.now()

        logger.info(
            "announcements_job_completed",
            job=self.name,
            symbols_processed=symbols_processed,
            symbols_failed=symbols_failed,
            announcements_processed=announcements_processed,
            new=announcements_new,
            duration_seconds=(completed_at - started_at).total_seconds(),
        )

        return JobResult(
            job_name=self.name,
            success=symbols_failed < symbols_processed,
            started_at=started_at,
            completed_at=completed_at,
            records_processed=announcements_new,
            records_failed=symbols_failed,
            error_message="; ".join(errors[:10]) if errors else None,
            metadata={
                "symbols_processed": symbols_processed,
                "symbols_failed": symbols_failed,
                "total_announcements_fetched": announcements_processed,
                "new_announcements": announcements_new,
            },
        )

    def _get_instruments_to_fetch(self) -> list[dict[str, Any]]:
        """Get list of instruments to fetch announcements for.
        
        Returns:
            List of instrument dictionaries with id and symbol.
        """
        if self.config.symbols_filter:
            instruments = []
            for symbol in self.config.symbols_filter:
                inst = self.db.get_instrument_by_symbol(symbol)
                if inst:
                    instruments.append(inst)
            return instruments
        
        response = self.db.client.table("instruments").select("id, symbol").eq("is_active", True).execute()
        return response.data or []

    def _fetch_announcements_for_symbol(self, symbol: str) -> list[AnnouncementRecord]:
        """Fetch announcements for a single symbol from the ASX API.

        Args:
            symbol: ASX stock symbol.

        Returns:
            List of announcement records.
        """
        url = f"{ASX_API_BASE_URL}/{symbol}/announcements"
        
        response = self._session.get(url, timeout=self.config.timeout)
        
        if response.status_code == 404:
            logger.debug("symbol_not_found_in_api", symbol=symbol)
            return []
            
        response.raise_for_status()
        
        data = response.json()
        items = data.get("data", {}).get("items", [])
        
        announcements = []
        for item in items:
            ann = self._parse_api_item(symbol, item)
            if ann:
                announcements.append(ann)
        
        return announcements

    def _parse_api_item(self, symbol: str, item: dict[str, Any]) -> AnnouncementRecord | None:
        """Parse an API response item into an AnnouncementRecord.

        Args:
            symbol: ASX stock symbol.
            item: API response item dictionary.

        Returns:
            AnnouncementRecord or None if parsing fails.
        """
        try:
            date_str = item.get("date", "")
            if not date_str:
                return None
            
            announced_at = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            
            headline = item.get("headline", "")
            if not headline:
                return None
            
            document_key = item.get("documentKey", "")
            url = None
            if document_key:
                url = f"https://www.asx.com.au/asxpdf/{document_key}.pdf"
            
            is_price_sensitive = item.get("isPriceSensitive", False)
            sensitivity = "price_sensitive" if is_price_sensitive else "not_price_sensitive"
            
            document_type = item.get("announcementType")
            
            file_size = item.get("fileSize", "")
            pages = self._estimate_pages_from_size(file_size)
            
            return AnnouncementRecord(
                symbol=symbol,
                announced_at=announced_at,
                headline=headline,
                url=url,
                document_type=document_type,
                sensitivity=sensitivity,
                pages=pages,
                asx_announcement_id=document_key,
            )
            
        except Exception as e:
            logger.debug("item_parse_failed", symbol=symbol, error=str(e))
            return None

    def _estimate_pages_from_size(self, file_size: str) -> int | None:
        """Estimate page count from file size string.
        
        Args:
            file_size: Size string like "161KB" or "2MB".
            
        Returns:
            Estimated page count or None.
        """
        if not file_size:
            return None
            
        try:
            size_str = file_size.upper().strip()
            if "KB" in size_str:
                kb = int(size_str.replace("KB", "").strip())
                return max(1, kb // 50)
            elif "MB" in size_str:
                mb = float(size_str.replace("MB", "").strip())
                return max(1, int(mb * 20))
        except (ValueError, TypeError):
            pass
        
        return None

    def _process_announcement(self, ann: AnnouncementRecord, instrument: dict[str, Any]) -> bool:
        """Process and store a single announcement.

        Args:
            ann: Announcement record to process.
            instrument: Instrument dictionary with id.

        Returns:
            True if this is a new announcement, False if duplicate.
        """
        content_hash = hashlib.md5(
            f"{ann.symbol}:{ann.announced_at.isoformat()}:{ann.headline}".encode()
        ).hexdigest()

        is_new = self.db.upsert_announcement(
            instrument_id=instrument["id"],
            announced_at=ann.announced_at.isoformat(),
            headline=ann.headline,
            url=ann.url,
            document_type=ann.document_type,
            sensitivity=ann.sensitivity,
            pages=ann.pages,
            asx_announcement_id=ann.asx_announcement_id,
            content_hash=content_hash,
        )

        return is_new
