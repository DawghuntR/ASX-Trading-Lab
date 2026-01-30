"""ASX Announcements Ingestion Job.

Implements Feature 021 - ASX Announcements Ingestion (HTML Scraper).
Scrapes ASX announcements pages and stores them in Supabase.
"""

import hashlib
import re
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from asx_jobs.database import Database
from asx_jobs.jobs.base import BaseJob, JobResult
from asx_jobs.logging import get_logger

logger = get_logger(__name__)

ASX_ANNOUNCEMENTS_URL = "https://www.asx.com.au/asx/v2/statistics/announcements.do"
ASX_BASE_URL = "https://www.asx.com.au"

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

    max_pages: int = 5
    request_delay: float = 1.0
    timeout: int = 30
    symbols_filter: list[str] | None = None


class IngestAnnouncementsJob(BaseJob):
    """Ingest ASX announcements from the ASX website."""

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
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        })

    @property
    def name(self) -> str:
        return "ingest_announcements"

    def run(self) -> JobResult:
        """Execute announcements ingestion."""
        started_at = datetime.now()
        announcements_processed = 0
        announcements_new = 0
        failed = 0
        errors: list[str] = []

        logger.info(
            "announcements_job_started",
            job=self.name,
            max_pages=self.config.max_pages,
        )

        try:
            all_announcements = self._fetch_announcements()
            logger.info(
                "announcements_fetched",
                total=len(all_announcements),
            )

            for ann in all_announcements:
                try:
                    is_new = self._process_announcement(ann)
                    announcements_processed += 1
                    if is_new:
                        announcements_new += 1
                except Exception as e:
                    failed += 1
                    errors.append(f"{ann.symbol}: {str(e)}")
                    logger.warning(
                        "announcement_processing_failed",
                        symbol=ann.symbol,
                        headline=ann.headline[:50],
                        error=str(e),
                    )

        except Exception as e:
            logger.error("announcements_fetch_failed", error=str(e))
            errors.append(f"Fetch failed: {str(e)}")

        completed_at = datetime.now()

        logger.info(
            "announcements_job_completed",
            job=self.name,
            processed=announcements_processed,
            new=announcements_new,
            failed=failed,
            duration_seconds=(completed_at - started_at).total_seconds(),
        )

        return JobResult(
            job_name=self.name,
            success=failed == 0 or announcements_new > 0,
            started_at=started_at,
            completed_at=completed_at,
            records_processed=announcements_new,
            records_failed=failed,
            error_message="; ".join(errors[:10]) if errors else None,
            metadata={
                "total_fetched": announcements_processed,
                "new_announcements": announcements_new,
            },
        )

    def _fetch_announcements(self) -> list[AnnouncementRecord]:
        """Fetch announcements from ASX website.

        Returns:
            List of parsed announcement records.
        """
        all_announcements: list[AnnouncementRecord] = []

        for page in range(1, self.config.max_pages + 1):
            logger.debug("fetching_page", page=page)

            try:
                announcements = self._fetch_page(page)
                all_announcements.extend(announcements)

                if len(announcements) == 0:
                    break

                if page < self.config.max_pages:
                    time.sleep(self.config.request_delay)

            except Exception as e:
                logger.warning("page_fetch_failed", page=page, error=str(e))
                break

        return all_announcements

    def _fetch_page(self, page: int) -> list[AnnouncementRecord]:
        """Fetch a single page of announcements.

        Args:
            page: Page number (1-indexed).

        Returns:
            List of announcement records from this page.
        """
        params = {
            "page": page,
            "by": "asxCode",
            "asxCode": "",
            "timeframe": "D",
            "dateReleased": "",
        }

        response = self._session.get(
            ASX_ANNOUNCEMENTS_URL,
            params=params,
            timeout=self.config.timeout,
        )
        response.raise_for_status()

        return self._parse_announcements_page(response.text)

    def _parse_announcements_page(self, html: str) -> list[AnnouncementRecord]:
        """Parse announcements from HTML page.

        Args:
            html: Raw HTML content.

        Returns:
            List of parsed announcement records.
        """
        soup = BeautifulSoup(html, "html.parser")
        announcements: list[AnnouncementRecord] = []

        table = soup.find("table", {"class": "announcements"})
        if not table:
            table = soup.find("table")

        if not table:
            return announcements

        rows = table.find_all("tr")

        for row in rows[1:]:
            try:
                ann = self._parse_row(row)
                if ann:
                    if self.config.symbols_filter is None or ann.symbol in self.config.symbols_filter:
                        announcements.append(ann)
            except Exception as e:
                logger.debug("row_parse_failed", error=str(e))
                continue

        return announcements

    def _parse_row(self, row: Any) -> AnnouncementRecord | None:
        """Parse a single table row into an announcement record.

        Args:
            row: BeautifulSoup row element.

        Returns:
            AnnouncementRecord or None if parsing fails.
        """
        cells = row.find_all("td")
        if len(cells) < 4:
            return None

        symbol_cell = cells[0]
        symbol_link = symbol_cell.find("a")
        symbol = symbol_link.text.strip() if symbol_link else symbol_cell.text.strip()
        symbol = symbol.upper()

        if not symbol or len(symbol) > 5:
            return None

        date_cell = cells[1] if len(cells) > 1 else None
        time_cell = cells[2] if len(cells) > 2 else None
        headline_cell = cells[3] if len(cells) > 3 else None
        pages_cell = cells[4] if len(cells) > 4 else None

        date_str = date_cell.text.strip() if date_cell else ""
        time_str = time_cell.text.strip() if time_cell else "00:00"

        try:
            announced_at = self._parse_datetime(date_str, time_str)
        except ValueError:
            return None

        headline = ""
        url = None
        if headline_cell:
            headline_link = headline_cell.find("a")
            if headline_link:
                headline = headline_link.text.strip()
                href = headline_link.get("href", "")
                if href:
                    url = urljoin(ASX_BASE_URL, href)
            else:
                headline = headline_cell.text.strip()

        if not headline:
            return None

        pages = None
        if pages_cell:
            pages_text = pages_cell.text.strip()
            pages_match = re.search(r"(\d+)", pages_text)
            if pages_match:
                pages = int(pages_match.group(1))

        sensitivity = self._detect_sensitivity(headline, row)

        asx_id = None
        if url:
            id_match = re.search(r"id=(\d+)", url)
            if id_match:
                asx_id = id_match.group(1)

        document_type = self._detect_document_type(headline)

        return AnnouncementRecord(
            symbol=symbol,
            announced_at=announced_at,
            headline=headline,
            url=url,
            document_type=document_type,
            sensitivity=sensitivity,
            pages=pages,
            asx_announcement_id=asx_id,
        )

    def _parse_datetime(self, date_str: str, time_str: str) -> datetime:
        """Parse date and time strings into datetime.

        Args:
            date_str: Date string (e.g., "30/01/2026").
            time_str: Time string (e.g., "10:30").

        Returns:
            Parsed datetime.

        Raises:
            ValueError: If parsing fails.
        """
        date_str = date_str.strip()
        time_str = time_str.strip() or "00:00"

        for date_fmt in ["%d/%m/%Y", "%d/%m/%y", "%Y-%m-%d"]:
            for time_fmt in ["%H:%M:%S", "%H:%M", "%I:%M%p", "%I:%M %p"]:
                try:
                    return datetime.strptime(f"{date_str} {time_str}", f"{date_fmt} {time_fmt}")
                except ValueError:
                    continue

        for date_fmt in ["%d/%m/%Y", "%d/%m/%y", "%Y-%m-%d"]:
            try:
                return datetime.strptime(date_str, date_fmt)
            except ValueError:
                continue

        raise ValueError(f"Cannot parse date: {date_str} {time_str}")

    def _detect_sensitivity(self, headline: str, row: Any) -> str:
        """Detect price sensitivity from headline or row styling.

        Args:
            headline: Announcement headline.
            row: BeautifulSoup row element.

        Returns:
            Sensitivity level: "price_sensitive", "not_price_sensitive", or "unknown".
        """
        row_class = row.get("class", [])
        if isinstance(row_class, list):
            row_class_str = " ".join(row_class)
        else:
            row_class_str = str(row_class)

        if "price-sensitive" in row_class_str.lower() or "pricesensitive" in row_class_str.lower():
            return "price_sensitive"

        sensitive_keywords = [
            "trading halt", "takeover", "acquisition", "merger",
            "earnings", "profit", "dividend", "capital raising",
            "placement", "material", "significant", "downgrade",
            "upgrade", "guidance", "restructure", "administration",
        ]
        headline_lower = headline.lower()
        for keyword in sensitive_keywords:
            if keyword in headline_lower:
                return "price_sensitive"

        return "unknown"

    def _detect_document_type(self, headline: str) -> str | None:
        """Detect document type from headline.

        Args:
            headline: Announcement headline.

        Returns:
            Document type or None.
        """
        headline_lower = headline.lower()

        type_patterns = {
            "Annual Report": ["annual report", "annual financial"],
            "Half Year Report": ["half year", "half-year", "interim"],
            "Quarterly Report": ["quarterly", "quarterly report", "appendix 4c", "appendix 5b"],
            "Trading Halt": ["trading halt"],
            "Dividend": ["dividend"],
            "ASX Query": ["asx query", "aware letter"],
            "Takeover": ["takeover", "acquisition", "merger"],
            "Capital Raising": ["capital raising", "placement", "share purchase plan", "rights issue"],
            "Director": ["director", "appendix 3x", "appendix 3y", "appendix 3z"],
            "Change of Address": ["change of address", "change of name"],
            "Constitution": ["constitution"],
            "Cleansing Notice": ["cleansing notice"],
        }

        for doc_type, patterns in type_patterns.items():
            for pattern in patterns:
                if pattern in headline_lower:
                    return doc_type

        return None

    def _process_announcement(self, ann: AnnouncementRecord) -> bool:
        """Process and store a single announcement.

        Args:
            ann: Announcement record to process.

        Returns:
            True if this is a new announcement, False if duplicate.
        """
        instrument = self.db.get_instrument_by_symbol(ann.symbol)
        if not instrument:
            logger.debug("instrument_not_found", symbol=ann.symbol)
            return False

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
