---
name: us-stock-analysis
description: Comprehensive US stock analysis including fundamental analysis (financial metrics, business quality, valuation), technical analysis (indicators, chart patterns, support/resistance), stock comparisons, and investment report generation. Data comes from verified local scripts (Yahoo Finance chart data and SEC EDGAR filings) first, web search second. Use when user requests analysis of US stock tickers (e.g., "analyze AAPL", "compare TSLA vs NVDA", "give me a report on Microsoft"), evaluation of financial metrics, technical chart analysis, or investment research for American stocks.
---

# US Stock Analysis

Adapted from tradermonty/claude-trading-skills (MIT License), with the data layer replaced by verified local scripts. The method, frameworks and reference files are the original work. The data commands below were verified on 2026-11-19.

## Overview

Perform comprehensive analysis of US stocks covering fundamental analysis (financials, business quality, valuation), technical analysis (indicators, trends, patterns), peer comparisons, and generate detailed investment reports. Fetch market data with the scripts in `scripts/` first, and use web search only for what the scripts cannot give (multiples, analyst consensus, news).

## Prerequisites

- **API keys:** None required.
- **Tools:** `muse.exec` to run the scripts, `browser.search` with the finance vertical for multiples, consensus and news.
- **Data:** The user provides the ticker or question, and may add their own data such as fundamentals or chart images.
- **Python:** 3.12 with pandas and numpy. No other packages needed.

## Data Sources

Run the scripts before searching. They print their source URL, HTTP status, raw values and dates, so every figure can be checked. Never quote an indicator or a filing figure from memory or from a search snippet when the script can compute it.

**Primary data, from the scripts:**

1. **Technical data.** Run `python3 scripts/ta.py <TICKER>` (default range 1y, daily). It fetches daily OHLCV from the Yahoo Finance v8 chart endpoint and computes SMA 20/50/200, EMA 12/26, MACD (12,26,9), RSI 14 (Wilder), ATR 14, volume vs its 20-day average, 60-day and 52-week high/low, and trailing returns. Indicators use the split- and dividend-adjusted close.
2. **Fundamental data.** Run `python3 scripts/fundamentals.py <TICKER>`. It resolves the ticker to a CIK through the SEC index, reads the XBRL company facts from SEC EDGAR, and prints the last four fiscal years from 10-K filings only: revenue, net income, gross, operating and net margins, R&D share of revenue, share count, cash and long-term debt, plus free cash flow (operating cash flow minus capex), cash conversion (FCF vs net income), ROE, ROA, leverage and interest coverage, with year-over-year change and the accession number of each filing.

**Secondary data, from web search (finance vertical):**

3. **Valuation multiples** (trailing and forward P/E, P/S, EV/EBITDA) and **analyst ratings, price targets and consensus**. EDGAR has no multiples and no estimates, and the Yahoo quoteSummary endpoint is crumb-blocked, so search is the only route for these. Prefer MarketBeat, Gekko, Yahoo Finance or TrendMatrix pages dated within the last few days, and name the source and its date. When sources disagree, show the range instead of picking one number.
4. **Recent news and developments.** Search with the news vertical, and give the publication time with each item.

**Sources that do not work in sandboxed environments, do not use them:**

- Stooq CSV downloads are JS-blocked in sandboxed environments.
- Yahoo quoteSummary needs a crumb and returns Unauthorized.
- Yahoo Finance does not carry TASE-traded funds (HTTP 404 for a TASE fund number). This skill covers US-listed stocks only.

## Scope

- US-listed stocks and ETFs only. The scripts take any Yahoo ticker symbol, including indices such as ^GSPC.
- This skill is research and education. It is not licensed investment advice, and its Buy/Hold/Sell rating in a report is an analytical rating, not a personal recommendation to trade. Say so in any full report.
- Answer in the user's language.
- Technical indicators describe the past. They do not predict the next move, and a single indicator never decides anything on its own.

## Analysis Types

This skill supports four types of analysis. Determine which type(s) the user needs:

1. **Basic Stock Info** - Quick overview with key metrics
2. **Fundamental Analysis** - Deep dive into business, financials, valuation
3. **Technical Analysis** - Chart patterns, indicators, trend analysis
4. **Comprehensive Report** - Complete analysis combining all approaches

## Analysis Workflows

### 1. Basic Stock Information

**When to Use:** User asks for quick overview or basic info

**Steps:**
1. Run `scripts/ta.py` for current price, volume, 52-week range and trailing returns
2. Search for key metrics (P/E, EPS, revenue growth, margins) and market cap
3. Find recent news or major developments
4. Present in concise summary format

**Output Format:**
- Company description (1-2 sentences)
- Current price and trading metrics
- Key valuation metrics (table)
- Recent performance
- Notable recent news (if any)

