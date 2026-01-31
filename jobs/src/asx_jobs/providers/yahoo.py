"""Yahoo Finance data provider adapter."""

import time
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any

import pandas as pd
import yfinance as yf
from tenacity import retry, stop_after_attempt, wait_exponential

from asx_jobs.config import YahooConfig
from asx_jobs.logging import get_logger
from asx_jobs.providers.base import BasePriceProvider, PriceBar

logger = get_logger(__name__)


@dataclass
class Quote:
    """Current quote snapshot."""

    symbol: str
    price: float
    change: float
    change_percent: float
    volume: int
    timestamp: datetime


def normalize_asx_symbol(symbol: str) -> str:
    """Convert ASX symbol to Yahoo Finance format.

    ASX symbols on Yahoo Finance use the .AX suffix.

    Args:
        symbol: ASX ticker symbol (e.g., 'BHP', 'CBA').

    Returns:
        Yahoo Finance symbol (e.g., 'BHP.AX', 'CBA.AX').
    """
    symbol = symbol.upper().strip()
    if not symbol.endswith(".AX"):
        return f"{symbol}.AX"
    return symbol


def denormalize_asx_symbol(yahoo_symbol: str) -> str:
    """Convert Yahoo Finance symbol back to ASX format.

    Args:
        yahoo_symbol: Yahoo Finance symbol (e.g., 'BHP.AX').

    Returns:
        ASX symbol (e.g., 'BHP').
    """
    if yahoo_symbol.endswith(".AX"):
        return yahoo_symbol[:-3]
    return yahoo_symbol


