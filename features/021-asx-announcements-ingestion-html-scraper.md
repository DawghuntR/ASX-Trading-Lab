---
id: 021
name: ASX Announcements Ingestion (HTML Scraper)
status: Completed
---

# 021 - ASX Announcements Ingestion (HTML Scraper)

Ingest ASX announcements using HTML scraping (free, best-effort) and store them in Supabase.

## Description

- Scrape the ASX announcements pages.
- Capture at minimum:
  - symbol
  - timestamp
  - headline/title
  - URL / reference id (for dedupe)
- Implement deduplication and incremental fetch.

## Impact

- Enables building edges around news-to-price reaction patterns.

## Success Criteria

- Daily run ingests new announcements and does not duplicate existing ones.
- Stored announcements are queryable by symbol and date.
- Scraper failures are logged and do not break unrelated jobs.
