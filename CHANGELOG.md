# Changelog

All notable changes to this marketplace and its plugins are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
per plugin (each plugin's version lives in its `plugin.json`). Marketplace-level
tags (`vX.Y.Z`) mark notable snapshots of the whole repo.

## [Unreleased]

## [0.1.0] - 2026-05-31

### Added

- Marketplace scaffolding: `marketplace.json`, multi-plugin `plugins/` layout,
  trunk linting, commitlint, CI, dependabot, and community-health files.
- **session-finder** `0.1.0` — `/sessions` command (router + namespaced
  `/sessions:find|list|show`), `session-finder` skill, and a stdlib `sessions.py`
  that lists, searches, and outlines past Claude Code sessions from local
  JSONL transcripts. Cross-OS path handling; Python 3.7+.

[unreleased]: https://github.com/SECOTRON/claude-plugins/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/SECOTRON/claude-plugins/releases/tag/v0.1.0
