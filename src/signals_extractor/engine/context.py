from typing import TYPE_CHECKING, Callable

import numpy as np

if TYPE_CHECKING:
    from signals_extractor.indicators._types import IndicatorType
    from signals_extractor.signals._types import SignalType


IndicatorCalcFunc = Callable[["BatchContext", "IndicatorType"], np.ndarray]
SignalCalcFunc = Callable[["BatchContext", "SignalType"], np.ndarray]


class BatchContext:
    """Context for batch indicator computation with caching."""

    def __init__(
        self,
        data: dict[str, np.ndarray],
        indicator_calcs: dict[str, IndicatorCalcFunc],
        signal_calcs: dict[str, SignalCalcFunc],
    ):
        self.data = data
        self._cache: dict[IndicatorType | SignalType, np.ndarray] = {}
        self._indicator_calcs = indicator_calcs
        self._signal_calcs = signal_calcs

    def get(self, obj: IndicatorType | SignalType) -> np.ndarray:
        if obj not in self._cache:
            if obj.type in self._indicator_calcs:
                return self.set(obj, self._indicator_calcs[obj.type](self, obj))  # type: ignore
            if obj.type in self._signal_calcs:
                return self.set(obj, self._signal_calcs[obj.type](self, obj))  # type: ignore
            raise KeyError(f"No calculator function found for: {obj.type}")
        return self._cache[obj]

    def set(self, obj: IndicatorType | SignalType, values: np.ndarray) -> np.ndarray:
        self._cache[obj] = values
        return values

    def has(self, obj: IndicatorType | SignalType) -> bool:
        return obj in self._cache

    def values(self) -> dict[IndicatorType | SignalType, np.ndarray]:
        return dict(self._cache)
