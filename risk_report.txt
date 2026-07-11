# risk_report.py - writes a full daily VaR / risk report as RISK_REPORT.md (renders on GitHub).
# Run alongside daily_desk.py in the same pipeline.
import datetime as dt
import numpy as np, pandas as pd, requests

Z = {0.95: 1.65, 0.99: 2.33}

# ---- the book you want risk-managed. Edit as your positions change. ----
BOOK = [
    {"name": "GB power DA (reference)", "side": "long", "volume_mwh": 100.0},
]
VAR_LIMIT_GBP     = 15000.0
MAX_POSITION_MWH  = 20000.0
STRESS_SHOCKS     = [-0.50, -0.20, -0.10, 0.10, 0.20, 0.50]

today = dt.date.today()


def daily_peak_price(start, end):
    rows = []
    d = start
    while d <= end:
        d2 = min(d + dt.timedelta(days=6), end)
        u = ("https://data.elexon.co.uk/bmrs/api/v1/balancing/pricing/market-index"
             f"?from={d}T00:00Z&to={d2}T23:59Z&format=json")
        try:
            rows += requests.get(u, timeout=60).json().get("data", [])
        except Exception as e:
            print("chunk failed:", d, type(e).__name__)
        d = d2 + dt.timedelta(days=1)
    rows = [x for x in rows if x.get("dataProvider") == "APXMIDP"]
    if not rows:
        return pd.Series(dtype=float)
    df = pd.DataFrame(rows)
    df["settlementDate"] = pd.to_datetime(df["settlementDate"]).dt.date
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    return df.groupby("settlementDate")["price"].max().sort_index()


# ---- market data: short and long volatility windows ----
hist_90 = daily_peak_price(today - dt.timedelta(days=95), today - dt.timedelta(days=1))
if hist_90.empty:
    raise SystemExit("no price data - aborting, will retry next run")

rets_90 = hist_90.pct_change().dropna()
vol_90  = float(rets_90.std())
vol_30  = float(rets_90.tail(30).std())
spot    = float(hist_90.iloc[-1])
p_min, p_max = float(hist_90.min()), float(hist_90.max())
worst_day = float(rets_90.min())

lines = []
A = lines.append

A(f"# Daily Risk Report")
A(f"_Generated {today.isoformat()} - GB day-ahead power. Auto-updated daily._\n")

A("## Market conditions\n")
A(f"| metric | value |")
A(f"|---|---|")
A(f"| spot (last daily peak) | £{spot:,.2f}/MWh |")
A(f"| 30-day daily volatility | **{vol_30*100:.1f}%** |")
A(f"| 90-day daily volatility | {vol_90*100:.1f}% |")
A(f"| 90-day range | £{p_min:,.0f} - £{p_max:,.0f}/MWh |")
A(f"| worst single-day move (90d) | {worst_day*100:.1f}% |")
A("")
regime = "ELEVATED" if vol_30 > vol_90 * 1.15 else ("CALM" if vol_30 < vol_90 * 0.85 else "NORMAL")
A(f"**Volatility regime: {regime}** (30d vs 90d). ")
if regime == "ELEVATED":
    A("Short-term volatility is running above the 90-day norm: cut size, widen stress assumptions.\n")
elif regime == "CALM":
    A("Short-term volatility is below the 90-day norm: conditions permit larger size, but do not confuse calm with safe.\n")
else:
    A("Short-term volatility is in line with the 90-day norm.\n")

# ---- VaR on the book ----
A("## Value at Risk (1-day, parametric)\n")
A("VaR = position value x daily volatility x z. Using the 30-day volatility.\n")
A("| position | side | volume (MWh) | value (£) | VaR 95% (£) | VaR 99% (£) |")
A("|---|---|---|---|---|---|")

total_value = total_var95 = total_var99 = 0.0
for p in BOOK:
    sign  = 1 if p["side"] == "long" else -1
    value = p["volume_mwh"] * sign * spot
    v95   = abs(p["volume_mwh"] * spot) * vol_30 * Z[0.95]
    v99   = abs(p["volume_mwh"] * spot) * vol_30 * Z[0.99]
    total_value  += value
    total_var95  += v95
    total_var99  += v99
    A(f"| {p['name']} | {p['side']} | {p['volume_mwh']:,.0f} | {value:,.0f} | {v95:,.0f} | {v99:,.0f} |")
A(f"| **PORTFOLIO** | | | **{total_value:,.0f}** | **{total_var95:,.0f}** | **{total_var99:,.0f}** |")
A("")
A(f"Interpretation: on roughly 1 day in 20, a loss of at least **£{total_var95:,.0f}** would be expected.\n")

# ---- stress tests ----
A("## Stress tests\n")
A("Deterministic shocks. Unlike VaR, these carry no probability - they size the scenario.\n")
A("| price shock | portfolio P&L (£) |")
A("|---|---|")
for s in STRESS_SHOCKS:
    pnl = sum(p["volume_mwh"] * (1 if p["side"] == "long" else -1) * spot * s for p in BOOK)
    A(f"| {s:+.0%} | {pnl:+,.0f} |")
A("")
A(f"Note: the worst single day in the last 90 was **{worst_day*100:.1f}%**, so the larger shocks above are not hypothetical.\n")

# ---- limits ----
A("## Exposure vs limits\n")
A(f"| limit | set | current | status |")
A(f"|---|---|---|---|")
biggest = max((p["volume_mwh"] for p in BOOK), default=0)
pos_ok  = "OK" if biggest <= MAX_POSITION_MWH else "**BREACH**"
var_ok  = "OK" if total_var95 <= VAR_LIMIT_GBP else "**BREACH**"
A(f"| max single position | {MAX_POSITION_MWH:,.0f} MWh | {biggest:,.0f} MWh | {pos_ok} |")
A(f"| max portfolio VaR (95%) | £{VAR_LIMIT_GBP:,.0f} | £{total_var95:,.0f} | {var_ok} |")
A("")

# ---- sizing guidance ----
max_size = VAR_LIMIT_GBP / (spot * vol_30 * Z[0.95])
A("## Position sizing at current volatility\n")
A(f"At **{vol_30*100:.1f}%** daily volatility and a £{VAR_LIMIT_GBP:,.0f} VaR limit, the largest permissible position is:\n")
A(f"### **{max_size:,.0f} MWh**\n")
A("Volatility dictates size. When volatility rises, the permissible position falls, even if conviction does not.\n")

# ---- honest limitations ----
A("## Limitations (read these)\n")
A("- **Parametric VaR assumes roughly normal returns.** Power prices have fat tails and spike on events, "
  "so real losses on bad days can exceed VaR. VaR is a routine-day gauge, not a worst case. That is why stress tests sit alongside it.")
A("- **Volatility is backward-looking.** It measures what happened, not what will.")
A("- **Portfolio VaR here is a simple sum** across positions, which ignores diversification and is therefore conservative.")
A("- **This is peak-price volatility**, the most volatile point of the day; average prices are calmer.")

open("RISK_REPORT.md", "w").write("\n".join(lines))
print("wrote RISK_REPORT.md")
print(f"vol30 {vol_30*100:.1f}% | VaR95 {total_var95:,.0f} | max size {max_size:,.0f} MWh | regime {regime}")
