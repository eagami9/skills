#!/usr/bin/env python3
"""Technical analysis from Yahoo Finance chart data (no API key).

Usage:
    python3 ta.py SYMBOL [--range 1y] [--interval 1d] [--json out.json]

Fetches daily OHLCV from the Yahoo Finance v8 chart endpoint, which was
verified reachable on 2026-11-19 (Stooq is JS-blocked in sandboxed
environments; quoteSummary needs a crumb). Computes SMA 20/50/200, EMA 12/26, MACD
(12,26,9), RSI 14 (Wilder), ATR 14, volume vs its 20-day average, 60-day
and 52-week high/low, and trailing returns. Prints a verbose text summary
so every figure can be checked against its source.

Indicators are computed on the split- and dividend-adjusted close, so
splits do not fake a trend break. The last price shown is the adjusted
close of the last session.
"""

import argparse
import json
import sys
import urllib.request
from datetime import datetime, timezone

import numpy as np
import pandas as pd

UA = {"User-Agent": "Mozilla/5.0"}


def fetch(symbol, range_, interval):
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        f"?range={range_}&interval={interval}"
    )
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as resp:
        status = resp.status
        payload = json.load(resp)
    if status != 200:
        raise RuntimeError(f"Yahoo chart API returned HTTP {status}")
    result = payload["chart"]["result"]
    if not result:
        raise RuntimeError(f"no chart data for {symbol}: {payload['chart'].get('error')}")
    return url, status, result[0]


def rsi_wilder(close, period=14):
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, adjust=False).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def build_frame(raw):
    ts = raw["timestamp"]
    quote = raw["indicators"]["quote"][0]
    adj = raw["indicators"].get("adjclose", [{}])[0].get("adjclose")
    df = pd.DataFrame(
        {
            "date": [datetime.fromtimestamp(t, tz=timezone.utc).date() for t in ts],
            "open": quote["open"],
            "high": quote["high"],
            "low": quote["low"],
            "close": quote["close"],
            "volume": quote["volume"],
            "adjclose": adj if adj else quote["close"],
        }
    )
    return df.dropna(subset=["adjclose"])


def analyze(df):
    close = df["adjclose"]
    out = {}
    out["last_date"] = str(df["date"].iloc[-1])
    out["last_close"] = round(float(close.iloc[-1]), 2)
    out["sessions"] = len(df)
    for n in (20, 50, 200):
        out[f"sma{n}"] = round(float(close.rolling(n).mean().iloc[-1]), 2)
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    out["ema12"] = round(float(ema12.iloc[-1]), 2)
    out["ema26"] = round(float(ema26.iloc[-1]), 2)
    out["macd"] = round(float(macd.iloc[-1]), 2)
    out["macd_signal"] = round(float(signal.iloc[-1]), 2)
    out["macd_hist"] = round(float((macd - signal).iloc[-1]), 2)
    out["macd_hist_prev"] = round(float((macd - signal).iloc[-2]), 2)
    out["rsi14"] = round(float(rsi_wilder(close).iloc[-1]), 1)
    tr = pd.concat(
        [
            df["high"] - df["low"],
            (df["high"] - close.shift()).abs(),
            (df["low"] - close.shift()).abs(),
        ],
        axis=1,
    ).max(axis=1)
    out["atr14"] = round(float(tr.rolling(14).mean().iloc[-1]), 2)
    vol = df["volume"]
    out["volume_last"] = int(vol.iloc[-1])
    out["volume_avg20"] = int(vol.rolling(20).mean().iloc[-1])
    out["volume_ratio"] = round(float(vol.iloc[-1] / vol.rolling(20).mean().iloc[-1]), 2)
    recent = df.tail(60)
    out["high_60d"] = round(float(recent["high"].max()), 2)
    out["low_60d"] = round(float(recent["low"].min()), 2)
    out["high_52w"] = round(float(df.tail(252)["high"].max()), 2)
    out["low_52w"] = round(float(df.tail(252)["low"].min()), 2)
    out["dist_52w_high_pct"] = round(float(close.iloc[-1] / out["high_52w"] - 1) * 100, 1)
    out["dist_52w_low_pct"] = round(float(close.iloc[-1] / out["low_52w"] - 1) * 100, 1)
    for label, n in (("1m", 21), ("3m", 63), ("6m", 126), ("1y", 252)):
        if len(df) > n:
            out[f"return_{label}_pct"] = round(
                float(close.iloc[-1] / close.iloc[-1 - n] - 1) * 100, 1
            )
    if "return_1y_pct" not in out and len(df) > 1:
        out["return_max_pct"] = round(
            float(close.iloc[-1] / close.iloc[0] - 1) * 100, 1
        )
        out["return_max_sessions"] = len(df) - 1
    out["price_vs_sma50"] = round(float(close.iloc[-1] / out["sma50"] - 1) * 100, 1)
    out["price_vs_sma200"] = round(float(close.iloc[-1] / out["sma200"] - 1) * 100, 1)
    out["sma50_vs_sma200_pct"] = round(float(out["sma50"] / out["sma200"] - 1) * 100, 1)
    return out