### 2. Fundamental Analysis

**When to Use:** User wants financial analysis, valuation assessment, or business evaluation

**Steps:**
1. **Gather comprehensive financial data:**
   - Run `scripts/fundamentals.py` for revenue, earnings, margins, R&D, cash, debt and share count over four fiscal years
   - Search for free cash flow, ROE and ROIC, which EDGAR facts do not give directly

2. **Read references/fundamental-analysis.md** for analytical framework

3. **Read references/financial-metrics.md** for metric definitions and calculations

4. **Analyze business quality:**
   - Competitive advantages
   - Management track record
   - Industry position

5. **Perform valuation analysis:**
   - Search for key ratios (P/E, PEG, P/B, EV/EBITDA) and compare to historical averages and the peer group
   - Compare to peer group
   - Estimate fair value range

6. **Identify risks:**
   - Company-specific risks
   - Market/macro risks
   - Red flags from financial data

7. **Generate output** following references/report-template.md structure

**Critical Analyses:**
- Profitability trends (improving/declining margins)
- Cash flow quality (FCF vs earnings)
- Balance sheet strength (debt levels, liquidity)
- Growth sustainability
- Valuation vs peers and historical average

### 3. Technical Analysis

**When to Use:** User asks for technical analysis, chart patterns, or trading signals

**Steps:**
1. **Gather technical data:**
   - Run `scripts/ta.py` for price, volume, moving averages (20-day, 50-day, 200-day), RSI, MACD, ATR and support/resistance levels (60-day and 52-week high/low)

2. **Read references/technical-analysis.md** for indicator definitions and patterns

3. **Identify trend:**
   - Uptrend, downtrend, or sideways
   - Strength of trend

4. **Locate support and resistance levels:**
   - Recent highs and lows from the script output
   - Moving average levels
   - Round numbers

5. **Analyze indicators:**
   - RSI: Overbought (>70) or oversold (<30)
   - MACD: Crossovers and divergences
   - Volume: Confirmation or divergence
   - ATR: Volatility and stop-loss placement

6. **Identify chart patterns:**
   - Reversal patterns (head and shoulders, double top/bottom)
   - Continuation patterns (flags, triangles)

7. **Generate technical outlook:**
   - Current trend assessment
   - Key levels to watch
   - Risk/reward analysis
   - Short and medium-term outlook

**Interpretation Guidelines:**
- Confirm signals with multiple indicators
- Consider volume for validation
- Note divergences between price and indicators
- Always identify risk levels (stop-loss)

### 4. Comprehensive Investment Report

**When to Use:** User asks for detailed report, investment recommendation, or complete analysis

**Steps:**
1. **Perform data gathering** (run both scripts, then search for multiples, consensus and news)

2. **Execute fundamental analysis** (follow workflow above)

3. **Execute technical analysis** (follow workflow above)

4. **Read references/report-template.md** for complete report structure

5. **Synthesize findings:**
   - Integrate fundamental and technical insights
   - Develop bull and bear cases
   - Assess risk/reward

6. **Generate recommendation:**
   - Buy/Hold/Sell analytical rating
   - Target price with timeframe
   - Conviction level
   - Entry strategy

7. **Create formatted report** following template structure

**Report Must Include:**
- Executive summary with recommendation
- Company overview
- Investment thesis (bull and bear cases)
- Fundamental analysis section
- Technical analysis section
- Valuation analysis
- Risk assessment
- Catalysts and timeline
- Conclusion

## Forming an Opinion (Buy/Hold/Sell)

A rating is earned from four pillars, not from one number. Rate each pillar Strong, Neutral or Weak from the evidence, then apply the decision rules. Never let a single indicator, a single quarter, or the user's existing gain or loss decide the rating.

**Pillar 1: Business and cash generation.** Revenue growth and margin trend over four years, FCF margin, and cash conversion (FCF vs net income). Strong means growing revenue, stable or widening margins, FCF margin above 20%, and conversion above 80%. Weak means shrinking revenue, compressing margins, or conversion below 80%.

**Pillar 2: Balance sheet.** Net cash or leverage (liabilities to equity), and interest coverage (operating income over interest expense). Strong means net cash or leverage below 1x with coverage above 5x. Weak means leverage above 2x or coverage below 2.5x and falling.

**Pillar 3: Valuation.** Forward P/E against growth (PEG), against its own history and peers, and FCF yield, computed as latest fiscal year FCF from `fundamentals.py` divided by market cap (last price from `ta.py` times shares outstanding from `fundamentals.py`). Strong means a forward P/E below its history and peers, or a PEG below 1.5 for a grower. Weak means a forward P/E far above history and peers with no growth to justify it.

