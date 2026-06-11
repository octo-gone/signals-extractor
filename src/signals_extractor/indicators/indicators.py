from signals_extractor.indicators._types import IndicatorType, indicator_factory


class Indicators:  # pylint: disable=too-many-public-methods,invalid-name
    @staticmethod
    @indicator_factory("roc")
    def ROC(period: int) -> "IndicatorType":
        "Rate of Change indicator factory."
        return IndicatorType("roc", period=period)

    @staticmethod
    @indicator_factory("cci")
    def CCI(period: int) -> "IndicatorType":
        "Commodity Channel Index indicator factory."
        return IndicatorType("cci", period=period)

    @staticmethod
    @indicator_factory("momentum")
    def MOMENTUM(period: int) -> "IndicatorType":
        "Momentum oscillator indicator factory."
        return IndicatorType("momentum", period=period)

    @staticmethod
    @indicator_factory("sma")
    def SMA(period: int) -> "IndicatorType":
        "Simple Moving Average indicator factory."
        return IndicatorType("sma", period=period)

    @staticmethod
    @indicator_factory("ema")
    def EMA(period: int) -> "IndicatorType":
        "Exponential Moving Average indicator factory."
        return IndicatorType("ema", period=period)

    @staticmethod
    @indicator_factory("macd_line")
    def MACD_LINE(short: int, long: int) -> "IndicatorType":
        "Moving Average Convergence Divergence line indicator factory."
        return IndicatorType("macd_line", short=short, long=long)

    @staticmethod
    @indicator_factory("macd_signal")
    def MACD_SIGNAL(short: int, long: int, signal: int) -> "IndicatorType":
        "Moving Average Convergence Divergence signal line indicator factory."
        return IndicatorType("macd_signal", short=short, long=long, signal=signal)

    @staticmethod
    @indicator_factory("macd_histogram")
    def MACD_HISTOGRAM(short: int, long: int, signal: int) -> "IndicatorType":
        "Moving Average Convergence Divergence histogram indicator factory."
        return IndicatorType("macd_histogram", short=short, long=long, signal=signal)

    @staticmethod
    @indicator_factory("adx")
    def ADX(period: int) -> "IndicatorType":
        "Average Directional Index indicator factory."
        return IndicatorType("adx", period=period)

    @staticmethod
    @indicator_factory("bb_upper")
    def BB_UPPER(period: int = 20, std_dev: float = 2.0) -> "IndicatorType":
        "Bollinger Band Upper indicator factory."
        return IndicatorType("bb_upper", period=period, std_dev=std_dev)

    @staticmethod
    @indicator_factory("bb_middle")
    def BB_MIDDLE(period: int = 20, std_dev: float = 2.0) -> "IndicatorType":
        "Bollinger Band Middle indicator factory."
        return IndicatorType("bb_middle", period=period, std_dev=std_dev)

    @staticmethod
    @indicator_factory("bb_lower")
    def BB_LOWER(period: int = 20, std_dev: float = 2.0) -> "IndicatorType":
        "Bollinger Band Lower indicator factory."
        return IndicatorType("bb_lower", period=period, std_dev=std_dev)

    @staticmethod
    @indicator_factory("bb_width")
    def BB_WIDTH(period: int = 20, std_dev: float = 2.0) -> "IndicatorType":
        "Bollinger Band Width indicator factory."
        return IndicatorType("bb_width", period=period, std_dev=std_dev)

    @staticmethod
    @indicator_factory("rsi")
    def RSI(period: int) -> "IndicatorType":
        "Relative Strength Index indicator factory."
        return IndicatorType("rsi", period=period)

    @staticmethod
    @indicator_factory("stoch_k")
    def STOCH_K(k_period: int = 14, d_period: int = 3) -> "IndicatorType":
        "Stochastic %K indicator factory."
        return IndicatorType("stoch_k", k_period=k_period, d_period=d_period)

    @staticmethod
    @indicator_factory("stoch_d")
    def STOCH_D(k_period: int = 14, d_period: int = 3) -> "IndicatorType":
        "Stochastic %D indicator factory."
        return IndicatorType("stoch_d", k_period=k_period, d_period=d_period)

    @staticmethod
    @indicator_factory("resistance_level")
    def RESISTANCE_LEVEL(period: int = 5) -> "IndicatorType":
        "Resistance Level indicator factory."
        return IndicatorType("resistance_level", period=period)

    @staticmethod
    @indicator_factory("support_level")
    def SUPPORT_LEVEL(period: int = 5) -> "IndicatorType":
        "Support Level indicator factory."
        return IndicatorType("support_level", period=period)

    @staticmethod
    @indicator_factory("key_resistance")
    def KEY_RESISTANCE(window: int = 5) -> "IndicatorType":
        "Key Resistance indicator factory."
        return IndicatorType("key_resistance", window=window)

    @staticmethod
    @indicator_factory("key_support")
    def KEY_SUPPORT(window: int = 5) -> "IndicatorType":
        "Key Support indicator factory."
        return IndicatorType("key_support", window=window)

    @staticmethod
    @indicator_factory("donchian_upper")
    def DONCHIAN_UPPER(period: int) -> "IndicatorType":
        "Donchian Channel Upper indicator factory."
        return IndicatorType("donchian_upper", period=period)

    @staticmethod
    @indicator_factory("donchian_middle")
    def DONCHIAN_MIDDLE(period: int) -> "IndicatorType":
        "Donchian Channel Middle indicator factory."
        return IndicatorType("donchian_middle", period=period)

    @staticmethod
    @indicator_factory("donchian_lower")
    def DONCHIAN_LOWER(period: int) -> "IndicatorType":
        "Donchian Channel Lower indicator factory."
        return IndicatorType("donchian_lower", period=period)

    @staticmethod
    @indicator_factory("keltner_upper")
    def KELTNER_UPPER(period: int, multiplier: float = 2.0) -> "IndicatorType":
        "Keltner Channel Upper indicator factory."
        return IndicatorType("keltner_upper", period=period, multiplier=multiplier)

    @staticmethod
    @indicator_factory("keltner_middle")
    def KELTNER_MIDDLE(period: int) -> "IndicatorType":
        "Keltner Channel Middle indicator factory."
        return IndicatorType("keltner_middle", period=period)

    @staticmethod
    @indicator_factory("keltner_lower")
    def KELTNER_LOWER(period: int, multiplier: float = 2.0) -> "IndicatorType":
        "Keltner Channel Lower indicator factory."
        return IndicatorType("keltner_lower", period=period, multiplier=multiplier)

    @staticmethod
    @indicator_factory("atr")
    def ATR(period: int) -> "IndicatorType":
        "Average True Range indicator factory."
        return IndicatorType("atr", period=period)

    @staticmethod
    @indicator_factory("obv")
    def OBV() -> "IndicatorType":
        "On-Balance Volume indicator factory."
        return IndicatorType("obv")

    @staticmethod
    @indicator_factory("accumulation_distribution")
    def ACCUMULATION_DISTRIBUTION() -> "IndicatorType":
        "Accumulation/Distribution indicator factory."
        return IndicatorType("accumulation_distribution")

    @staticmethod
    @indicator_factory("cmf")
    def CMF(period: int) -> "IndicatorType":
        "Chaikin Money Flow indicator factory."
        return IndicatorType("cmf", period=period)


