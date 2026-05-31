---
description: Full-text search past Claude Code sessions by topic or keyword.
argument-hint: "<words> [here]"
---

Use the **session-finder** skill to search my past Claude Code sessions.

Search terms: `$ARGUMENTS`

Run the bundled script:
`python3 ${CLAUDE_PLUGIN_ROOT}/skills/session-finder/scripts/sessions.py search "<terms>"`

- Strip a trailing `here` from the terms and pass `--here` to limit the search
  to the current project; otherwise search every project and surface.
- Present the hits as a short scannable list: title, how long ago, project path,
  the id, and the matched snippet.
- When I pick one, give the exact `claude --resume <id>` command (prefixed with
  `cd <project> &&` if it belongs to a different directory).

Only report what the script returns — never invent session ids or content.
