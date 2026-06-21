from typing import Literal

from signals_extractor.signals._types import SignalType, signal_factory


class Signals:  # pylint: disable=too-many-public-methods,invalid-name
    @staticmethod
    @signal_factory("roc_positive")
    def ROC_POSITIVE(period: int) -> "SignalType":
        "Positive Rate of Change signal factory."
        return SignalType("roc_positive", period=period)

    @staticmethod
    @signal_factory("roc_negative")
    def ROC_NEGATIVE(period: int) -> "SignalType":
        "Negative Rate of Change signal factory."
        return SignalType("roc_negative", period=period)

    @staticmethod
    @signal_factory("cci_overbought")
    def CCI_OVERBOUGHT(period: int) -> "SignalType":
        "Overbought Commodity Channel Index signal factory."
        return SignalType("cci_overbought", period=period)

    @staticmethod
    @signal_factory("cci_oversold")
    def CCI_OVERSOLD(period: int) -> "SignalType":
        "Oversold Commodity Channel Index signal factory."
        return SignalType("cci_oversold", period=period)

    @staticmethod
    @signal_factory("momentum_positive")
    def MOMENTUM_POSITIVE(period: int) -> "SignalType":
        "Positive momentum oscillator signal factory."
        return SignalType("momentum_positive", period=period)

    @staticmethod
    @signal_factory("momentum_negative")
    def MOMENTUM_NEGATIVE(period: int) -> "SignalType":
        "Negative momentum oscillator signal factory."
        return SignalType("momentum_negative", period=period)

    @staticmethod
    @signal_factory("price_above_sma")
    def PRICE_ABOVE_SMA(period: int) -> "SignalType":
        "Price above Simple Moving Average signal factory."
        return SignalType("price_above_sma", period=period)

    @staticmethod
    @signal_factory("price_below_sma")
    def PRICE_BELOW_SMA(period: int) -> "SignalType":
        "Price below Simple Moving Average signal factory."
        return SignalType("price_below_sma", period=period)

    @staticmethod
    @signal_factory("sma_golden_cross")
    def SMA_GOLDEN_CROSS(short: int, long: int) -> "SignalType":
        "Simple Moving Average Golden Cross signal factory. Short line crosses long line from bottom."
        return SignalType("sma_golden_cross", short=short, long=long)

    @staticmethod
    @signal_factory("sma_death_cross")
    def SMA_DEATH_CROSS(short: int, long: int) -> "SignalType":
        "Simple Moving Average Death Cross signal factory. Short line crosses long line from top."
        return SignalType("sma_death_cross", short=short, long=long)

    @staticmethod
    @signal_factory("ema_golden_cross")
    def EMA_GOLDEN_CROSS(short: int, long: int) -> "SignalType":
        "Exponential Moving Average Golden Cross signal factory. Short line crosses long line from bottom."
        return SignalType("ema_golden_cross", short=short, long=long)

    @staticmethod
    @signal_factory("ema_death_cross")
    def EMA_DEATH_CROSS(short: int, long: int) -> "SignalType":
        "Exponential Moving Average Death Cross signal factory. Short line crosses long line from top."
        return SignalType("ema_death_cross", short=short, long=long)

    @staticmethod
    @signal_factory("macd_crossover_bullish")
    def MACD_CROSSOVER_BULLISH(short: int, long: int, signal: int) -> "SignalType":
        "MACD Bullish Crossover signal factory. MACD line crosses signal line from bottom."
        return SignalType("macd_crossover_bullish", short=short, long=long, signal=signal)

    @staticmethod
    @signal_factory("macd_crossover_bearish")
    def MACD_CROSSOVER_BEARISH(short: int, long: int, signal: int) -> "SignalType":
        "MACD Bullish Crossover signal factory. MACD line crosses signal line from top."
        return SignalType("macd_crossover_bearish", short=short, long=long, signal=signal)

    @staticmethod
    @signal_factory("macd_histogram_positive")
    def MACD_HISTOGRAM_POSITIVE(short: int, long: int, signal: int) -> "SignalType":
        "MACD Histogram Positive signal factory."
        return SignalType("macd_histogram_positive", short=short, long=long, signal=signal)

    @staticmethod
    @signal_factory("macd_histogram_negative")
    def MACD_HISTOGRAM_NEGATIVE(short: int, long: int, signal: int) -> "SignalType":
        "MACD Histogram Negative signal factory."
        return SignalType("macd_histogram_negative", short=short, long=long, signal=signal)

    @staticmethod
    @signal_factory("macd_zero_cross_bullish")
    def MACD_ZERO_CROSS_BULLISH(short: int, long: int) -> "SignalType":
        "MACD Zero Cross Bullish signal factory. MACD line crosses zero from bottom."
        return SignalType("macd_zero_cross_bullish", short=short, long=long)

    @staticmethod
    @signal_factory("macd_zero_cross_bearish")
    def MACD_ZERO_CROSS_BEARISH(short: int, long: int) -> "SignalType":
        "MACD Zero Cross Bearish signal factory. MACD line crosses zero from top."
        return SignalType("macd_zero_cross_bearish", short=short, long=long)

    @staticmethod
    @signal_factory("macd_histogram_reversal_positive")
    def MACD_HISTOGRAM_REVERSAL_POSITIVE(short: int, long: int, signal: int) -> "SignalType":
        "MACD Histogram Reversal Positive signal factory."
        return SignalType("macd_histogram_reversal_positive", short=short, long=long, signal=signal)

    @staticmethod
    @signal_factory("macd_histogram_reversal_negative")
    def MACD_HISTOGRAM_REVERSAL_NEGATIVE(short: int, long: int, signal: int) -> "SignalType":
        "MACD Histogram Reversal Negative signal factory."
        return SignalType("macd_histogram_reversal_negative", short=short, long=long, signal=signal)

    @staticmethod
    @signal_factory("adx_trend_strength")
    def ADX_TREND_STRENGTH(period: int, threshold: int) -> "SignalType":
        "ADX Trend Strength signal factory."
        return SignalType("adx_trend_strength", period=period, threshold=threshold)

    @staticmethod
    @signal_factory("bb_price_bounce_upper")
    def BB_PRICE_BOUNCE_UPPER(period: int = 20, std_dev: float = 2.0) -> "SignalType":
        "Upper Bollinger Band price bounce signal factory."
        return SignalType("bb_price_bounce_upper", period=period, std_dev=std_dev)

    @staticmethod
    @signal_factory("bb_price_bounce_lower")
    def BB_PRICE_BOUNCE_LOWER(period: int = 20, std_dev: float = 2.0) -> "SignalType":
        "Lower Bollinger Band price bounce signal factory."
        return SignalType("bb_price_bounce_lower", period=period, std_dev=std_dev)

    @staticmethod
    @signal_factory("bb_price_break_upper")
    def BB_PRICE_BREAK_UPPER(period: int = 20, std_dev: float = 2.0) -> "SignalType":
        "Upper Bollinger Band price break signal factory."
        return SignalType("bb_price_break_upper", period=period, std_dev=std_dev)

    @staticmethod
    @signal_factory("bb_price_break_lower")
    def BB_PRICE_BREAK_LOWER(period: int = 20, std_dev: float = 2.0) -> "SignalType":
        "Lower Bollinger Band price break signal factory."
        return SignalType("bb_price_break_lower", period=period, std_dev=std_dev)

    @staticmethod
    @signal_factory("bb_width_breakout")
    def BB_WIDTH_BREAKOUT(period: int = 20, std_dev: float = 2.0) -> "SignalType":
        "Bollinger Band width breakout signal factory."
        return SignalType("bb_width_breakout", period=period, std_dev=std_dev)

    @staticmethod
    @signal_factory("rsi_overbought")
    def RSI_OVERBOUGHT(period: int, threshold: int = 70) -> "SignalType":
        "Overbought RSI signal factory."
        return SignalType("rsi_overbought", period=period, threshold=threshold)

    @staticmethod
    @signal_factory("rsi_oversold")
    def RSI_OVERSOLD(period: int, threshold: int = 30) -> "SignalType":
        "Oversold RSI signal factory."
        return SignalType("rsi_oversold", period=period, threshold=threshold)

    @staticmethod
    @signal_factory("rsi_bullish_divergence")
    def RSI_BULLISH_DIVERGENCE(period: int) -> "SignalType":
        "Bullish RSI divergence signal factory."
        return SignalType("rsi_bullish_divergence", period=period)

    @staticmethod
    @signal_factory("rsi_bearish_divergence")
    def RSI_BEARISH_DIVERGENCE(period: int) -> "SignalType":
        "Bearish RSI divergence signal factory."
        return SignalType("rsi_bearish_divergence", period=period)

    @staticmethod
    @signal_factory("stoch_overbought")
    def STOCH_OVERBOUGHT(k_period: int = 14, d_period: int = 3, threshold: int = 80) -> "SignalType":
        "Overbought stochastic oscillator signal factory."
        return SignalType("stoch_overbought", k_period=k_period, d_period=d_period, threshold=threshold)

    @staticmethod
    @signal_factory("stoch_oversold")
    def STOCH_OVERSOLD(k_period: int = 14, d_period: int = 3, threshold: int = 20) -> "SignalType":
        "Oversold stochastic oscillator signal factory."
        return SignalType("stoch_oversold", k_period=k_period, d_period=d_period, threshold=threshold)

    @staticmethod
    @signal_factory("stoch_bullish_crossover")
    def STOCH_BULLISH_CROSSOVER(k_period: int = 14, d_period: int = 3) -> "SignalType":
        "Bullish stochastic crossover signal factory."
        return SignalType("stoch_bullish_crossover", k_period=k_period, d_period=d_period)

    @staticmethod
    @signal_factory("stoch_bearish_crossover")
    def STOCH_BEARISH_CROSSOVER(k_period: int = 14, d_period: int = 3) -> "SignalType":
        "Bearish stochastic crossover signal factory."
        return SignalType("stoch_bearish_crossover", k_period=k_period, d_period=d_period)

    @staticmethod
    @signal_factory("resistance_breakout")
    def RESISTANCE_BREAKOUT(period: int = 5) -> "SignalType":
        "Resistance breakout signal factory."
        return SignalType("resistance_breakout", period=period)

    @staticmethod
    @signal_factory("support_breakout")
    def SUPPORT_BREAKOUT(period: int = 5) -> "SignalType":
        "Support breakout signal factory."
        return SignalType("support_breakout", period=period)

    @staticmethod
    @signal_factory("key_resistance_breakout")
    def KEY_RESISTANCE_BREAKOUT(window: int = 5) -> "SignalType":
        "Key resistance breakout signal factory."
        return SignalType("key_resistance_breakout", window=window)

    @staticmethod
    @signal_factory("key_support_breakout")
    def KEY_SUPPORT_BREAKOUT(window: int = 5) -> "SignalType":
        "Key support breakout signal factory."
        return SignalType("key_support_breakout", window=window)

    @staticmethod
    @signal_factory("donchian_breakout_upper")
    def DONCHIAN_BREAKOUT_UPPER(period: int) -> "SignalType":
        "Upper Donchian breakout signal factory."
        return SignalType("donchian_breakout_upper", period=period)

    @staticmethod
    @signal_factory("donchian_breakout_lower")
    def DONCHIAN_BREAKOUT_LOWER(period: int) -> "SignalType":
        "Lower Donchian breakout signal factory."
        return SignalType("donchian_breakout_lower", period=period)

    @staticmethod
    @signal_factory("keltner_breakout_upper")
    def KELTNER_BREAKOUT_UPPER(period: int, multiplier: float = 2.0) -> "SignalType":
        "Upper Keltner breakout signal factory."
        return SignalType("keltner_breakout_upper", period=period, multiplier=multiplier)

    @staticmethod
    @signal_factory("keltner_breakout_lower")
    def KELTNER_BREAKOUT_LOWER(period: int, multiplier: float = 2.0) -> "SignalType":
        "Lower Keltner breakout signal factory."
        return SignalType("keltner_breakout_lower", period=period, multiplier=multiplier)

    @staticmethod
    @signal_factory("atr_breakout_up")
    def ATR_BREAKOUT_UP(
        period: int,
        breakout_period: int,
        calc: Literal["donchian", "previous"] = "donchian",
        multiplier: float = 0.5,
    ) -> "SignalType":
        "Upward ATR breakout signal factory."
        return SignalType(
            "atr_breakout_up", period=period, breakout_period=breakout_period, calc=calc, multiplier=multiplier
        )

    @staticmethod
    @signal_factory("atr_breakout_down")
    def ATR_BREAKOUT_DOWN(
        period: int,
        breakout_period: int,
        calc: Literal["donchian", "previous"] = "donchian",
        multiplier: float = 0.5,
    ) -> "SignalType":
        "Downward ATR breakout signal factory."
        return SignalType(
            "atr_breakout_down", period=period, breakout_period=breakout_period, calc=calc, multiplier=multiplier
        )

    @staticmethod
    @signal_factory("obv_positive_trend")
    def OBV_POSITIVE_TREND() -> "SignalType":
        "Positive OBV trend signal factory."
        return SignalType("obv_positive_trend")

    @staticmethod
    @signal_factory("obv_negative_trend")
    def OBV_NEGATIVE_TREND() -> "SignalType":
        "Negative OBV trend signal factory."
        return SignalType("obv_negative_trend")

    @staticmethod
    @signal_factory("ad_positive")
    def AD_POSITIVE() -> "SignalType":
        "Positive accumulation/distribution signal factory."
        return SignalType("ad_positive")

    @staticmethod
    @signal_factory("ad_negative")
    def AD_NEGATIVE() -> "SignalType":
        "Negative accumulation/distribution signal factory."
        return SignalType("ad_negative")

    @staticmethod
    @signal_factory("cmf_positive")
    def CMF_POSITIVE(period: int) -> "SignalType":
        "Positive CMF signal factory."
        return SignalType("cmf_positive", period=period)

    @staticmethod
    @signal_factory("cmf_negative")
    def CMF_NEGATIVE(period: int) -> "SignalType":
        "Negative CMF signal factory."
        return SignalType("cmf_negative", period=period)

    @staticmethod
    @signal_factory("cmf_strong_positive")
    def CMF_STRONG_POSITIVE(period: int, threshold: float = 0.2) -> "SignalType":
        "Strong positive CMF signal factory."
        return SignalType("cmf_strong_positive", period=period, threshold=threshold)

    @staticmethod
    @signal_factory("cmf_strong_negative")
    def CMF_STRONG_NEGATIVE(period: int, threshold: float = -0.2) -> "SignalType":
        "Strong negative CMF signal factory."
        return SignalType("cmf_strong_negative", period=period, threshold=threshold)


