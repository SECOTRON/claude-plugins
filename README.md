<p align="center">
  <img src="assets/logo.png" alt="SECOTRON" width="120" height="120">
</p>

<h1 align="center">SECOTRON / claude-plugins</h1>

<p align="center">
  SECOTRON's <a href="https://claude.com/claude-code">Claude Code</a> plugin marketplace.
</p>

## Install the marketplace

From Claude Code:

```text
/plugin marketplace add secotron/claude-plugins
```

Then install any plugin below with `/plugin install <name>@secotron`.

## Plugins

| Plugin                                     | Description                                                                                                                                                |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`session-finder`](plugins/session-finder) | Find, search, summarize and resume past Claude Code sessions across surfaces (terminal, VS Code, desktop app, web) by reading the local JSONL transcripts. |

```text
/plugin install session-finder@secotron
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
make setup    # one-time: trunk + linters + git hooks
make test     # validate manifests + lint + smoke test
make fmt      # auto-format
```

## Contributing

Contributions welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for setup, commit
conventions, and how to add a plugin. By participating you agree to the
[Code of Conduct](CODE_OF_CONDUCT.md). Found a vulnerability? See
[SECURITY.md](SECURITY.md).

## Support

If these plugins are useful, you can [sponsor on GitHub](https://github.com/sponsors/thomasgeens)
or [buy me a coffee](https://www.buymeacoffee.com/thomas.geens). ☕

## License

[MIT](LICENSE) © Thomas Geens
