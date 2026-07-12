# scorecard.py - the honest performance record. Writes SCORECARD.md (renders on GitHub).
#
# TWO SEPARATE SCORECARDS, deliberately not mixed:
#   A. FORECAST ACCURACY  - is the model right? (MAE, RMSE, directional accuracy, vs benchmarks)
#   B. SIGNAL PERFORMANCE - does acting on it make money? (hit rate, net P&L, drawdown, VaR breaches)
# A model can be accurate and still lose money, because the market already priced it in.
# Conflating these two is how people talk themselves into bad trades.
import os, datetime as dt
import numpy as np, pandas as pd, requests

PRICE_LOG_URL = os.environ.get("FORECAST_LOG_URL", "")
DESK_LOG      = "desk_log.csv"
COST_PER_MWH  = 1.0
MIN_SAMPLE    = 20        # below this, refuse to draw conclusions

today = dt.date.today()
L = []
A = L.append


def daily_peak_price(start, end):
    rows=[]; d=start
    while d<=end:
        d2=min(d+dt.timedelta(days=6), end)
        u=("https://data.elexon.co.uk/bmrs/api/v1/balancing/pricing/market-index"
           f"?from={d}T00:00Z&to={d2}T23:59Z&format=json")
        try: rows += requests.get(u, timeout=60).json().get("data", [])
        except Exception: pass
        d=d2+dt.timedelta(days=1)
    rows=[x for x in rows if x.get("dataProvider")=="APXMIDP"]
    if not rows: return pd.Series(dtype=float)
    df=pd.DataFrame(rows)
    df["settlementDate"]=pd.to_datetime(df["settlementDate"]).dt.date
    df["price"]=pd.to_numeric(df["price"],errors="coerce")
    return df.groupby("settlementDate")["price"].max().sort_index()


A("# Performance Scorecard")
A(f"_Auto-generated {today.isoformat()}. Live, forward, out-of-sample. Not a backtest._\n")
A("> Two scorecards below, kept separate on purpose. **Accuracy** asks whether the forecast is right. "
  "**Signal performance** asks whether acting on it makes money after costs. These are different questions, "
  "and a model can pass the first while failing the second.\n")

# =====================================================================
# A. FORECAST ACCURACY
# =====================================================================
A("## A. Forecast accuracy (price model)\n")
try:
    fl = pd.read_csv(PRICE_LOG_URL)
    fl = fl[pd.to_numeric(fl["actual_price"], errors="coerce").notna()].copy()
    fl["target_date"] = pd.to_datetime(fl["target_date"]).dt.date
    fl["predicted_price"] = pd.to_numeric(fl["predicted_price"], errors="coerce")
    fl["actual_price"]    = pd.to_numeric(fl["actual_price"], errors="coerce")
    fl = fl.dropna(subset=["predicted_price","actual_price"]).sort_values("target_date")

    n = len(fl)
    if n == 0:
        A("_No graded forecasts yet. The price pipeline grades itself daily; check back once it has._\n")
    else:
        lo = fl["target_date"].min() - dt.timedelta(days=10)
        hi = fl["target_date"].max()
        hist = daily_peak_price(lo, hi)

        # benchmarks, each computed only from information available before the target day
        def bench(d, kind):
            try:
                if kind == "yesterday":   return float(hist.loc[d - dt.timedelta(days=1)])
                if kind == "last_week":   return float(hist.loc[d - dt.timedelta(days=7)])
                if kind == "avg7":
                    w = [hist.loc[d - dt.timedelta(days=k)] for k in range(1,8) if (d - dt.timedelta(days=k)) in hist.index]
                    return float(np.mean(w)) if w else np.nan
            except KeyError:
                return np.nan
            return np.nan

        fl["b_yesterday"] = [bench(d,"yesterday") for d in fl["target_date"]]
        fl["b_last_week"] = [bench(d,"last_week") for d in fl["target_date"]]
        fl["b_avg7"]      = [bench(d,"avg7")      for d in fl["target_date"]]

        def mae(a,b):  return float(np.nanmean(np.abs(a-b)))
        def rmse(a,b): return float(np.sqrt(np.nanmean((a-b)**2)))

        act = fl["actual_price"].values
        rows = [("**Model**", fl["predicted_price"].values),
                ("Benchmark: yesterday's price", fl["b_yesterday"].values),
                ("Benchmark: 7-day average",     fl["b_avg7"].values),
                ("Benchmark: same day last week",fl["b_last_week"].values)]

        A(f"Graded days: **{n}**"
          + ("  \n_Sample below 20 - treat every number here as provisional._\n" if n < MIN_SAMPLE else "\n"))
        A("| model / benchmark | MAE (£/MWh) | RMSE (£/MWh) |")
        A("|---|---|---|")
        for name, pred in rows:
            if np.all(np.isnan(pred)): continue
            A(f"| {name} | {mae(act,pred):.2f} | {rmse(act,pred):.2f} |")
        A("")

        # directional accuracy: did we get the direction of change right vs yesterday?
        prev = fl["b_yesterday"].values
        ok = ~np.isnan(prev)
        if ok.sum():
            dir_actual = np.sign(act[ok] - prev[ok])
            dir_pred   = np.sign(fl["predicted_price"].values[ok] - prev[ok])
            da = 100 * float(np.mean(dir_actual == dir_pred))
            A(f"**Directional accuracy:** {da:.0f}% (did we call up/down correctly vs yesterday, over {int(ok.sum())} days)\n")

        err = fl["predicted_price"] - fl["actual_price"]
        A(f"**Bias:** {err.mean():+.2f} £/MWh "
          + ("(over-forecasting)" if err.mean()>0 else "(under-forecasting)") + "\n")

        beat = mae(act, fl["predicted_price"].values) < mae(act, fl["b_yesterday"].values)
        A(f"**Verdict:** the model {'BEATS' if beat else 'does NOT beat'} the persistence benchmark on MAE"
          + (" - but the sample is small.\n" if n < MIN_SAMPLE else ".\n"))
