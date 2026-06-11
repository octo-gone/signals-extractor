"""
Breakout helper functions.

Contains optimized numba functions for breakout indicators.
"""

import numpy as np
from numba import jit  # type: ignore


@jit(nopython=True, cache=True)  # type: ignore
def find_pivot_points(high: np.ndarray, low: np.ndarray, period: int = 5) -> tuple[np.ndarray, np.ndarray]:
    """Find pivot points (local highs and lows)."""
    n = len(high)
    pivots_high = np.zeros(n)
    pivots_low = np.zeros(n)

    for i in range(period, n - period):
        # Check if current high is higher than surrounding highs
        is_pivot_high = True
        for j in range(i - period, i + period + 1):
            if j != i and high[j] >= high[i]:
                is_pivot_high = False
                break
        if is_pivot_high:
            pivots_high[i] = high[i]

        # Check if current low is lower than surrounding lows
        is_pivot_low = True
        for j in range(i - period, i + period + 1):
            if j != i and low[j] <= low[i]:
                is_pivot_low = False
                break
        if is_pivot_low:
            pivots_low[i] = low[i]

    return pivots_high, pivots_low


@jit(nopython=True, cache=True)  # type: ignore
def donchian_channel(high: np.ndarray, low: np.ndarray, period: int = 20) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate Donchian Channel."""
    n = len(high)
    upper = np.full(n, np.nan)
    lower = np.full(n, np.nan)
    middle = np.full(n, np.nan)

    for i in range(period - 1, n):
        window_high = high[i - period + 1 : i + 1]
        window_low = low[i - period + 1 : i + 1]

        upper[i] = np.max(window_high)
        lower[i] = np.min(window_low)
        middle[i] = (upper[i] + lower[i]) / 2

    return upper, middle, lower


@jit(nopython=True, cache=True)  # type: ignore
def atr(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14) -> np.ndarray:
    """Calculate Average True Range."""
    n = len(high)
    atr_result = np.full(n, np.nan)

    if n < period + 1:
        return atr_result

    # Calculate True Range
    tr = np.zeros(n)
    for i in range(1, n):
        tr[i] = max(high[i] - low[i], abs(high[i] - close[i - 1]), abs(low[i] - close[i - 1]))

    # Calculate ATR
    atr_result[period] = np.mean(tr[1 : period + 1])
    for i in range(period + 1, n):
        atr_result[i] = (atr_result[i - 1] * (period - 1) + tr[i]) / period

    return atr_result
