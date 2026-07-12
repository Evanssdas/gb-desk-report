# Performance Scorecard
_Auto-generated 2026-07-12. Live, forward, out-of-sample. Not a backtest._

> Two scorecards below, kept separate on purpose. **Accuracy** asks whether the forecast is right. **Signal performance** asks whether acting on it makes money after costs. These are different questions, and a model can pass the first while failing the second.

## A. Forecast accuracy (price model)

Graded days: **1**  
_Sample below 20 - treat every number here as provisional._

| model / benchmark | MAE (£/MWh) | RMSE (£/MWh) |
|---|---|---|
| **Model** | 3.08 | 3.08 |
| Benchmark: yesterday's price | 23.98 | 23.98 |
| Benchmark: 7-day average | 12.63 | 12.63 |
| Benchmark: same day last week | 2.78 | 2.78 |

**Directional accuracy:** 100% (did we call up/down correctly vs yesterday, over 1 days)

**Bias:** -3.08 £/MWh (under-forecasting)

**Verdict:** the model BEATS the persistence benchmark on MAE - but the sample is small.

## B. Signal performance (does acting on it pay?)

Signal frequency: **0** LONG/SHORT, **0** FLAT (no trade)

_No completed trades yet. A signal that rarely fires is not a fault: it means we rarely disagree with the market by enough to act._

## Method notes

- Everything here is **forward-looking**: the forecast and the signal were recorded before the outcome was known. A forward record cannot be curve-fitted, unlike a backtest.
- Benchmarks use only information available before the target day.
- Accuracy and profitability are reported separately, on purpose.
- No conclusion is drawn below 20 observations.