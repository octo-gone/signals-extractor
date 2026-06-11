"""Unified Processor for batch indicator/signal computation."""

import numpy as np
import pandas as pd

from signals_extractor.engine.context import BatchContext, IndicatorCalcFunc, SignalCalcFunc
from signals_extractor.engine.data import ProcessingResult, Result
from signals_extractor.engine.spec import Spec
from signals_extractor.indicators import IndicatorType
from signals_extractor.indicators.calc import INDICATORS_CALCS
from signals_extractor.indicators.spec import INDICATORS_SPECS
from signals_extractor.signals import SignalType
from signals_extractor.signals.calc import SIGNALS_CALCS
from signals_extractor.signals.spec import SIGNALS_SPECS


class Processor:
    """Processor for calculating indicators and signals from OHLCV data."""

    def __init__(
        self,
        enabled_indicators: list[IndicatorType] | None = None,
        enabled_signals: list[SignalType] | None = None,
        indicator_specs: dict[str, Spec] | None = None,
        signal_specs: dict[str, Spec] | None = None,
        indicator_calcs: dict[str, IndicatorCalcFunc] | None = None,
        signal_calcs: dict[str, SignalCalcFunc] | None = None,
    ):
        if enabled_indicators is None:
            enabled_indicators = []
        if enabled_signals is None:
            enabled_signals = []
        if indicator_specs is None:
            indicator_specs = INDICATORS_SPECS
        if signal_specs is None:
            signal_specs = SIGNALS_SPECS
        if indicator_calcs is None:
            indicator_calcs = INDICATORS_CALCS
        if signal_calcs is None:
            signal_calcs = SIGNALS_CALCS

        self.enabled_indicators = enabled_indicators
        self.enabled_signals = enabled_signals
        self.indicator_specs: dict[str, Spec] = indicator_specs
        self.signal_specs: dict[str, Spec] = signal_specs
        self.indicator_calcs: dict[str, IndicatorCalcFunc] = indicator_calcs
        self.signal_calcs: dict[str, SignalCalcFunc] = signal_calcs

    def dependencies(self, target: IndicatorType | SignalType) -> set[IndicatorType | SignalType]:
        out = []

        def get_req(obj: IndicatorType | SignalType) -> None:
            if isinstance(obj, SignalType):
                for parent_obj in self.signal_specs[obj.type].resolve(obj):
                    out.append(parent_obj)
                    get_req(parent_obj)
            else:
                for parent_obj in self.indicator_specs[obj.type].resolve(obj):
                    out.append(parent_obj)
                    get_req(parent_obj)

        get_req(target)
        return set(out)

    def calculate(self, df: pd.DataFrame, verbose: bool = False) -> ProcessingResult:
        if verbose:
            print(f"Processing {len(df)} data points...")

        data: dict[str, np.ndarray] = {}
        needed = ["open", "high", "low", "close", "volume"]
        for col in needed:
            if col not in df.columns:
                raise ValueError(f"Required column '{col}' not found in data")
            data[col] = df[col].to_numpy()

        ctx = BatchContext(data, self.indicator_calcs, self.signal_calcs)
        result = ProcessingResult()

        for indicator in self.enabled_indicators:
            values = ctx.get(indicator)
            result.indicators[indicator] = Result(
                str(indicator),
                values,
            )

        for signal in self.enabled_signals:
            values = ctx.get(signal)
            result.signals[signal] = Result(
                str(signal),
                values,
            )

        if verbose:
            print(f"Calculated {len(result.indicators)} indicators and {len(result.signals)} signals")

        return result
