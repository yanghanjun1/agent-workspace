#!/usr/bin/env python3
"""aw link - wire a workspace into a harness, or explain why nothing is needed.

The workspace is the thing that gets opened; the agent is a process started inside it.
For most harnesses that means no linking at all: `cd workspace && agent`. Linking
exists only for harnesses that discover skills from a fixed directory.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

IDENTITY = "AGENTS.md"


def _remove_link(path: Path) -> bool:
    if path.is_symlink():
        path.unlink()
        return True
    try:
        path.rmdir()  # removes a junction; fails on a real directory with content
        return True
    except OSError:
        return False


def make_link(src: Path, dst: Path) -> bool:
    if dst.exists() or dst.is_symlink():
        if not _remove_link(dst):
            print(f"  skip {dst.name}: a real directory is there, not a link")
            return False
    try:
        os.symlink(src, dst, target_is_directory=True)
        return True
    except (OSError, NotImplementedError):
        pass
    if os.name == "nt":
        result = subprocess.run(["cmd", "/c", "mklink", "/J", str(dst), str(src)],
                                capture_output=True, text=True)
        return result.returncode == 0
    return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aw link")
    parser.add_argument("--target", required=True, choices=("dsh", "plain"))
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--prefix", default="ca-")
    args = parser.parse_args(argv)

    ws = Path(args.workspace).expanduser().resolve()
    if not (ws / IDENTITY).is_file():
        print(f"not a workspace: {ws} has no {IDENTITY}")
        return 2

    domains = sorted(p for p in ws.iterdir() if p.is_dir() and p.name.startswith(args.prefix))

    if args.target == "plain":
        print("nothing to link.")
        print("open the workspace with any agent that can read a directory:")
        print(f"  cd {ws} && <agent>")
        print(f"the agent reads {IDENTITY} at session start and follows the routing table.")
        return 0

    skills = ws / ".dsh" / "skills"
    skills.mkdir(parents=True, exist_ok=True)
    count = 0
    for dom in domains:
        if (dom / "SKILL.md").is_file() and make_link(dom, skills / dom.name):
            print(f"  linked {dom.name}")
            count += 1
    print(f"\n{count} domain(s) linked into {skills}")
    return 0 if count or not domains else 1


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    raise SystemExit(main())
