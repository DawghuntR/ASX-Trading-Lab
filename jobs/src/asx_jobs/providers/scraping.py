"""ASX Web Scraping Fallback Provider.

Implements Feature 031 - Price Data Fallback Provider (Python Web Scraping).

This provider scrapes price data from public websites when the primary
Yahoo Finance provider is unavailable or unreliable. It targets free,
publicly accessible price data sources.

IMPORTANT: This is a fallback mechanism. Web scraping is inherently brittle
and may break if the target website changes its structure. Use the Yahoo
Finance provider as the primary source whenever possible.
"""

import re
import time
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any

import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential

from asx_jobs.logging import get_logger
from asx_jobs.providers.base import BasePriceProvider, PriceBar

logger = get_logger(__name__)


@dataclass
class ScrapingConfig:
    """Configuration for web scraping provider."""

    rate_limit_delay: float = 1.0
    timeout: int = 30
    max_retries: int = 3
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )


class ASXScrapingProvider(BasePriceProvider):
    """Web scraping fallback provider for ASX price data.
    
    Scrapes price data from publicly accessible sources. This provider
    is designed as a fallback when Yahoo Finance is unavailable.
    
    Current scraping targets:
    - MarketIndex.com.au - Australian stock market data
    - ASX.com.au - Official ASX website (limited)
    
    Note: Web scraping is subject to website changes and rate limits.
    Always be respectful of the target website's terms of service.
    """

    def __init__(self, config: ScrapingConfig | None = None) -> None:
        """Initialize the scraping provider.

        Args:
            config: Scraping configuration.
        """
        self.config = config or ScrapingConfig()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.config.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-AU,en;q=0.9",
        })
        logger.info(
            "scraping_provider_initialized",
            rate_limit_delay=self.config.rate_limit_delay,
        )

    @property
    def name(self) -> str:
        return "asx_scraping"

    def _rate_limit(self) -> None:
        """Apply rate limiting delay between requests."""
        if self.config.rate_limit_delay > 0:
            time.sleep(self.config.rate_limit_delay)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def _fetch_page(self, url: str) -> BeautifulSoup | None:
        """Fetch and parse a web page.

        Args:
            url: URL to fetch.

        Returns:
            BeautifulSoup object or None if fetch failed.
        """
        try:
            self._rate_limit()
            response = self.session.get(url, timeout=self.config.timeout)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            logger.warning("fetch_failed", url=url, error=str(e))
            return None

    def _parse_price(self, text: str) -> float | None:
        """Parse a price string to float.

        Args:
            text: Price text (e.g., '$45.23', '45.23', '1,234.56').

        Returns:
            Float value or None if parsing failed.
        """
        if not text:
            return None
        cleaned = re.sub(r"[,$]", "", text.strip())
        try:
            return float(cleaned)
        except ValueError:
            return None

    def _parse_volume(self, text: str) -> int:
        """Parse a volume string to integer.

        Args:
            text: Volume text (e.g., '1,234,567', '1.2M', '500K').

        Returns:
            Integer value or 0 if parsing failed.
        """
        if not text:
            return 0
        cleaned = text.strip().upper().replace(",", "")
        try:
            if "M" in cleaned:
                return int(float(cleaned.replace("M", "")) * 1_000_000)
            elif "K" in cleaned:
                return int(float(cleaned.replace("K", "")) * 1_000)
            elif "B" in cleaned:
                return int(float(cleaned.replace("B", "")) * 1_000_000_000)
            return int(float(cleaned))
        except ValueError:
            return 0

    def _scrape_marketindex_quote(self, symbol: str) -> PriceBar | None:
        """Scrape current quote from MarketIndex.com.au.

        Args:
            symbol: ASX ticker symbol.

        Returns:
            PriceBar with today's data or None if scraping failed.
        """
        url = f"https://www.marketindex.com.au/asx/{symbol.lower()}"
        soup = self._fetch_page(url)
        
        if not soup:
            return None

        try:
            price_elem = soup.select_one(".quote-price, .price, [data-price]")
            if not price_elem:
                logger.debug("no_price_element", symbol=symbol, url=url)
                return None

            close_price = self._parse_price(price_elem.get_text())
            if close_price is None:
                return None

            volume = 0
            volume_elem = soup.select_one(".volume, [data-volume]")
            if volume_elem:
                volume = self._parse_volume(volume_elem.get_text())

            open_price = None
            open_elem = soup.select_one(".open, [data-open]")
            if open_elem:
                open_price = self._parse_price(open_elem.get_text())

            high_price = None
            high_elem = soup.select_one(".high, [data-high]")
            if high_elem:
                high_price = self._parse_price(high_elem.get_text())

            low_price = None
            low_elem = soup.select_one(".low, [data-low]")
            if low_elem:
                low_price = self._parse_price(low_elem.get_text())

            return PriceBar(
                trade_date=date.today(),
                open=open_price,
                high=high_price,
                low=low_price,
                close=close_price,
                volume=volume,
                adjusted_close=close_price,
            )

        except Exception as e:
            logger.warning("scrape_parse_error", symbol=symbol, error=str(e))
            return None

    def _scrape_asx_quote(self, symbol: str) -> PriceBar | None:
        """Scrape current quote from ASX.com.au (backup source).

        Args:
            symbol: ASX ticker symbol.

        Returns:
            PriceBar with today's data or None if scraping failed.
        """
        url = f"https://www2.asx.com.au/markets/company/{symbol.upper()}"
        soup = self._fetch_page(url)
        
        if not soup:
            return None

        try:
            price_elem = soup.select_one("[data-testid='last-price'], .last-price")
            if not price_elem:
                return None

            close_price = self._parse_price(price_elem.get_text())
            if close_price is None:
                return None

            return PriceBar(
                trade_date=date.today(),
                open=None,
                high=None,
                low=None,
                close=close_price,
                volume=0,
                adjusted_close=close_price,
            )

        except Exception as e:
            logger.warning("asx_scrape_error", symbol=symbol, error=str(e))
            return None

    def get_price_history(
        self,
        symbol: str,
        start_date: date | None = None,
        end_date: date | None = None,
        period: str | None = None,
    ) -> list[PriceBar]:
        """Fetch price data via web scraping.

        Note: Web scraping typically only provides current/recent quotes,
        not historical data. This method returns today's price only.

        Args:
            symbol: ASX ticker symbol.
            start_date: Ignored (scraping provides current data only).
            end_date: Ignored (scraping provides current data only).
            period: Ignored (scraping provides current data only).

        Returns:
            List containing today's PriceBar, or empty list if failed.
        """
        bar = self._scrape_marketindex_quote(symbol)
        
        if bar is None:
            bar = self._scrape_asx_quote(symbol)

        if bar is None:
            logger.warning("scraping_failed", symbol=symbol)
            return []

        logger.debug(
            "price_scraped",
            symbol=symbol,
            close=bar.close,
            volume=bar.volume,
        )

        return [bar]

    def get_bulk_history(
        self,
        symbols: list[str],
        start_date: date | None = None,
        end_date: date | None = None,
        period: str | None = None,
    ) -> dict[str, list[PriceBar]]:
        """Fetch prices for multiple symbols via web scraping.

        Note: This method processes symbols sequentially with rate limiting.
        It's slower than the Yahoo Finance bulk download but serves as a
        reliable fallback.

        Args:
            symbols: List of ASX ticker symbols.
            start_date: Ignored (scraping provides current data only).
            end_date: Ignored (scraping provides current data only).
            period: Ignored (scraping provides current data only).

        Returns:
            Dictionary mapping symbol to list of PriceBar objects.
        """
        results: dict[str, list[PriceBar]] = {}

        for symbol in symbols:
            try:
                bars = self.get_price_history(symbol)
                results[symbol] = bars
            except Exception as e:
                logger.warning("bulk_symbol_error", symbol=symbol, error=str(e))
                results[symbol] = []

        successful = sum(1 for bars in results.values() if bars)
        logger.info(
            "bulk_scraping_completed",
            total=len(symbols),
            successful=successful,
            failed=len(symbols) - successful,
        )

        return results

    def get_instrument_info(self, symbol: str) -> dict[str, Any] | None:
        """Fetch basic instrument info via scraping.

        Args:
            symbol: ASX ticker symbol.

        Returns:
            Dictionary with basic info or None if unavailable.
        """
        url = f"https://www.marketindex.com.au/asx/{symbol.lower()}"
        soup = self._fetch_page(url)

        if not soup:
            return None

        try:
            name_elem = soup.select_one("h1, .company-name, [data-company-name]")
            name = name_elem.get_text().strip() if name_elem else None

            sector_elem = soup.select_one(".sector, [data-sector]")
            sector = sector_elem.get_text().strip() if sector_elem else None

            return {
                "symbol": symbol.upper(),
                "name": name,
                "sector": sector,
                "industry": None,
                "market_cap": None,
                "currency": "AUD",
                "exchange": "ASX",
            }

        except Exception as e:
            logger.warning("info_scrape_error", symbol=symbol, error=str(e))
            return None
