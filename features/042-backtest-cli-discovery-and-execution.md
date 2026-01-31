---
id: 042
name: Backtest CLI Discovery and Execution
status: Planned
---

# 042 - Backtest CLI Discovery and Execution

Provide a supported, documented CLI entrypoint for running backtests end-to-end, and ensure the CLI surface is discoverable (help text + docs) so operators can confidently run backtests and populate the database for the frontend.

This feature combines:

- **CLI discovery**: make it obvious whether backtesting is available, how to invoke it, and what it does.
- **CLI execution**: wire/implement `asx-jobs backtest ...` so it runs a strategy backtest and persists results to the DB.

## Description

Add a backtesting command to the jobs runner CLI (`asx-jobs`) that:

1. Selects a strategy by **name** (e.g., `"Mean Reversion"`, `"Breakout"`).
2. Executes the backtest via the existing BacktestEngine.
3. Persists results to the DB tables used by reporting:
   - `backtest_runs`
   - `backtest_trades`
   - `backtest_metrics`

The command should be discoverable via `asx-jobs --help` and `asx-jobs backtest --help`, and any related documentation should clearly describe prerequisites (e.g., price data present) and the expected side effects (DB writes).

## Impact

- Enables operators to run backtests without writing ad-hoc scripts.
- Ensures backtest reporting views (e.g., `v_backtest_leaderboard`) can be populated consistently.
- Reduces confusion during backend validation by making the population mechanism explicit and repeatable.

## Success Criteria

- `asx-jobs --help` lists a `backtest` command.
- `asx-jobs backtest --help` documents usage and clearly states that results are written to the database.
- Running a backtest by strategy name (e.g., `asx-jobs backtest --strategy "Mean Reversion" --start YYYY-MM-DD --end YYYY-MM-DD`) completes without error when prerequisites are satisfied.
- After a successful run, the database contains:
  - A new row in `backtest_runs` linked to the selected strategy.
  - One or more rows in `backtest_trades` when trades are generated.
  - Exactly one row in `backtest_metrics` for the run.
- `v_backtest_leaderboard` becomes non-empty once at least one run exists (assuming the view is installed).

## Notes / Open Questions

- Define the minimal required CLI flags beyond `--strategy` (e.g., `--start`, `--end`, `--initial-capital`, `--universe`).
- Determine expected behavior when:
  - the named strategy does not exist in DB,
  - the strategy exists but is `is_active = false`,
  - there is insufficient historical price data for the requested date range.
