# secotron/claude-plugins

Secotron's [Claude Code](https://claude.com/claude-code) plugin marketplace.

## Install the marketplace

From Claude Code:

```text
/plugin marketplace add secotron/claude-plugins
```

Then install any plugin below with `/plugin install <name>@secotron`.

## Plugins

| Plugin | Description |
| ------ | ----------- |
| [`claude-session-finder`](plugins/claude-session-finder) | Find, search, summarize and resume past Claude Code sessions across surfaces (terminal, VS Code, desktop app, web) by reading the local JSONL transcripts. |

```text
/plugin install claude-session-finder@secotron
```

## Repository layout

```text
.
├── .claude-plugin/marketplace.json   # marketplace manifest (lists all plugins)
└── plugins/
    └── <plugin-name>/
        ├── .claude-plugin/plugin.json
        ├── commands/   skills/   README.md
        └── ...
```

Each plugin is self-contained under `plugins/<name>/`. Add a new plugin by
creating its directory and appending an entry to
[`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json).

## Development

Linting is handled by [trunk](https://trunk.io) at the repo root:

```text
trunk check --all
trunk fmt
```

## License

MIT
