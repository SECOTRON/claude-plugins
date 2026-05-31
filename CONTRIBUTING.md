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

Plugins install directly from this repo — there is no build step or registry, so
releases are lightweight and manual:

1. Bump the affected plugin's `version` in its `plugin.json` (SemVer).
2. Move the relevant `CHANGELOG.md` entries from `[Unreleased]` into a new
   dated version section.
3. Commit (`chore(release): <plugin> vX.Y.Z`), then tag a marketplace snapshot:
   `git tag vX.Y.Z && git push --tags`.
4. Optionally publish a GitHub Release from the tag with the changelog notes.

Users always get the latest `main` when they install; tags exist for changelog
and reference. If release cadence grows, consider automating with
[Changesets](https://github.com/changesets/changesets) (per-plugin versions +
changelogs for a monorepo) — deferred until warranted.
