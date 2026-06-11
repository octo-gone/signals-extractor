"""
Momentum helper functions.

Contains optimized numba functions for momentum indicators.
"""

import numpy as np
from numba import jit  # type: ignore


@jit(nopython=True, cache=True)  # type: ignore
def roc(close: np.ndarray, period: int = 10) -> np.ndarray:
    """Calculate Rate of Change."""
    n = len(close)
    roc_result = np.full(n, np.nan)

    for i in range(period, n):
        if close[i - period] != 0:
            roc_result[i] = 100 * (close[i] - close[i - period]) / close[i - period]

    return roc_result


@jit(nopython=True, cache=True)  # type: ignore
def cci(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 20) -> np.ndarray:
    """Calculate Commodity Channel Index."""
    n = len(close)
    cci_result = np.full(n, np.nan)

    for i in range(period - 1, n):
        # Calculate Typical Price
        tp = (high[i - period + 1 : i + 1] + low[i - period + 1 : i + 1] + close[i - period + 1 : i + 1]) / 3

        # Calculate SMA of TP
        sma_tp = np.mean(tp)

        # Calculate Mean Deviation
        mean_dev = np.mean(np.abs(tp - sma_tp))

        # Calculate CCI
        if mean_dev != 0:
            cci_result[i] = (tp[-1] - sma_tp) / (0.015 * mean_dev)

    return cci_result


@jit(nopython=True, cache=True)  # type: ignore
def momentum_oscillator(close: np.ndarray, period: int = 10) -> np.ndarray:
    """Calculate Momentum Oscillator."""
    n = len(close)
    momentum = np.full(n, np.nan)

    for i in range(period, n):
        momentum[i] = 100 * (close[i] / close[i - period] - 1)

    return momentum
