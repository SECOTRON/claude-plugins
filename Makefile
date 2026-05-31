# SECOTRON claude-plugins — developer tasks.
# Run `make` or `make help` for the list.

PYTHON ?= python3

.DEFAULT_GOAL := help

.PHONY: help setup install test validate check fmt smoke clean

help: ## Show this help
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

setup: ## One-time dev bootstrap: install trunk + linters + git hooks
	@command -v trunk >/dev/null 2>&1 || { \
		echo "Installing trunk..."; \
		curl https://get.trunk.io -fsSL | bash; \
	}
	trunk install

install: ## Print how to add this marketplace to Claude Code for local testing
	@echo "Add this repo as a local marketplace, then install a plugin:"
	@echo ""
	@echo "  /plugin marketplace add $(CURDIR)"
	@echo "  /plugin install session-finder@secotron"
	@echo ""
	@echo "Or from GitHub once pushed:"
	@echo "  /plugin marketplace add secotron/claude-plugins"

test: validate check smoke ## Validate manifests, lint, and smoke-test scripts

validate: ## Validate marketplace.json + every plugin.json
	$(PYTHON) scripts/validate_manifests.py

check: ## Lint everything with trunk
	trunk check --all --no-fix

fmt: ## Auto-format with trunk
	trunk fmt

smoke: ## Sanity-run the session-finder script
	$(PYTHON) plugins/session-finder/skills/session-finder/scripts/sessions.py list --limit 1 >/dev/null
	@echo "✓ session-finder script runs"

clean: ## Remove trunk caches and Python bytecode
	-trunk cache clean >/dev/null 2>&1 || true
	find . -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