except Exception as e:
    A(f"_Accuracy section unavailable ({type(e).__name__})._\n")

# =====================================================================
# B. SIGNAL PERFORMANCE
# =====================================================================
A("## B. Signal performance (does acting on it pay?)\n")
try:
    if not os.path.exists(DESK_LOG):
        raise FileNotFoundError(DESK_LOG)
    dl = pd.read_csv(DESK_LOG)
    dl["signal_pnl"] = pd.to_numeric(dl["signal_pnl"], errors="coerce")
    traded = dl[(dl["lean"].isin(["LONG","SHORT"])) & (dl["signal_pnl"].notna())]
    flat   = dl[dl["lean"] == "FLAT"]
    nt = len(traded)

    A(f"Signal frequency: **{nt}** LONG/SHORT, **{len(flat)}** FLAT (no trade)\n")
    if nt == 0:
        A("_No completed trades yet. A signal that rarely fires is not a fault: it means we rarely disagree "
          "with the market by enough to act._\n")
    else:
        pnl = traded["signal_pnl"]
        cum = pnl.cumsum()
        dd  = float((cum - cum.cummax()).min())
        A("| metric | value |")
        A("|---|---|")
        A(f"| trades | {nt} |")
        A(f"| hit rate | {100*(pnl>0).mean():.0f}% |")
        A(f"| net P&L (per MWh, after £{COST_PER_MWH} cost) | {pnl.sum():+.2f} |")
        A(f"| average trade | {pnl.mean():+.2f} |")
        A(f"| best / worst | {pnl.max():+.2f} / {pnl.min():+.2f} |")
        A(f"| max drawdown | {dd:,.2f} |")
        A("")
        if nt < MIN_SAMPLE:
            A(f"**Verdict: too few trades ({nt}) to conclude anything.** Numbers this small are noise. "
              "No edge is claimed.\n")
        elif pnl.sum() <= 0:
            A("**Verdict: no edge after costs.** The market is not fooled by this signal. "
              "This is a legitimate finding, not a failure - and the signal should not be traded.\n")
        else:
            A("**Verdict: positive after costs**, on this sample. Treat with caution until the sample is large.\n")

    # VaR breach check - the honest test of the risk model itself
    dl["var_ref"] = pd.to_numeric(dl["var_ref_100mwh"], errors="coerce")
    chk = dl[(dl["signal_pnl"].notna()) & (dl["var_ref"].notna())]
    if len(chk):
        # signal_pnl is per MWh; the reference VaR is for 100 MWh
        loss_100 = -chk["signal_pnl"] * 100.0
        breaches = int((loss_100 > chk["var_ref"]).sum())
        rate = 100 * breaches / len(chk)
        A(f"**VaR breaches:** {breaches} of {len(chk)} days ({rate:.0f}%). "
          f"A 95% VaR should be exceeded about 5% of the time. "
          + ("Materially more than that means the VaR is understating the tail, which is expected "
             "in this market: parametric VaR assumes normal returns and power prices spike.\n"
             if rate > 8 else "In line with expectation.\n"))
except Exception as e:
    A(f"_Signal section unavailable ({type(e).__name__})._\n")

A("## Method notes\n")
A("- Everything here is **forward-looking**: the forecast and the signal were recorded before the outcome was known. "
  "A forward record cannot be curve-fitted, unlike a backtest.")
A("- Benchmarks use only information available before the target day.")
A("- Accuracy and profitability are reported separately, on purpose.")
A(f"- No conclusion is drawn below {MIN_SAMPLE} observations.")

open("SCORECARD.md","w").write("\n".join(L))
print("wrote SCORECARD.md")
