---
id: 026
name: Paper Trading Ledger v1 (EOD)
status: Completed
---

# 026 - Paper Trading Ledger v1 (EOD)

Implement paper trading as a persisted ledger of simulated executions using end-of-day (daily close) fills.

## Description

- Consume signals (or manual triggers) and record simulated trades.
- Use daily close as fill price (v1).
- Persist orders/executions and positions.

## Impact

- Enables forward-testing strategies without real money.

## Success Criteria

- Paper trades can be recorded deterministically for a given day.
- Positions and basic P/L can be derived from the ledger.
- Data is queryable by the UI.

## Implementation

### Files Created

- `jobs/src/asx_jobs/paper/__init__.py` - Module exports
- `jobs/src/asx_jobs/paper/engine.py` - PaperTradingEngine class
- `jobs/src/asx_jobs/paper/executor.py` - EODExecutor class

### Database Methods Added

In `jobs/src/asx_jobs/database.py`:
- `create_paper_account()` - Create new paper trading account
- `get_paper_account()` / `get_paper_account_by_name()` - Retrieve accounts
- `get_all_paper_accounts()` - List all accounts
- `update_paper_account_balance()` - Update cash balance
- `submit_paper_order()` - Submit a new order
- `get_pending_paper_orders()` - Get unfilled orders
- `fill_paper_order()` - Mark order as filled
- `cancel_paper_order()` - Cancel an order
- `get_paper_orders()` - List orders for account
- `upsert_paper_position()` - Update position
- `get_paper_positions()` / `get_paper_position()` - Retrieve positions
- `create_portfolio_snapshot()` - Create daily snapshot
- `get_portfolio_snapshots()` / `get_latest_portfolio_snapshot()` - Retrieve snapshots
- `get_latest_price_for_instrument()` - Get latest price
- `get_prices_for_date()` - Get all prices for a date

### CLI Commands Added

```bash
# Account Management
asx-jobs paper account create "My Account" --balance 100000
asx-jobs paper account list
asx-jobs paper account show 1

# Order Management
asx-jobs paper order buy BHP 100 --account 1
asx-jobs paper order sell CBA 50 --account 1 --limit 95.00
asx-jobs paper order list --account 1
asx-jobs paper order cancel 123

# Execution
asx-jobs paper execute --date 2024-01-15
asx-jobs paper execute --account 1

# Portfolio
asx-jobs paper positions --account 1
asx-jobs paper snapshot --account 1 --date 2024-01-15
```

### Features

1. **Account Management**
   - Create named accounts with initial balance
   - Track cash balance separately from positions
   - Support multiple accounts

2. **Order Submission**
   - Market orders (fill at close)
   - Limit orders (fill if price reached during day)
   - Buy/sell validation (cash check, position check)

3. **EOD Execution**
   - Execute all pending orders at daily close
   - Limit orders check high/low for fill eligibility
   - Update positions and cash balances

4. **Position Tracking**
   - Track quantity, average entry price
   - Calculate unrealized P&L
   - Track realized P&L on sales

5. **Portfolio Snapshots**
   - Daily portfolio value snapshots
   - Track daily P&L and returns
   - Store position details for historical analysis
