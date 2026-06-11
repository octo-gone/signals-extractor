"""
Reversal helper functions.

Contains optimized numba functions for reversal indicators.
"""

import numpy as np
from numba import jit  # type: ignore


# TODO: split k and d calc
@jit(nopython=True, cache=True)  # type: ignore
def stochastic(
    high: np.ndarray, low: np.ndarray, close: np.ndarray, k_period: int = 14, d_period: int = 3
) -> tuple[np.ndarray, np.ndarray]:
    """Stochastic Oscillator."""
    n = len(close)
    k = np.full(n, np.nan)
    d = np.full(n, np.nan)

    for i in range(k_period - 1, n):
        high_max = np.max(high[i - k_period + 1 : i + 1])
        low_min = np.min(low[i - k_period + 1 : i + 1])
        k[i] = 100 * (close[i] - low_min) / (high_max - low_min) if high_max != low_min else 50

    # Calculate %D (SMA of %K)
    for i in range(d_period - 1, n):
        d[i] = np.mean(k[i - d_period + 1 : i + 1])

    return k, d


# WIP: baseline patterns calculator
@jit(nopython=True, cache=True)  # type: ignore
def candlestick_patterns(
    open_price: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray
) -> dict[str, np.ndarray]:
    """Calculate basic candlestick patterns."""
    n = len(close)
    hammer = np.zeros(n)
    hanging_man = np.zeros(n)
    doji = np.zeros(n)
    engulfing_bullish = np.zeros(n)
    engulfing_bearish = np.zeros(n)

    for i in range(1, n):
        body = abs(close[i] - open_price[i])
        upper_wick = high[i] - max(open_price[i], close[i])
        lower_wick = min(open_price[i], close[i]) - low[i]
        total_range = high[i] - low[i]

        if total_range > 0:
            body_ratio = body / total_range

            # Hammer: small body, long lower wick (at least 2x body), small upper wick
            if lower_wick >= 2 * body and upper_wick <= 0.1 * total_range and body_ratio <= 0.3:
                # Bullish if in downtrend (simplified)
                if close[i] > open_price[i]:  # Green candle
                    hammer[i] = 1

            # Hanging Man: similar to hammer but in uptrend (simplified)
            if lower_wick >= 2 * body and upper_wick <= 0.1 * total_range and body_ratio <= 0.3:
                if close[i] < open_price[i]:  # Red candle
                    hanging_man[i] = 1

            # Doji: very small body relative to total range
            if body_ratio <= 0.05:
                doji[i] = 1

        # Bullish engulfing: current green candle completely engulfs previous red candle
        if (
            close[i] > open_price[i]  # Current is green
            and close[i - 1] < open_price[i - 1]  # Previous is red
            and open_price[i] <= close[i - 1]  # Current open <= previous close
            and close[i] >= open_price[i - 1]
        ):  # Current close >= previous open
            engulfing_bullish[i] = 1

        # Bearish engulfing: current red candle completely engulfs previous green candle
        if (
            close[i] < open_price[i]  # Current is red
            and close[i - 1] > open_price[i - 1]  # Previous is green
            and open_price[i] >= close[i - 1]  # Current open >= previous close
            and close[i] <= open_price[i - 1]
        ):  # Current close <= previous open
            engulfing_bearish[i] = 1

    return {
        "hammer": hammer,
        "hanging_man": hanging_man,
        "doji": doji,
        "engulfing_bullish": engulfing_bullish,
        "engulfing_bearish": engulfing_bearish,
    }
