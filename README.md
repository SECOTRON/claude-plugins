# claude-session-finder

A Claude Code plugin to **find, search, summarize and resume past sessions across
every surface** (terminal, VS Code, desktop app, web).

Each Claude Code surface keeps its own session picker, so a session you started in
VS Code won't show up in the desktop app's list. But all transcripts live on the
same disk under `~/.claude/projects/`. This plugin reads them directly, so you get
one searchable view — and the exact command to resume any of them.

## What you get

- **`/sessions`** slash command — a router; `find`, `list`, or `show` past
  sessions. Also exposed as namespaced subcommands `/sessions:find`,
  `/sessions:list`, `/sessions:show`.
- **`session-finder`** skill — auto-triggers on natural phrases like
  "find the chat where we fixed the auth bug" or "what did we decide about X".
- A stdlib-only Python parser (no dependencies) at
  `skills/session-finder/scripts/sessions.py`.

This does **not** override the built-in `/resume`. `/resume` is the per-project
picker for the current surface; this plugin adds cross-project, cross-surface
search and hands you `claude --resume <id>` when you've found the one you want.

## Install

The repo doubles as a local marketplace (manifest + marketplace.json in
`.claude-plugin/`). From Claude Code:

```
/plugin marketplace add /path/to/claude-session-finder
/plugin install claude-session-finder@thomas-local
```

Or point at it from a git URL once you push it somewhere. Restart / reload when
prompted.

## Use

```
/sessions                          # recent sessions, all projects
/sessions here                     # recent sessions, current project only
/sessions invoice forwarding       # search message text
/sessions 11111111-aaaa-...        # outline one session by id

# or the namespaced subcommands:
/sessions:list here
/sessions:find race condition
/sessions:show <id> full
```

Or just ask in plain language — the skill will fire on its own.

### Direct script use (optional)

```
python3 skills/session-finder/scripts/sessions.py list --here
python3 skills/session-finder/scripts/sessions.py search "race condition"
python3 skills/session-finder/scripts/sessions.py show <id> --full
```

Flags: `--here`, `--project <path>`, `--limit N`, `--json`, `--full` (show only).

## Notes

- Honours `$CLAUDE_CONFIG_DIR` (defaults to `~/.claude`).
- Claude Code deletes transcripts older than ~30 days by default
  (`cleanupPeriodDays`); raise it in settings if you want to keep more history.
- Works wherever Claude Code has filesystem access (terminal, VS Code, the
  desktop **Code** section, Cowork). Not the plain desktop **Chat** section.

## License

MIT
