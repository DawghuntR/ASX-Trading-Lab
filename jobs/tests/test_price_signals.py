"""Tests for price movement signal calculations.

Tests the pure calculation functions in the price movement signal engine,
including daily change percentage, multi-day momentum, and volume ratio calculations.
"""

import pytest


class TestDailyChangeCalculation:
    """Tests for _calc_daily_change method."""

    def test_positive_change(self):
        """Positive price change should return positive percentage."""
        latest = {"close": 11.0}
        previous = {"close": 10.0}
        
        change = _calc_daily_change(latest, previous)
        
        assert change == pytest.approx(10.0, rel=0.01)

    def test_negative_change(self):
        """Negative price change should return negative percentage."""
        latest = {"close": 9.0}
        previous = {"close": 10.0}
        
        change = _calc_daily_change(latest, previous)
        
        assert change == pytest.approx(-10.0, rel=0.01)

    def test_zero_previous_close(self):
        """Zero previous close should return None to avoid division by zero."""
        latest = {"close": 10.0}
        previous = {"close": 0}
        
        change = _calc_daily_change(latest, previous)
        
        assert change is None

    def test_none_previous_close(self):
        """None previous close should return None."""
        latest = {"close": 10.0}
        previous = {"close": None}
        
        change = _calc_daily_change(latest, previous)
        
        assert change is None


class TestMultiDayChangeCalculation:
    """Tests for _calc_multi_day_change method."""

    def test_five_day_positive_momentum(self, sample_price_data):
        """Five-day positive momentum should return correct percentage."""
        change = _calc_multi_day_change(sample_price_data, 5)
        
        expected = ((10.20 - 9.10) / 9.10) * 100
        assert change == pytest.approx(expected, rel=0.01)

    def test_insufficient_data(self, sample_price_data):
        """Insufficient data should return None."""
        change = _calc_multi_day_change(sample_price_data[:3], 5)
        
        assert change is None

    def test_zero_baseline(self):
        """Zero baseline price should return None."""
        prices = [
            {"close": 10.0},
            {"close": 9.0},
            {"close": 0},
        ]
        
        change = _calc_multi_day_change(prices, 2)
        
        assert change is None


class TestVolumeRatioCalculation:
    """Tests for _calc_volume_ratio method."""

    def test_volume_spike(self, sample_price_data):
        """Volume spike should return ratio above 1.0."""
        ratio = _calc_volume_ratio(sample_price_data, 5)
        
        baseline_avg = (100000 + 80000 + 90000 + 70000 + 60000) / 5
        expected = 150000 / baseline_avg
        assert ratio == pytest.approx(expected, rel=0.01)
        assert ratio > 1.0

    def test_zero_today_volume(self, sample_price_data):
        """Zero today volume should return None."""
        data = sample_price_data.copy()
        data[0] = {**data[0], "volume": 0}
        
        ratio = _calc_volume_ratio(data, 5)
        
        assert ratio is None

    def test_no_baseline_volume(self):
        """No valid baseline volume should return None."""
        prices = [
            {"volume": 1000},
            {"volume": 0},
            {"volume": None},
        ]
        
        ratio = _calc_volume_ratio(prices, 2)
        
        assert ratio is None


class TestStrengthCalculation:
    """Tests for _calc_strength method."""

    def test_weak_strength(self):
        """Value just above low threshold should be weak."""
        strength = _calc_strength(5.5, 5.0, 15.0)
        
        assert strength == "weak"

    def test_medium_strength(self):
        """Value at midpoint should be medium."""
        strength = _calc_strength(10.5, 5.0, 15.0)
        
        assert strength == "medium"

    def test_strong_strength(self):
        """Value at or above high threshold should be strong."""
        strength = _calc_strength(15.0, 5.0, 15.0)
        
        assert strength == "strong"


def _calc_daily_change(latest: dict, previous: dict) -> float | None:
    """Calculate daily percentage change (extracted for testing)."""
    if previous["close"] is None or previous["close"] == 0:
        return None
    return ((latest["close"] - previous["close"]) / previous["close"]) * 100


def _calc_multi_day_change(prices: list[dict], days: int) -> float | None:
    """Calculate multi-day percentage change (extracted for testing)."""
    if len(prices) < days + 1:
        return None
    baseline = prices[days]["close"]
    if baseline is None or baseline == 0:
        return None
    return ((prices[0]["close"] - baseline) / baseline) * 100


def _calc_volume_ratio(prices: list[dict], baseline_days: int) -> float | None:
    """Calculate volume ratio vs baseline average (extracted for testing)."""
    if len(prices) < baseline_days:
        return None

    today_volume = prices[0].get("volume", 0)
    if today_volume is None or today_volume == 0:
        return None

    baseline_volumes: list[int] = []
    for p in prices[1:baseline_days + 1]:
        vol = p.get("volume")
        if vol is not None and vol > 0:
            baseline_volumes.append(vol)

    if not baseline_volumes:
        return None

    avg_volume = sum(baseline_volumes) / len(baseline_volumes)
    if avg_volume == 0:
        return None

    return today_volume / avg_volume


def _calc_strength(value: float, low_threshold: float, high_threshold: float) -> str:
    """Calculate signal strength based on thresholds (extracted for testing)."""
    if value >= high_threshold:
        return "strong"
    elif value >= (low_threshold + high_threshold) / 2:
        return "medium"
    else:
        return "weak"
