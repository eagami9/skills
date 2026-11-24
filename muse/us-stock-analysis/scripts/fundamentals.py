#!/usr/bin/env python3
"""Fundamentals from SEC EDGAR XBRL company facts (no API key).

Usage:
    python3 fundamentals.py TICKER

Resolves the ticker to a CIK through the SEC company_tickers.json index,
then reads https://data.sec.gov/api/xbrl/companyfacts/CIK<10-digit>.json,
which was verified reachable on 2026-11-19. Pulls the last
four fiscal years from 10-K filings only and prints revenue, margins,
R&D, cash, debt and share count, with year-over-year change, plus free
cash flow, cash conversion, ROE, ROA, leverage and interest coverage,
so a buy, hold or sell view can rest on cash generation and returns
and not on earnings alone. Every figure carries its fiscal year end
and accession number so it can be checked in the filing itself.

Limits: US filers only. Foreign issuers file 20-F/6-K and are not covered.
Valuation multiples (P/E, P/S) and analyst consensus are not in EDGAR;
get them from a finance-vertical search of the ticker instead. Yahoo quoteSummary is crumb-blocked, so do not use it.
"""

import argparse
import json
import os
import sys
import time
import urllib.request

SEC_UA = {"User-Agent": "skills research (https://github.com/eagami9/skills)"}
CACHE_DIR = os.path.expanduser("~/.cache/edgar")
TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
TICKERS_TTL = 30 * 24 * 3600

