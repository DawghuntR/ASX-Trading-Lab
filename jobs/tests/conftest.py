"""pytest configuration and shared fixtures."""

import pytest


@pytest.fixture
def sample_price_data() -> list[dict]:
    """Sample price data for testing calculations.
    
    Returns:
        List of price records ordered most recent first.
    """
    return [
        {"trade_date": "2024-01-20", "open": 10.00, "high": 10.50, "low": 9.80, "close": 10.20, "volume": 150000},
        {"trade_date": "2024-01-19", "open": 9.50, "high": 10.10, "low": 9.40, "close": 10.00, "volume": 100000},
        {"trade_date": "2024-01-18", "open": 9.20, "high": 9.60, "low": 9.10, "close": 9.50, "volume": 80000},
        {"trade_date": "2024-01-17", "open": 9.00, "high": 9.30, "low": 8.90, "close": 9.20, "volume": 90000},
        {"trade_date": "2024-01-16", "open": 9.10, "high": 9.20, "low": 8.80, "close": 9.00, "volume": 70000},
        {"trade_date": "2024-01-15", "open": 9.20, "high": 9.40, "low": 9.00, "close": 9.10, "volume": 60000},
        {"trade_date": "2024-01-14", "open": 9.30, "high": 9.50, "low": 9.10, "close": 9.20, "volume": 55000},
    ]


@pytest.fixture
def sample_portfolio_snapshots() -> list[dict]:
    """Sample portfolio snapshots for testing metrics.
    
    Returns:
        List of portfolio snapshots ordered oldest first.
    """
    return [
        {"snapshot_date": "2024-01-15", "total_value": 100000.00, "cash_balance": 50000.00, "positions_value": 50000.00, "daily_pnl": 0.0, "daily_return": 0.0},
        {"snapshot_date": "2024-01-16", "total_value": 102000.00, "cash_balance": 50000.00, "positions_value": 52000.00, "daily_pnl": 2000.0, "daily_return": 0.02},
        {"snapshot_date": "2024-01-17", "total_value": 105000.00, "cash_balance": 50000.00, "positions_value": 55000.00, "daily_pnl": 3000.0, "daily_return": 0.0294},
        {"snapshot_date": "2024-01-18", "total_value": 101000.00, "cash_balance": 50000.00, "positions_value": 51000.00, "daily_pnl": -4000.0, "daily_return": -0.0381},
        {"snapshot_date": "2024-01-19", "total_value": 103000.00, "cash_balance": 50000.00, "positions_value": 53000.00, "daily_pnl": 2000.0, "daily_return": 0.0198},
    ]


@pytest.fixture
def sample_equity_curve():
    """Sample equity curve points for testing drawdown calculations."""
    from asx_jobs.paper.metrics import EquityPoint
    
    return [
        EquityPoint(date="2024-01-15", total_value=100000.0, cash_balance=50000.0, positions_value=50000.0, daily_pnl=0.0, daily_return=0.0, cumulative_return=0.0, drawdown=0.0, drawdown_pct=0.0),
        EquityPoint(date="2024-01-16", total_value=105000.0, cash_balance=50000.0, positions_value=55000.0, daily_pnl=5000.0, daily_return=0.05, cumulative_return=0.05, drawdown=0.0, drawdown_pct=0.0),
        EquityPoint(date="2024-01-17", total_value=102000.0, cash_balance=50000.0, positions_value=52000.0, daily_pnl=-3000.0, daily_return=-0.0286, cumulative_return=0.02, drawdown=3000.0, drawdown_pct=0.0286),
        EquityPoint(date="2024-01-18", total_value=98000.0, cash_balance=50000.0, positions_value=48000.0, daily_pnl=-4000.0, daily_return=-0.0392, cumulative_return=-0.02, drawdown=7000.0, drawdown_pct=0.0667),
        EquityPoint(date="2024-01-19", total_value=106000.0, cash_balance=50000.0, positions_value=56000.0, daily_pnl=8000.0, daily_return=0.0816, cumulative_return=0.06, drawdown=0.0, drawdown_pct=0.0),
    ]
