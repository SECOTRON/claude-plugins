#!/usr/bin/env python3
"""Validate the marketplace manifest and every plugin manifest.

Checks, with a non-zero exit on any failure:
  - .claude-plugin/marketplace.json parses and has name/owner/plugins
  - each listed plugin's source directory exists
  - each plugin's .claude-plugin/plugin.json parses and has name/description/version
  - the plugin.json name matches the marketplace entry name

Stdlib only; run with `python3 scripts/validate_manifests.py` from the repo root.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def fail(msg: str) -> None:
    print(f"✖ {msg}")
    sys.exit(1)


def load_json(path: Path):
    if not path.is_file():
        fail(f"missing file: {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def main() -> None:
    market = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    for key in ("name", "owner", "plugins"):
        if key not in market:
            fail(f"marketplace.json missing required key: {key!r}")
    if not isinstance(market["plugins"], list) or not market["plugins"]:
        fail("marketplace.json 'plugins' must be a non-empty list")

    seen = set()
    for entry in market["plugins"]:
        name = entry.get("name")
        source = entry.get("source")
        if not name or not source:
            fail(f"plugin entry needs 'name' and 'source': {entry!r}")
        if name in seen:
            fail(f"duplicate plugin name in marketplace: {name!r}")
        seen.add(name)

        plugin_dir = (ROOT / source).resolve()
        if not plugin_dir.is_dir():
            fail(f"plugin {name!r} source dir does not exist: {source}")

        manifest = load_json(plugin_dir / ".claude-plugin" / "plugin.json")
        for key in ("name", "description", "version"):
            if key not in manifest:
                fail(f"plugin {name!r} plugin.json missing key: {key!r}")
        if manifest["name"] != name:
            fail(f"plugin.json name {manifest['name']!r} != marketplace entry {name!r}")
        print(f"✓ {name}  ({source})")

    print(f"✓ marketplace {market['name']!r}: {len(seen)} plugin(s) valid")


if __name__ == "__main__":
    main()