class IndicatorsCollection:
    """Collection of commonly used indicator configurations."""

    ROC_10 = Indicators.ROC(10)
    CCI_20 = Indicators.CCI(20)
    MOMENTUM_10 = Indicators.MOMENTUM(10)
    SMA_10 = Indicators.SMA(10)
    SMA_50 = Indicators.SMA(50)
    EMA_12 = Indicators.EMA(12)
    EMA_26 = Indicators.EMA(26)
    MACD_LINE = Indicators.MACD_LINE(12, 26)
    MACD_SIGNAL = Indicators.MACD_SIGNAL(12, 26, 9)
    MACD_HISTOGRAM = Indicators.MACD_HISTOGRAM(12, 26, 9)
    ADX_14 = Indicators.ADX(14)
    BB_MIDDLE = Indicators.BB_MIDDLE()
    BB_UPPER = Indicators.BB_UPPER()
    BB_LOWER = Indicators.BB_LOWER()
    BB_WIDTH = Indicators.BB_WIDTH()
    RSI_14 = Indicators.RSI(14)
    STOCH_K = Indicators.STOCH_K()
    STOCH_D = Indicators.STOCH_D()
    OBV = Indicators.OBV()
    ACCUMULATION_DISTRIBUTION = Indicators.ACCUMULATION_DISTRIBUTION()
    CMF_21 = Indicators.CMF(21)
    ATR_14 = Indicators.ATR(14)
    DONCHIAN_UPPER_20 = Indicators.DONCHIAN_UPPER(20)
    DONCHIAN_LOWER_20 = Indicators.DONCHIAN_LOWER(20)
