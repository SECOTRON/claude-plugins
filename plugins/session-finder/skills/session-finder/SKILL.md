---
name: session-finder
description: >-
  Find, search, summarize and resume past Claude Code sessions across every
  surface (terminal CLI, VS Code extension, desktop app, web) by reading the
  local JSONL transcripts under ~/.claude/projects. Use this whenever the user
  wants to locate an old session, recall or look up what was discussed before,
  search their conversation history by topic, keyword or date, find a session
  they started in a different surface, or get the command to resume a previous
  session. Trigger even when the user does not say the word "session" — phrases
  like "what did we decide about X", "the chat where we fixed the auth bug",
  "find where I worked on the invoice script", or "I can't see my VS Code
  session in the desktop app" should all use this skill.
---

# Session Finder

Claude Code saves every conversation as a JSONL transcript on disk. Each surface
(terminal, VS Code, desktop app, web) keeps its **own** session picker, so a
session started in one place is not listed in another — but the transcripts all
sit on the same disk. This skill reads them directly, so you can browse and
search across all of them from one place.

## The tool

A stdlib-only Python script does the parsing:

```text
${CLAUDE_PLUGIN_ROOT}/skills/session-finder/scripts/sessions.py
```

Run it with `python3` (or `python` on Windows, which usually has no `python3`).
Five subcommands:

| Goal                           | Command                                |
| ------------------------------ | -------------------------------------- |
| List recent sessions           | `python3 <script> list`                |
| Search message text            | `python3 <script> search "auth bug"`   |
| Outline one session            | `python3 <script> show <session-id>`   |
| Load a session for soft-resume | `python3 <script> recap [session-id]`  |
| Get a real resume command      | `python3 <script> resume [session-id]` |

Scope flags (for `list`, `search`, `recap`, `resume`): `--here` (only the
current directory's project), `--project <path>` (a specific project), or
nothing (all projects). Other flags: `--limit N` (list/search, default 20),
`--tail N` (recap, default 60), `--full` (recap/show), `--json`.

Two ways to "resume", and they differ:

- **`recap`** = _soft resume_. Dumps the session's conversation tail so you can
  read it, summarize where it left off, and **continue on that topic in the
  current conversation** — regardless of the current directory/project. This is
  the right choice in-session. It rehydrates context, not the exact message log
  or tool state.
- **`resume`** = prints the `claude --resume <id>` command for an _exact_ switch
  the user runs in their own terminal. A command can't swap its own live session
  the way built-in `/resume` does, so this is a hand-off.

## Workflow

1. **Figure out the intent.** A topic or keywords → `search`. "What was I just
   doing / recent sessions" → `list`. A uuid-like id → `show`. "Resume / pick up
   / continue where I left off" → `recap` (soft resume: load + keep going here).
   "Give me the resume command" / wants an exact switch → `resume`.
2. **Start narrow, then widen.** If the user is clearly talking about the
   project they're in, try `--here` first; if nothing fits, rerun without it to
   cover all projects and surfaces.
3. **Run the script** and read its output. Prefer `--json` when you need to
   reason over many results; use the plain output when you'll show it as-is.
4. **Present matches** as a short list: title, how long ago, project path, and
   the id. Keep it scannable.
5. **Resume.** Two modes: _soft_ — run `recap <id>`, summarize where it left
   off, and continue on that topic in this conversation (works across projects).
   _Exact_ — give the `claude --resume <id>` command (cd-prefixed for other
   dirs) for the user to run in their CLI/IDE. Offer the exact switch when they
   need the real session back (e.g. to edit that project's files in its dir).
6. **Summaries.** If asked what happened in a session, run `show` (optionally
   `--full`) and summarize from the real output. Never fabricate ids or content.

## Good to know

- Storage lives at `~/.claude/projects/<encoded-path>/<id>.jsonl`, or under
  `$CLAUDE_CONFIG_DIR` if that env var is set. The script honours it.
- Transcripts are matched to a project by the `cwd` recorded inside them, not by
  the (lossy) encoded folder name — so project filtering is reliable.
- Claude Code deletes transcripts older than ~30 days by default
  (`cleanupPeriodDays`). If an old session can't be found, it may simply have
  been cleaned up. Worth mentioning to the user rather than guessing.
- This skill only works where there is filesystem access (terminal, VS Code, the
  desktop **Code** section, Cowork). It does nothing in the plain desktop Chat
  section, which has no disk access.