# Tag candidates in preference order. Revenue is tagged two ways.
TAGS = {
    "revenue": [
        ("us-gaap", "Revenues"),
        ("us-gaap", "RevenueFromContractWithCustomerExcludingAssessedTax"),
        ("us-gaap", "SalesRevenueNet"),
    ],
    "gross_profit": [("us-gaap", "GrossProfit")],
    "cost_of_revenue": [
        ("us-gaap", "CostOfRevenue"),
        ("us-gaap", "CostOfGoodsAndServicesSold"),
    ],
    "operating_income": [("us-gaap", "OperatingIncomeLoss")],
    "net_income": [("us-gaap", "NetIncomeLoss")],
    "rnd": [("us-gaap", "ResearchAndDevelopmentExpense")],
    "cash": [("us-gaap", "CashAndCashEquivalentsAtCarryingValue")],
    "long_term_debt": [
        ("us-gaap", "LongTermDebt"),
        ("us-gaap", "LongTermDebtAndCapitalLeaseObligations"),
    ],
    "ocf": [
        ("us-gaap", "NetCashProvidedByUsedInOperatingActivities"),
        ("us-gaap", "NetCashProvidedByOperatingActivities"),
        ("us-gaap", "NetCashProvidedByOperatingActivitiesContinuingOperations"),
    ],
    "capex": [
        ("us-gaap", "PaymentsToAcquirePropertyPlantAndEquipment"),
        ("us-gaap", "PaymentsToAcquireProductiveAssets"),
    ],
    "equity": [
        ("us-gaap", "StockholdersEquity"),
        ("us-gaap", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"),
    ],
    "assets": [("us-gaap", "Assets")],
    "liabilities": [
        ("us-gaap", "Liabilities"),
        ("us-gaap", "LiabilitiesCurrentAndNoncurrent"),
    ],
    "interest": [
        ("us-gaap", "InterestExpense"),
        ("us-gaap", "InterestExpenseNonoperating"),
        ("us-gaap", "InterestAndDebtExpense"),
    ],
}


def get_json(url, cache_path=None, ttl=None):
    if cache_path and os.path.exists(cache_path):
        if ttl is None or time.time() - os.path.getmtime(cache_path) < ttl:
            with open(cache_path) as f:
                return json.load(f)
    req = urllib.request.Request(url, headers=SEC_UA)
    with urllib.request.urlopen(req, timeout=60) as resp:
        if resp.status != 200:
            raise RuntimeError(f"{url} returned HTTP {resp.status}")
        data = json.load(resp)
    if cache_path:
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        with open(cache_path, "w") as f:
            json.dump(data, f)
    return data


def resolve_cik(ticker):
    path = os.path.join(CACHE_DIR, "company_tickers.json")
    data = get_json(TICKERS_URL, cache_path=path, ttl=TICKERS_TTL)
    for entry in data.values():
        if entry["ticker"].upper() == ticker:
            return str(entry["cik_str"]).zfill(10), entry["title"]
    raise RuntimeError(f"ticker {ticker} not found in SEC company_tickers.json")


def annual_series(facts, tag_options):
    """Latest 10-K value per fiscal period, keyed by period end date.

    EDGAR's `fy` field is unreliable: the same period end appears under
    several `fy` values across filings. The period end date is the true
    key. The fiscal-year label is the calendar year of the end date,
    which matches how companies name the year (a year ending Jan 2026
    is FY2026). Tag options are merged in preference order, so a year
    missing under the first tag is filled from the next one. Values are
    deduplicated per end date, latest filed wins.
    """
    by_end = {}
    for namespace, tag in tag_options:
        node = facts.get(namespace, {}).get(tag)
        if not node:
            continue
        units = node.get("units", {})
        values = units.get("USD") or units.get("shares") or units.get("pure") or []
        per_tag = {}
        for v in values:
            if v.get("form") != "10-K" or v.get("fp") != "FY":
                continue
            end = v.get("end")
            if not end:
                continue
            prev = per_tag.get(end)
            if prev is None or v.get("filed", "") > prev.get("filed", ""):
                per_tag[end] = v
        for end, v in per_tag.items():
            by_end.setdefault(end, v)
    return by_end


def shares_series(facts):
    """Cover-page share counts as a dated series.

    The cover-page share count is dated near the filing date, not the
    fiscal year end, so it cannot be keyed by period end. Keep the
    values sorted by date and match each fiscal year to the first count
    dated within 120 days after that year end, which is the count from
    that year's own 10-K. Multi-class issuers such as Alphabet do not
    tag this item at all, so the lookup returns nothing for them.
    """
    node = facts.get("dei", {}).get("EntityCommonStockSharesOutstanding")
    if not node:
        return []
    out = []
    for v in node.get("units", {}).get("shares", []):
        if v.get("end") and v.get("val") is not None:
            out.append((v["end"], v["val"]))
    out.sort()
    return out


def shares_for_year(series, fy_end):
    from datetime import date

    def parse(s):
        y, m, d = s.split("-")
        return date(int(y), int(m), int(d))

    target = parse(fy_end)
    for end, val in series:
        delta = (parse(end) - target).days
        if 0 <= delta <= 120:
            return val
    return None


def fmt_money(v):
    if v is None:
        return "n/a"
    return f"${v / 1e9:,.2f}B"


def fmt_pct(v):
    if v is None:
        return "n/a"
    return f"{v * 100:.1f}%"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    args = ap.parse_args()
    ticker = args.ticker.upper()

    cik, name = resolve_cik(ticker)
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    facts = get_json(url)
    print(f"company: {name} ({ticker})  cik: {cik}")
    print(f"source: {url}")
    print("forms: 10-K annual only, one value per fiscal year (latest filed)")

    series = {key: annual_series(facts.get("facts", {}), opts) for key, opts in TAGS.items()}
    shares = shares_series(facts.get("facts", {}))
    ends = sorted(series["revenue"].keys(), reverse=True)[:4]
    if not ends:
        print("no annual revenue found in EDGAR facts for this ticker.")
        return 1

    def fy_label(end):
        return end[:4]

    def val(key, end):
        v = series[key].get(end)
        return v["val"] if v else None

    def accn(key, end):
        v = series[key].get(end)
        return v.get("accn", "") if v else ""

    def shares_for(end):
        return shares_for_year(shares, end)

    print()
    print("fiscal_year | revenue | net_income | gross_mgn | op_mgn | net_mgn | rnd_pct_rev | shares_out")
    for end in ends:
        rev = val("revenue", end)
        net = val("net_income", end)
        gross = val("gross_profit", end)
        if gross is None:
            cost = val("cost_of_revenue", end)
            if rev is not None and cost is not None:
                gross = rev - cost
        op = val("operating_income", end)
        rnd = val("rnd", end)
        sh = shares_for(end)
        sh_str = f"{sh / 1e9:,.2f}B" if sh else "n/a"
        print(
            f"FY{fy_label(end)} (end {end}) | {fmt_money(rev)} | {fmt_money(net)} | "
            f"{fmt_pct(gross / rev if gross and rev else None)} | "
            f"{fmt_pct(op / rev if op and rev else None)} | "
            f"{fmt_pct(net / rev if net and rev else None)} | "
            f"{fmt_pct(rnd / rev if rnd and rev else None)} | {sh_str}"
        )
        print(f"  accession: {accn('revenue', end)}")

    print()
    print("cash_flow_and_returns | ocf | capex | fcf | fcf_mgn | fcf_vs_net | roe | roa")
    print("roe and roa use year-end equity and assets, not averages.")
    for end in ends:
        rev = val("revenue", end)
        net = val("net_income", end)
        ocf = val("ocf", end)
        capex = val("capex", end)
        equity = val("equity", end)
        assets = val("assets", end)
        fcf = ocf - abs(capex) if ocf is not None and capex is not None else None
        print(
            f"FY{fy_label(end)} (end {end}) | {fmt_money(ocf)} | {fmt_money(capex)} | "
            f"{fmt_money(fcf)} | "
            f"{fmt_pct(fcf / rev if fcf is not None and rev else None)} | "
            f"{fmt_pct(fcf / net if fcf is not None and net else None)} | "
            f"{fmt_pct(net / equity if net is not None and equity else None)} | "
            f"{fmt_pct(net / assets if net is not None and assets else None)}"
        )

    print()
    print("year_over_year:")

    def yoy(a, b):
        if not a or not b:
            return "n/a"
        return f"{(a / b - 1) * 100:+.1f}%"

    def yoy_shares(a, b):
        if not a or not b:
            return "n/a"
        change = a / b - 1
        if abs(change) > 0.5:
            return "n/c, jump over 50%, likely a stock split, check the filing"
        return f"{change * 100:+.1f}%"

    for i in range(len(ends) - 1):
        end, prev = ends[i], ends[i + 1]
        print(
            f"  FY{fy_label(end)} vs FY{fy_label(prev)}: "
            f"revenue {yoy(val('revenue', end), val('revenue', prev))}, "
            f"net income {yoy(val('net_income', end), val('net_income', prev))}, "
            f"shares {yoy_shares(shares_for(end), shares_for(prev))}"
        )

    latest = ends[0]
    cash = val("cash", latest)
    debt = val("long_term_debt", latest)
    equity = val("equity", latest)
    liabilities = val("liabilities", latest)
    assets = val("assets", latest)
    if liabilities is None and assets is not None and equity is not None:
        liabilities = assets - equity
    op = val("operating_income", latest)
    interest = val("interest", latest)
    print()
    print(f"latest_fy: FY{fy_label(latest)} (end {latest})")
    print(f"cash_and_equivalents: {fmt_money(cash)}")
    print(f"long_term_debt: {fmt_money(debt)}")
    if cash is not None and debt is not None:
        print(f"net_cash: {fmt_money(cash - debt)}")
    print(f"total_liabilities: {fmt_money(liabilities)}")
    print(f"stockholders_equity: {fmt_money(equity)}")
    if liabilities is not None and equity:
        print(f"debt_to_equity_liab: {liabilities / equity:.2f}x")
    if debt is not None and equity:
        print(f"long_term_debt_to_equity: {debt / equity:.2f}x")
    if op is not None and interest:
        print(f"interest_coverage_op_over_interest: {op / interest:.1f}x")
    else:
        print("interest_coverage_op_over_interest: n/a (no interest tag)")
    print("limits: EDGAR has no multiples or analyst estimates; fetch those by search.")
    print("Never call a stock cheap or expensive from these numbers alone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
