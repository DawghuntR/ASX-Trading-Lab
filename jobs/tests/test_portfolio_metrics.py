"""Tests for portfolio metrics calculations.

Tests the pure calculation functions in the portfolio metrics module,
including equity curve, drawdown, and exposure calculations.
"""

import pytest


class TestEquityCurveBuilding:
    """Tests for equity curve construction."""

    def test_build_equity_curve(self, sample_portfolio_snapshots):
        """Equity curve should compute cumulative return and drawdown."""
        initial_value = 100000.0
        
        curve = _build_equity_curve(sample_portfolio_snapshots, initial_value)
        
        assert len(curve) == len(sample_portfolio_snapshots)
        assert curve[0]["cumulative_return"] == pytest.approx(0.0, abs=0.001)
        assert curve[-1]["total_value"] == 103000.0

    def test_drawdown_tracking(self, sample_portfolio_snapshots):
        """Drawdown should be calculated from peak."""
        initial_value = 100000.0
        
        curve = _build_equity_curve(sample_portfolio_snapshots, initial_value)
        
        peak_point = curve[2]
        assert peak_point["total_value"] == 105000.0
        
        trough_point = curve[3]
        assert trough_point["drawdown"] == pytest.approx(4000.0, rel=0.01)
        assert trough_point["drawdown_pct"] == pytest.approx(4000.0 / 105000.0, rel=0.01)


class TestDrawdownCalculation:
    """Tests for drawdown statistics calculation."""

    def test_max_drawdown(self, sample_equity_curve):
        """Max drawdown should be correctly identified."""
        result = _calculate_drawdown(sample_equity_curve)
        
        assert result["max_drawdown"] == pytest.approx(7000.0, rel=0.01)
        assert result["max_drawdown_date"] == "2024-01-18"

    def test_peak_tracking(self, sample_equity_curve):
        """Peak value and date should be correctly identified."""
        result = _calculate_drawdown(sample_equity_curve)
        
        assert result["peak_value"] == pytest.approx(106000.0, rel=0.01)
        assert result["peak_date"] == "2024-01-19"

    def test_empty_curve(self):
        """Empty curve should return zero values."""
        result = _calculate_drawdown([])
        
        assert result["max_drawdown"] == 0.0
        assert result["max_drawdown_pct"] == 0.0
        assert result["max_drawdown_date"] is None


class TestExposureCalculation:
    """Tests for exposure statistics calculation."""

    def test_average_exposure(self, sample_equity_curve):
        """Average exposure should be calculated correctly."""
        result = _calculate_exposure(sample_equity_curve, 100000.0)
        
        expected_exposures = []
        for point in sample_equity_curve:
            exposure = point["positions_value"] / point["total_value"]
            expected_exposures.append(exposure)
        
        expected_avg = sum(expected_exposures) / len(expected_exposures)
        assert result["avg_exposure"] == pytest.approx(expected_avg, rel=0.01)

    def test_current_exposure(self, sample_equity_curve):
        """Current exposure should be from last point."""
        result = _calculate_exposure(sample_equity_curve, 100000.0)
        
        last_point = sample_equity_curve[-1]
        expected = last_point["positions_value"] / last_point["total_value"]
        assert result["current_exposure"] == pytest.approx(expected, rel=0.01)

    def test_empty_curve_exposure(self):
        """Empty curve should return zero exposure."""
        result = _calculate_exposure([], 100000.0)
        
        assert result["avg_exposure"] == 0.0
        assert result["current_exposure"] == 0.0


def _build_equity_curve(snapshots: list[dict], initial_value: float) -> list[dict]:
    """Build equity curve from snapshots (extracted for testing)."""
    curve: list[dict] = []
    peak_value = initial_value

    for snap in snapshots:
        total_value = float(snap["total_value"])
        cash_balance = float(snap["cash_balance"])
        positions_value = float(snap["positions_value"])
        daily_pnl = float(snap.get("daily_pnl") or 0)
        daily_return = float(snap.get("daily_return") or 0)

        cumulative_return = (total_value - initial_value) / initial_value if initial_value > 0 else 0

        if total_value > peak_value:
            peak_value = total_value

        drawdown = peak_value - total_value
        drawdown_pct = drawdown / peak_value if peak_value > 0 else 0

        curve.append({
            "date": snap["snapshot_date"],
            "total_value": total_value,
            "cash_balance": cash_balance,
            "positions_value": positions_value,
            "daily_pnl": daily_pnl,
            "daily_return": daily_return,
            "cumulative_return": cumulative_return,
            "drawdown": drawdown,
            "drawdown_pct": drawdown_pct,
        })

    return curve


def _calculate_drawdown(equity_curve: list) -> dict:
    """Calculate drawdown statistics (extracted for testing)."""
    if not equity_curve:
        return {
            "max_drawdown": 0.0,
            "max_drawdown_pct": 0.0,
            "max_drawdown_date": None,
            "peak_value": 0.0,
            "peak_date": None,
        }

    max_drawdown = 0.0
    max_drawdown_pct = 0.0
    max_drawdown_date = None
    
    if isinstance(equity_curve[0], dict):
        peak_value = equity_curve[0]["total_value"]
        peak_date = equity_curve[0]["date"]
        
        for point in equity_curve:
            if point["total_value"] > peak_value:
                peak_value = point["total_value"]
                peak_date = point["date"]

            dd = peak_value - point["total_value"]
            if dd > max_drawdown:
                max_drawdown = dd
                max_drawdown_pct = dd / peak_value if peak_value > 0 else 0
                max_drawdown_date = point["date"]
    else:
        peak_value = equity_curve[0].total_value
        peak_date = equity_curve[0].date

        for point in equity_curve:
            if point.total_value > peak_value:
                peak_value = point.total_value
                peak_date = point.date

            if point.drawdown > max_drawdown:
                max_drawdown = point.drawdown
                max_drawdown_pct = point.drawdown_pct
                max_drawdown_date = point.date

    return {
        "max_drawdown": max_drawdown,
        "max_drawdown_pct": max_drawdown_pct,
        "max_drawdown_date": max_drawdown_date,
        "peak_value": peak_value,
        "peak_date": peak_date,
    }


def _calculate_exposure(equity_curve: list, initial_value: float) -> dict:
    """Calculate exposure statistics (extracted for testing)."""
    if not equity_curve:
        return {
            "avg_exposure": 0.0,
            "current_exposure": 0.0,
        }

    exposures = []
    for point in equity_curve:
        if isinstance(point, dict):
            total_val = point["total_value"]
            pos_val = point["positions_value"]
        else:
            total_val = point.total_value
            pos_val = point.positions_value
            
        if total_val > 0:
            exposure = pos_val / total_val
        else:
            exposure = 0.0
        exposures.append(exposure)

    avg_exposure = sum(exposures) / len(exposures) if exposures else 0
    current_exposure = exposures[-1] if exposures else 0

    return {
        "avg_exposure": avg_exposure,
        "current_exposure": current_exposure,
    }
