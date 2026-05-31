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
Four subcommands:

| Goal                 | Command                                |
| -------------------- | -------------------------------------- |
| List recent sessions | `python3 <script> list`                |
| Search message text  | `python3 <script> search "auth bug"`   |
| Outline one session  | `python3 <script> show <session-id>`   |
| Get a resume command | `python3 <script> resume [session-id]` |

Scope flags (for `list`, `search`, `resume`): `--here` (only the current
directory's project), `--project <path>` (a specific project), or nothing (all
projects). Other flags: `--limit N` (default 20), `--json` (machine-readable),
and `--full` (longer previews, `show` only).

`resume` with no id picks the most recent session in scope; with an id (or
prefix) it targets that one. It prints the `claude --resume <id>` command — it
does **not** swap the live conversation in place the way the built-in `/resume`
does; the user runs the printed command in their CLI/IDE.

## Workflow

1. **Figure out the intent.** A topic or keywords → `search`. "What was I just
   doing / recent sessions" → `list`. A uuid-like id → `show`. "Resume X / pick
   up where I left off" → `resume` (latest in scope, or by id).
2. **Start narrow, then widen.** If the user is clearly talking about the
   project they're in, try `--here` first; if nothing fits, rerun without it to
   cover all projects and surfaces.
3. **Run the script** and read its output. Prefer `--json` when you need to
   reason over many results; use the plain output when you'll show it as-is.
4. **Present matches** as a short list: title, how long ago, project path, and
   the id. Keep it scannable.
5. **Resume hand-off.** When the user picks one, give the exact command:
   `claude --resume <id>` — prefixed with `cd <project-path> &&` when the
   session belongs to a different directory than the current one. Resuming
   happens in the CLI/IDE; this skill does not resume for them.
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
