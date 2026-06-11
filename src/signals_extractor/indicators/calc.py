from typing import TYPE_CHECKING

import numpy as np

from signals_extractor.engine.helpers.breakout import atr, donchian_channel, find_pivot_points
from signals_extractor.engine.helpers.common import ema, rsi, sma
from signals_extractor.engine.helpers.momentum import cci, momentum_oscillator, roc
from signals_extractor.engine.helpers.reversal import stochastic
from signals_extractor.engine.helpers.trend import adx, bollinger_bands
from signals_extractor.engine.helpers.volume import accumulation_distribution, chaikin_money_flow, obv
from signals_extractor.indicators._types import IndicatorType
from signals_extractor.indicators.indicators import Indicators

if TYPE_CHECKING:
    from signals_extractor.engine.context import BatchContext, IndicatorCalcFunc


def _compute_roc(ctx: BatchContext, ind: IndicatorType) -> np.ndarray:
    period = int(ind.params["period"])
    return ctx.set(ind, roc(ctx.data["close"], period))


def _compute_cci(ctx: BatchContext, ind: IndicatorType) -> np.ndarray:
    period = int(ind.params["period"])
    return ctx.set(ind, cci(ctx.data["high"], ctx.data["low"], ctx.data["close"], period))


def _compute_momentum(ctx: BatchContext, ind: IndicatorType) -> np.ndarray:
    period = int(ind.params["period"])
    return ctx.set(ind, momentum_oscillator(ctx.data["close"], period))


def _compute_sma(ctx: BatchContext, ind: IndicatorType) -> np.ndarray:
    period = int(ind.params["period"])
    return ctx.set(ind, sma(ctx.data["close"], period))


def _compute_ema(ctx: BatchContext, ind: IndicatorType) -> np.ndarray:
    period = int(ind.params["period"])
    return ctx.set(ind, ema(ctx.data["close"], period))


def _compute_macd_line(ctx: BatchContext, ind: IndicatorType) -> np.ndarray:
    short = int(ind.params["short"])
    long = int(ind.params["long"])
    ema_short = ctx.get(Indicators.EMA(short))
    ema_long = ctx.get(Indicators.EMA(long))
    return ctx.set(ind, ema_short - ema_long)


def _compute_macd_signal(ctx: BatchContext, ind: IndicatorType) -> np.ndarray:
    short = int(ind.params["short"])
    long = int(ind.params["long"])
    signal = int(ind.params["signal"])
    macd_line = ctx.get(Indicators.MACD_LINE(short, long))
    return ctx.set(ind, ema(macd_line, signal))


def _compute_macd_histogram(ctx: BatchContext, ind: IndicatorType) -> np.ndarray:
    short = int(ind.params["short"])
    long = int(ind.params["long"])
    signal = int(ind.params["signal"])
    macd_line = ctx.get(Indicators.MACD_LINE(short, long))
    signal_line = ctx.get(Indicators.MACD_SIGNAL(short, long, signal))
    return ctx.set(ind, macd_line - signal_line)


def _compute_adx(ctx: BatchContext, ind: IndicatorType) -> np.ndarray:
    period = int(ind.params["period"])
    return ctx.set(ind, adx(ctx.data["high"], ctx.data["low"], ctx.data["close"], period))


def _compute_bb(ctx: BatchContext, ind: IndicatorType) -> np.ndarray:
    period = int(ind.params.get("period", 20))
    std_dev = float(ind.params.get("std_dev", 2.0))
    middle, upper, lower = bollinger_bands(ctx.data["close"], period, std_dev)
    ctx.set(Indicators.BB_UPPER(period=period, std_dev=std_dev), upper)
    ctx.set(Indicators.BB_MIDDLE(period=period, std_dev=std_dev), middle)
    ctx.set(Indicators.BB_LOWER(period=period, std_dev=std_dev), lower)
    if ind.type == "bb_middle":
        return middle  # type: ignore
    if ind.type == "bb_upper":
        return upper  # type: ignore
    if ind.type == "bb_lower":
        return lower  # type: ignore
    raise ValueError(f"Unknown BB type: {ind.type}")


def _compute_bb_width(ctx: BatchContext, ind: IndicatorType) -> np.ndarray:
    period = int(ind.params.get("period", 20))
    std_dev = float(ind.params.get("std_dev", 2.0))
    upper = ctx.get(Indicators.BB_UPPER(period, std_dev))
    lower = ctx.get(Indicators.BB_LOWER(period, std_dev))
    middle = ctx.get(Indicators.BB_MIDDLE(period, std_dev))
    return ctx.set(ind, (upper - lower) / middle)


def _compute_rsi(ctx: BatchContext, ind: IndicatorType) -> np.ndarray:
    period = int(ind.params["period"])
    return ctx.set(ind, rsi(ctx.data["close"], period))


def _compute_stoch_k(ctx: BatchContext, ind: IndicatorType) -> np.ndarray:
    k_period = int(ind.params.get("k_period", 14))
    d_period = int(ind.params.get("d_period", 3))
    k, d = stochastic(ctx.data["high"], ctx.data["low"], ctx.data["close"], k_period, d_period)
    ctx.set(Indicators.STOCH_K(k_period=k_period, d_period=d_period), k)
    ctx.set(Indicators.STOCH_D(k_period=k_period, d_period=d_period), d)
    return k  # type: ignore


