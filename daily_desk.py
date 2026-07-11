# daily_desk.py - daily analyst desk report: spread signal, risk conditions, live signal scorecard.
#
# Each run:
#   1. grade past signals: what did the price actually do vs what our lean said?
#   2. risk conditions: live volatility, VaR of a reference position, max size at limit
#   3. today's spread: our price forecast vs the market -> LONG / SHORT / FLAT
#   4. write or UPDATE the row for tomorrow (refreshes through the day; never duplicates)
#
# This is NOT a backtest. It records what the signal said BEFORE the outcome was known,
# then grades it. A forward record cannot be curve-fitted, which is the point.
import os, datetime as dt
import numpy as np, pandas as pd, requests

LOG = "desk_log.csv"
FORECAST_LOG_URL = os.environ.get("FORECAST_LOG_URL", "")
THRESHOLD    = 10.0      # GBP/MWh - only call a lean if we disagree by more than this
COST_PER_MWH = 1.0       # assumed round-trip cost
REF_SIZE     = 100.0     # reference position for the risk readout (MWh)
VAR_LIMIT    = 15000.0   # GBP - the VaR limit we size against
Z95 = 1.65

COLS = ["date_made","target_date","forecast","market","spread","lean",
        "settled","signal_pnl","daily_vol_pct","var_ref_100mwh","max_size_at_limit","status"]

today = pd.Timestamp.now(tz="Europe/London").normalize()
tom   = today + pd.Timedelta(days=1)

log = pd.read_csv(LOG) if os.path.exists(LOG) else pd.DataFrame(columns=COLS)
for c in COLS:
    if c not in log.columns:
        log[c] = ""


def elexon_daily_peak_price(start, end):
    """Daily peak day-ahead price (APX), paged in 7-day chunks (Elexon range limit)."""
    rows = []
    d = start
    while d <= end:
        d2 = min(d + dt.timedelta(days=6), end)
        u = ("https://data.elexon.co.uk/bmrs/api/v1/balancing/pricing/market-index"
             f"?from={d}T00:00Z&to={d2}T23:59Z&format=json")
        rows += requests.get(u, timeout=60).json().get("data", [])
        d = d2 + dt.timedelta(days=1)
    rows = [x for x in rows if x.get("dataProvider") == "APXMIDP"]
    if not rows:
        return pd.Series(dtype=float)
    df = pd.DataFrame(rows)
    df["settlementDate"] = pd.to_datetime(df["settlementDate"]).dt.date
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    return df.groupby("settlementDate")["price"].max()


# ---------- 1. grade past signals (forward, out-of-sample) ----------
try:
    due = log[(log["settled"].astype(str).str.strip() == "") &
              (log["target_date"].astype(str).str.strip() != "") &
              (pd.to_datetime(log["target_date"]).dt.date < today.date())]
    if len(due):
        lo = pd.to_datetime(due["target_date"]).min().date()
        hi = pd.to_datetime(due["target_date"]).max().date()
        settled = elexon_daily_peak_price(lo, hi)
        for i, r in due.iterrows():
            d = pd.to_datetime(r["target_date"]).date()
            if d in settled.index:
                s = round(float(settled.loc[d]), 2)
                log.at[i, "settled"] = s
                try:
                    lean = str(r["lean"]).strip()
                    mkt = float(r["market"])
                    if lean in ("LONG", "SHORT"):
                        direction = 1 if lean == "LONG" else -1
                        log.at[i, "signal_pnl"] = round((s - mkt) * direction - COST_PER_MWH, 2)
                    else:
                        log.at[i, "signal_pnl"] = 0.0
                except (ValueError, TypeError):
                    pass
        print("graded past signals")
except Exception as e:
    print("grading skipped:", type(e).__name__)


# ---------- 2. risk conditions: live volatility ----------
daily_vol = var_ref = max_size = np.nan
try:
    hist = elexon_daily_peak_price(today.date() - dt.timedelta(days=35),
                                   today.date() - dt.timedelta(days=1)).sort_index()
    daily_vol = float(hist.pct_change().dropna().std())
    last_price = float(hist.iloc[-1])
    var_ref  = REF_SIZE * last_price * daily_vol * Z95
    max_size = VAR_LIMIT / (last_price * daily_vol * Z95)
    print(f"vol {daily_vol*100:.1f}% | VaR({REF_SIZE:.0f}MWh) {var_ref:,.0f} | max size {max_size:,.0f} MWh")
except Exception as e:
    print("risk calc failed:", type(e).__name__)


# ---------- 3. today's spread: forecast vs market ----------
row = {
    "date_made": today.date().isoformat(),
    "target_date": tom.date().isoformat(),
    "forecast": "", "market": "", "spread": "", "lean": "",
    "settled": "", "signal_pnl": "",
    "daily_vol_pct":     round(daily_vol * 100, 1) if daily_vol == daily_vol else "",
    "var_ref_100mwh":    round(var_ref, 0)         if var_ref  == var_ref  else "",
    "max_size_at_limit": round(max_size, 0)        if max_size == max_size else "",
    "status": "ok",
}
try:
    if not FORECAST_LOG_URL:
        raise RuntimeError("FORECAST_LOG_URL not set")
    fl = pd.read_csv(FORECAST_LOG_URL)
    fl = fl[fl["target_date"].astype(str) == tom.date().isoformat()]
    if fl.empty:
        raise RuntimeError("no forecast for tomorrow yet")
    fc = float(fl.iloc[-1]["predicted_price"])
    mk = float(elexon_daily_peak_price(today.date() - dt.timedelta(days=2),
                                       today.date() - dt.timedelta(days=1)).sort_index().iloc[-1])
    sp = round(fc - mk, 2)
    row.update({"forecast": round(fc, 2), "market": round(mk, 2), "spread": sp,
                "lean": "LONG" if sp > THRESHOLD else ("SHORT" if sp < -THRESHOLD else "FLAT")})
    print(f"forecast {fc:.2f} | market {mk:.2f} | spread {sp:+.2f} -> {row['lean']}")
except Exception as e:
    row["status"] = f"spread skipped: {type(e).__name__}"
    print("spread skipped:", e)


# ---------- 4. write OR UPDATE the row for tomorrow ----------
mask = log["target_date"].astype(str) == tom.date().isoformat()

if mask.any():
    idx = log.index[mask][-1]
    # fill the spread only if it was previously blank and we now have one
    if str(log.at[idx, "spread"]).strip() == "" and row["spread"] != "":
        for k in ["forecast", "market", "spread", "lean", "status"]:
            log.at[idx, k] = row[k]
        print("updated existing row for", tom.date(), "with spread")
    # always refresh the risk numbers - they move through the day
    for k in ["daily_vol_pct", "var_ref_100mwh", "max_size_at_limit"]:
        log.at[idx, k] = row[k]
    print("refreshed risk numbers for", tom.date())
else:
    log = pd.concat([log, pd.DataFrame([row])], ignore_index=True)
    print("logged new row:", row)

log[COLS].to_csv(LOG, index=False)


# ---------- 5. running scorecard ----------
traded = log[(pd.to_numeric(log["signal_pnl"], errors="coerce").notna()) &
             (log["lean"].isin(["LONG", "SHORT"]))]
if len(traded):
    pnl = pd.to_numeric(traded["signal_pnl"], errors="coerce")
    print(f"\n--- live signal scorecard: {len(traded)} trades ---")
    print(f"net P&L per MWh: {pnl.sum():+.2f} | win rate: {100*(pnl>0).mean():.0f}%")
    if len(traded) < 30:
        print("(sample too small to mean anything yet - do not read into it)")
