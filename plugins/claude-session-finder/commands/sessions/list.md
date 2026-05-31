---
description: List recent Claude Code sessions, newest first.
argument-hint: "[here | all]"
---

Use the **session-finder** skill to list my recent Claude Code sessions.

Scope: `$ARGUMENTS`

Run the bundled script (use `python` instead of `python3` on Windows):
`python3 ${CLAUDE_PLUGIN_ROOT}/skills/session-finder/scripts/sessions.py list`

- If the scope is `here`, add `--here` to list only the current project's
  sessions. Empty or `all` → list every project, newest first.
- Present the results as a short scannable list: title, how long ago, project
  path, and the id.
- When I pick one, give the exact `claude --resume <id>` command (prefixed with
  `cd <project> &&` if it belongs to a different directory).

Only report what the script returns — never invent session ids or content.
