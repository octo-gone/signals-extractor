from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

import numpy as np

if TYPE_CHECKING:
    from signals_extractor.indicators import IndicatorType
    from signals_extractor.signals import SignalType


@dataclass
class Result:
    """Container for indicator/signal calculation results."""

    name: str
    values: np.ndarray
    metadata: dict[str, Any] | None = None


@dataclass
class ProcessingResult:
    """Batch processing output with indicators and signals."""

    indicators: dict[IndicatorType, Result] = field(default_factory=dict)
    signals: dict[SignalType, Result] = field(default_factory=dict)
