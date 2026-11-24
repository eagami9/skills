---
name: il_health_reimbursement
description: Verify Israeli supplementary and private insurance reimbursement for a private specialist before booking, so the net cost you quote is the cost the user will actually pay.
---

# Check Israeli Private Specialist Reimbursement Before Booking

## Rank fit before price

- Start from the clinical fit the user asked for, such as the relevant subspecialty, and rank named doctors on fit first.

- Ask the user which fit factor matters most when two doctors fit differently, such as speed, location or subspecialty, before you rank on price.

- Keep the fit ranking separate from the money ranking, and do not let a cheaper copay promote a worse fit.

## Verify eligibility in the claim system

- Treat the insurer general web page as background only, and never use it as proof that a named doctor is reimbursable.

- Check each named doctor in the insurer claim system itself, or by phone to the insurer, before you state any reimbursement figure.

- Remember that a doctor on the arrangement list may be barred from the reimbursement track for the same consultation, so an arrangement listing is not reimbursement eligibility.

- Record the exact track for each doctor, arrangement or reimbursement, with the source and the date you checked it.

- Own the error at once and correct the figure when the claim system contradicts an earlier general page answer.

## Price the visit from the actual policy

- Price the visit from the user actual policy document or insurer portal, and never from an example policy found online.

- Read the cap, the yearly limit, the deductible and any rule that waives the deductible after a supplementary fund claim, and quote each figure with its source section.

- Show the stacking arithmetic step by step, naming what each payer covers and what remains, and mark any step that is still unconfirmed.

- Ask the insurer or the broker in writing when a stacking step is unconfirmed, and do not present it as settled until it is confirmed.

- Keep the net cost as a range when a figure depends on an unconfirmed step, and say which confirmation would settle it.

## Re-verify the slot and confirm before paying

- Re-verify a displayed appointment slot shortly before the user acts on it, because displayed slots go stale within hours.

- When a clinic confirmation and the user diary disagree by a few minutes, aim for the earlier time.

- Tell the user what to bring for the claim, such as the list of treatments tried with dates, photos from the start and an original tax invoice and visit summary.

- Do not tell the user to pay a full private price on the promise of later reimbursement until the claim system check and the stacking confirmation both support it.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Websites

- [Dorbit](https://www.dorbit.co.il/) for the user group policy and online claims when the user policy is held there. Carry the policy dates, the consultation cap, the yearly limit and the deductible rule into the price calculation, and verify each figure in the portal.

## Alternatives for better results

- Ask the user to phone the insurer helpline when the claim system is unclear, and record the answer with the date.

- Compare a nearby arrangement doctor with a fast slot against a better fit reimbursement doctor with a later slot, and let the user choose the trade off.

- Suggest the user ask the clinic for the full private price in writing before booking, so the stacking arithmetic uses a real figure.
