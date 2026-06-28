"""
Trend helper functions.

Contains optimized numba functions for trend indicators.
"""

import numpy as np
from numba import jit  # type: ignore


@jit(nopython=True, cache=True)  # type: ignore
def adx(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14) -> np.ndarray:
    """Average Directional Index (Wilder's method)."""
    n = len(high)
    adx_result = np.full(n, np.nan)

    if n < 2 * period:
        return adx_result

    tr = np.zeros(n)
    dm_plus = np.zeros(n)
    dm_minus = np.zeros(n)

    for i in range(1, n):
        up_move = high[i] - high[i - 1]
        down_move = low[i - 1] - low[i]

        tr[i] = max(
            high[i] - low[i],
            abs(high[i] - close[i - 1]),
            abs(low[i] - close[i - 1]),
        )

        if up_move > down_move and up_move > 0:
            dm_plus[i] = up_move

        if down_move > up_move and down_move > 0:
            dm_minus[i] = down_move

    atr = np.sum(tr[1 : period + 1])
    dm_plus_sm = np.sum(dm_plus[1 : period + 1])
    dm_minus_sm = np.sum(dm_minus[1 : period + 1])

    dx = np.full(n, np.nan)

    for i in range(period, n):
        if i > period:
            atr = atr - atr / period + tr[i]
            dm_plus_sm = dm_plus_sm - dm_plus_sm / period + dm_plus[i]
            dm_minus_sm = dm_minus_sm - dm_minus_sm / period + dm_minus[i]

        if atr == 0.0:
            continue

        di_plus = 100.0 * dm_plus_sm / atr
        di_minus = 100.0 * dm_minus_sm / atr

        denom = di_plus + di_minus
        if denom == 0.0:
            dx[i] = 0.0
        else:
            dx[i] = 100.0 * abs(di_plus - di_minus) / denom

    adx_start = 2 * period - 1
    adx_result[adx_start] = np.mean(dx[period : adx_start + 1])

    for i in range(adx_start + 1, n):
        adx_result[i] = ((adx_result[i - 1] * (period - 1)) + dx[i]) / period

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
