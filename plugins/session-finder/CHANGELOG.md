# Changelog

## [0.3.0](https://github.com/SECOTRON/claude-plugins/compare/session-finder-v0.2.0...session-finder-v0.3.0) (2026-05-31)


### Features

* **session-finder:** add soft-resume via recap subcommand ([e53c7f4](https://github.com/SECOTRON/claude-plugins/commit/e53c7f480f6c706b7d332baecae992dc391e2040))

## [0.2.0](https://github.com/SECOTRON/claude-plugins/compare/session-finder-v0.1.0...session-finder-v0.2.0) (2026-05-31)


### Features

* **session-finder:** add resume subcommand ([289f868](https://github.com/SECOTRON/claude-plugins/commit/289f868b68c58d385e79c74fb1f6bf803581fb1c))


### Bug Fixes

* **session-finder:** make resume output a clear copy-paste hand-off ([58a159d](https://github.com/SECOTRON/claude-plugins/commit/58a159dd26167025da281a073d8f8c09050baa98))

## 0.1.0 (2026-05-31)

### Features

- `/sessions` command — router plus namespaced `/sessions:find`,
  `/sessions:list`, `/sessions:show`.
- `session-finder` skill that auto-triggers on natural phrasing.
- stdlib `sessions.py` to list, search, and outline past Claude Code sessions
  from local JSONL transcripts. Cross-OS path handling; Python 3.7+.
