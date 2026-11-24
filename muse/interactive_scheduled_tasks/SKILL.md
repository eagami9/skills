---
name: interactive_scheduled_tasks
description: Design scheduled work that needs a one-time code or approval so it wakes the user for a live run instead of failing in a scheduled window.
---

# Scheduled tasks that need a login code

## Recognise an interactive task

- Treat a scheduled task as interactive when it needs a one-time code, an approval tap, a fresh login or a challenge that only the user can pass.

- Check whether the login session survives between browser windows before you promise an unattended run, and do not assume that it does.

- Treat a code that lives only a few minutes as a live task, because an approval card can arrive after the code has already expired.

- Do not try to type a code into a scheduled task window from another chat, because the system blocks that injection and the scheduled run stays stuck on the code page.

## Design the wake-up pattern

- Schedule a short prompt instead of the work itself when the task is interactive, and let the prompt ask whether to run the check live together.

- Keep the prompt time and add a backup prompt later when the user wants a second chance, and tell the user to ignore the backup when the live check already ran.

- Keep codes, phone numbers and identity numbers out of the scheduled task body, and collect each code live in chat only when the check runs.

- Tell the user before the run that a fresh code will arrive, that it expires in a few minutes and that the live check needs a quick reply.

## Run the check live

- Start the check in a live browser window in chat with `browser.browse`, and enter each code as soon as it arrives instead of waiting for an approval card.

- Stop a stuck scheduled run before you start the live run, so two runs do not request codes for the same login.

- Request a new code when the old one expires, and never reuse an expired code.

- Report only what the live check found, and book or pay for nothing unless the user approved that exact action.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Alternatives for better results

- Use an unattended scheduled run only when the whole task needs no login, code or approval, such as a public data refresh.

- Prefer a persistent login, an official API or a notification from the provider when one exists, and use the live check only while no such route exists.

- Offer once to file feedback with the Muse team when the platform itself blocks a code from reaching a scheduled run, and file it only after the user agrees.
