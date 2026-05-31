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

Important: this is a hand-off, not an in-place resume. When you present the
result, tell me explicitly to **run the printed command in my own terminal**
to resume — do NOT imply the current conversation has been switched (it has
not; a command can't swap its own live session the way built-in `/resume`
does). Never invent session ids.
