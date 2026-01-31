# Rate limits
Keep jobs fast and steady under provider limits.

---

## See the scope

The system targets whole-of-ASX coverage (~2000 symbols). It relies on free data providers with rate limits.

Runs on home lab hardware (Ubuntu 24.04) with a daily schedule at 12:00 Sydney time.

---

## Set budgets

### Daily job runtime targets

| Job | Target duration | Notes |
|-----|-----------------|-------|
| Symbol ingestion | < 5 minutes | One-time/weekly updates |
| Price ingestion (ASX300) | < 30 minutes | ~300 symbols with rate limiting |
| Price ingestion (full ASX) | < 2 hours | ~2000 symbols |
| Signal generation | < 10 minutes | Post-price computation |
| Announcements | < 15 minutes | HTML scraping |
| **Total daily run** | **< 3 hours** | ASX300 fallback: < 1 hour |

### UI query targets

| Query | Target response | Notes |
|-------|-----------------|-------|
| Dashboard load | < 2 seconds | Uses cached views |
| Symbol drilldown | < 1 second | Indexed queries |
| Signal listing | < 1 second | Paginated |
| Backtest results | < 2 seconds | Precomputed metrics |

---

## Configure limits

### Yahoo Finance provider

From `jobs/.env.example`:

```
YAHOO_RATE_LIMIT_DELAY=0.5  # Seconds between requests
YAHOO_BATCH_SIZE=10          # Symbols per batch request
YAHOO_TIMEOUT=30             # Request timeout in seconds
```

### Job runner settings

```
ASX_JOBS_BATCH_SIZE=50       # Records per database batch
ASX_JOBS_RETRY_ATTEMPTS=3    # Retries on failure
ASX_JOBS_RETRY_DELAY=5       # Seconds between retries
```

### Tune for your environment

- Increase delays if hitting rate limits (429 errors).
- Decrease delays for faster runs (if not hitting limits).
- Adjust batch sizes based on memory constraints.

---

## Optimize the database

### Index strategy

See `database/migrations/014_performance_indexes.sql` for the full list.

Key indexes:

- `idx_daily_prices_instrument_date_desc` - Price history queries
- `idx_daily_prices_covering` - Avoids table lookups
- `idx_signals_recent` - Partial index for 30-day window
- `idx_*_pending` - Fast order/position lookups

### Query optimization tips

- Use date ranges to limit data scanned.
- Leverage partial indexes for common filters.
- Use `EXPLAIN ANALYZE` to profile slow queries.

### Run maintenance

```sql
-- Update statistics (run weekly or after large imports)
ANALYZE instruments;
ANALYZE daily_prices;
ANALYZE signals;

-- Check index usage
SELECT * FROM pg_stat_user_indexes WHERE idx_scan = 0;
```

---

## Monitor runs

### Track job durations

Job runs are logged in the `job_runs` table.

```sql
SELECT job_name, duration_seconds, records_processed
FROM job_runs
WHERE duration_seconds > 300
ORDER BY started_at DESC;
```

### Find bottlenecks

- Check journald logs: `journalctl -u asx-jobs.service --since "today"`.
- Look for rate limit warnings.
- Monitor database connection times.

---

## Plan scaling

### When running full ASX

Expect 2+ hours for complete ingestion. Use a systemd timer with sufficient timeout.

Consider splitting into multiple job runs.

### Home lab hardware recommendations

- 2+ CPU cores
- 4GB+ RAM
- SSD storage (for database performance)
- Stable internet connection

---

## Troubleshoot slowdowns

### Job taking too long

1. Check rate limit settings (may be too conservative).
2. Verify network connectivity.
3. Check for provider API issues.
4. Consider reducing universe (ASX300 fallback).

### UI queries slow

1. Run `ANALYZE` on relevant tables.
2. Check for missing indexes.
3. Review query patterns in slow queries.
4. Consider materialized views for complex aggregations.

### Database growing large

1. Implement retention cleanup (see [data retention](data-retention.md)).
2. Archive old data before deletion.
3. Run `VACUUM ANALYZE` after large deletes.