class SignalsCollection:
    """Collection of commonly used signal configurations."""

    ROC_POSITIVE_10 = Signals.ROC_POSITIVE(10)
    ROC_NEGATIVE_10 = Signals.ROC_NEGATIVE(10)
    CCI_OVERBOUGHT_20 = Signals.CCI_OVERBOUGHT(20)
    CCI_OVERSOLD_20 = Signals.CCI_OVERSOLD(20)
    MOMENTUM_POSITIVE_10 = Signals.MOMENTUM_POSITIVE(10)
    MOMENTUM_NEGATIVE_10 = Signals.MOMENTUM_NEGATIVE(10)
    PRICE_ABOVE_SMA_10 = Signals.PRICE_ABOVE_SMA(10)
    PRICE_ABOVE_SMA_50 = Signals.PRICE_ABOVE_SMA(50)
    PRICE_BELOW_SMA_10 = Signals.PRICE_BELOW_SMA(10)
    PRICE_BELOW_SMA_50 = Signals.PRICE_BELOW_SMA(50)
    SMA_GOLDEN_CROSS = Signals.SMA_GOLDEN_CROSS(20, 50)
    SMA_DEATH_CROSS = Signals.SMA_DEATH_CROSS(20, 50)
    EMA_GOLDEN_CROSS = Signals.EMA_GOLDEN_CROSS(12, 26)
    EMA_DEATH_CROSS = Signals.EMA_DEATH_CROSS(12, 26)
    MACD_CROSSOVER_BULLISH = Signals.MACD_CROSSOVER_BULLISH(12, 26, 9)
    MACD_CROSSOVER_BEARISH = Signals.MACD_CROSSOVER_BEARISH(12, 26, 9)
    MACD_HISTOGRAM_POSITIVE = Signals.MACD_HISTOGRAM_POSITIVE(12, 26, 9)
    MACD_HISTOGRAM_NEGATIVE = Signals.MACD_HISTOGRAM_NEGATIVE(12, 26, 9)
    MACD_ZERO_CROSS_BULLISH = Signals.MACD_ZERO_CROSS_BULLISH(12, 26)
    MACD_ZERO_CROSS_BEARISH = Signals.MACD_ZERO_CROSS_BEARISH(12, 26)
    ADX_TREND_STRENGTH_14 = Signals.ADX_TREND_STRENGTH(14, 20)
    BB_PRICE_BOUNCE_UPPER = Signals.BB_PRICE_BOUNCE_UPPER()
    BB_PRICE_BOUNCE_LOWER = Signals.BB_PRICE_BOUNCE_LOWER()
    BB_PRICE_BREAK_UPPER = Signals.BB_PRICE_BREAK_UPPER()
    BB_PRICE_BREAK_LOWER = Signals.BB_PRICE_BREAK_LOWER()
    BB_WIDTH_BREAKOUT = Signals.BB_WIDTH_BREAKOUT()
    RSI_OVERBOUGHT_14 = Signals.RSI_OVERBOUGHT(14, 70)
    RSI_OVERSOLD_14 = Signals.RSI_OVERSOLD(14, 30)
    RSI_BULLISH_DIVERGENCE_14 = Signals.RSI_BULLISH_DIVERGENCE(14)
    RSI_BEARISH_DIVERGENCE_14 = Signals.RSI_BEARISH_DIVERGENCE(14)
    STOCH_OVERBOUGHT = Signals.STOCH_OVERBOUGHT(14, 3, 80)
    STOCH_OVERSOLD = Signals.STOCH_OVERSOLD(14, 3, 20)
    STOCH_BULLISH_CROSSOVER = Signals.STOCH_BULLISH_CROSSOVER()
    STOCH_BEARISH_CROSSOVER = Signals.STOCH_BEARISH_CROSSOVER()
    OBV_POSITIVE_TREND = Signals.OBV_POSITIVE_TREND()
    OBV_NEGATIVE_TREND = Signals.OBV_NEGATIVE_TREND()
    CMF_POSITIVE_21 = Signals.CMF_POSITIVE(21)
    CMF_NEGATIVE_21 = Signals.CMF_NEGATIVE(21)
    CMF_STRONG_POSITIVE_21 = Signals.CMF_STRONG_POSITIVE(21, 0.2)
    CMF_STRONG_NEGATIVE_21 = Signals.CMF_STRONG_NEGATIVE(21, -0.2)
    ATR_BREAKOUT_UP_14_20 = Signals.ATR_BREAKOUT_UP(14, 20, calc="donchian", multiplier=0.5)
    ATR_BREAKOUT_DOWN_14_20 = Signals.ATR_BREAKOUT_DOWN(14, 20, calc="donchian", multiplier=0.5)
    RESISTANCE_BREAKOUT_5 = Signals.RESISTANCE_BREAKOUT(5)
    SUPPORT_BREAKOUT_5 = Signals.SUPPORT_BREAKOUT(5)
    KEY_RESISTANCE_BREAKOUT_5 = Signals.KEY_RESISTANCE_BREAKOUT(5)
    KEY_SUPPORT_BREAKOUT_5 = Signals.KEY_SUPPORT_BREAKOUT(5)
    DONCHIAN_BREAKOUT_UPPER_20 = Signals.DONCHIAN_BREAKOUT_UPPER(20)
    DONCHIAN_BREAKOUT_LOWER_20 = Signals.DONCHIAN_BREAKOUT_LOWER(20)
