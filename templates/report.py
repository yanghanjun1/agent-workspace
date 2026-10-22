#!/usr/bin/env python3
"""Report for {{name}}.

Numbers come from here, never from the model. The model understands the request
and explains the result; this script produces it.

    python 4-engine/report.py --week
    python 4-engine/report.py --month --field pages
"""

from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import sys

DATA = pathlib.Path(__file__).resolve().parents[1] / "{{data_dir}}"


def parse_date(value: str) -> datetime.date | None:
    try:
        return datetime.date.fromisoformat(str(value)[:10])
    except (ValueError, TypeError):
        return None


def load() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(DATA.glob("*.jsonl")):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                print(f"{path.name}:{number}: not valid JSON, skipped", file=sys.stderr)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Report for {{name}}")
    parser.add_argument("--week", action="store_true", help="current week, Monday first")
    parser.add_argument("--month", action="store_true")
    parser.add_argument("--field", help="numeric field to sum, e.g. pages")
    args = parser.parse_args()

    rows = load()
    today = datetime.date.today()

    if args.week:
        start = today - datetime.timedelta(days=today.weekday())
        rows = [r for r in rows if (d := parse_date(r.get("date"))) and start <= d <= today]
    elif args.month:
        rows = [r for r in rows
                if (d := parse_date(r.get("date"))) and (d.year, d.month) == (today.year, today.month)]

    print(f"records: {len(rows)}")
    if args.field:
        total = 0.0
        for row in rows:
            try:
                total += float(row.get(args.field) or 0)
            except (TypeError, ValueError):
                pass
        print(f"{args.field}: {total:g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
