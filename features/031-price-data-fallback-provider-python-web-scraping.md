---
id: 031
name: Price Data Fallback Provider (Python Web Scraping)
status: Planned
---

# 031 - Price Data Fallback Provider (Python Web Scraping)

Provide a no-key, free fallback mechanism to collect the minimum required daily price/volume data via Python web scraping when API-style free endpoints are unavailable or unreliable.

## Description

- Define scrape targets and the minimum dataset required for v1:
  - daily close (and ideally OHLCV)
  - volume
  - timestamp/date
- Implement scraping with:
  - throttling and politeness
  - retries/backoff
  - HTML parsing robustness
- Integrate into the jobs runner as a selectable provider.

## Impact

- Protects the platform from provider volatility while remaining free.

## Success Criteria

- Can fetch and store daily data for a test subset.
- Can run daily at midday Sydney without breaking due to minor site changes (best-effort).
- Provider can be toggled via configuration.
