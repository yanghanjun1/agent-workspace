#!/usr/bin/env python3
"""aw check - reference implementation of SPEC.md.

Every MUST in the spec maps to one function below. Exit 0 = conforming,
exit 1 = at least one violation, exit 2 = bad invocation.

Two deliberate constraints:

* Standard library only. A workspace must stay readable by an agent that has
  nothing installed but a shell.
* Output must survive a cp936 console. A Chinese Windows console cannot encode
  a check mark or an arrow, and the checker used to die on its own success
  message. Failures are reported as FAIL/WARN, never as decoration.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

IDENTITY = "AGENTS.md"
MAX_IDENTITY_LINES = 200
MIN_DESCRIPTION = 12
DEFAULT_PREFIX = "ca-"

# First existing name wins, so a workspace may use either language.
LOG_NAMES = ("log.md", "流水.md")
DECISION_NAMES = ("decisions.md", "维护日志.md")

SECRET_PATTERNS = (
    (re.compile(r"\bsk-[A-Za-z0-9_-]{16,}"), "API key"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key block"),
    (re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"), "phone number"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"), "GitHub token"),
)

ROUTING_HEADERS = ("说什么", "读", "words", "say", "trigger", "route", "task", "任务")
COMPUTE_WORDS = re.compile(r"统计|汇总|对账|求和|周报|月报|report|summary|total|reconcile|aggregate", re.I)
SCRIPT_REF = re.compile(r"([\w./\\\-\u4e00-\u9fff]+\.(?:py|sh|js|ps1|bash))")
CJK = re.compile(r"[\u4e00-\u9fff]")


class Finding:
    __slots__ = ("level", "rule", "message")

    def __init__(self, level: str, rule: str, message: str) -> None:
        self.level = level
        self.rule = rule
        self.message = message

    def as_dict(self) -> dict:
        return {"level": self.level, "rule": self.rule, "message": self.message}

    def __str__(self) -> str:
        return f"{self.level:<4} {self.rule:<3} {self.message}"


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(text: str) -> dict:
    """Minimal YAML frontmatter: flat key: value pairs, nothing else."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    data = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([\w-]+):\s*(.*)$", line.strip())
        if m:
            data[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return data


def content_lines(text: str) -> list[str]:
    """Lines that carry meaning: no headings, quotes, comments or blanks."""
    out = []
    for raw in text.splitlines():
        s = raw.strip()
        if not s or s.startswith("#") or s.startswith(">") or s.startswith("<!--"):
            continue
        out.append(s)
    return out


def table_blocks(text: str) -> list[list[str]]:
    blocks, current = [], []
    for raw in text.splitlines():
        if raw.strip().startswith("|"):
            current.append(raw.strip())
        elif current:
            blocks.append(current)
            current = []
    if current:
        blocks.append(current)
    return blocks


def first_existing(directory: Path, names: tuple[str, ...]) -> Path | None:
    for name in names:
        candidate = directory / name
        if candidate.is_file():
            return candidate
    return None


def domains(ws: Path, prefix: str) -> list[Path]:
    if not ws.is_dir():
        return []
    return sorted(p for p in ws.iterdir() if p.is_dir() and p.name.startswith(prefix))


# --------------------------------------------------------------------------- #
# M0 - one workspace, one root
# --------------------------------------------------------------------------- #
def check_m0(ws: Path, prefix: str) -> list[Finding]:
    out: list[Finding] = []
    identity = ws / IDENTITY

    if not identity.is_file():
        if domains(ws, prefix):
            out.append(Finding("FAIL", "M0",
                f"domains exist here but there is no {IDENTITY}: a domain is not a workspace"))
        else:
            out.append(Finding("FAIL", "M0", f"no {IDENTITY} at {ws}"))

    for parent in ws.parents:
        if (parent / IDENTITY).is_file():
            out.append(Finding("FAIL", "M0",
                f"nested workspace: {parent} also holds {IDENTITY} (one root, one identity)"))
            break

    return out


# --------------------------------------------------------------------------- #
# M1 - the identity file writes routes, not procedures
# --------------------------------------------------------------------------- #
def check_m1(ws: Path) -> list[Finding]:
    out: list[Finding] = []
    identity = ws / IDENTITY
    if not identity.is_file():
        return out
    text = _read(identity)
    lines = text.splitlines()

    if len(lines) > MAX_IDENTITY_LINES:
        out.append(Finding("FAIL", "M1",
            f"{IDENTITY} is {len(lines)} lines, budget is {MAX_IDENTITY_LINES}: move procedures into manuals"))

    routing = [b for b in table_blocks(text)
               if len(b) >= 3 and any(h.lower() in b[0].lower() for h in ROUTING_HEADERS)]
    if not routing:
        out.append(Finding("FAIL", "M1",
            "no routing table: the identity file must map the user's own words to a domain"))

    for pattern, label in SECRET_PATTERNS:
        if pattern.search(text):
            out.append(Finding("FAIL", "M1", f"{label} found in {IDENTITY}"))

    return out


# --------------------------------------------------------------------------- #
# M2 - a domain is a directory with a manual
# --------------------------------------------------------------------------- #
def check_m2(dom: Path) -> list[Finding]:
    out: list[Finding] = []
    skill = dom / "SKILL.md"
    if not skill.is_file():
        return [Finding("FAIL", "M2", f"{dom.name}: no SKILL.md")]
    fm = parse_frontmatter(_read(skill))

    if fm.get("name") != dom.name:
        out.append(Finding("FAIL", "M2",
            f"{dom.name}: frontmatter name={fm.get('name')!r} must equal the directory name"))

    desc = fm.get("description", "")
    if len(desc) < MIN_DESCRIPTION:
        out.append(Finding("FAIL", "M2",
            f"{dom.name}: description too short ({len(desc)} chars), the manual will never be selected"))
    elif "use when" not in desc.lower() and not CJK.search(desc):
        out.append(Finding("FAIL", "M2",
            f"{dom.name}: description must say when to use it (e.g. 'Use when the user mentions ...')"))

    return out


# --------------------------------------------------------------------------- #
# M3 - two axes, both non-empty
# --------------------------------------------------------------------------- #
def check_m3(dom: Path) -> list[Finding]:
    out: list[Finding] = []
    for names, label in ((LOG_NAMES, "event log"), (DECISION_NAMES, "decision log")):
        path = first_existing(dom, names)
        if path is None:
            out.append(Finding("FAIL", "M3",
                f"{dom.name}: no {label} ({' or '.join(names)})"))
        elif not content_lines(_read(path)):
            out.append(Finding("FAIL", "M3",
                f"{dom.name}: {label} is empty - an empty file is not an axis"))
    return out


# --------------------------------------------------------------------------- #
# M4a - decision log entry format
# --------------------------------------------------------------------------- #
DECISION_LINE = re.compile(r"^-\s*\d{4}-\d{2}-\d{2}\s*[·|]")


def check_m4a(dom: Path) -> list[Finding]:
    path = first_existing(dom, DECISION_NAMES)
    if path is None:
        return []
    out: list[Finding] = []
    for number, raw in enumerate(_read(path).splitlines(), 1):
        s = raw.strip()
        if not s.startswith("-"):
            continue
        if not DECISION_LINE.match(s):
            out.append(Finding("FAIL", "M4a",
                f"{dom.name}:{number}: entry must look like '- YYYY-MM-DD · from X to Y · because Z'"))
    return out


# --------------------------------------------------------------------------- #
# M5 - computation belongs in a script
# --------------------------------------------------------------------------- #
def check_m5(dom: Path) -> list[Finding]:
    skill = dom / "SKILL.md"
    if not skill.is_file():
        return []
    text = _read(skill)
    if not COMPUTE_WORDS.search(text):
        return []

    out: list[Finding] = []
    refs = [r for r in SCRIPT_REF.findall(text) if not r.endswith(("SKILL.md",))]
    if not refs:
        out.append(Finding("FAIL", "M5",
            f"{dom.name}: the manual produces numbers but names no script - the model would do arithmetic"))
        return out
    for ref in refs:
        if not (dom / ref).exists():
            out.append(Finding("FAIL", "M5",
                f"{dom.name}: manual references {ref}, which does not exist"))
    return out


# --------------------------------------------------------------------------- #
# M6 - one source per fact
# --------------------------------------------------------------------------- #
def check_m6(ws: Path, prefix: str) -> list[Finding]:
    identity = ws / IDENTITY
    if not identity.is_file():
        return []
    own = {s for s in content_lines(_read(identity)) if len(s) >= 12 and not s.startswith("|")}
    out: list[Finding] = []
    for dom in domains(ws, prefix):
        skill = dom / "SKILL.md"
        if not skill.is_file():
            continue
        for line in content_lines(_read(skill)):
            if len(line) >= 12 and line in own:
                out.append(Finding("FAIL", "M6",
                    f"{dom.name}: this line is also in {IDENTITY} - one source per fact: {line[:60]}"))
                break
    return out


# --------------------------------------------------------------------------- #
def run(ws: Path, prefix: str = DEFAULT_PREFIX) -> list[Finding]:
    ws = ws.expanduser().resolve()
    findings = check_m0(ws, prefix)
    if (ws / IDENTITY).is_file():
        findings += check_m1(ws)
        findings += check_m6(ws, prefix)
    for dom in domains(ws, prefix):
        findings += check_m2(dom) + check_m3(dom) + check_m4a(dom) + check_m5(dom)
    return findings


def main(path: str = ".", prefix: str = DEFAULT_PREFIX, as_json: bool = False) -> int:
    ws = Path(path)
    findings = run(ws, prefix)
    failures = [f for f in findings if f.level == "FAIL"]

    if as_json:
        print(json.dumps({"workspace": str(ws.resolve()),
                          "conforming": not failures,
                          "findings": [f.as_dict() for f in findings]}, ensure_ascii=False, indent=2))
        return 1 if failures else 0

    print(f"workspace: {ws.resolve()}")
    print(f"domains:   {len(domains(ws.expanduser().resolve(), prefix))}")
    print()
    for finding in findings:
        print(f"  {finding}")
    if not findings:
        print("  OK   --   conforming at level 2 (all MUST)")
    print()
    if failures:
        print(f"{len(failures)} violation(s). SPEC.md explains why each rule exists.")
        return 1
    print("conforming.")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    parser = argparse.ArgumentParser(prog="check.py", description="Check a workspace against SPEC.md")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--prefix", default=DEFAULT_PREFIX)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    raise SystemExit(main(args.path, args.prefix, args.json))
