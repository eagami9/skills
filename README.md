# skills

A collection of agent skills, built for real use and shared openly. The Muse skills live under [`muse/`](muse/), with room for other agents' skills later.

אוסף סקילים לסוכני AI, שנבנו לשימוש אמיתי ומשותפים בפתיחות. הסקילים של Muse נמצאים תחת [`muse/`](muse/), ויש מקום לסקילים של סוכנים אחרים בהמשך.

## Skills / הסקילים

All skills below live under `muse/`.

| Skill | What it does |
| --- | --- |
| [ailist](muse/ailist/) | Read and update an [AIList](https://ai-list.web.app) household shopping list through its REST API. |
| [il-supermarket-compare](muse/il-supermarket-compare/) | Compare today's supermarket prices in Israel for a whole shopping list near an address, from the chains' official price-transparency files. |
| [il_espp_rsu_tax_check](muse/il_espp_rsu_tax_check/) | Verify realised capital gains and the correct ESPP/RSU cost basis before computing any tax saving from selling and rebuying shares in Israel. |
| [il_health_reimbursement](muse/il_health_reimbursement/) | Verify Israeli supplementary/private insurance reimbursement for a private specialist before booking, so the quoted net cost is the cost actually paid. |
| [il_used_car_search](muse/il_used_car_search/) | Find and verify a used car in Israel against hard filters, checking each listing and its plate history before presenting it. |
| [interactive_scheduled_tasks](muse/interactive_scheduled_tasks/) | Design scheduled work that needs a one-time code or approval so it wakes the user for a live run instead of failing in a scheduled window. |
| [live_source_check](muse/live_source_check/) | Check the user's named live source before dismissing a price, quote or figure they cite that disagrees with other sources. |
| [us-stock-analysis](muse/us-stock-analysis/) | Comprehensive US stock analysis: fundamentals from SEC EDGAR, technicals from Yahoo Finance chart data, valuation, comparisons and investment reports. |

## Install / התקנה

**Muse:** copy a skill folder from `muse/` into `~/workspace/custom-skills/`.

**Claude Code:** copy a skill folder from `muse/` into `~/.claude/skills/` for personal use, or `.claude/skills/` inside a project. See the [Claude Code skills guide](https://code.claude.com/docs/en/skills.md).

Some skills need Python 3 with `requests`, `pandas` and `numpy` (see each skill's SKILL.md). No API keys are needed for the data sources used here.

## Data sources / מקורות מידע

The Israeli skills use official public data sources: the supermarket chains' price-transparency files, published daily by law (חוק קידום התחרות בענף המזון); SEC EDGAR filings and Yahoo Finance chart data for US stocks. No comparison site is scraped.

## Attribution / קרדיט

- **us-stock-analysis** is adapted from [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills) (MIT License), with the data layer replaced by verified local scripts. The method, frameworks and reference files are the original work.
- **il-supermarket-compare** is adapted from Tamar Dobrin's `il-supermarket-compare` Claude Code plugin, in her public marketplace [tamardobrin/claude-plugins](https://github.com/tamardobrin/claude-plugins) (see also [dobrin.xyz/plugins](https://dobrin.xyz/plugins)).
- The remaining skills are original.

## License / רישיון

The original content of this repo is MIT licensed, see [LICENSE](LICENSE). Adapted skills keep the attribution above; `us-stock-analysis` is MIT licensed via its source. **Note: no license file was found in the `tamardobrin/claude-plugins` repo (checked 2026-11-24), so `il-supermarket-compare` is published here with credit to its author but without a license grant from her.**

## Disclaimer

These skills are research and workflow aids. They are not licensed investment, tax, legal or medical advice; the US stock analysis skill states this in its own text as well. Verify figures against their sources before acting on them.
