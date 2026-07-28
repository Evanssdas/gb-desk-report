# Performance Scorecard
_Auto-generated 2026-07-28. Live, forward, out-of-sample. Not a backtest._

> Two scorecards below, kept separate on purpose. **Accuracy** asks whether the forecast is right. **Signal performance** asks whether acting on it makes money after costs. These are different questions, and a model can pass the first while failing the second.

## A. Forecast accuracy (price model)

Graded days: **17**  
_Sample below 20 - treat every number here as provisional._

| model / benchmark | MAE (£/MWh) | RMSE (£/MWh) |
|---|---|---|
| **Model** | 33.78 | 38.18 |
| Benchmark: yesterday's price | 14.84 | 19.83 |
| Benchmark: 7-day average | 11.68 | 15.46 |
| Benchmark: same day last week | 15.58 | 21.06 |

**Directional accuracy:** 47% (did we call up/down correctly vs yesterday, over 17 days)

**Bias:** -33.78 £/MWh (under-forecasting)

**Verdict:** the model does NOT beat the persistence benchmark on MAE - but the sample is small.

## B. Signal performance (does acting on it pay?)

Signal frequency: **0** LONG/SHORT, **10** FLAT (no trade)

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
| 30 days | 28 | **+0.23** |
| 90 days | 69 | **+0.16** |

### NO ACTION: correlation is +0.16.

**Gas is not a useful feature right now.** Power is being priced by system scarcity rather than fuel cost, so adding TTF would fit noise. The data continues to accumulate in the price log; this test re-runs daily and will say so when that changes.

_Why the threshold: a feature with a change-correlation near zero adds noise, and a gradient-booster will happily fit spurious patterns in it. The bar exists to stop that._
