# Performance Scorecard
_Auto-generated 2026-11-13. Live, forward, out-of-sample. Not a backtest._

> Two scorecards below, kept separate on purpose. **Accuracy** asks whether the forecast is right. **Signal performance** asks whether acting on it makes money after costs. These are different questions, and a model can pass the first while failing the second.

## A. Forecast accuracy (price model)

Graded days: **115**

| model / benchmark | MAE (£/MWh) | RMSE (£/MWh) |
|---|---|---|
| **Model** | 70.20 | 81.15 |
| Benchmark: yesterday's price | 23.09 | 37.25 |
| Benchmark: 7-day average | 21.68 | 35.14 |
| Benchmark: same day last week | 28.87 | 43.92 |

**Directional accuracy:** 52% (did we call up/down correctly vs yesterday, over 115 days)

**Bias:** -70.08 £/MWh (under-forecasting)

**Verdict:** the model does NOT beat the persistence benchmark on MAE.

## B. Signal performance (does acting on it pay?)

Signal frequency: **0** LONG/SHORT, **29** FLAT (no trade)

_No completed trades yet. A signal that rarely fires is not a fault: it means we rarely disagree with the market by enough to act._

## Method notes

- Everything here is **forward-looking**: the forecast and the signal were recorded before the outcome was known. A forward record cannot be curve-fitted, unlike a backtest.
- Benchmarks use only information available before the target day.
- Accuracy and profitability are reported separately, on purpose.
- No conclusion is drawn below 20 observations.

## Gas watch: is TTF worth adding to the price model yet?

_The model currently does **not** use gas as a feature. The pipeline logs TTF daily so the history accumulates; this test decides when it earns its place._

_Gas watch unavailable (AttributeError)._
