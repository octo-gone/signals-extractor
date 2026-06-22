# signals-extractor

A configurable Python library for calculating technical analysis **indicators** and **signals** from OHLCV candlestick data. Indicators are raw continuous series (SMA, RSI, MACD line); signals are derived events (crossovers, breakouts, overbought flags).

## Features

- Separate `Indicators` and `Signals` factories with explicit dependency metadata.
- `Processor` resolves only the indicators and signals you enable.
- Batch mode (`calculate`) for full DataFrame processing.
- Factory-based type definitions with `indicator_factory` and `signal_factory`.
- Dependency inspection via `Processor.dependencies(...)` for the current spec graph.

## Disclaimer

This library is provided solely for educational, research, and experimental purposes. None of the technical indicators, signals, or derived calculations constitute financial advice, trading recommendations, or an offer to buy/sell any asset. You should always consult a qualified financial advisor before making investment decisions.

### No Guarantee of Correctness

While efforts have been made to implement standard technical indicators, there is no guarantee that calculations are error-free, complete, or up-to-date with all industry conventions. Some implementation have seeding values for non error calculation.

### Variations in Formulas

Different trading platforms, data providers, and academic sources define technical indicators differently (e.g., Wilder's smoothing vs. simple exponential smoothing for RSI, or varying periods for ATR). This library may not match the output of any specific platform.

### Data Quality Dependency

The accuracy of any signal or indicator is entirely dependent on the quality, frequency, and source of the input data (e.g., price, volume, timestamp). Incomplete, delayed, or erroneous data will produce misleading outputs.

## Installation

This repository is packaged with `pyproject.toml` and uses `hatchling` as the build backend.

```bash
uv add ../signals-extractor
```

## Contribution

For any concerns about indicator implementations — including but not limited to potential calculation errors, deviations from published formulas, unexpected signal behavior, numerical stability issues, efficiency, or edge-case failures — open a detailed issue on the official repository, including specific references to the code lines in question, input data samples, expected vs. actual outputs, and citations to authoritative formula definitions.

If you believe that any naming — including function names, variable names, class names, method names, parameter names, or constant names — could be clearer, more consistent, or more intuitive, please create an issue on the repository with your specific suggestion.

## Core API

| Symbol | Role |
|--------|------|
| `Processor` | Batch calculator for OHLCV data (`calculate`) |
| `Indicators` | Factory for raw indicator descriptors (`Indicators.SMA(10)`) |
| `Signals` | Factory for signal descriptors (`Signals.PRICE_ABOVE_SMA(10)`) |
| `IndicatorsCollection` / `SignalsCollection` | Common presets for popular combinations |
| `IndicatorType` / `SignalType` | Immutable typed descriptors used internally |
| `Result` / `ProcessingResult` | Output containers returned from `calculate` |
| `indicator_factory` / `signal_factory` | Decorators for custom factories |
| `processor.dependencies(...)` | Inspect dependency dependencies for a target type |
| `processor.required_columns()` | Inspect required columns for provided indicators/signals/specs/calculators |

## Data Requirements

`processor.calculate(...)` expect OHLCV data. Required columns will be calculated from enabled indicators/signalsspecs/calculator via `processor.required_columns()` (e.g. `Signals.RSI_OVERBOUGHT` needs only `close`).

### Commonly used columns

| Column | Description |
|--------|-------------|
| `open` | Opening price |
| `high` | Highest price |
| `low` | Lowest price |
| `close` | Closing price |
| `volume` | Traded volume |


### Example data

```python
import pandas as pd

df = pd.DataFrame({
    "open":   [100.0, 101.0, 102.0, 103.0, 104.0],
    "high":   [101.0, 102.5, 103.5, 104.5, 105.0],
    "low":    [ 99.5, 100.5, 101.5, 102.5, 103.5],
    "close":  [100.8, 102.0, 103.0, 104.2, 104.8],
    "volume": [1000,  1100,  1150,  1200,  1250],
})
```

## Quick Start

### Batch processing

```python
import pandas as pd
from signals_extractor import Processor, Indicators, Signals


df = pd.DataFrame({
    "open":   [100.0, 101.0, 102.0],
    "high":   [101.0, 102.0, 103.0],
    "low":    [ 99.0, 100.0, 101.0],
    "close":  [100.5, 101.5, 102.5],
    "volume": [1000.0, 1100.0, 1200.0],
})

processor = Processor(
    enabled_indicators=[Indicators.SMA(2)],
    enabled_signals=[Signals.PRICE_ABOVE_SMA(2)],
)

result = processor.calculate(df)

sma = result.indicators[Indicators.SMA(2)]
print(sma.name)
# SMA (period=2)
print(sma.values.tolist())
# [nan, 101.0, 102.0]

above = result.signals[Signals.PRICE_ABOVE_SMA(2)]
print(above.values.tolist())
# [0, 1, 1]
```

### Inspecting dependencies

`processor.dependencies(...)` inspect the dependency graph for a target type (uses provided specs or default).

```python
from signals_extractor import Processor, Signals

processor = Processor()
for dep in processor.dependencies(Signals.MACD_CROSSOVER_BULLISH(12, 26, 9)):
    print(dep)
# EMA (period=12)
# EMA (period=26)
# MACD_SIGNAL (long=26, short=12, signal=9)
# MACD_LINE (long=26, short=12)
```

### Using collection presets

```python
from signals_extractor import Processor, IndicatorsCollection, SignalsCollection

processor = Processor(
    enabled_indicators=[IndicatorsCollection.SMA_10, IndicatorsCollection.RSI_14],
    enabled_signals=[SignalsCollection.PRICE_ABOVE_SMA_10, SignalsCollection.RSI_OVERBOUGHT_14],
)
result = processor.calculate(df)
```

## Indicators vs Signals

| Layer | Factory | Examples |
|-------|---------|----------|
| **Indicators** | `Indicators.*` | `ROC`, `CCI`, `MOMENTUM`, `SMA`, `EMA`, `MACD_LINE`, `RSI`, `OBV`, `CMF`, `ATR` |
| **Signals** | `Signals.*` | `PRICE_ABOVE_SMA`, `RSI_OVERBOUGHT`, `MACD_CROSSOVER_BULLISH`, `BB_WIDTH_BREAKOUT`, `OBV_POSITIVE_TREND`, `CMF_POSITIVE` |

`IndicatorsCollection` provides presets like `SMA_10`, `RSI_14`, `MACD_LINE`.
`SignalsCollection` provides presets like `PRICE_ABOVE_SMA_10`, `RSI_OVERBOUGHT_14`.

## Customizing

### ... with your own specs and calculators

The current processor accepts custom `indicator_specs`, `signal_specs`, `indicator_calcs`, and `signal_calcs` dictionaries. That lets you plug in your own factories and batch logic without changing the core engine.

Here is a minimal VWAP example:

```python
import numpy as np
import pandas as pd

from signals_extractor import IndicatorType, SignalType, Processor, indicator_factory, signal_factory
from signals_extractor.engine.spec import Spec, _dep
from signals_extractor.indicators.spec import INDICATORS_SPECS
from signals_extractor.indicators.calc import INDICATORS_CALCS
from signals_extractor.signals.spec import SIGNALS_SPECS
from signals_extractor.signals.calc import SIGNALS_CALCS


@indicator_factory("vwap")
def VWAP(period: int) -> IndicatorType:
    return IndicatorType("vwap", period=period)


@signal_factory("price_above_vwap")
def PRICE_ABOVE_VWAP(period: int) -> SignalType:
    return SignalType("price_above_vwap", period=period)


INDICATOR_SPECS = {
    "vwap": Spec("vwap", ("close", "volume")),
}
SIGNAL_SPECS = {
    "price_above_vwap": Spec(
        "price_above_vwap",
        ("close",),
        depends=(_dep(VWAP, period="period"),),
    ),
}

def _compute_vwap(ctx, ind):
    high = ctx.data["high"]
    low = ctx.data["low"]
    close = ctx.data["close"]
    volume = ctx.data["volume"]

    typical_price = (high + low + close) / 3.0

    cum_pv = np.cumsum(typical_price * volume)
    cum_vol = np.cumsum(volume)

    out = np.full(len(close), np.nan, dtype=float)

    mask = cum_vol > 0
    out[mask] = cum_pv[mask] / cum_vol[mask]

    return ctx.set(ind, out)


def _derive_price_above_vwap(ctx, signal):
    vwap_values = ctx.get(VWAP(period=int(signal.params["period"])))
    close_prices = ctx.data["close"]
    return ctx.set(signal, (close_prices > vwap_values).astype(int))

INDICATOR_CALCS = {"vwap": _compute_vwap}
SIGNAL_CALCS = {
    "price_above_vwap": _derive_price_above_vwap
}

df = pd.DataFrame(
    {
        "open":   [100, 110, 120,  90,  80],
        "high":   [101, 111, 121,  91,  81],
        "low":    [ 99, 109, 119,  89,  79],
        "close":  [100, 110, 120,  90,  80],
        "volume": [1000, 1000, 1000, 1000, 1000],
    }
)

processor = Processor(
    enabled_indicators=[VWAP(2)],
    enabled_signals=[PRICE_ABOVE_VWAP(2)],
    # or without extending if other specs/calcs not used
    indicator_specs=INDICATORS_SPECS | INDICATOR_SPECS,
    signal_specs=SIGNALS_SPECS | SIGNAL_SPECS,
    indicator_calcs=INDICATORS_CALCS | INDICATOR_CALCS,
    signal_calcs=SIGNALS_CALCS | SIGNAL_CALCS,
)

result = processor.calculate(df)
print(result.indicators[VWAP(2)].values.tolist())
# [100.0, 105.0, 110.0, 105.0, 100.0]
print(result.signals[PRICE_ABOVE_VWAP(2)].values.tolist())
# [0, 1, 1, 0, 0]
print(processor.dependencies(PRICE_ABOVE_VWAP(2)))
# {VWAP (period=2)}
```

The same pattern works for any custom indicator/signal combination: register the type with `indicator_factory` / `signal_factory`, add it to the spec dictionaries, and provide the calculator functions you want the processor to use.

### ... with dynamic dependencies

Use `ParamDependency` when a dependency is not derived from parameters but is represented by a predefined indicator/signal. Instead of resolving the dependency through a factory and parameter mapping, `ParamDependency` uses the parameter value directly as the dependency.

```python
...
from signals_extractor import ParamDependency

@signal_factory("trend_reverse")
def TREND_REVERSE(
    signal: SignalType,
    trend_indicator: IndicatorType,
    direction: Literal["bullish", "bearish", "all"],
) -> SignalType:
    return SignalType(
        "trend_reverse",
        signal=signal,
        trend_indicator=trend_indicator,
        direction=direction,
    )

def _derive_trend_reverse(
    ctx: BatchContext,
    ind: IndicatorType,
):
    direction = ind.params["direction"]
    signal = ctx.get(ind.params["signal"])
    trend = ctx.get(ind.params["trend_indicator"])
    out = np.zeros_like(trend, dtype=float)
    mask = signal == 1.0
    if direction == "bullish":
        mask &= trend < 0
    elif direction == "bearish":
        mask &= trend > 0
    out[mask] = -trend[mask]
    return ctx.set(ind, out)

S_CALCS = SIGNALS_CALCS | {
    ...
    "trend_reverse": _derive_trend_reverse,
}

S_SPECS = SIGNALS_SPECS | {
    ...
    "trend_reverse": Spec(
        "trend_reverse",
        depends=(
            ParamDependency("signal"),
            ParamDependency("trend_indicator"),
        ),
    ),
}

trend_reversal_signal = TREND_REVERSE(
    # where does darth vader get his shoes from?
    DARTH_MAUL(), TREND_SCORE(8, 3), direction="bullish"
)
```

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependencies control and other stuff.

Checking `uv`:

```bash
uv
```

```
An extremely fast Python package manager.

Usage: uv [OPTIONS] <COMMAND>

Commands:
  auth     Manage authentication
  run      Run a command or script
...
```

Installing dependencies:

```bash
uv sync
```

Installing dev dependencies:

```bash
uv sync --group dev
```

