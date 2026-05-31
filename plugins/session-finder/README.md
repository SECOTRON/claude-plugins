# session-finder

A Claude Code plugin to **find, search, summarize and resume past sessions across
every surface** (terminal, VS Code, desktop app, web).

Each Claude Code surface keeps its own session picker, so a session you started in
VS Code won't show up in the desktop app's list. But all transcripts live on the
same disk under `~/.claude/projects/`. This plugin reads them directly, so you get
one searchable view — and the exact command to resume any of them.

## What you get

- **`/sessions`** slash command — a router; `find`, `list`, `show`, `resume`, or
  `recap` past sessions. Also exposed as namespaced subcommands `/sessions:find`,
  `/sessions:list`, `/sessions:show`, `/sessions:resume`.
- **`session-finder`** skill — auto-triggers on natural phrases like
  "find the chat where we fixed the auth bug" or "what did we decide about X".
- A stdlib-only Python parser (no dependencies) at
  `skills/session-finder/scripts/sessions.py`.

### Two ways to pick up a past session

- **Soft resume (in place):** `/sessions resume` loads the target session's
  context and **continues on that topic in your current conversation** —
  regardless of which project you're in. Best for "catch me up and keep going."
  It rehydrates context, not the exact message log or tool state.
- **Exact switch:** the recap also prints `claude --resume <id>` (cd-prefixed)
  for a true restore you run in your own terminal. A command can't swap its own
  live session the way the built-in `/resume` does, so that part is a hand-off.

This does **not** override the built-in `/resume`. `/resume` is the per-project
picker for the current surface; this plugin adds a cross-project view, content
search, and a soft-resume that works from anywhere.

## Install

This plugin ships in the [`secotron/claude-plugins`](https://github.com/secotron/claude-plugins)
marketplace. From Claude Code:

```text
/plugin marketplace add secotron/claude-plugins
/plugin install session-finder@secotron
```

For local development, point the marketplace at a checkout instead:

```text
/plugin marketplace add /path/to/claude-plugins
/plugin install session-finder@secotron
```

Restart / reload when prompted.

## Use

```text
/sessions                          # recent sessions, all projects
/sessions here                     # recent sessions, current project only
/sessions invoice forwarding       # search message text
/sessions 11111111-aaaa-...        # outline one session by id
/sessions resume here              # soft-resume the latest session here
/sessions recap <id>               # load a session, summarize, don't continue

# or the namespaced subcommands:
/sessions:list here
/sessions:find race condition
/sessions:show <id> full
/sessions:resume                   # soft-resume the latest session
```

Or just ask in plain language — the skill will fire on its own.

### Direct script use (optional)

Use `python3` on macOS/Linux, or `python` on Windows (which usually has no
`python3`). The script runs on Python 3.7+ with no dependencies.

```text
python3 skills/session-finder/scripts/sessions.py list --here
python3 skills/session-finder/scripts/sessions.py search "race condition"
python3 skills/session-finder/scripts/sessions.py show <id> --full
python3 skills/session-finder/scripts/sessions.py recap <id> --tail 40
python3 skills/session-finder/scripts/sessions.py resume --here
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