def verdict(a):
    lines = []
    if a["last_close"] > a["sma50"] and a["sma50"] > a["sma200"]:
        lines.append("Price above SMA50 above SMA200, an uptrend on both horizons.")
    elif a["last_close"] < a["sma50"] and a["sma50"] < a["sma200"]:
        lines.append("Price below SMA50 below SMA200, a downtrend on both horizons.")
    elif a["last_close"] < a["sma50"] and a["last_close"] < a["sma200"]:
        lines.append(
            "Price below SMA50 and SMA200, a short-term downtrend, "
            "but SMA50 is still above SMA200, so no death cross yet."
        )
    elif a["last_close"] > a["sma50"] and a["last_close"] > a["sma200"]:
        lines.append(
            "Price above SMA50 and SMA200, a short-term uptrend, "
            "but SMA50 is still below SMA200, so no golden cross yet."
        )
    else:
        lines.append("Price and moving averages disagree, no clean trend.")
    if a["rsi14"] >= 70:
        lines.append(f"RSI {a['rsi14']} is overbought (70 or higher).")
    elif a["rsi14"] <= 30:
        lines.append(f"RSI {a['rsi14']} is oversold (30 or lower).")
    else:
        lines.append(f"RSI {a['rsi14']} is neutral (between 30 and 70).")
    if a["macd_hist"] > 0 and a["macd_hist_prev"] <= 0:
        lines.append("MACD histogram just crossed up through zero.")
    elif a["macd_hist"] < 0 and a["macd_hist_prev"] >= 0:
        lines.append("MACD histogram just crossed down through zero.")
    elif a["macd_hist"] > 0:
        lines.append("MACD histogram is positive and rising" if a["macd_hist"] > a["macd_hist_prev"] else "MACD histogram is positive but falling.")
    else:
        lines.append("MACD histogram is negative and falling" if a["macd_hist"] < a["macd_hist_prev"] else "MACD histogram is negative but rising.")
    lines.append(
        f"Last session volume was {a['volume_ratio']}x the 20-day average."
    )
    lines.append(
        f"Price sits {a['dist_52w_high_pct']}% below its 52-week high "
        f"and {a['dist_52w_low_pct']}% above its 52-week low."
    )
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("symbol")
    ap.add_argument("--range", default="1y", dest="range_")
    ap.add_argument("--interval", default="1d")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    symbol = args.symbol.upper()
    try:
        url, status, raw = fetch(symbol, args.range_, args.interval)
    except urllib.error.HTTPError as e:
        print(f"error: Yahoo chart API returned HTTP {e.code} for {symbol}.")
        print("Yahoo covers US-listed stocks and ETFs. TASE-traded funds are")
        print("not on Yahoo; use the TASE maya pages instead, see the skill.")
        return 1
    except urllib.error.URLError as e:
        print(f"error: could not reach Yahoo chart API: {e.reason}")
        return 1
    meta = raw["meta"]
    df = build_frame(raw)
    a = analyze(df)

    print(f"symbol: {symbol} ({meta.get('longName', meta.get('shortName', ''))})")
    print(f"source: {url}")
    print(f"http_status: {status}")
    print(f"sessions: {a['sessions']} (range {args.range_}, interval {args.interval})")
    print(f"last_session: {a['last_date']}  currency: {meta.get('currency')}")
    print(f"last_close_adj: {a['last_close']}")
    print(f"sma20: {a['sma20']}  sma50: {a['sma50']}  sma200: {a['sma200']}")
    print(f"ema12: {a['ema12']}  ema26: {a['ema26']}")
    print(f"macd: {a['macd']}  signal: {a['macd_signal']}  hist: {a['macd_hist']} (prev {a['macd_hist_prev']})")
    print(f"rsi14: {a['rsi14']}  atr14: {a['atr14']}")
    print(f"volume_last: {a['volume_last']:,}  volume_avg20: {a['volume_avg20']:,}  ratio: {a['volume_ratio']}x")
    print(f"high_60d: {a['high_60d']}  low_60d: {a['low_60d']}")
    print(f"high_52w: {a['high_52w']}  low_52w: {a['low_52w']}")
    for label in ("1m", "3m", "6m", "1y"):
        key = f"return_{label}_pct"
        if key in a:
            print(f"return_{label}: {a[key]}%")
    if "return_max_pct" in a:
        print(f"return_max: {a['return_max_pct']}% over {a['return_max_sessions']} sessions (full year not in range)")
    print(f"price_vs_sma50: {a['price_vs_sma50']}%  price_vs_sma200: {a['price_vs_sma200']}%")
    print("read:")
    for line in verdict(a):
        print(f"  - {line}")
    print("limits: indicators describe the past, they do not predict the next move.")
    print("A single indicator never decides anything on its own.")

    if args.json:
        with open(args.json, "w") as f:
            json.dump({"symbol": symbol, "source": url, **a}, f, indent=2)
        print(f"json_written: {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