class YahooFinanceProvider(BasePriceProvider):
    """Yahoo Finance data provider for ASX stocks."""

    def __init__(self, config: YahooConfig | None = None) -> None:
        """Initialize Yahoo Finance provider.

        Args:
            config: Provider configuration.
        """
        self.config = config or YahooConfig()
        logger.info(
            "yahoo_provider_initialized",
            rate_limit_delay=self.config.rate_limit_delay,
            batch_size=self.config.batch_size,
        )

    @property
    def name(self) -> str:
        return "yahoo"

    def _rate_limit(self) -> None:
        """Apply rate limiting delay."""
        if self.config.rate_limit_delay > 0:
            time.sleep(self.config.rate_limit_delay)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def get_price_history(
        self,
        symbol: str,
        start_date: date | None = None,
        end_date: date | None = None,
        period: str | None = None,
    ) -> list[PriceBar]:
        """Fetch historical daily price bars.

        Args:
            symbol: ASX ticker symbol.
            start_date: Start date (inclusive).
            end_date: End date (inclusive).
            period: Alternative to dates (e.g., '1mo', '3mo', '1y', 'max').

        Returns:
            List of PriceBar objects.

        Raises:
            ValueError: If no price data available.
        """
        yahoo_symbol = normalize_asx_symbol(symbol)
        ticker = yf.Ticker(yahoo_symbol)

        self._rate_limit()

        if period:
            df = ticker.history(period=period)
        else:
            start = start_date or (date.today() - timedelta(days=365))
            end = end_date or date.today()
            df = ticker.history(start=start, end=end + timedelta(days=1))

        if df.empty:
            logger.warning("no_price_data", symbol=symbol, yahoo_symbol=yahoo_symbol)
            return []

        bars: list[PriceBar] = []
        for idx, row in df.iterrows():
            trade_date = idx.date() if hasattr(idx, "date") else idx
            bars.append(
                PriceBar(
                    trade_date=trade_date,
                    open=float(row["Open"]) if pd.notna(row["Open"]) else None,
                    high=float(row["High"]) if pd.notna(row["High"]) else None,
                    low=float(row["Low"]) if pd.notna(row["Low"]) else None,
                    close=float(row["Close"]),
                    volume=int(row["Volume"]) if pd.notna(row["Volume"]) else 0,
                    adjusted_close=(
                        float(row["Close"]) if pd.notna(row["Close"]) else None
                    ),
                )
            )

        logger.debug(
            "price_history_fetched",
            symbol=symbol,
            bars_count=len(bars),
            start=bars[0].trade_date.isoformat() if bars else None,
            end=bars[-1].trade_date.isoformat() if bars else None,
        )

        return bars

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def get_quote(self, symbol: str) -> Quote | None:
        """Fetch current quote snapshot.

        Args:
            symbol: ASX ticker symbol.

        Returns:
            Quote object or None if unavailable.
        """
        yahoo_symbol = normalize_asx_symbol(symbol)
        ticker = yf.Ticker(yahoo_symbol)

        self._rate_limit()

        info = ticker.info
        if not info or "regularMarketPrice" not in info:
            logger.warning("no_quote_data", symbol=symbol, yahoo_symbol=yahoo_symbol)
            return None

        return Quote(
            symbol=symbol,
            price=float(info.get("regularMarketPrice", 0)),
            change=float(info.get("regularMarketChange", 0)),
            change_percent=float(info.get("regularMarketChangePercent", 0)),
            volume=int(info.get("regularMarketVolume", 0)),
            timestamp=datetime.now(),
        )

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
        results: dict[str, list[PriceBar]] = {}
        yahoo_symbols = [normalize_asx_symbol(s) for s in symbols]

        self._rate_limit()

        if period:
            df = yf.download(
                yahoo_symbols,
                period=period,
                group_by="ticker",
                progress=False,
                threads=False,
            )
        else:
            start = start_date or (date.today() - timedelta(days=365))
            end = end_date or date.today()
            df = yf.download(
                yahoo_symbols,
                start=start,
                end=end + timedelta(days=1),
                group_by="ticker",
                progress=False,
                threads=False,
            )

        if df.empty:
            logger.warning("bulk_download_empty", symbols_count=len(symbols))
            return results

        for yahoo_sym, asx_sym in zip(yahoo_symbols, symbols):
            try:
                if len(yahoo_symbols) == 1:
                    symbol_df = df
                else:
                    symbol_df = df[yahoo_sym] if yahoo_sym in df.columns.levels[0] else None

                if symbol_df is None or symbol_df.empty:
                    results[asx_sym] = []
                    continue

                bars: list[PriceBar] = []
                for idx, row in symbol_df.iterrows():
                    trade_date = idx.date() if hasattr(idx, "date") else idx
                    if pd.isna(row.get("Close")):
                        continue
                    bars.append(
                        PriceBar(
                            trade_date=trade_date,
                            open=float(row["Open"]) if pd.notna(row.get("Open")) else None,
                            high=float(row["High"]) if pd.notna(row.get("High")) else None,
                            low=float(row["Low"]) if pd.notna(row.get("Low")) else None,
                            close=float(row["Close"]),
                            volume=int(row["Volume"]) if pd.notna(row.get("Volume")) else 0,
                            adjusted_close=float(row["Close"]) if pd.notna(row.get("Close")) else None,
                        )
                    )
                results[asx_sym] = bars

            except Exception as e:
                logger.warning("bulk_symbol_error", symbol=asx_sym, error=str(e))
                results[asx_sym] = []

        return results

    def get_instrument_info(self, symbol: str) -> dict[str, Any] | None:
        """Fetch instrument metadata.

        Args:
            symbol: ASX ticker symbol.

        Returns:
            Dictionary with instrument info or None.
        """
        yahoo_symbol = normalize_asx_symbol(symbol)
        ticker = yf.Ticker(yahoo_symbol)

        self._rate_limit()

        info = ticker.info
        if not info or "symbol" not in info:
            return None

        return {
            "symbol": symbol,
            "name": info.get("longName") or info.get("shortName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "market_cap": info.get("marketCap"),
            "currency": info.get("currency", "AUD"),
            "exchange": info.get("exchange"),
        }
