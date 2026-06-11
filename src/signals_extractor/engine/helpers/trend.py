"""
Trend helper functions.

Contains optimized numba functions for trend indicators.
"""

import numpy as np
from numba import jit  # type: ignore


@jit(nopython=True, cache=True)  # type: ignore
def adx(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14) -> np.ndarray:
    """Average Directional Index."""
    n = len(high)
    adx_result = np.full(n, np.nan)

    if n < period + 1:
        return adx_result

    # Calculate True Range
    tr = np.zeros(n)
    for i in range(1, n):
        tr[i] = max(high[i] - low[i], abs(high[i] - close[i - 1]), abs(low[i] - close[i - 1]))

    # Calculate Directional Movement
    dm_plus = np.zeros(n)
    dm_minus = np.zeros(n)

    for i in range(1, n):
        move_up = high[i] - high[i - 1]
        move_down = low[i - 1] - low[i]

        if move_up > move_down and move_up > 0:
            dm_plus[i] = move_up
        if move_down > move_up and move_down > 0:
            dm_minus[i] = move_down

    # Calculate smoothed averages
    atr = np.zeros(n)
    di_plus = np.zeros(n)
    di_minus = np.zeros(n)

    # Initialize first values
    atr[period] = np.mean(tr[1 : period + 1])
    di_plus[period] = 100 * np.mean(dm_plus[1 : period + 1]) / atr[period]
    di_minus[period] = 100 * np.mean(dm_minus[1 : period + 1]) / atr[period]

    # Calculate subsequent values
    for i in range(period + 1, n):
        atr[i] = (atr[i - 1] * (period - 1) + tr[i]) / period
        di_plus[i] = 100 * (di_plus[i - 1] * (period - 1) + dm_plus[i]) / (period * atr[i])
        di_minus[i] = 100 * (di_minus[i - 1] * (period - 1) + dm_minus[i]) / (period * atr[i])

        # Calculate DX and ADX
        dx = 100 * abs(di_plus[i] - di_minus[i]) / (di_plus[i] + di_minus[i])
        if i >= 2 * period - 1:
            if i == 2 * period - 1:
                # Calculate initial ADX as mean of first DX values
                dx_sum = 0.0
                for j in range(period, i + 1):
                    dx_val = 100 * abs(di_plus[j] - di_minus[j]) / (di_plus[j] + di_minus[j])
                    dx_sum += dx_val
                adx_result[i] = dx_sum / period
            else:
                adx_result[i] = (adx_result[i - 1] * (period - 1) + dx) / period

    return adx_result


@jit(nopython=True, cache=True)  # type: ignore
def bollinger_bands(
    close: np.ndarray, period: int = 20, std_dev: float = 2.0
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Bollinger Bands."""
    n = len(close)
    sma = np.full(n, np.nan)
    upper = np.full(n, np.nan)
    lower = np.full(n, np.nan)

    for i in range(period - 1, n):
        window = close[i - period + 1 : i + 1]
        mean = np.mean(window)
        std = np.std(window)

        sma[i] = mean
        upper[i] = mean + std_dev * std
        lower[i] = mean - std_dev * std

    return sma, upper, lower