def _compute_stoch_d(ctx: BatchContext, ind: IndicatorType) -> np.ndarray:
    k_period = int(ind.params.get("k_period", 14))
    d_period = int(ind.params.get("d_period", 3))
    k, d = stochastic(ctx.data["high"], ctx.data["low"], ctx.data["close"], k_period, d_period)
    ctx.set(Indicators.STOCH_K(k_period=k_period, d_period=d_period), k)
    ctx.set(Indicators.STOCH_D(k_period=k_period, d_period=d_period), d)
    return d  # type: ignore


def _compute_pivot(ctx: BatchContext, ind: IndicatorType) -> np.ndarray:
    period = int(ind.params.get("period", 5))
    resistance, support = find_pivot_points(ctx.data["high"], ctx.data["low"], period)
    ctx.set(Indicators.RESISTANCE_LEVEL(period=period), resistance)
    ctx.set(Indicators.SUPPORT_LEVEL(period=period), support)
    if ind.type == "resistance_level":
        return resistance  # type: ignore
    return support  # type: ignore


def _compute_key_level(ctx: BatchContext, ind: IndicatorType) -> np.ndarray:
    close = ctx.data["close"]
    window = int(ind.params.get("window", 5))
    key_levels: list[tuple[float, float]] = []
    for i in range(window, len(close)):
        recent_high = np.max(close[i - window : i])
        recent_low = np.min(close[i - window : i])
        rounded_high = round(recent_high / 100) * 100
        rounded_low = round(recent_low / 100) * 100
        key_levels.append((rounded_high, rounded_low))
    key_levels.extend([(np.nan, np.nan)] * window)
    resistance = ctx.set(Indicators.KEY_RESISTANCE(window=window), np.array([level[0] for level in key_levels]))
    support = ctx.set(Indicators.KEY_SUPPORT(window=window), np.array([level[1] for level in key_levels]))
    if ind.type == "key_resistance":
        return resistance
    return support


def _compute_donchian(ctx: BatchContext, ind: IndicatorType) -> np.ndarray:
    period = int(ind.params["period"])
    upper, middle, lower = donchian_channel(ctx.data["high"], ctx.data["low"], period)
    ctx.set(Indicators.DONCHIAN_UPPER(period=period), upper)
    ctx.set(Indicators.DONCHIAN_MIDDLE(period=period), middle)
    ctx.set(Indicators.DONCHIAN_LOWER(period=period), lower)
    if ind.type == "donchian_upper":
        return upper  # type: ignore
    if ind.type == "donchian_middle":
        return middle  # type: ignore
    return lower  # type: ignore


def _compute_atr(ctx: BatchContext, ind: IndicatorType) -> np.ndarray:
    period = int(ind.params["period"])
    return ctx.set(ind, atr(ctx.data["high"], ctx.data["low"], ctx.data["close"], period))


def _compute_keltner_middle(ctx: BatchContext, ind: IndicatorType) -> np.ndarray:
    period = int(ind.params["period"])
    return ctx.set(ind, ctx.get(Indicators.EMA(period)))


def _compute_keltner_band(ctx: BatchContext, ind: IndicatorType) -> np.ndarray:
    period = int(ind.params["period"])
    multiplier = float(ind.params.get("multiplier", 2.0))
    middle = ctx.get(Indicators.KELTNER_MIDDLE(period))
    atr_values = ctx.get(Indicators.ATR(period))
    lower = ctx.set(Indicators.KELTNER_LOWER(period), middle - (atr_values * multiplier))
    upper = ctx.set(Indicators.KELTNER_UPPER(period), middle - (atr_values * multiplier))
    if ind.type == "keltner_upper":
        return upper
    return lower


def _compute_obv(ctx: BatchContext, ind: IndicatorType) -> np.ndarray:
    return ctx.set(ind, obv(ctx.data["close"], ctx.data["volume"]))


def _compute_ad(ctx: BatchContext, ind: IndicatorType) -> np.ndarray:
    return ctx.set(
        ind, accumulation_distribution(ctx.data["close"], ctx.data["high"], ctx.data["low"], ctx.data["volume"])
    )


def _compute_cmf(ctx: BatchContext, ind: IndicatorType) -> np.ndarray:
    period = int(ind.params["period"])
    return ctx.set(
        ind, chaikin_money_flow(ctx.data["close"], ctx.data["high"], ctx.data["low"], ctx.data["volume"], period)
    )


INDICATORS_CALCS: dict[str, IndicatorCalcFunc] = {
    "roc": _compute_roc,
    "cci": _compute_cci,
    "momentum": _compute_momentum,
    "sma": _compute_sma,
    "ema": _compute_ema,
    "macd_line": _compute_macd_line,
    "macd_signal": _compute_macd_signal,
    "macd_histogram": _compute_macd_histogram,
    "adx": _compute_adx,
    "bb_middle": _compute_bb,
    "bb_upper": _compute_bb,
    "bb_lower": _compute_bb,
    "bb_width": _compute_bb_width,
    "rsi": _compute_rsi,
    "stoch_k": _compute_stoch_k,
    "stoch_d": _compute_stoch_d,
    "resistance_level": _compute_pivot,
    "support_level": _compute_pivot,
    "key_resistance": _compute_key_level,
    "key_support": _compute_key_level,
    "donchian_upper": _compute_donchian,
    "donchian_middle": _compute_donchian,
    "donchian_lower": _compute_donchian,
    "atr": _compute_atr,
    "keltner_middle": _compute_keltner_middle,
    "keltner_upper": _compute_keltner_band,
    "keltner_lower": _compute_keltner_band,
    "obv": _compute_obv,
    "accumulation_distribution": _compute_ad,
    "cmf": _compute_cmf,
}
