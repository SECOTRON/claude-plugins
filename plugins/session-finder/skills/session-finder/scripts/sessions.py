#!/usr/bin/env python3
"""Read, search and summarize local Claude Code session transcripts.

Claude Code stores every conversation as a JSONL transcript on disk, by default
under ~/.claude/projects/<encoded-project-path>/<session-id>.jsonl (one JSON
object per line: a message, a tool use, or a metadata entry). Each surface
(terminal CLI, VS Code extension, desktop app, web) keeps its own picker, but
the transcripts all live on the same disk -- so this script can browse them all.

Subcommands:
    list                 List recent sessions (newest first).
    search <query>       Full-text search across session messages.
    show <session-id>    Print an outline of one session.
    recap [session-id]   Dump a session's conversation for in-session rehydration
                         (soft resume); latest in scope when no id is given.
    resume [session-id]  Print the `claude --resume` command for a session
                         (the latest in scope when no id is given).

Scope flags:
    --here               Only sessions whose recorded cwd == current directory.
    --project <path>     Only sessions whose recorded cwd == this path.
    (default)            All projects.

Other flags:  --limit N   --json   --full (show only)

Honours $CLAUDE_CONFIG_DIR (falls back to ~/.claude). Note: Claude Code deletes
transcripts older than ~30 days by default (cleanupPeriodDays), so very old
sessions may already be gone.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path


def config_root() -> Path:
    env = os.environ.get("CLAUDE_CONFIG_DIR")
    return Path(env).expanduser() if env else Path.home() / ".claude"


def _norm(path):
    """Normalize a path for cross-OS comparison.

    normcase folds Windows case-insensitivity + backslashes; realpath collapses
    separators and symlinks. Returns the input unchanged if falsy.
    """
    if not path:
        return path
    return os.path.normcase(os.path.realpath(os.path.expanduser(path)))


def session_roots() -> list[Path]:
    roots = []
    primary = config_root() / "projects"
    if primary.is_dir():
        roots.append(primary)
    # macOS desktop app sometimes stores sessions here too (best effort).
    mac = (
        Path.home()
        / "Library"
        / "Application Support"
        / "Claude"
        / "claude-code-sessions"
    )
    if mac.is_dir():
        roots.append(mac)
    return roots


def session_files() -> list[Path]:
    files = []
    for root in session_roots():
        for path in root.rglob("*.jsonl"):
            # Skip sidechain subagent transcripts (agent-*.jsonl): they are not
            # top-level sessions and `claude --resume agent-...` cannot resume them.
            if path.stem.startswith("agent-"):
                continue
            files.append(path)
    return files


def _text_from_message(msg) -> str:
    """Pull plain text out of a message object (string or list of blocks)."""
    if not isinstance(msg, dict):
        return ""
    content = msg.get("content", "")
    if isinstance(content, str):
        return content
    out = []
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                out.append(block.get("text", ""))
            elif isinstance(block, str):
                out.append(block)
    return " ".join(out)


def quick_meta(path: Path) -> dict:
    """Cheap metadata: read the head only. Good enough for listing."""
    meta = {
        "id": path.stem,
        "file": str(path),
        "cwd": None,
        "branch": None,
        "summary": None,
        "first_prompt": None,
        "mtime": path.stat().st_mtime,
    }
    try:
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for i, line in enumerate(fh):
                if i > 120:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if meta["cwd"] is None and obj.get("cwd"):
                    meta["cwd"] = obj["cwd"]
                if meta["branch"] is None and obj.get("gitBranch"):
                    meta["branch"] = obj["gitBranch"]
                if obj.get("type") == "summary" and not meta["summary"]:
                    meta["summary"] = obj.get("summary")
                if meta["first_prompt"] is None and obj.get("type") == "user":
                    txt = _text_from_message(obj.get("message", {})).strip()
                    if txt:
                        meta["first_prompt"] = txt
    except OSError:
        pass
    return meta


def title_of(meta: dict) -> str:
    t = meta.get("summary") or meta.get("first_prompt") or "(no title)"
    t = " ".join(t.split())
    return t[:100] + ("..." if len(t) > 100 else "")


def matches_scope(meta: dict, args) -> bool:
    if args.here:
        return _norm(meta.get("cwd")) == _norm(os.getcwd())
    if args.project:
        return _norm(meta.get("cwd")) == _norm(args.project)
    return True


def fmt_age(mtime: float) -> str:
    secs = max(0, time.time() - mtime)
    if secs < 3600:
        return f"{int(secs // 60)}m ago"
    if secs < 86400:
        return f"{int(secs // 3600)}h ago"
    return f"{int(secs // 86400)}d ago"


def cmd_list(args):
    metas = [quick_meta(p) for p in session_files()]
    metas = [m for m in metas if matches_scope(m, args)]
    metas.sort(key=lambda m: m["mtime"], reverse=True)
    metas = metas[: args.limit]
    if args.json:
        print(json.dumps(metas, indent=2))
        return
    if not metas:
        print("No sessions found for this scope.")
        return
    for m in metas:
        print(f"- {title_of(m)}")
        loc = m.get("cwd") or "(unknown project)"
        branch = f" [{m['branch']}]" if m.get("branch") else ""
        print(f"    id: {m['id']}")
        print(f"    {fmt_age(m['mtime'])}  ·  {loc}{branch}")


def cmd_search(args):
    needle = args.query if args.case_sensitive else args.query.lower()
    hits = []
    for path in session_files():
        meta = quick_meta(path)
        if not matches_scope(meta, args):
            continue
        snippet = None
        try:
            with path.open("r", encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    if not line.strip():
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if obj.get("type") not in ("user", "assistant"):
                        continue
                    txt = _text_from_message(obj.get("message", {}))
                    hay = txt if args.case_sensitive else txt.lower()
                    if needle in hay:
                        idx = hay.find(needle)
                        start = max(0, idx - 60)
                        snippet = " ".join(txt[start : idx + 120].split())
                        break
        except OSError:
            continue
        if snippet is not None:
            meta["snippet"] = snippet
            hits.append(meta)
    hits.sort(key=lambda m: m["mtime"], reverse=True)
    hits = hits[: args.limit]
    if args.json:
        print(json.dumps(hits, indent=2))
        return
    if not hits:
        print(f"No sessions mention {args.query!r} in this scope.")
        return
    for m in hits:
        print(f"- {title_of(m)}")
        loc = m.get("cwd") or "(unknown project)"
        print(f"    id: {m['id']}  ·  {fmt_age(m['mtime'])}  ·  {loc}")
        print(f"    match: ...{m['snippet']}...")


def find_by_id(session_id: str) -> Path | None:
    for path in session_files():
        if path.stem == session_id:
            return path
    # allow prefix match for convenience
    for path in session_files():
        if path.stem.startswith(session_id):
            return path
    return None


def resume_line(meta: dict) -> str:
    """The exact command to resume a session, cd-prefixed if in another dir."""
    cwd = meta.get("cwd")
    if cwd and _norm(cwd) != _norm(os.getcwd()):
        return f"cd {cwd} && claude --resume {meta['id']}"
    return f"claude --resume {meta['id']}"


def cmd_show(args):
    path = find_by_id(args.session_id)
    if path is None:
        print(f"No session file found for id {args.session_id!r}.")
        sys.exit(1)
    meta = quick_meta(path)
    rows = []
    count = 0
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("type") in ("user", "assistant"):
                count += 1
                txt = " ".join(_text_from_message(obj.get("message", {})).split())
                limit = 400 if args.full else 120
                if txt:
                    rows.append(
                        (obj["type"], txt[:limit] + ("..." if len(txt) > limit else ""))
                    )
    if args.json:
        print(json.dumps({"meta": meta, "messages": count, "rows": rows}, indent=2))
        return
    print(f"Title:   {title_of(meta)}")
    print(f"Id:      {meta['id']}")
    print(f"Project: {meta.get('cwd') or '(unknown)'}")
    if meta.get("branch"):
        print(f"Branch:  {meta['branch']}")
    print(f"Messages: {count}   ·   last activity {fmt_age(meta['mtime'])}")
    print("-" * 60)
    for role, txt in rows:
        tag = "you" if role == "user" else "claude"
        print(f"[{tag}] {txt}")
    print("-" * 60)
    print(f"To resume:  {resume_line(meta)}")


def _resolve_target(args) -> tuple:
    """Resolve the target session: an explicit id/prefix, else latest in scope.

    Returns (path, meta). Exits with a message if nothing matches.
    """
    if args.session_id:
        path = find_by_id(args.session_id)
        if path is None:
            print(f"No session file found for id {args.session_id!r}.")
            sys.exit(1)
        return path, quick_meta(path)
    pairs = [(p, quick_meta(p)) for p in session_files()]
    pairs = [(p, m) for p, m in pairs if matches_scope(m, args)]
    if not pairs:
        print("No sessions found for this scope.")
        sys.exit(1)
    pairs.sort(key=lambda pm: pm[1]["mtime"], reverse=True)
    return pairs[0]


def cmd_resume(args):
    _, meta = _resolve_target(args)
    if args.json:
        print(
            json.dumps(
                {
                    "id": meta["id"],
                    "cwd": meta.get("cwd"),
                    "command": resume_line(meta),
                },
                indent=2,
            )
        )
        return
    print(f"# Resume: {title_of(meta)}")
    print(f"# {fmt_age(meta['mtime'])} · {meta.get('cwd') or '(unknown project)'}")
    print("# Copy-paste into your own terminal (this prints the command, it does")
    print("# NOT switch the current conversation):")
    print(resume_line(meta))


def _conversation(path: Path, tail: int, cap: int) -> tuple:
    """Return (total_count, rows) where rows are the last `tail` (role, text)
    user/assistant turns, each capped at `cap` chars. Tool-only lines skipped."""
    rows = []
    total = 0
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("type") not in ("user", "assistant"):
                continue
            txt = " ".join(_text_from_message(obj.get("message", {})).split())
            if not txt:
                continue
            total += 1
            rows.append((obj["type"], txt[:cap] + ("…" if len(txt) > cap else "")))
    if tail and len(rows) > tail:
        rows = rows[-tail:]
    return total, rows


def cmd_recap(args):
    """Dump a session as context for in-session rehydration (soft resume)."""
    path, meta = _resolve_target(args)
    cap = 4000 if args.full else 1500
    tail = 0 if args.full else args.tail
    total, rows = _conversation(path, tail, cap)
    if args.json:
        print(
            json.dumps(
                {
                    "id": meta["id"],
                    "title": title_of(meta),
                    "cwd": meta.get("cwd"),
                    "branch": meta.get("branch"),
                    "age": fmt_age(meta["mtime"]),
                    "messages": total,
                    "shown": len(rows),
                    "resume_command": resume_line(meta),
                    "rows": rows,
                },
                indent=2,
            )
        )
        return
    print(f"Session: {title_of(meta)}")
    print(f"Id:      {meta['id']}")
    print(f"Project: {meta.get('cwd') or '(unknown)'}")
    if meta.get("branch"):
        print(f"Branch:  {meta['branch']}")
    shown = f"last {len(rows)} of {total}" if total > len(rows) else f"{total}"
    print(f"Messages: {shown}   ·   last activity {fmt_age(meta['mtime'])}")
    print("=" * 60)
    for role, txt in rows:
        tag = "you" if role == "user" else "claude"
        print(f"[{tag}] {txt}")
    print("=" * 60)
    print("# For a true session switch (exact history, in its project dir):")
    print(f"#   {resume_line(meta)}")


def build_parser():
    p = argparse.ArgumentParser(description="Browse local Claude Code sessions.")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_scope(sp):
        sp.add_argument(
            "--here", action="store_true", help="only current directory's project"
        )
        sp.add_argument("--project", help="only this project path")
        sp.add_argument("--limit", type=int, default=20)
        sp.add_argument("--json", action="store_true")

    lp = sub.add_parser("list", help="list recent sessions")
    add_scope(lp)
    lp.set_defaults(func=cmd_list)

    spx = sub.add_parser("search", help="full-text search across sessions")
    spx.add_argument("query")
    spx.add_argument("--case-sensitive", action="store_true")
    add_scope(spx)
    spx.set_defaults(func=cmd_search)

    shp = sub.add_parser("show", help="print an outline of one session")
    shp.add_argument("session_id")
    shp.add_argument("--full", action="store_true", help="longer message previews")
    shp.add_argument("--json", action="store_true")
    shp.set_defaults(func=cmd_show)

    rp = sub.add_parser(
        "resume",
        help="print the resume command for a session (latest in scope, or by id)",
    )
    rp.add_argument(
        "session_id",
        nargs="?",
        help="session id or prefix; omit to use the latest in scope",
    )
    rp.add_argument(
        "--here", action="store_true", help="only current directory's project"
    )
    rp.add_argument("--project", help="only this project path")
    rp.add_argument("--json", action="store_true")
    rp.set_defaults(func=cmd_resume)

    rcp = sub.add_parser(
        "recap",
        help="dump a session's conversation for in-session rehydration (soft resume)",
    )
    rcp.add_argument(
        "session_id",
        nargs="?",
        help="session id or prefix; omit to use the latest in scope",
    )
    rcp.add_argument(
        "--here", action="store_true", help="only current directory's project"
    )
    rcp.add_argument("--project", help="only this project path")
    rcp.add_argument(
        "--tail",
        type=int,
        default=60,
        help="show only the last N turns (default 60; ignored with --full)",
    )
    rcp.add_argument(
        "--full", action="store_true", help="all turns, longer per-turn text"
    )
    rcp.add_argument("--json", action="store_true")
    rcp.set_defaults(func=cmd_recap)
    return p


def main():
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
