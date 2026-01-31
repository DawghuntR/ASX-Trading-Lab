"""Base provider interface for price data sources."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class PriceBar:
    """Single day price bar - common data structure for all providers."""

    trade_date: date
    open: float | None
    high: float | None
    low: float | None
    close: float
    volume: int
    adjusted_close: float | None = None


class BasePriceProvider(ABC):
    """Abstract base class for price data providers.
    
    All price providers must implement this interface to ensure
    consistent behavior across Yahoo Finance, web scraping, and
    any future data sources.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the provider name for logging and data_source tracking."""
        pass

    @abstractmethod
    def get_price_history(
        self,
        symbol: str,
        start_date: date | None = None,
        end_date: date | None = None,
        period: str | None = None,
    ) -> list[PriceBar]:
        """Fetch historical daily price bars for a single symbol.

        Args:
            symbol: ASX ticker symbol (canonical format, e.g., 'BHP').
            start_date: Start date (inclusive).
            end_date: End date (inclusive).
            period: Alternative to dates (e.g., '1mo', '3mo', '1y').

        Returns:
            List of PriceBar objects, sorted by date ascending.
        """
        pass

    @abstractmethod
    def get_bulk_history(
        self,
        symbols: list[str],
        start_date: date | None = None,
        end_date: date | None = None,
        period: str | None = None,
    ) -> dict[str, list[PriceBar]]:
        """Fetch historical prices for multiple symbols.

        Args:
            symbols: List of ASX ticker symbols.
            start_date: Start date (inclusive).
            end_date: End date (inclusive).
            period: Alternative to dates.

        Returns:
            Dictionary mapping symbol to list of PriceBar objects.
        """
        pass

    def get_instrument_info(self, symbol: str) -> dict[str, Any] | None:
        """Fetch instrument metadata (optional).

        Args:
            symbol: ASX ticker symbol.

        Returns:
            Dictionary with instrument info or None if not supported.
        """
        return None