**Pillar 4: Technicals and timing.** Trend against SMA 50 and SMA 200, RSI, MACD histogram direction, volume, and distance from the 52-week high and low. Strong means price above SMA 50 above SMA 200 with rising momentum. Weak means price below both averages in a confirmed downtrend.

**Decision rules:**

- **Buy** when pillars 1 and 2 are Strong, pillar 3 is Strong or Neutral, and pillar 4 is not Weak. A dip-buy also qualifies when pillars 1 to 3 are Strong and pillar 4 is Weak but RSI is below 30 and the price closes above its 52-week low; intraday touches of the low do not count. Name the stop level in that case.
- **Hold** when the pillars conflict, for example a strong business with weak technicals, or when valuation is fair and nothing has changed. State what would upgrade the rating to Buy or downgrade it to Sell.
- **Sell** when the thesis breaks: margins compressing for two years, cash conversion below 80% for two consecutive years, leverage rising while coverage falls, or a better alternative with the same risk. A price fall alone is never a sell reason.

**Red lines that override a Buy:** an accounting restatement or fraud allegation, cash conversion below 80% for two consecutive years, or interest coverage below 2.5x and falling. When a red line is crossed, the rating is Hold at best until the filing explains it.

**Separate the rating from the position.** The rating is about the stock. The user's cost basis, holding size and paper gain or loss are reported separately and never flip the rating. Say which is which.

## Stock Comparison Analysis

**When to Use:** User asks to compare two or more stocks (e.g., "compare AAPL vs MSFT")

**Steps:**
1. **Gather data for all stocks:**
   - Run both scripts for each ticker
   - Search for multiples and consensus for each ticker
   - Ensure comparable timeframes

2. **Read references/fundamental-analysis.md** and references/financial-metrics.md

3. **Create side-by-side comparison:**
   - Business models comparison
   - Financial metrics table (all key ratios)
   - Valuation metrics table
   - Growth rates comparison
   - Profitability comparison
   - Balance sheet strength

4. **Identify relative strengths:**
   - Where each company excels
   - Quantified advantages

5. **Technical comparison:**
   - Relative strength
   - Momentum comparison
   - Which is in better technical position

6. **Generate recommendation:**
   - Which stock is more attractive and why
   - Consider both fundamental and technical factors
   - Portfolio allocation suggestion
   - Risk-adjusted return assessment

**Output Format:** Follow "Comparison Report Structure" in references/report-template.md

## Output Guidelines

**General Principles:**
- Use tables for financial data and comparisons (easy to scan)
- Bold key metrics and findings
- Include data sources and dates
- Quantify whenever possible
- Present both bull and bear perspectives
- Be clear about assumptions and uncertainties

**Formatting:**
- **Headers** for clear section separation
- **Tables** for metrics, comparisons, historical data
- **Bullet points** for lists, factors, risks
- **Bold text** for key findings, important metrics
- **Percentages** for growth rates, returns, margins
- **Currency** formatted consistently ($B for billions, $M for millions)

**Tone:**
- Objective and balanced
- Acknowledge uncertainty
- Support claims with data
- Avoid hyperbole
- Present risks clearly

## Reference Files

Load these references as needed during analysis:

**references/technical-analysis.md**
- When: Performing technical analysis or interpreting indicators
- Contains: Indicator definitions, chart patterns, support/resistance concepts, analysis workflow

**references/fundamental-analysis.md**
- When: Performing fundamental analysis or business evaluation
- Contains: Business quality assessment, financial health analysis, valuation frameworks, risk assessment, red flags

**references/financial-metrics.md**
- When: Need definitions or calculation methods for financial ratios
- Contains: All key metrics with formulas (profitability, valuation, growth, liquidity, leverage, efficiency, cash flow)

**references/report-template.md**
- When: Creating comprehensive report or comparison
- Contains: Complete report structure, formatting guidelines, section templates, comparison format

## Example Queries

**Basic Info:**
- "What's the current price of AAPL?"
- "Give me key metrics for Tesla"
- "Quick overview of Microsoft stock"

**Fundamental:**
- "Analyze NVDA's financials"
- "Is Amazon overvalued?"
- "Evaluate Apple's business quality"
- "What's Google's debt situation?"

**Technical:**
- "Technical analysis of TSLA"
- "Is Netflix oversold?"
- "Show me support levels for AAPL"
- "What's the trend for AMD?"

**Comprehensive:**
- "Complete analysis of Microsoft"
- "Give me a full report on AAPL"
- "Should I invest in Tesla? Give me detailed analysis"

**Comparison:**
- "Compare AAPL vs MSFT"
- "Tesla vs Nvidia - which is better?"
- "Analyze Meta vs Google"
