# Price providers
Fetch and store price data from multiple sources with automatic fallback.

---

## Set the context
The jobs runner needs daily price data (OHLCV) to compute signals and update dashboards. External APIs can be unreliable or rate-limited, so the system supports multiple providers and automatic fallback.

This guide explains the provider architecture and how to configure or extend it.

---

## Choose a provider
Two providers are available out of the box:

| Provider | Key | Description |
|----------|-----|-------------|
| Yahoo Finance | `yahoo` | Primary provider using the `yfinance` library. Fast and reliable for most ASX symbols. |
| ASX Scraping | `scraping` | Web scraping fallback. Slower but works when Yahoo is unavailable. |

Set the default provider via environment variable:

```bash
PRICE_PROVIDER=yahoo
```

---

## Enable fallback
When the primary provider fails, the runner can automatically try the fallback provider. Enable this with:

```bash
PRICE_PROVIDER_FALLBACK=scraping
PRICE_PROVIDER_FALLBACK_ENABLED=true
```

The fallback is disabled by default for predictable behavior during development.

---

## Configure rate limits
Both providers support rate limiting to avoid bans or throttling.

Yahoo Finance:
```bash
YAHOO_RATE_LIMIT_DELAY=0.5
YAHOO_BATCH_SIZE=10
```

Scraping provider:
```bash
SCRAPING_RATE_LIMIT_DELAY=2.0
SCRAPING_TIMEOUT=30
```

The scraping provider uses a longer delay to be polite to the ASX website.

---

## Use the provider factory
The `get_provider()` function returns a configured provider instance:

```python
from asx_jobs.providers import get_provider

# Get the default provider (from config)
provider = get_provider()

# Get a specific provider
yahoo = get_provider("yahoo")
scraper = get_provider("scraping")

# Fetch price history
bars = provider.get_price_history("BHP", period="1mo")
```

All providers implement the `BasePriceProvider` interface with consistent methods.

---

## Understand the interface
The base provider defines these methods:

```python
class BasePriceProvider:
    @property
    def name(self) -> str:
        """Provider identifier."""

    def get_price_history(
        self,
        symbol: str,
        start_date: date | None = None,
        end_date: date | None = None,
        period: str | None = None,
    ) -> list[PriceBar]:
        """Fetch historical daily OHLCV data."""
```

The `PriceBar` dataclass contains:
- `trade_date`: Date of the trading session
- `open`, `high`, `low`, `close`: Price values
- `volume`: Trading volume
- `adjusted_close`: Split-adjusted close price (optional)

---

## Add a new provider
1. Create a new file in `jobs/src/asx_jobs/providers/`.
2. Inherit from `BasePriceProvider` and implement required methods.
3. Add the provider to `get_provider()` in `__init__.py`.
4. Add configuration to `config.py` if needed.
5. Update `.env.example` with any new settings.

Example skeleton:

```python
from asx_jobs.providers.base import BasePriceProvider, PriceBar

class MyNewProvider(BasePriceProvider):
    @property
    def name(self) -> str:
        return "my_provider"

    def get_price_history(self, symbol, **kwargs) -> list[PriceBar]:
        # Implementation here
        pass
```

---

## Handle errors gracefully
Providers should return empty lists rather than raising exceptions for missing data. Log warnings for debugging but don't crash the job.

```python
if not data:
    logger.warning("no_price_data", symbol=symbol)
    return []
```

Use retry decorators for transient network errors:

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential())
def get_price_history(self, symbol, **kwargs):
    # ...
```

---

## Test providers
Run basic syntax checks:

```bash
cd jobs
python -m py_compile src/asx_jobs/providers/yahoo.py
python -m py_compile src/asx_jobs/providers/scraping.py
```

Test with real symbols:

```bash
asx-jobs daily --symbols BHP,CBA --dry-run
```

---

## Explore related files
- [`jobs/src/asx_jobs/providers/base.py`](../../jobs/src/asx_jobs/providers/base.py) - Base interface
- [`jobs/src/asx_jobs/providers/yahoo.py`](../../jobs/src/asx_jobs/providers/yahoo.py) - Yahoo Finance provider
- [`jobs/src/asx_jobs/providers/scraping.py`](../../jobs/src/asx_jobs/providers/scraping.py) - Scraping fallback
- [`jobs/src/asx_jobs/config.py`](../../jobs/src/asx_jobs/config.py) - Provider configuration
- [Symbol normalization](./symbol-normalization.md) - How symbols are converted between providers
