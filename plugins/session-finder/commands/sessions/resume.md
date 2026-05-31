---
description: Get the command to resume a past Claude Code session.
argument-hint: "[<session-id> | here | <words>]"
---

Use the **session-finder** skill to hand me the command to resume a session.

Request: `$ARGUMENTS`

Run the bundled script (use `python` instead of `python3` on Windows):
`python3 ${CLAUDE_PLUGIN_ROOT}/skills/session-finder/scripts/sessions.py resume`

Interpret the request:

- Empty → `resume` (the most recent session overall).
- `here` → `resume --here` (the most recent session in this project).
- A uuid-like token → `resume <id>` (that specific session).
- Free-text words → run `search "<words>"` first, then `resume <id>` for the
  best match; show me the match before handing over the command.

Then give me the exact line the script prints — `claude --resume <id>`
(prefixed with `cd <project> &&` when the session is in another directory).

Note: this hands you the command to run; it does not swap the live
conversation in place the way the built-in `/resume` does. Run the printed
command in your terminal / IDE to actually resume. Never invent session ids.
