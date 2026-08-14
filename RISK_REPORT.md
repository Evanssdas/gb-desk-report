# Daily Risk Report
_Generated 2026-08-14 - GB day-ahead power. Auto-updated daily._

## Market conditions

| metric | value |
|---|---|
| spot (last daily peak) | £141.01/MWh |
| 30-day daily volatility | **13.0%** |
| 90-day daily volatility | 28.5% |
| 90-day range | £95 - £561/MWh |
| worst single-day move (90d) | -57.3% |

**Volatility regime: CALM** (30d vs 90d). 
Short-term volatility is below the 90-day norm: conditions permit larger size, but do not confuse calm with safe.

## Value at Risk (1-day, parametric)

VaR = position value x daily volatility x z. Using the 30-day volatility.

| position | side | volume (MWh) | value (£) | VaR 95% (£) | VaR 99% (£) |
|---|---|---|---|---|---|
| GB power DA (reference) | long | 100 | 14,101 | 3,030 | 4,279 |
| **PORTFOLIO** | | | **14,101** | **3,030** | **4,279** |

Interpretation: on roughly 1 day in 20, a loss of at least **£3,030** would be expected.

## Stress tests

Deterministic shocks. Unlike VaR, these carry no probability - they size the scenario.

| price shock | portfolio P&L (£) |
|---|---|
| -50% | -7,050 |
| -20% | -2,820 |
| -10% | -1,410 |
| +10% | +1,410 |
| +20% | +2,820 |
| +50% | +7,050 |

Note: the worst single day in the last 90 was **-57.3%**, so the larger shocks above are not hypothetical.

## Exposure vs limits

| limit | set | current | status |
|---|---|---|---|
| max single position | 20,000 MWh | 100 MWh | OK |
| max portfolio VaR (95%) | £15,000 | £3,030 | OK |

## Position sizing at current volatility

At **13.0%** daily volatility and a £15,000 VaR limit, the largest permissible position is:

### **495 MWh**

Volatility dictates size. When volatility rises, the permissible position falls, even if conviction does not.

## Limitations (read these)

- **Parametric VaR assumes roughly normal returns.** Power prices have fat tails and spike on events, so real losses on bad days can exceed VaR. VaR is a routine-day gauge, not a worst case. That is why stress tests sit alongside it.
- **Volatility is backward-looking.** It measures what happened, not what will.
- **Portfolio VaR here is a simple sum** across positions, which ignores diversification and is therefore conservative.
- **This is peak-price volatility**, the most volatile point of the day; average prices are calmer.