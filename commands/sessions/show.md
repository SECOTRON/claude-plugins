---
description: Outline or summarize one past Claude Code session by id.
argument-hint: "<session-id> [full]"
---

Use the **session-finder** skill to outline one Claude Code session.

Request: `$ARGUMENTS`

Run the bundled script:
`python3 ${CLAUDE_PLUGIN_ROOT}/skills/session-finder/scripts/sessions.py show <id>`

- Take the session id (a uuid-like token) from the request. A bare prefix is
  fine — the script does prefix matching.
- If the request also contains `full`, add `--full` for longer message previews.
- Summarize from the real script output; never fabricate ids or content.
- End with the exact resume command the script prints
  (`claude --resume <id>`, prefixed with `cd <project> &&` when the session
  belongs to a different directory).
