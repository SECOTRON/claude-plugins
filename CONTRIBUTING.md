# Contributing

Thanks for your interest in improving SECOTRON's Claude Code plugins.

## Development setup

```bash
make setup   # installs trunk, downloads linters, wires git hooks
```

Trunk drives all linting and formatting; no other toolchain is required beyond
`git`, `python3`, and (for linting) Node — both provided by Trunk's runtimes.

## Commit conventions

This repo uses [Conventional Commits](https://www.conventionalcommits.org),
enforced by commitlint via a Trunk pre-commit hook after `make setup`.

| Type       | Use for                               |
| ---------- | ------------------------------------- |
| `feat`     | a new plugin, command, or capability  |
| `fix`      | a bug fix                             |
| `docs`     | README / docs only                    |
| `chore`    | tooling, config, housekeeping         |
| `refactor` | restructuring without behavior change |
| `ci`       | workflow / CI changes                 |

Scopes nest with slashes, e.g. `feat(session-finder): ...`.

## Repository layout

```text
.
├── .claude-plugin/marketplace.json   # lists every plugin
└── plugins/
    └── <plugin-name>/
        ├── .claude-plugin/plugin.json
        ├── commands/   skills/   README.md
        └── ...
```

### Adding a new plugin

1. Create `plugins/<name>/` with its own `.claude-plugin/plugin.json`
   (`name`, `description`, `version` required — `name` must match the
   marketplace entry).
2. Add `commands/` and/or `skills/` as needed.
3. Append an entry to [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)
   with `name`, `source: ./plugins/<name>`, and `description`.
4. Run `make validate` to confirm the manifests are consistent.

## Testing & checks

```bash
make test       # validate manifests + trunk lint + script smoke test
make validate   # manifests only
make check      # trunk lint only
make fmt        # auto-format
```

## Pull requests

1. Branch off `main`.
2. Use Conventional Commit messages.
3. Make sure `make test` passes and CI is green.
4. Open the PR against [`SECOTRON/claude-plugins`](https://github.com/SECOTRON/claude-plugins).

Rebase merges are preferred when history is clean and linear.

## Releasing

Releases are automated with
[release-please](https://github.com/googleapis/release-please). You don't bump
versions or edit the changelog by hand:

1. Land Conventional-Commit PRs on `main` as usual.
2. release-please keeps an open **"release PR"** that accumulates the next
   version bump (from commit types) and the generated `CHANGELOG.md`.
3. **Merge the release PR** when ready. That tags `vX.Y.Z`, updates
   `CHANGELOG.md` + the plugin's `plugin.json` version, and publishes a GitHub
   Release.

`feat` → minor, `fix` → patch, `feat!`/`BREAKING CHANGE` → major. `chore`/`ci`
are hidden from the changelog.

> **Versioning model:** _per-plugin_. Each plugin is its own release-please
> package — it bumps only on commits that touch its `plugins/<name>/` path,
> keeps its own `CHANGELOG.md`, and tags `<plugin>-vX.Y.Z` (e.g.
> `session-finder-v0.1.1`). release-please may open one release PR per plugin.
> Register a new plugin under `packages` in `release-please-config.json` and add
> its baseline to `.release-please-manifest.json`.

Plugins install directly from `main`, so tags/releases are for clarity and
reference, not delivery.
