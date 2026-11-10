# Daily Risk Report
_Generated 2026-11-10 - GB day-ahead power. Auto-updated daily._

## Market conditions

| metric | value |
|---|---|
| spot (last daily peak) | £498.16/MWh |
| 30-day daily volatility | **20.7%** |
| 90-day daily volatility | 20.0% |
| 90-day range | £118 - £498/MWh |
| worst single-day move (90d) | -42.9% |

**Volatility regime: NORMAL** (30d vs 90d). 
Short-term volatility is in line with the 90-day norm.

## Value at Risk (1-day, parametric)

VaR = position value x daily volatility x z. Using the 30-day volatility.

| position | side | volume (MWh) | value (£) | VaR 95% (£) | VaR 99% (£) |
|---|---|---|---|---|---|
| GB power DA (reference) | long | 100 | 49,816 | 17,018 | 24,031 |
| **PORTFOLIO** | | | **49,816** | **17,018** | **24,031** |

Interpretation: on roughly 1 day in 20, a loss of at least **£17,018** would be expected.

## Stress tests

Deterministic shocks. Unlike VaR, these carry no probability - they size the scenario.

| price shock | portfolio P&L (£) |
|---|---|
| -50% | -24,908 |
| -20% | -9,963 |
| -10% | -4,982 |
| +10% | +4,982 |
| +20% | +9,963 |
| +50% | +24,908 |

Note: the worst single day in the last 90 was **-42.9%**, so the larger shocks above are not hypothetical.

## Exposure vs limits

| limit | set | current | status |
|---|---|---|---|
| max single position | 20,000 MWh | 100 MWh | OK |
| max portfolio VaR (95%) | £15,000 | £17,018 | **BREACH** |

## Position sizing at current volatility

At **20.7%** daily volatility and a £15,000 VaR limit, the largest permissible position is:

### **88 MWh**

Volatility dictates size. When volatility rises, the permissible position falls, even if conviction does not.

## Limitations (read these)

- **Parametric VaR assumes roughly normal returns.** Power prices have fat tails and spike on events, so real losses on bad days can exceed VaR. VaR is a routine-day gauge, not a worst case. That is why stress tests sit alongside it.
- **Volatility is backward-looking.** It measures what happened, not what will.
- **Portfolio VaR here is a simple sum** across positions, which ignores diversification and is therefore conservative.
- **This is peak-price volatility**, the most volatile point of the day; average prices are calmer.