#!/usr/bin/env python3
"""aw new - generate a domain, then prove it conforms.

A domain is generated, not hand-written: the owner states a need in their own words
and the agent produces the manual, the two axes, and the first decision entry. What
is *not* generated is the identity file - that one says who the assistant is and what
it owns, and an agent writing its own job description will write one it likes.

Two guards, both learned the hard way:

* Refuse to run outside a workspace. A domain is not a workspace (M0).
* Compare conformance before and after. If the new domain introduces violations,
  remove it instead of leaving a half-dead folder behind.
"""

from __future__ import annotations

import argparse
import datetime
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"
IDENTITY = "AGENTS.md"

DIRS = {"en": ("0-raw", "1-data", "4-engine"), "zh": ("0-原料", "1-整理", "4-引擎")}
LOG_NAME = {"en": "log.md", "zh": "流水.md"}
DECISIONS_NAME = {"en": "decisions.md", "zh": "维护日志.md"}


def template(lang: str, stem: str) -> Path:
    suffix = ".zh.md" if lang == "zh" else ".md"
    return TEMPLATES / f"{stem}{suffix}"


def fill(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def oneline(value: str) -> str:
    """Collapse to a single line.

    Everything the owner types ends up in a file an agent will read: the description in
    frontmatter, the first event block, the first decision entry. A newline in an input
    could add a frontmatter key or forge a decision-log entry, so inputs never carry one.
    """
    return " ".join(str(value).split())


def describe(lang: str, words: str, need: str) -> str:
    if lang == "zh":
        return f"Use when 主人提{words}，或要{need}。"
    return f"Use when the user mentions {words}, or needs to {need}."


def first_block(lang: str, date: str, name: str, need: str) -> str:
    log, decisions = LOG_NAME[lang], DECISIONS_NAME[lang]
    if lang == "zh":
        return (f"## {date}\n"
                f"- 今天做了：建 {name} 域 —— 需求是「{need}」\n"
                f"- 产出物：`{name}/SKILL.md`、`{name}/{log}`、`{name}/{decisions}`\n"
                f"- 卡点·待决：还没记过真实的一条\n"
                f"- 明天第一件事：记一条真的，然后跑 `aw verify {name}`\n"
                f"- 交接·备份：—")
    return (f"## {date}\n"
            f"- did: created {name} for: {need}\n"
            f"- artifacts: `{name}/SKILL.md`, `{name}/{log}`, `{name}/{decisions}`\n"
            f"- blocked / open: no real record yet\n"
            f"- next: record one real item, then run `aw verify {name}`\n"
            f"- handoff: -")


def first_entry(lang: str, date: str, name: str, need: str) -> str:
    if lang == "zh":
        return f"- {date} · 域 {name} 建立 · 因为你说「{need}」"
    return f"- {date} · domain created · because the owner asked for: {need}"


def plan(name: str, need: str, words: str, lang: str, date: str) -> dict:
    summary = need if len(need) <= 40 else need[:37] + "..."
    data_dir, engine_dir = DIRS[lang][1], DIRS[lang][2]
    values = {
        "name": name,
        "description": describe(lang, words, need),
        "summary": summary,
        "need": need,
        "words": words,
        "data_dir": data_dir,
        "first_block": first_block(lang, date, name, need),
        "first_entry": first_entry(lang, date, name, need),
    }
    files = {
        "SKILL.md": fill(template(lang, "SKILL").read_text(encoding="utf-8"), values),
        LOG_NAME[lang]: fill(template(lang, "log").read_text(encoding="utf-8"), values),
        DECISIONS_NAME[lang]: fill(template(lang, "decisions").read_text(encoding="utf-8"), values),
        # A real reporter, not a placeholder: M5 is only honest if the script exists.
        f"{engine_dir}/report.py": fill(
            (TEMPLATES / "report.py").read_text(encoding="utf-8"), values),
    }
    return {"name": name, "lang": lang, "values": values, "files": files,
            "dirs": DIRS[lang], "date": date, "need": need, "words": words}


def apply(job: dict, ws: Path) -> list[Path]:
    dom = ws / job["name"]
    dom.mkdir(parents=False, exist_ok=False)
    written = []
    for rel, text in job["files"].items():
        path = dom / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        written.append(path)
    for sub in job["dirs"]:
        folder = dom / sub
        folder.mkdir(exist_ok=True)
        if not any(folder.iterdir()):
            keep = folder / ".gitkeep"
            keep.write_text("", encoding="utf-8")
            written.append(keep)
    return written


def _is_separator(line: str) -> bool:
    return re.fullmatch(r"\|[\s:|-]+\|", line.strip()) is not None


def _insert_row(text: str, header_pred, row: str) -> tuple[str, bool]:
    lines = text.splitlines()
    for i in range(len(lines) - 1):
        if lines[i].strip().startswith("|") and header_pred(lines[i]) and _is_separator(lines[i + 1]):
            j = i + 1
            while j + 1 < len(lines) and lines[j + 1].strip().startswith("|"):
                j += 1
            lines.insert(j + 1, row)
            return "\n".join(lines) + "\n", True
    return text, False


def register(ws: Path, job: dict) -> list[str]:
    identity = ws / IDENTITY
    text = identity.read_text(encoding="utf-8")
    name, need = job["name"], job["need"]
    short = need if len(need) <= 30 else need[:27] + "..."

    domain_row = f"| {name} | `{name}/` | {short} | `{name}/SKILL.md` |"
    route_row = f"| {job['words']} | `{name}` |"

    notes = []
    text, ok = _insert_row(text, lambda l: ("域" in l) or ("domain" in l.lower()), domain_row)
    notes.append(("ownership table" if ok else "ownership table NOT found"))
    text, ok = _insert_row(text, lambda l: ("说什么" in l) or ("say" in l.lower()), route_row)
    notes.append(("routing table" if ok else "routing table NOT found"))

    identity.with_suffix(".md.bak").write_text(
        identity.read_text(encoding="utf-8"), encoding="utf-8")
    identity.write_text(text, encoding="utf-8")
    return notes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aw new", description="Generate a domain, then check it")
    parser.add_argument("name", help="domain directory name, e.g. ca-coffee")
    parser.add_argument("--need", required=True, help="what the owner asked for, in their words")
    parser.add_argument("--words", required=True, help="words the owner actually says, e.g. 'coffee/pour-over/beans'")
    parser.add_argument("--lang", default="en", choices=("en", "zh"))
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--prefix", default="ca-")
    parser.add_argument("--date", default=datetime.date.today().isoformat())
    parser.add_argument("--yes", action="store_true", help="skip the receipt prompt")
    parser.add_argument("--register", action="store_true", help="add the two rows to the identity file")
    args = parser.parse_args(argv)

    # Everything below ends up in a file an agent reads, so it never carries a newline.
    need, words, date = oneline(args.need), oneline(args.words), oneline(args.date)

    ws = Path(args.workspace).expanduser().resolve()
    if not (ws / IDENTITY).is_file():
        print(f"not a workspace: {ws} has no {IDENTITY}. A domain is not a workspace (M0).")
        return 2

    name = args.name if args.name.startswith(args.prefix) else args.prefix + args.name
    if not re.fullmatch(re.escape(args.prefix) + r"[a-z0-9][a-z0-9-]*", name):
        print(f"bad domain name: {name!r} (lowercase, digits, dashes)")
        return 2
    if (ws / name).exists():
        print(f"{name} already exists")
        return 2

    job = plan(name, need, words, args.lang, date)

    print("plan")
    print(f"  workspace:   {ws}")
    print(f"  domain:      {name}")
    print(f"  description: {job['values']['description']}")
    for rel in job["files"]:
        print(f"  file:        {name}/{rel}")
    print(f"  dirs:        {', '.join(job['dirs'])}")
    print(f"  register:    {'yes' if args.register else 'no (rows printed at the end)'}")
    if not args.yes:
        answer = input("\napply? [y/N] ").strip().lower()
        if answer not in ("y", "yes"):
            print("cancelled")
            return 1

    import check
    before = {str(f) for f in check.run(ws, args.prefix) if f.level == "FAIL"}

    apply(job, ws)

    if args.register:
        for note in register(ws, job):
            print(f"  {note}")

    after = [f for f in check.run(ws, args.prefix) if f.level == "FAIL"]
    introduced = [f for f in after if str(f) not in before]
    if introduced:
        print("\nthis domain does not conform; removing it")
        for finding in introduced:
            print(f"  {finding}")
        shutil.rmtree(ws / name)
        return 1

    print(f"\ncreated {name}")
    if not args.register:
        print("\nregister it by adding two rows to " + IDENTITY + ":")
        print(f"  | {name} | `{name}/` | <one line> | `{name}/SKILL.md` |")
        print(f"  | {args.words} | `{name}` |")
        print("  (or rerun with --register)")
    print(f"\nacceptance - a domain is not built until these pass:")
    print(f"  aw verify {name}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    raise SystemExit(main())
