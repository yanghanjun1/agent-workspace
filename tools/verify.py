#!/usr/bin/env python3
"""aw verify - the three acceptance questions.

Creating a domain is cheap; a generated domain that was never exercised is a folder
with good intentions. These three questions are the difference between "the files
exist" and "the domain works on this harness":

  1. route    - say it the way you normally would; did the agent open the manual?
  2. compute  - ask for a number; did it run a script instead of doing arithmetic?
  3. write    - ask it to record something; did both axes gain a line?

Static checks cannot answer any of them. That is why this is a separate command.
"""

from __future__ import annotations

import argparse
import datetime
import sys
from pathlib import Path

QUESTIONS = (
    ("route", "Say it the way you normally would. Did the agent open this domain's manual?"),
    ("compute", "Ask for a number. Did it run a script instead of doing arithmetic itself?"),
    ("write", "Ask it to record one item. Did the event log AND the decision log each gain a line?"),
)

MATRIX_HEADER = ("| date | harness | domain | route | compute | write | verdict |",
                 "|---|---|---|---|---|---|---|")


def cell(value: str) -> str:
    """One markdown table cell: no newline, no unescaped pipe.

    The value lands in PORTABILITY.md, which people paste from; a pipe would silently
    split the row and a newline would forge a second one.
    """
    return " ".join(str(value).split()).replace("|", "\\|")


def ask(answers: str | None) -> list[str]:
    if answers:
        given = [a.strip().lower() for a in answers.split(",")]
        if len(given) != len(QUESTIONS):
            raise SystemExit("--answers needs three values, e.g. y,y,n")
        return given
    out = []
    for key, text in QUESTIONS:
        reply = input(f"[{key}] {text} [y/N] ").strip().lower()
        out.append("y" if reply in ("y", "yes") else "n")
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aw verify")
    parser.add_argument("domain")
    parser.add_argument("--harness", default="unknown", help="e.g. codex, dsh, claude-code")
    parser.add_argument("--answers", help="non-interactive: y,y,y")
    parser.add_argument("--date", default=datetime.date.today().isoformat())
    parser.add_argument("--portability", default="PORTABILITY.md")
    args = parser.parse_args(argv)

    results = ask(args.answers)
    passed = all(r == "y" for r in results)
    verdict = "accepted" if passed else "not accepted"

    cells = " | ".join("yes" if r == "y" else "no" for r in results)
    row = (f"| {cell(args.date)} | {cell(args.harness)} | {cell(args.domain)} "
           f"| {cells} | {verdict} |")
    print()
    print(row)

    target = Path(args.portability)
    if target.is_file():
        text = target.read_text(encoding="utf-8")
        if MATRIX_HEADER[0] in text and row not in text:
            target.write_text(text.rstrip() + "\n" + row + "\n", encoding="utf-8")
            print(f"appended to {target}")
    else:
        print("(no PORTABILITY.md here; the row was printed, not recorded)")

    if not passed:
        first = next(q for q, r in zip(QUESTIONS, results) if r == "n")
        print(f"\nfix [{first[0]}] first: {first[1]}")
    return 0 if passed else 1


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    raise SystemExit(main())
