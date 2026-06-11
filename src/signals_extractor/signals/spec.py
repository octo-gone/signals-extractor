from signals_extractor.engine.spec import Spec, _dep
from signals_extractor.indicators import Indicators

SIGNALS_SPECS: dict[str, Spec] = {
    "roc_positive": Spec("roc_positive", depends=(_dep(Indicators.ROC, period="period"),)),
    "roc_negative": Spec("roc_negative", depends=(_dep(Indicators.ROC, period="period"),)),
    "cci_overbought": Spec("cci_overbought", depends=(_dep(Indicators.CCI, period="period"),)),
    "cci_oversold": Spec("cci_oversold", depends=(_dep(Indicators.CCI, period="period"),)),
    "momentum_positive": Spec("momentum_positive", depends=(_dep(Indicators.MOMENTUM, period="period"),)),
    "momentum_negative": Spec("momentum_negative", depends=(_dep(Indicators.MOMENTUM, period="period"),)),
    "price_above_sma": Spec("price_above_sma", ("close",), depends=(_dep(Indicators.SMA, period="period"),)),
    "price_below_sma": Spec("price_below_sma", ("close",), depends=(_dep(Indicators.SMA, period="period"),)),
    "sma_golden_cross": Spec(
        "sma_golden_cross",
        depends=(
            _dep(Indicators.SMA, period="short"),
            _dep(Indicators.SMA, period="long"),
        ),
    ),
    "sma_death_cross": Spec(
        "sma_death_cross",
        depends=(
            _dep(Indicators.SMA, period="short"),
            _dep(Indicators.SMA, period="long"),
        ),
    ),
    "ema_crossover": Spec(
        "ema_crossover",
        depends=(
            _dep(Indicators.EMA, period="short"),
            _dep(Indicators.EMA, period="long"),
        ),
    ),
    "macd_crossover_bullish": Spec(
        "macd_crossover_bullish",
        depends=(
            _dep(Indicators.MACD_LINE, short="short", long="long"),
            _dep(Indicators.MACD_SIGNAL, short="short", long="long", signal="signal"),
        ),
    ),
    "macd_crossover_bearish": Spec(
        "macd_crossover_bearish",
        depends=(
            _dep(Indicators.MACD_LINE, short="short", long="long"),
            _dep(Indicators.MACD_SIGNAL, short="short", long="long", signal="signal"),
        ),
    ),
    "macd_histogram_positive": Spec(
        "macd_histogram_positive",
        depends=(_dep(Indicators.MACD_HISTOGRAM, short="short", long="long", signal="signal"),),
    ),
    "macd_histogram_negative": Spec(
        "macd_histogram_negative",
        depends=(_dep(Indicators.MACD_HISTOGRAM, short="short", long="long", signal="signal"),),
    ),
    "macd_zero_cross_bullish": Spec(
        "macd_zero_cross_bullish",
        depends=(_dep(Indicators.MACD_LINE, short="short", long="long"),),
    ),
    "macd_zero_cross_bearish": Spec(
        "macd_zero_cross_bearish",
        depends=(_dep(Indicators.MACD_LINE, short="short", long="long"),),
    ),
    "macd_histogram_reversal_positive": Spec(
        "macd_histogram_reversal_positive",
        depends=(_dep(Indicators.MACD_HISTOGRAM, short="short", long="long", signal="signal"),),
    ),
    "macd_histogram_reversal_negative": Spec(
        "macd_histogram_reversal_negative",
        depends=(_dep(Indicators.MACD_HISTOGRAM, short="short", long="long", signal="signal"),),
    ),
    "adx_trend_strength": Spec("adx_trend_strength", depends=(_dep(Indicators.ADX, period="period"),)),
    "price_bounce_upper_bb": Spec(
        "price_bounce_upper_bb",
        ("close",),
        depends=(_dep(Indicators.BB_UPPER, period="period", std_dev="std_dev"),),
    ),
    "price_bounce_lower_bb": Spec(
        "price_bounce_lower_bb",
        ("close",),
        depends=(_dep(Indicators.BB_LOWER, period="period", std_dev="std_dev"),),
    ),
    "price_break_upper_bb": Spec(
        "price_break_upper_bb",
        ("close",),
        depends=(_dep(Indicators.BB_UPPER, period="period", std_dev="std_dev"),),
    ),
    "price_break_lower_bb": Spec(
        "price_break_lower_bb",
        ("close",),
        depends=(_dep(Indicators.BB_LOWER, period="period", std_dev="std_dev"),),
    ),
    "bb_width_breakout": Spec(
        "bb_width_breakout",
        depends=(_dep(Indicators.BB_WIDTH, period="period", std_dev="std_dev"),),
    ),
    "rsi_overbought": Spec("rsi_overbought", depends=(_dep(Indicators.RSI, period="period"),)),
    "rsi_oversold": Spec("rsi_oversold", depends=(_dep(Indicators.RSI, period="period"),)),
    "rsi_bearish_divergence": Spec(
        "rsi_bearish_divergence",
        ("close",),
        depends=(_dep(Indicators.RSI, period="period"),),
    ),
    "stoch_overbought": Spec(
        "stoch_overbought",
        depends=(_dep(Indicators.STOCH_K, k_period="k_period", d_period="d_period"),),
    ),
    "stoch_oversold": Spec(
        "stoch_oversold",
        depends=(_dep(Indicators.STOCH_K, k_period="k_period", d_period="d_period"),),
    ),
    "stoch_bullish_crossover": Spec(
        "stoch_bullish_crossover",
        depends=(
            _dep(Indicators.STOCH_K, k_period="k_period", d_period="d_period"),
            _dep(Indicators.STOCH_D, k_period="k_period", d_period="d_period"),
        ),
    ),
    "stoch_bearish_crossover": Spec(
        "stoch_bearish_crossover",
        depends=(
            _dep(Indicators.STOCH_K, k_period="k_period", d_period="d_period"),
            _dep(Indicators.STOCH_D, k_period="k_period", d_period="d_period"),
        ),
    ),
    "resistance_breakout": Spec(
        "resistance_breakout",
        ("close",),
        (_dep(Indicators.RESISTANCE_LEVEL, period="period"),),
    ),
    "support_breakout": Spec(
        "support_breakout",
        ("close",),
        (_dep(Indicators.SUPPORT_LEVEL, period="period"),),
    ),
    "key_resistance_breakout": Spec(
        "key_resistance_breakout",
        ("close",),
        (_dep(Indicators.KEY_RESISTANCE, window="window"),),
    ),
    "key_support_breakout": Spec(
        "key_support_breakout",
        ("close",),
        (_dep(Indicators.KEY_SUPPORT, window="window"),),
    ),
    "donchian_breakout_upper": Spec(
        "donchian_breakout_upper",
        ("close",),
        (_dep(Indicators.DONCHIAN_UPPER, period="period"),),
    ),
    "donchian_breakout_lower": Spec(
        "donchian_breakout_lower",
        ("close",),
        (_dep(Indicators.DONCHIAN_LOWER, period="period"),),
    ),
    "keltner_breakout_upper": Spec(
        "keltner_breakout_upper",
        ("close",),
        (_dep(Indicators.KELTNER_UPPER, period="period", multiplier="multiplier"),),
    ),
    "keltner_breakout_lower": Spec(
        "keltner_breakout_lower",
        ("close",),
        (_dep(Indicators.KELTNER_LOWER, period="period", multiplier="multiplier"),),
    ),
    "atr_breakout_up": Spec(
        "atr_breakout_up",
        ("close", "high"),
        (
            _dep(Indicators.ATR, period="period"),
            _dep(Indicators.DONCHIAN_UPPER, period="breakout_period"),
        ),
    ),
    "atr_breakout_down": Spec(
        "atr_breakout_down",
        ("close", "low"),
        (
            _dep(Indicators.ATR, period="period"),
            _dep(Indicators.DONCHIAN_LOWER, period="breakout_period"),
        ),
    ),
    "obv_positive_trend": Spec("obv_positive_trend", depends=(_dep(Indicators.OBV),)),
    "obv_negative_trend": Spec("obv_negative_trend", depends=(_dep(Indicators.OBV),)),
    "ad_positive": Spec("ad_positive", depends=(_dep(Indicators.ACCUMULATION_DISTRIBUTION),)),
    "ad_negative": Spec("ad_negative", depends=(_dep(Indicators.ACCUMULATION_DISTRIBUTION),)),
    "cmf_positive": Spec("cmf_positive", depends=(_dep(Indicators.CMF, period="period"),)),
    "cmf_negative": Spec("cmf_negative", depends=(_dep(Indicators.CMF, period="period"),)),
    "cmf_strong_positive": Spec("cmf_strong_positive", depends=(_dep(Indicators.CMF, period="period"),)),
    "cmf_strong_negative": Spec("cmf_strong_negative", depends=(_dep(Indicators.CMF, period="period"),)),
}
