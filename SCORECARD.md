# Performance Scorecard
_Auto-generated 2026-07-13. Live, forward, out-of-sample. Not a backtest._

> Two scorecards below, kept separate on purpose. **Accuracy** asks whether the forecast is right. **Signal performance** asks whether acting on it makes money after costs. These are different questions, and a model can pass the first while failing the second.

## A. Forecast accuracy (price model)

Graded days: **2**  
_Sample below 20 - treat every number here as provisional._

| model / benchmark | MAE (£/MWh) | RMSE (£/MWh) |
|---|---|---|
| **Model** | 2.91 | 2.91 |
| Benchmark: yesterday's price | 13.85 | 17.16 |
| Benchmark: 7-day average | 14.69 | 14.83 |
| Benchmark: same day last week | 1.64 | 2.00 |

**Directional accuracy:** 100% (did we call up/down correctly vs yesterday, over 2 days)

**Bias:** -2.91 £/MWh (under-forecasting)

**Verdict:** the model BEATS the persistence benchmark on MAE - but the sample is small.

## B. Signal performance (does acting on it pay?)

Signal frequency: **0** LONG/SHORT, **1** FLAT (no trade)

_No completed trades yet. A signal that rarely fires is not a fault: it means we rarely disagree with the market by enough to act._

## Method notes

- Everything here is **forward-looking**: the forecast and the signal were recorded before the outcome was known. A forward record cannot be curve-fitted, unlike a backtest.
- Benchmarks use only information available before the target day.
- Accuracy and profitability are reported separately, on purpose.
- No conclusion is drawn below 20 observations.