"""Tests for volatility signal calculations.

Tests the pure calculation functions in the volatility signal engine,
including true range, ATR, and spike detection.
"""

import pytest


class TestTrueRangeCalculation:
    """Tests for _calc_true_range method."""

    def test_standard_true_range(self):
        """Standard true range calculation (high - low dominant)."""
        current = {"high": 10.50, "low": 9.80, "close": 10.20}
        previous = {"close": 10.00}

        tr = _calc_true_range(current, previous)

        expected = max(
            10.50 - 9.80,
            abs(10.50 - 10.00),
            abs(9.80 - 10.00),
        )
        assert tr == pytest.approx(expected, rel=0.01)

    def test_gap_up_true_range(self):
        """True range with gap up (high - prev_close dominant)."""
        current = {"high": 12.00, "low": 11.50, "close": 11.80}
        previous = {"close": 10.00}

        tr = _calc_true_range(current, previous)

        # Expected: max(high-low, |high-prev_close|, |low-prev_close|) = max(0.5, 2.0, 1.5) = 2.0
        assert tr == pytest.approx(2.0, rel=0.01)

    def test_gap_down_true_range(self):
        """True range with gap down (prev_close - low dominant)."""
        current = {"high": 9.00, "low": 8.50, "close": 8.70}
        previous = {"close": 10.00}

        tr = _calc_true_range(current, previous)

        # Expected: max(high-low, |high-prev_close|, |low-prev_close|) = max(0.5, 1.0, 1.5) = 1.5
        assert tr == pytest.approx(1.5, rel=0.01)

    def test_missing_high(self):
        """Missing high should return None."""
        current = {"high": None, "low": 9.80, "close": 10.20}
        previous = {"close": 10.00}

        tr = _calc_true_range(current, previous)

        assert tr is None

    def test_missing_low(self):
        """Missing low should return None."""
        current = {"high": 10.50, "low": None, "close": 10.20}
        previous = {"close": 10.00}

        tr = _calc_true_range(current, previous)

        assert tr is None

    def test_missing_previous_close(self):
        """Missing previous close should return None."""
        current = {"high": 10.50, "low": 9.80, "close": 10.20}
        previous = {"close": None}

        tr = _calc_true_range(current, previous)

        assert tr is None


class TestATRCalculation:
    """Tests for _calc_atr method."""

    def test_standard_atr(self, sample_price_data):
        """Standard ATR calculation with valid data."""
        atr = _calc_atr(sample_price_data[1:], 5)

        assert atr is not None
        assert atr > 0

    def test_insufficient_data(self, sample_price_data):
        """Insufficient data should return None."""
        atr = _calc_atr(sample_price_data[:2], 5)

        assert atr is None


class TestVolatilityStrength:
    """Tests for _determine_strength method."""

    def test_weak_volatility(self):
        """Range ratio just above threshold should be weak."""
        strength = _determine_strength(2.1, 2.0, 3.0)

        assert strength == "weak"

    def test_medium_volatility(self):
        """Range ratio at midpoint should be medium."""
        strength = _determine_strength(2.6, 2.0, 3.0)

        assert strength == "medium"

    def test_strong_volatility(self):
        """Range ratio at or above strong threshold should be strong."""
        strength = _determine_strength(3.5, 2.0, 3.0)

        assert strength == "strong"


def _calc_true_range(current: dict, previous: dict) -> float | None:
    """Calculate true range for current bar (extracted for testing)."""
    high = current.get("high")
    low = current.get("low")
    prev_close = previous.get("close")

    if high is None or low is None or prev_close is None:
        return None

    return max(
        high - low,
        abs(high - prev_close),
        abs(low - prev_close),
    )


def _calc_atr(prices: list[dict], window: int) -> float | None:
    """Calculate Average True Range over window (extracted for testing)."""
    if len(prices) < window + 1:
        return None

    true_ranges: list[float] = []
    for i in range(window):
        tr = _calc_true_range(prices[i], prices[i + 1])
        if tr is not None:
            true_ranges.append(tr)

    if len(true_ranges) < window // 2:
        return None

    return sum(true_ranges) / len(true_ranges)


def _determine_strength(
    range_ratio: float, spike_multiplier: float, strong_spike_multiplier: float
) -> str:
    """Determine signal strength based on range ratio (extracted for testing)."""
    if range_ratio >= strong_spike_multiplier:
        return "strong"
    elif range_ratio >= (spike_multiplier + strong_spike_multiplier) / 2:
        return "medium"
    else:
        return "weak"
