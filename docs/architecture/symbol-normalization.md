# Symbol normalization
Keep provider formats consistent across the system.

---

## Set the context
Different data providers use different identifier formats for the same instrument. ASX uses plain codes like `BHP`, while Yahoo Finance uses the `.AX` suffix like `BHP.AX`.

Future providers may introduce other patterns, so the system needs a stable internal format. This guide explains how the database and code keep everything aligned.

---

## Use canonical format
The database stores canonical ASX identifiers without suffixes. The `instruments` table is the source of truth for these values, and all internal references should use the canonical form.

Example canonical values: `BHP`, `CBA`, `WOW`.

---

## Map providers
The `provider_mappings` table links each `instrument_id` to a provider-specific identifier. This supports multiple providers per instrument and records active or inactive mappings.

See the migration at [`database/migrations/013_provider_mappings.sql`](../../database/migrations/013_provider_mappings.sql).

SQL example:

```sql
insert into provider_mappings (instrument_id, provider, provider_symbol, is_active)
values (123, 'yahoo', 'BHP.AX', true)
```

---

## Track history
The `symbol_history` table records corporate actions and identifier changes over time. It supports renames, mergers or demergers, delistings, and historical lookups.

SQL example:

```sql
insert into symbol_history (instrument_id, old_symbol, new_symbol, effective_date, reason)
values (123, 'BHP', 'BHP.AX', '2006-01-01', 'provider_format_change')
```

---

## Use database helpers
Use the helper functions to convert between formats as close to the data boundary as possible. This keeps application code stable and avoids format drift.

```sql
select get_provider_symbol('BHP', 'yahoo')
select get_canonical_symbol('BHP.AX', 'yahoo')
```

---

## Reference implementation
The Yahoo provider shows the Python implementation details. See `jobs/src/asx_jobs/providers/yahoo.py` and the functions `normalize_asx_symbol()` and `denormalize_asx_symbol()`.

This is the pattern to follow when adding new adapters. Keep the conversion small and easy to test.

---

## Add a provider
1. Define the provider's identifier format and edge rules.
2. Add mappings in `provider_mappings` for each instrument.
3. Create a provider adapter with normalization and denormalization helpers.
4. Test with edge cases and real-world samples.

Tip: add a small fixture set for known tricky codes.

---

## Handle edge cases
Plan for delisted instruments, renames, and special characters. Include non-equity instruments like ETFs and warrants, which may have distinct formats.

Use `symbol_history` for transitions and `provider_mappings` for provider-specific quirks.

---

## Explore related docs
- [Feature specs](../../features/)
- [Database migrations](../../database/migrations/)
