---
name: live_source_check
description: Check the user's named live source before dismissing a price, quote or figure they cite that disagrees with your other sources.
---

# Verify a Live Figure Before Contradicting It

## Check the named source first

- Open the source the user named before you answer when the user cites a live figure from it.

- Read the figure, its timestamp and its session label on that source, such as pre-market, regular session or after hours.

- Treat the user's own screen, cart or app as the ground truth for what that source shows them, and re-check it live instead of defending a different source.

- Use `browser.open` for a recent copy first and start a live browser task with `browser.browse` when the copy is stale, blocked or does not settle the figure.

## Reconcile a disagreement before calling it broken

- Compare timestamps before you compare figures, because a quote from before an announcement and a quote from after it can both be correct at their own times.

- Search for breaking news about the subject in the same window when two live sources disagree by a large amount.

- Do not call a feed broken, stale or wrong from one conflicting source alone, and do not present the lower or earlier figure as the current one.

- Say which source showed which figure at which time when you cannot reconcile them, and ask the user to confirm what their source shows now.

## Present what you found

- State the named source, the figure you read there, its timestamp and any news that explains the move, before you give your own reading.

- Own the earlier dismissal plainly and withdraw the wrong figure when a live check proves it wrong.

- Keep the corrected figure and its source in the record so the next check starts from it.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Websites

- [Yahoo Finance](https://finance.yahoo.com/) for a live quote with its timestamp and pre-market or after-hours label. Carry the exact ticker and the figure the user cited into the browser task and verify the quote, the change and the time it was taken.

- [Finviz](https://finviz.com/) for a second quote and a quick news scan when a figure looks like an outlier. Carry the ticker and the time window and verify whether the quote predates an announcement.

## Alternatives for better results

- Ask the user what their source shows now when live sources still disagree after a fresh check, instead of picking one source and dismissing the other.

- Check the news first when a move is large, because a reinstatement, resignation or earnings release explains an outlier more often than a broken feed does.
