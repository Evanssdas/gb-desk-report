# Daily Risk Report
_Generated 2026-07-11 - GB day-ahead power. Auto-updated daily._

## Market conditions

| metric | value |
|---|---|
| spot (last daily peak) | £122.94/MWh |
| 30-day daily volatility | **47.0%** |
| 90-day daily volatility | 42.0% |
| 90-day range | £36 - £561/MWh |
| worst single-day move (90d) | -71.8% |

**Volatility regime: NORMAL** (30d vs 90d). 
Short-term volatility is in line with the 90-day norm.

## Value at Risk (1-day, parametric)

VaR = position value x daily volatility x z. Using the 30-day volatility.

| position | side | volume (MWh) | value (£) | VaR 95% (£) | VaR 99% (£) |
|---|---|---|---|---|---|
| GB power DA (reference) | long | 100 | 12,294 | 9,541 | 13,473 |
| **PORTFOLIO** | | | **12,294** | **9,541** | **13,473** |

Interpretation: on roughly 1 day in 20, a loss of at least **£9,541** would be expected.

## Stress tests

Deterministic shocks. Unlike VaR, these carry no probability - they size the scenario.

| price shock | portfolio P&L (£) |
|---|---|
| -50% | -6,147 |
| -20% | -2,459 |
| -10% | -1,229 |
| +10% | +1,229 |
| +20% | +2,459 |
| +50% | +6,147 |

Note: the worst single day in the last 90 was **-71.8%**, so the larger shocks above are not hypothetical.

## Exposure vs limits

| limit | set | current | status |
|---|---|---|---|
| max single position | 20,000 MWh | 100 MWh | OK |
| max portfolio VaR (95%) | £15,000 | £9,541 | OK |

## Position sizing at current volatility

At **47.0%** daily volatility and a £15,000 VaR limit, the largest permissible position is:

### **157 MWh**

Volatility dictates size. When volatility rises, the permissible position falls, even if conviction does not.

## Limitations (read these)

- **Parametric VaR assumes roughly normal returns.** Power prices have fat tails and spike on events, so real losses on bad days can exceed VaR. VaR is a routine-day gauge, not a worst case. That is why stress tests sit alongside it.
- **Volatility is backward-looking.** It measures what happened, not what will.
- **Portfolio VaR here is a simple sum** across positions, which ignores diversification and is therefore conservative.
- **This is peak-price volatility**, the most volatile point of the day; average prices are calmer.