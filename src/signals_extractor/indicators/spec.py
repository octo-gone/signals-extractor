from signals_extractor.engine.spec import Spec, _dep
from signals_extractor.indicators import Indicators

INDICATORS_SPECS: dict[str, Spec] = {
    "roc": Spec("roc", ("close",)),
    "cci": Spec("cci", ("high", "low", "close")),
    "momentum": Spec("momentum", ("close",)),
    "sma": Spec("sma", ("close",)),
    "ema": Spec("ema", ("close",)),
    "macd_line": Spec(
        "macd_line",
        ("close",),
        (
            _dep(Indicators.EMA, period="short"),
            _dep(Indicators.EMA, period="long"),
        ),
    ),
    "macd_signal": Spec(
        "macd_signal",
        ("close",),
        (_dep(Indicators.MACD_LINE, short="short", long="long"),),
    ),
    "macd_histogram": Spec(
        "macd_histogram",
        ("close",),
        (
            _dep(Indicators.MACD_LINE, short="short", long="long"),
            _dep(Indicators.MACD_SIGNAL, short="short", long="long", signal="signal"),
        ),
    ),
    "adx": Spec("adx", ("high", "low", "close")),
    "bb_middle": Spec("bb_middle", ("close",)),
    "bb_upper": Spec("bb_upper", ("close",)),
    "bb_lower": Spec("bb_lower", ("close",)),
    "bb_width": Spec(
        "bb_width",
        ("close",),
        (
            _dep(Indicators.BB_UPPER, period="period", std_dev="std_dev"),
            _dep(Indicators.BB_LOWER, period="period", std_dev="std_dev"),
            _dep(Indicators.BB_MIDDLE, period="period", std_dev="std_dev"),
        ),
    ),
    "rsi": Spec("rsi", ("close",)),
    "stoch_k": Spec("stoch_k", ("high", "low", "close")),
    "stoch_d": Spec(
        "stoch_d",
        ("high", "low", "close"),
        (_dep(Indicators.STOCH_K, k_period="k_period", d_period="d_period"),),
    ),
    "resistance_level": Spec("resistance_level", ("high", "low")),
    "support_level": Spec("support_level", ("high", "low")),
    "key_resistance": Spec("key_resistance", ("close",)),
    "key_support": Spec("key_support", ("close",)),
    "donchian_upper": Spec("donchian_upper", ("high", "low")),
    "donchian_middle": Spec("donchian_middle", ("high", "low")),
    "donchian_lower": Spec("donchian_lower", ("high", "low")),
    "atr": Spec("atr", ("high", "low", "close")),
    "keltner_middle": Spec(
        "keltner_middle",
        ("close",),
        (_dep(Indicators.EMA, period="period"),),
    ),
    "keltner_upper": Spec(
        "keltner_upper",
        ("high", "low", "close"),
        (
            _dep(Indicators.KELTNER_MIDDLE, period="period"),
            _dep(Indicators.ATR, period="period"),
        ),
    ),
    "keltner_lower": Spec(
        "keltner_lower",
        ("high", "low", "close"),
        (
            _dep(Indicators.KELTNER_MIDDLE, period="period"),
            _dep(Indicators.ATR, period="period"),
        ),
    ),
    "obv": Spec("obv", ("close", "volume")),
    "accumulation_distribution": Spec("accumulation_distribution", ("high", "low", "close", "volume")),
    "cmf": Spec("cmf", ("high", "low", "close", "volume")),
    "candlestick_hammer": Spec("candlestick_hammer", ("open", "high", "low", "close")),
    "candlestick_hanging_man": Spec("candlestick_hanging_man", ("open", "high", "low", "close")),
    "candlestick_doji": Spec("candlestick_doji", ("open", "high", "low", "close")),
    "candlestick_engulfing_bullish": Spec("candlestick_engulfing_bullish", ("open", "high", "low", "close")),
    "candlestick_engulfing_bearish": Spec("candlestick_engulfing_bearish", ("open", "high", "low", "close")),
}
