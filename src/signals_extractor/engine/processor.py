"""Unified Processor for batch indicator/signal computation."""

from typing import Callable

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
        """Retrieve all indicator/signal dependencies, including dependencies' dependencies and so on."""
        out = []

        def collect(obj: IndicatorType | SignalType) -> None:
            spec = (
                self.signal_specs.get(obj.type) if isinstance(obj, SignalType) else self.indicator_specs.get(obj.type)
            )
            if spec is None:
                return

            for dep in spec.resolve(obj):
                out.append(dep)
                collect(dep)

        collect(target)
        return set(out)

    def required_columns(self, targets: list[IndicatorType | SignalType] | None = None) -> set[str]:
        """Collect all dataframe columns required by the enabled indicators/signals and their dependencies."""
        if targets is None:
            targets = [*self.enabled_indicators, *self.enabled_signals]

        required: set[str] = set()

        def collect(obj: IndicatorType | SignalType) -> None:
            spec = (
                self.indicator_specs.get(obj.type)
                if isinstance(obj, IndicatorType)
                else self.signal_specs.get(obj.type)
            )
            if spec is None:
                return

            required.update(spec.inputs)
            for dep in spec.resolve(obj):
                collect(dep)

        for target in targets:
            collect(target)

        return required

    def validate_columns(self, df: pd.DataFrame) -> None:
        """Ensure the input frame contains every column required by the configured dependency graph."""
        missing = sorted(self.required_columns() - set(df.columns))
        if missing:
            raise ValueError(f"Required column(s) not found in data: {', '.join(missing)}")

    def _calc(
        self, obj: IndicatorType | SignalType
    ) -> Callable[[BatchContext, IndicatorType | SignalType], np.ndarray]:
        """Retrieve calculator for indicator/signal."""
        if obj.type in self.indicator_calcs:
            return self.indicator_calcs[obj.type]  # type: ignore
        if obj.type in self.signal_calcs:
            return self.signal_calcs[obj.type]  # type: ignore
        raise KeyError(f"No calculator function found for: {obj.type}")

    def calculate(self, df: pd.DataFrame, verbose: bool = False) -> ProcessingResult:
        """Calculate all signals in one batch for provided dataframe."""
        if verbose:
            print(f"Processing {len(df)} data points...")

        self.validate_columns(df)

        data: dict[str, np.ndarray] = {}
        for col in self.required_columns():
            data[col] = df[col].to_numpy()

        ctx = BatchContext(data, self._calc)
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
