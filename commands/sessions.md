---
description: Find, search, summarize or resume a past Claude Code session.
argument-hint: "[find <words> | list | show <id> | here | all | <words> | <id>]"
---

Use the **session-finder** skill to help me find a past Claude Code session.

My request: `$ARGUMENTS`

The session-parsing script is bundled at:
`${CLAUDE_PLUGIN_ROOT}/skills/session-finder/scripts/sessions.py`
Invoke it with `python3` (or `python` on Windows, which usually has no `python3`).

This is the `/sessions` router. Interpret `$ARGUMENTS` and run the right
subcommand. The first word may be an explicit subcommand; if it is not, infer
intent from the whole string.

- First word `find`, `search`, or free-text words → run
  `search "<the rest>"` (add `--here` to limit to this project).
- First word `list`, or empty / `here` / `all` → run `list`
  (add `--here` for the current project only; default lists every project,
  newest first).
- First word `show`, or a uuid-like token → run `show <id>` to print an outline.

Then show me the matches as a short readable list, and when I pick one, give me
the exact `claude --resume <id>` command (prefixed with `cd <project> &&` if it
belongs to a different directory). Do not invent session ids or content — only
report what the script returns.
