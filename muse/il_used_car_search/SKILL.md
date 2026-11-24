---
name: il_used_car_search
description: Find and verify a used car in Israel against the user hard filters, checking each listing and its plate history before presenting it.
---

# Search for a Used Car in Israel

## Collect the hard filters first

- Collect the budget ceiling, mileage cap, ownership exclusions, brand exclusions, fuel or powertrain, and distance limit before you search.

- Treat each stated filter as a hard filter, not a preference, and keep the full list where you can recheck it against every candidate.

- Audit any list handed to you against the filters before you present it, including a list from another agent, and drop every listing that breaks a filter.

- Record a new exclusion the moment the user states it, remove the candidates it disqualifies, and name the new leading candidate.

- Check the distance and travel time from the user home city before you present a candidate as a leader, and drop a candidate that is too far to visit.

## Verify each listing in the ad itself

- Open the ad itself and verify the price, mileage, year, hand, ownership history, test validity, and location before you present the candidate.

- Verify the powertrain from the ad specification, such as battery size and electric range, and check horsepower when the fuel type is in doubt, because a site fuel filter does not reliably filter.

- Mark a fact as unverified when the site blocks the ad, and recheck it later instead of repeating the earlier listing as verified.

- Record a price cut with the earlier price when the ad shows one, and treat the ad mileage as a claim until an official reading confirms it.

- Note the contact route and the seller availability, and use the platform chat or a weekday when a phone call is unlikely to be answered.

## Run the plate checks

- Read the full plate from the car photos when the ad text hides it.

- Run the free registration check by plate, for example through CARFACT, for the year, hand, test mileage, licence validity, open recalls, recorded changes, and rental or leasing or taxi history.

- Run the free Israel Police stolen vehicle check by plate and report the result.

- Ask the seller to order or show the insurance history report, because only the registered owner can order it, and remember that a rental or leasing car may lack comprehensive insurance so some accidents may not appear there.

- Check the Pledges Registrar by plate for a lien, and remember that a lien stays with the car after ownership transfers.

- Let the user complete any login code in a browser takeover and resume after, and never ask the user to send you a login code in chat.

- Present the plate findings plainly, including a mileage gap between the ad and the official test reading, the ownership history, the test expiry, and anything the photos show, and name what you did not check.

## Ask only questions you can act on

- Ask only a question the user can answer or you can act on, such as whether leasing is also excluded or whether a distance is acceptable.

- Do not ask the user which car to check first when you cannot contact a seller or inspect a car, and present the verified comparison instead.

- State plainly what you can do, such as read the ad and run the plate checks, and what you cannot do, such as call a seller or inspect a car.

- Restate the choice in plain terms when the user says your question is unclear, and do not repeat the same question.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Websites

- [Yad2](https://www.yad2.co.il/) for used car listings in Israel. Carry the budget, mileage cap, ownership exclusions, and home city into the search, and verify each listing in the ad itself.

## Alternatives for better results

- Ask the seller to show the insurance history and the lien screen from the owner personal area when you cannot order those checks yourself.

- Compare a dealer or trade in offer when warranty or convenience matters more than the lowest price.

- Wait for a better listing when the user can wait, instead of settling for a weak match.
