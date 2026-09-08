# Daily Risk Report
_Generated 2026-09-08 - GB day-ahead power. Auto-updated daily._

## Market conditions

| metric | value |
|---|---|
| spot (last daily peak) | £134.10/MWh |
| 30-day daily volatility | **11.9%** |
| 90-day daily volatility | 27.9% |
| 90-day range | £95 - £561/MWh |
| worst single-day move (90d) | -57.3% |

**Volatility regime: CALM** (30d vs 90d). 
Short-term volatility is below the 90-day norm: conditions permit larger size, but do not confuse calm with safe.

## Value at Risk (1-day, parametric)

VaR = position value x daily volatility x z. Using the 30-day volatility.

| position | side | volume (MWh) | value (£) | VaR 95% (£) | VaR 99% (£) |
|---|---|---|---|---|---|
| GB power DA (reference) | long | 100 | 13,410 | 2,622 | 3,703 |
| **PORTFOLIO** | | | **13,410** | **2,622** | **3,703** |

Interpretation: on roughly 1 day in 20, a loss of at least **£2,622** would be expected.

## Stress tests

Deterministic shocks. Unlike VaR, these carry no probability - they size the scenario.

| price shock | portfolio P&L (£) |
|---|---|
| -50% | -6,705 |
| -20% | -2,682 |
| -10% | -1,341 |
| +10% | +1,341 |
| +20% | +2,682 |
| +50% | +6,705 |

Note: the worst single day in the last 90 was **-57.3%**, so the larger shocks above are not hypothetical.

## Exposure vs limits

| limit | set | current | status |
|---|---|---|---|
| max single position | 20,000 MWh | 100 MWh | OK |
| max portfolio VaR (95%) | £15,000 | £2,622 | OK |

## Position sizing at current volatility

At **11.9%** daily volatility and a £15,000 VaR limit, the largest permissible position is:

### **572 MWh**

Volatility dictates size. When volatility rises, the permissible position falls, even if conviction does not.

## Limitations (read these)

- **Parametric VaR assumes roughly normal returns.** Power prices have fat tails and spike on events, so real losses on bad days can exceed VaR. VaR is a routine-day gauge, not a worst case. That is why stress tests sit alongside it.
- **Volatility is backward-looking.** It measures what happened, not what will.
- **Portfolio VaR here is a simple sum** across positions, which ignores diversification and is therefore conservative.
- **This is peak-price volatility**, the most volatile point of the day; average prices are calmer.