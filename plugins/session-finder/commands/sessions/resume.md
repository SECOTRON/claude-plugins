---
description: Soft-resume a past Claude Code session — load its context and continue here.
argument-hint: "[<session-id> | here | <words>]"
---

Use the **session-finder** skill to **soft-resume** a past session: load what it
was about and keep working on that topic in _this_ conversation, regardless of
which directory or project I'm currently in.

Request: `$ARGUMENTS`

Resolve the target session, then load it:

- Empty → the most recent session overall.
- `here` → most recent in this project (`recap --here`).
- A uuid-like token → that session (`recap <id>`).
- Free-text words → run `search "<words>"` first, then `recap <id>` for the
  best match.

Run (use `python` instead of `python3` on Windows):
`python3 ${CLAUDE_PLUGIN_ROOT}/skills/session-finder/scripts/sessions.py recap <id>`

Use `--full` if I ask for the complete history; otherwise the default tail is
enough. Then:

1. Read the recap output.
2. Give me a short "**Picking up where you left off:**" summary — the topic, key
   decisions, what was in progress, and the obvious next step.
3. **Continue from there in this conversation.** Adopt that context and proceed
   as if we never stopped. Do not start a brand-new session or make me repeat
   myself.

This is a _soft_ resume: it rehydrates the topic and context here, but it is not
a byte-for-byte restore of the original session (no exact message log, tool
state, or permissions). For an exact switch — especially to edit that project's
files in the right working directory — also offer me the real command the recap
prints at the end: `claude --resume <id>` (cd-prefixed), to run in my terminal.

Never invent session ids or content — only use what the script returns.
