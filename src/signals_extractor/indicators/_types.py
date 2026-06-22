# pylint: disable=invalid-name
from functools import total_ordering, wraps
from types import MappingProxyType
from typing import Any, Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R", bound="IndicatorType")


@total_ordering
class IndicatorType:
    """Immutable typed descriptors representing indicator type and it's parameters."""

    __slots__ = ["type", "params"]

    def __init__(self, type_: str, **params: "str | int | float | IndicatorType"):
        self.type = type_
        self.params = MappingProxyType(params)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, IndicatorType):
            return self.type == other.type and self.params == other.params
        if callable(other):
            return self.type == getattr(other, "__indicator_type__", None)
        raise NotImplementedError

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, IndicatorType):
            raise NotImplementedError
        return self.type < other.type

    def __hash__(self) -> int:
        return hash((self.type, tuple(frozenset(sorted(self.params.items())))))

    def __repr__(self) -> str:
        if self.params:
            params_str = ", ".join(f"{k}={v!r}" for k, v in sorted(self.params.items()))
            return f"{self.type.upper()} ({params_str})"
        return self.type.upper()


def indicator_factory(indicator_type: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Create a decorator that tags a indicator factory function with a indicator type and custom equality.

    The returned decorator attaches a `__indicator_type__` attribute and overrides
    `__eq__` to compare based on the indicator type. This is useful for comparing instances of
    `IndicatorType` with respective indicator factory.

    Parameters
    ----------
    indicator_type : str
        Identifier for the indicator type (e.g., 'rsi', 'bb_upper'). Will be stored
        on the decorated function as `__indicator_type__`.

    Returns
    -------
    Callable[[Callable[P, R]], Callable[P, R]]
        A decorator that accepts a function and returns a wrapped version with
        the added attributes.

    Example
    -------
    >>> @indicator_factory("regime")
    ... def REGIME():
    ...     return SignalType("regime")
    >>> REGIME.__indicator_type__
    'regime'
    >>> REGIME() == REGIME
    True
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            return func(*args, **kwargs)

        def wrapper_eq(value: object) -> bool:
            if isinstance(value, IndicatorType):
                return value.type == indicator_type
            raise NotImplementedError

        setattr(wrapper, "__indicator_type__", indicator_type)
        setattr(wrapper, "__eq__", wrapper_eq)

        return wrapper

    return decorator
