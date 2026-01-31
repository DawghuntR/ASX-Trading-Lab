"""Data providers for ASX Jobs Runner.

This module provides price data providers for the jobs runner.
The primary provider is Yahoo Finance, with web scraping as a fallback.

Usage:
    from asx_jobs.providers import get_provider, YahooFinanceProvider

    # Get default provider (Yahoo Finance)
    provider = get_provider()

    # Get specific provider
    yahoo = get_provider("yahoo")
    scraper = get_provider("scraping")

    # Direct instantiation
    provider = YahooFinanceProvider()
"""

from asx_jobs.config import YahooConfig
from asx_jobs.providers.base import BasePriceProvider, PriceBar
from asx_jobs.providers.scraping import ASXScrapingProvider, ScrapingConfig
from asx_jobs.providers.yahoo import YahooFinanceProvider

__all__ = [
    "BasePriceProvider",
    "PriceBar",
    "YahooFinanceProvider",
    "ASXScrapingProvider",
    "ScrapingConfig",
    "get_provider",
]


def get_provider(
    provider_name: str = "yahoo",
    yahoo_config: YahooConfig | None = None,
    scraping_config: ScrapingConfig | None = None,
) -> BasePriceProvider:
    """Factory function to get a price data provider.

    Args:
        provider_name: Provider to use ('yahoo' or 'scraping').
        yahoo_config: Configuration for Yahoo Finance provider.
        scraping_config: Configuration for scraping provider.

    Returns:
        Configured price provider instance.

    Raises:
        ValueError: If provider_name is not recognized.
    """
    provider_name = provider_name.lower().strip()

    if provider_name in ("yahoo", "yf", "yahoo_finance"):
        return YahooFinanceProvider(config=yahoo_config)
    elif provider_name in ("scraping", "scrape", "asx_scraping", "fallback"):
        return ASXScrapingProvider(config=scraping_config)
    else:
        raise ValueError(f"Unknown provider: {provider_name}. Valid options: 'yahoo', 'scraping'")
