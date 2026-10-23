# Performance Scorecard
_Auto-generated 2026-10-23. Live, forward, out-of-sample. Not a backtest._

> Two scorecards below, kept separate on purpose. **Accuracy** asks whether the forecast is right. **Signal performance** asks whether acting on it makes money after costs. These are different questions, and a model can pass the first while failing the second.

## A. Forecast accuracy (price model)

Graded days: **97**

| model / benchmark | MAE (£/MWh) | RMSE (£/MWh) |
|---|---|---|
| **Model** | 60.73 | 66.76 |
| Benchmark: yesterday's price | 20.79 | 30.43 |
| Benchmark: 7-day average | 18.23 | 25.89 |
| Benchmark: same day last week | 25.76 | 37.33 |

**Directional accuracy:** 53% (did we call up/down correctly vs yesterday, over 97 days)

**Bias:** -60.58 £/MWh (under-forecasting)

**Verdict:** the model does NOT beat the persistence benchmark on MAE.

## B. Signal performance (does acting on it pay?)

Signal frequency: **0** LONG/SHORT, **28** FLAT (no trade)

_No completed trades yet. A signal that rarely fires is not a fault: it means we rarely disagree with the market by enough to act._

## Method notes

- Everything here is **forward-looking**: the forecast and the signal were recorded before the outcome was known. A forward record cannot be curve-fitted, unlike a backtest.
- Benchmarks use only information available before the target day.
- Accuracy and profitability are reported separately, on purpose.
- No conclusion is drawn below 20 observations.

## Gas watch: is TTF worth adding to the price model yet?

_The model currently does **not** use gas as a feature. The pipeline logs TTF daily so the history accumulates; this test decides when it earns its place._

| window | overlapping days | TTF-vs-price change correlation |
|---|---:|---:|
| 30 days | 30 | **-0.02** |
| 90 days | 73 | **+0.07** |

### NO ACTION: correlation is +0.07.

**Gas is not a useful feature right now.** Power is being priced by system scarcity rather than fuel cost, so adding TTF would fit noise. The data continues to accumulate in the price log; this test re-runs daily and will say so when that changes.

_Why the threshold: a feature with a change-correlation near zero adds noise, and a gradient-booster will happily fit spurious patterns in it. The bar exists to stop that._
