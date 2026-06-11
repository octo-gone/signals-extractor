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
        calc_handler: Callable[[IndicatorType | SignalType], IndicatorCalcFunc | SignalCalcFunc],
    ):
        self.data = data
        self._cache: dict[IndicatorType | SignalType, np.ndarray] = {}
        self._calc_handler = calc_handler

    def get(self, obj: IndicatorType | SignalType) -> np.ndarray:
        if obj not in self._cache:
            return self.set(obj, self._calc_handler(obj)(self, obj))  # type: ignore
        return self._cache[obj]

    def set(self, obj: IndicatorType | SignalType, values: np.ndarray) -> np.ndarray:
        self._cache[obj] = values
        return values

    def has(self, obj: IndicatorType | SignalType) -> bool:
        return obj in self._cache

    def values(self) -> dict[IndicatorType | SignalType, np.ndarray]:
        return dict(self._cache)
