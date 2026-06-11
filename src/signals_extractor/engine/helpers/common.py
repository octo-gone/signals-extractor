"""
Base helper functions.

Contains optimized numba functions for common technical indicators.
"""

import numpy as np
from numba import jit  # type: ignore


@jit(nopython=True, cache=True)  # type: ignore
def sma(values: np.ndarray, period: int) -> np.ndarray:
    """Numba-optimized Simple Moving Average."""
    n = len(values)
    result = np.full(n, np.nan)

    for i in range(period - 1, n):
        result[i] = np.mean(values[i - period + 1 : i + 1])

    return result


@jit(nopython=True, cache=True)  # type: ignore
def ema(values: np.ndarray, period: int) -> np.ndarray:
    """Numba-optimized Exponential Moving Average."""
    n = values.shape[0]
    out = np.empty(n, dtype=np.float64)
    out[:] = np.nan

    if n == 0:
        return out

    alpha = 2.0 / (period + 1.0)

    # Find first valid value
    start = -1
    for i in range(n):
        if not np.isnan(values[i]):
            start = i
            break

    if start == -1:
        return out  # all NaNs

    # Seed EMA with first valid value
    ema_prev = values[start]
    out[start] = ema_prev

    # EMA recursion
    for i in range(start + 1, n):
        v = values[i]

        if np.isnan(v):
            out[i] = ema_prev
        else:
            ema_prev = ema_prev + alpha * (v - ema_prev)
            out[i] = ema_prev

    return out


@jit(nopython=True, cache=True)  # type: ignore
def rsi(close: np.ndarray, period: int = 14) -> np.ndarray:
    """Numba-optimized Relative Strength Index."""
    n = len(close)
    rsi_result = np.full(n, np.nan)

    if n < period + 1:
        return rsi_result

    gains = np.zeros(n)
    losses = np.zeros(n)

    # Calculate price changes
    for i in range(1, n):
        change = close[i] - close[i - 1]
        gains[i] = max(change, 0)
        losses[i] = max(-change, 0)

    # Calculate initial averages
    avg_gain = np.mean(gains[1 : period + 1])
    avg_loss = np.mean(losses[1 : period + 1])

    if avg_loss == 0:
        rsi_result[period] = 100.0
    else:
        rs = avg_gain / avg_loss
        rsi_result[period] = 100.0 - (100.0 / (1.0 + rs))

    # Calculate subsequent values
    for i in range(period + 1, n):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

        if avg_loss == 0:
            rsi_result[i] = 100.0
        else:
            rs = avg_gain / avg_loss
            rsi_result[i] = 100.0 - (100.0 / (1.0 + rs))

    return rsi_result
