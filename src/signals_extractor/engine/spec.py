from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, Protocol

if TYPE_CHECKING:
    from signals_extractor.indicators import IndicatorType
    from signals_extractor.signals import SignalType

Params = dict[str, "str | int | float | IndicatorType | SignalType"]


class ResolveMethod(Protocol):
    def __call__(
        self,
        params: Params,
    ) -> IndicatorType | SignalType: ...


class HasResolve(Protocol):
    resolve: ResolveMethod


@dataclass(frozen=True)
class Dependency:
    """Dependency on another indicator/signal."""

    factory: Callable[..., IndicatorType | SignalType]
    param_map: dict[str, str] | Callable[[Params], Params]

    def resolve(self, params: Params) -> IndicatorType | SignalType:
        if callable(self.param_map):
            mapped = self.param_map(params)
        else:
            mapped = _map_params(params, self.param_map)
        return self.factory(**mapped)


@dataclass(frozen=True)
class ParamDependency:
    param: str

    def resolve(self, params: Params) -> IndicatorType | SignalType:
        return params[self.param]  # type: ignore


@dataclass(frozen=True)
class Spec:
    """Specification for indicator/signal data dependencies."""

    name: str
    inputs: tuple[str, ...] = ()
    depends: tuple[HasResolve, ...] = ()

    def resolve(self, obj: IndicatorType | SignalType) -> list[IndicatorType | SignalType]:
        params = dict(obj.params)
        return [d.resolve(params) for d in self.depends]


def _map_params(source_params: Params, mapping: dict[str, str]) -> Params:
    """Map signal params to indicator params using a field mapping."""
    return {target: source_params[src] for target, src in mapping.items() if src in source_params}


def _dep(factory: Callable[..., IndicatorType | SignalType], **param_map: str) -> Dependency:
    return Dependency(factory=factory, param_map=param_map)
