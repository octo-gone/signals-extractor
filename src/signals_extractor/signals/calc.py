from typing import TYPE_CHECKING

import numpy as np

from signals_extractor.signals.spec import SIGNALS_SPECS
from signals_extractor.utils import roll

if TYPE_CHECKING:
    from signals_extractor.engine.context import BatchContext, SignalCalcFunc
    from signals_extractor.signals import SignalType


def _deps(ctx: BatchContext, signal: SignalType) -> list[np.ndarray]:
    return [ctx.get(dep) for dep in SIGNALS_SPECS[signal.type].resolve(signal)]


def _derive_roc_positive(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    roc_values = _deps(ctx, signal)[0]
    return ctx.set(signal, (roc_values > 0).astype(int))


def _derive_roc_negative(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    roc_values = _deps(ctx, signal)[0]
    return ctx.set(signal, (roc_values < 0).astype(int))


def _derive_cci_overbought(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    cci_values = _deps(ctx, signal)[0]
    return ctx.set(signal, (cci_values > 100).astype(int))


def _derive_cci_oversold(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    cci_values = _deps(ctx, signal)[0]
    return ctx.set(signal, (cci_values < -100).astype(int))


def _derive_momentum_positive(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    momentum_values = _deps(ctx, signal)[0]
    return ctx.set(signal, (momentum_values > 0).astype(int))


def _derive_momentum_negative(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    momentum_values = _deps(ctx, signal)[0]
    return ctx.set(signal, (momentum_values < 0).astype(int))


def _derive_price_above_sma(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    sma_values = _deps(ctx, signal)[0]
    return ctx.set(signal, (ctx.data["close"] > sma_values).astype(int))


def _derive_price_below_sma(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    sma_values = _deps(ctx, signal)[0]
    return ctx.set(signal, (ctx.data["close"] < sma_values).astype(int))


def _derive_sma_golden_cross(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    ma_short, ma_long = _deps(ctx, signal)
    return ctx.set(signal, ((ma_short > ma_long) & (roll(ma_short, 1) <= roll(ma_long, 1))).astype(int))


def _derive_sma_death_cross(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    ma_short, ma_long = _deps(ctx, signal)
    return ctx.set(signal, ((ma_short < ma_long) & (roll(ma_short, 1) >= roll(ma_long, 1))).astype(int))


def _derive_ema_crossover(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    ema_short, ema_long = _deps(ctx, signal)
    return ctx.set(signal, ((ema_short > ema_long) & (roll(ema_short, 1) <= roll(ema_long, 1))).astype(int))


def _derive_macd_crossover_bullish(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    macd_line, signal_line = _deps(ctx, signal)
    return ctx.set(signal, ((macd_line > signal_line) & (roll(macd_line, 1) <= roll(signal_line, 1))).astype(int))


def _derive_macd_crossover_bearish(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    macd_line, signal_line = _deps(ctx, signal)
    return ctx.set(signal, ((macd_line < signal_line) & (roll(macd_line, 1) >= roll(signal_line, 1))).astype(int))


def _derive_macd_histogram_positive(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    histogram = _deps(ctx, signal)[0]
    return ctx.set(signal, ((histogram > 0) & (roll(histogram, 1) <= 0)).astype(int))


def _derive_macd_histogram_negative(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    histogram = _deps(ctx, signal)[0]
    return ctx.set(signal, ((histogram < 0) & (roll(histogram, 1) >= 0)).astype(int))


def _derive_macd_zero_cross_bullish(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    macd_line = _deps(ctx, signal)[0]
    return ctx.set(signal, ((macd_line > 0) & (roll(macd_line, 1) <= 0)).astype(int))


def _derive_macd_zero_cross_bearish(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    macd_line = _deps(ctx, signal)[0]
    return ctx.set(signal, ((macd_line < 0) & (roll(macd_line, 1) >= 0)).astype(int))


def _derive_macd_histogram_reversal_positive(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    histogram = _deps(ctx, signal)[0]
    return ctx.set(
        signal,
        ((histogram > roll(histogram, 1)) & (roll(histogram, 1) < roll(histogram, 2)) & (histogram > 0)).astype(int),
    )


def _derive_macd_histogram_reversal_negative(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    histogram = _deps(ctx, signal)[0]
    return ctx.set(
        signal,
        ((histogram < roll(histogram, 1)) & (roll(histogram, 1) > roll(histogram, 2)) & (histogram < 0)).astype(int),
    )


def _derive_adx_trend_strength(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    adx_values = _deps(ctx, signal)[0]
    threshold = int(signal.params["threshold"])
    return ctx.set(signal, (adx_values > threshold).astype(int))


def _derive_price_bounce_upper_bb(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    upper = _deps(ctx, signal)[0]
    close = ctx.data["close"]
    return ctx.set(signal, ((close >= upper) & (roll(close, 1) < roll(upper, 1))).astype(int))


def _derive_price_bounce_lower_bb(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    lower = _deps(ctx, signal)[0]
    close = ctx.data["close"]
    return ctx.set(signal, ((close <= lower) & (roll(close, 1) > roll(lower, 1))).astype(int))


def _derive_price_break_upper_bb(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    upper = _deps(ctx, signal)[0]
    return ctx.set(signal, (ctx.data["close"] > upper).astype(int))


def _derive_price_break_lower_bb(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    lower = _deps(ctx, signal)[0]
    return ctx.set(signal, (ctx.data["close"] < lower).astype(int))


def _derive_bb_width_breakout(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    width = _deps(ctx, signal)[0]
    return ctx.set(signal, (width > roll(width, 1)).astype(int))


def _derive_rsi_overbought(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    rsi_values = _deps(ctx, signal)[0]
    threshold = int(signal.params.get("threshold", 70))
    return ctx.set(signal, (rsi_values > threshold).astype(int))


def _derive_rsi_oversold(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    rsi_values = _deps(ctx, signal)[0]
    threshold = int(signal.params.get("threshold", 30))
    return ctx.set(signal, (rsi_values < threshold).astype(int))


def _derive_rsi_bearish_divergence(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    rsi_values = _deps(ctx, signal)[0]
    close = ctx.data["close"]
    price_highs = np.maximum.accumulate(close)
    rsi_highs = np.maximum.accumulate(rsi_values)
    return ctx.set(signal, ((close == price_highs) & (rsi_values < rsi_highs)).astype(int))


def _derive_stoch_overbought(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    k = _deps(ctx, signal)[0]
    threshold = int(signal.params.get("threshold", 80))
    return ctx.set(signal, (k > threshold).astype(int))


def _derive_stoch_oversold(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    k = _deps(ctx, signal)[0]
    threshold = int(signal.params.get("threshold", 20))
    return ctx.set(signal, (k < threshold).astype(int))


def _derive_stoch_bullish_crossover(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    k, d = _deps(ctx, signal)
    return ctx.set(signal, ((k > d) & (roll(k, 1) <= roll(d, 1))).astype(int))


def _derive_stoch_bearish_crossover(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    k, d = _deps(ctx, signal)
    return ctx.set(signal, ((k < d) & (roll(k, 1) >= roll(d, 1))).astype(int))


def _derive_resistance_breakout(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    resistance = _deps(ctx, signal)[0]
    return ctx.set(signal, (ctx.data["close"] > resistance).astype(int))


def _derive_support_breakout(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    support = _deps(ctx, signal)[0]
    return ctx.set(signal, (ctx.data["close"] < support).astype(int))


def _derive_key_resistance_breakout(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    key_resistance = _deps(ctx, signal)[0]
    return ctx.set(signal, (ctx.data["close"] > key_resistance).astype(int))


def _derive_key_support_breakout(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    key_support = _deps(ctx, signal)[0]
    return ctx.set(signal, (ctx.data["close"] < key_support).astype(int))


def _derive_donchian_breakout_upper(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    dc_upper = _deps(ctx, signal)[0]
    return ctx.set(signal, (ctx.data["close"] > dc_upper).astype(int))


def _derive_donchian_breakout_lower(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    dc_lower = _deps(ctx, signal)[0]
    return ctx.set(signal, (ctx.data["close"] < dc_lower).astype(int))


def _derive_keltner_breakout_upper(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    kc_upper = _deps(ctx, signal)[0]
    return ctx.set(signal, (ctx.data["close"] > kc_upper).astype(int))


def _derive_keltner_breakout_lower(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    kc_lower = _deps(ctx, signal)[0]
    return ctx.set(signal, (ctx.data["close"] < kc_lower).astype(int))


def _derive_atr_breakout_up(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    atr_values, level = _deps(ctx, signal)
    multiplier = float(signal.params.get("multiplier", 0.5))
    calc = signal.params.get("calc", "donchian")
    if calc == "donchian":
        resistance = level
    else:
        resistance = roll(ctx.data["high"], 1)
    return ctx.set(signal, (ctx.data["close"] > (resistance + atr_values * multiplier)).astype(int))


def _derive_atr_breakout_down(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    atr_values, level = _deps(ctx, signal)
    multiplier = float(signal.params.get("multiplier", 0.5))
    calc = signal.params.get("calc", "donchian")
    if calc == "donchian":
        support = level
    else:
        support = roll(ctx.data["low"], 1)
    return ctx.set(signal, (ctx.data["close"] < (support - atr_values * multiplier)).astype(int))


def _derive_obv_positive_trend(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    obv_values = _deps(ctx, signal)[0]
    return ctx.set(signal, (obv_values > roll(obv_values, 1)).astype(int))


def _derive_obv_negative_trend(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    obv_values = _deps(ctx, signal)[0]
    return ctx.set(signal, (obv_values < roll(obv_values, 1)).astype(int))


def _derive_ad_positive(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    ad_values = _deps(ctx, signal)[0]
    return ctx.set(signal, (ad_values > roll(ad_values, 1)).astype(int))


def _derive_ad_negative(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    ad_values = _deps(ctx, signal)[0]
    return ctx.set(signal, (ad_values < roll(ad_values, 1)).astype(int))


def _derive_cmf_positive(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    cmf_values = _deps(ctx, signal)[0]
    return ctx.set(signal, (cmf_values > 0).astype(int))


def _derive_cmf_negative(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    cmf_values = _deps(ctx, signal)[0]
    return ctx.set(signal, (cmf_values < 0).astype(int))


def _derive_cmf_strong_positive(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    threshold = float(signal.params.get("threshold", 0.2))
    return ctx.set(signal, (_deps(ctx, signal)[0] > threshold).astype(int))


def _derive_cmf_strong_negative(ctx: BatchContext, signal: SignalType) -> np.ndarray:
    threshold = float(signal.params.get("threshold", -0.2))
    return ctx.set(signal, (_deps(ctx, signal)[0] < threshold).astype(int))


SIGNALS_CALCS: dict[str, SignalCalcFunc] = {
    "roc_positive": _derive_roc_positive,
    "roc_negative": _derive_roc_negative,
    "cci_overbought": _derive_cci_overbought,
    "cci_oversold": _derive_cci_oversold,
    "momentum_positive": _derive_momentum_positive,
    "momentum_negative": _derive_momentum_negative,
    "price_above_sma": _derive_price_above_sma,
    "price_below_sma": _derive_price_below_sma,
    "sma_golden_cross": _derive_sma_golden_cross,
    "sma_death_cross": _derive_sma_death_cross,
    "ema_crossover": _derive_ema_crossover,
    "macd_crossover_bullish": _derive_macd_crossover_bullish,
    "macd_crossover_bearish": _derive_macd_crossover_bearish,
    "macd_histogram_positive": _derive_macd_histogram_positive,
    "macd_histogram_negative": _derive_macd_histogram_negative,
    "macd_zero_cross_bullish": _derive_macd_zero_cross_bullish,
    "macd_zero_cross_bearish": _derive_macd_zero_cross_bearish,
    "macd_histogram_reversal_positive": _derive_macd_histogram_reversal_positive,
    "macd_histogram_reversal_negative": _derive_macd_histogram_reversal_negative,
    "adx_trend_strength": _derive_adx_trend_strength,
    "price_bounce_upper_bb": _derive_price_bounce_upper_bb,
    "price_bounce_lower_bb": _derive_price_bounce_lower_bb,
    "price_break_upper_bb": _derive_price_break_upper_bb,
    "price_break_lower_bb": _derive_price_break_lower_bb,
    "bb_width_breakout": _derive_bb_width_breakout,
    "rsi_overbought": _derive_rsi_overbought,
    "rsi_oversold": _derive_rsi_oversold,
    "rsi_bearish_divergence": _derive_rsi_bearish_divergence,
    "stoch_overbought": _derive_stoch_overbought,
    "stoch_oversold": _derive_stoch_oversold,
    "stoch_bullish_crossover": _derive_stoch_bullish_crossover,
    "stoch_bearish_crossover": _derive_stoch_bearish_crossover,
    "resistance_breakout": _derive_resistance_breakout,
    "support_breakout": _derive_support_breakout,
    "key_resistance_breakout": _derive_key_resistance_breakout,
    "key_support_breakout": _derive_key_support_breakout,
    "donchian_breakout_upper": _derive_donchian_breakout_upper,
    "donchian_breakout_lower": _derive_donchian_breakout_lower,
    "keltner_breakout_upper": _derive_keltner_breakout_upper,
    "keltner_breakout_lower": _derive_keltner_breakout_lower,
    "atr_breakout_up": _derive_atr_breakout_up,
    "atr_breakout_down": _derive_atr_breakout_down,
    "obv_positive_trend": _derive_obv_positive_trend,
    "obv_negative_trend": _derive_obv_negative_trend,
    "ad_positive": _derive_ad_positive,
    "ad_negative": _derive_ad_negative,
    "cmf_positive": _derive_cmf_positive,
    "cmf_negative": _derive_cmf_negative,
    "cmf_strong_positive": _derive_cmf_strong_positive,
    "cmf_strong_negative": _derive_cmf_strong_negative,
}
