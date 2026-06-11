"""
Volume helper functions.

Contains optimized numba functions for volume indicators.
"""

import numpy as np
from numba import jit  # type: ignore


@jit(nopython=True)  # type: ignore
def obv(close: np.ndarray, volume: np.ndarray) -> np.ndarray:
    """Calculate On-Balance Volume."""
    n = len(close)
    obv_result = np.zeros(n)
    obv_result[0] = volume[0]

    for i in range(1, n):
        if close[i] > close[i - 1]:
            obv_result[i] = obv_result[i - 1] + volume[i]
        elif close[i] < close[i - 1]:
            obv_result[i] = obv_result[i - 1] - volume[i]
        else:
            obv_result[i] = obv_result[i - 1]

    return obv_result


@jit(nopython=True)  # type: ignore
def accumulation_distribution(close: np.ndarray, high: np.ndarray, low: np.ndarray, volume: np.ndarray) -> np.ndarray:
    """Calculate Accumulation/Distribution Line."""
    n = len(close)
    ad = np.zeros(n)

    for i in range(n):
        if high[i] != low[i]:
            # Money Flow Multiplier
            mfm = ((close[i] - low[i]) - (high[i] - close[i])) / (high[i] - low[i])
            # Money Flow Volume
            mfv = mfm * volume[i]

            if i == 0:
                ad[i] = mfv
            else:
                ad[i] = ad[i - 1] + mfv

    return ad


@jit(nopython=True)  # type: ignore
def chaikin_money_flow(
    close: np.ndarray, high: np.ndarray, low: np.ndarray, volume: np.ndarray, period: int = 21
) -> np.ndarray:
    """Calculate Chaikin Money Flow."""
    n = len(close)
    cmf = np.full(n, np.nan)

    for i in range(period - 1, n):
        # Calculate Money Flow Volume for the period
        mfv_sum = 0.0
        volume_sum = 0.0

        for j in range(i - period + 1, i + 1):
            if high[j] != low[j]:
                mfm = ((close[j] - low[j]) - (high[j] - close[j])) / (high[j] - low[j])
                mfv = mfm * volume[j]
                mfv_sum += mfv
                volume_sum += volume[j]

        if volume_sum != 0:
            cmf[i] = mfv_sum / volume_sum

    return cmf
