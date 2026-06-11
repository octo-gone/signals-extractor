from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from signals_extractor.indicators import IndicatorType
    from signals_extractor.signals import SignalType


@dataclass(frozen=True)
class Dependency:
    """Dependency on another indicator/signal."""

    factory: Callable[..., IndicatorType | SignalType]
    param_map: dict[str, str] | Callable[[dict[str, str | int | float]], dict[str, str | int | float]]

    def resolve(self, params: dict[str, str | int | float]) -> IndicatorType | SignalType:
        if callable(self.param_map):
            mapped = self.param_map(params)
        else:
            mapped = _map_params(params, self.param_map)
        return self.factory(**mapped)


@dataclass(frozen=True)
class Spec:
    """Specification for indicator/signal data dependencies."""

    name: str
    inputs: tuple[str, ...] = ()
    depends: tuple[Dependency, ...] = ()

    def resolve(self, obj: IndicatorType | SignalType) -> list[IndicatorType | SignalType]:
        params = dict(obj.params)
        return [d.resolve(params) for d in self.depends]


def _map_params(source_params: dict[str, str | int | float], mapping: dict[str, str]) -> dict[str, str | int | float]:
    """Map signal params to indicator params using a field mapping."""
    return {target: source_params[src] for target, src in mapping.items() if src in source_params}


def _dep(factory: Callable[..., IndicatorType | SignalType], **param_map: str) -> Dependency:
    return Dependency(factory=factory, param_map=param_map)
