#!/usr/bin/env python3
"""Ledger for ca-finance. Every number the assistant reports comes from here.

    python 4-engine/ledger.py summary --month 2026-10
    python 4-engine/ledger.py record --date 2026-10-12 --amount -12.50 \
        --category food --account account-a --note lunch

The rule this script exists to enforce is M5: a model that adds up a column gives a
different answer each time it is asked. It is also the place where "read before write"
lives - see append(), which reads the whole ledger before it touches the file.
"""

from __future__ import annotations

import argparse
import csv
import datetime
import pathlib
import sys

LEDGER = pathlib.Path(__file__).resolve().parents[1] / "0-ledger"
FIELDS = ("date", "amount", "category", "account", "note")
ACCOUNTS = "accounts.csv"


def ledger_files() -> list[pathlib.Path]:
    return sorted(p for p in LEDGER.glob("*.csv") if p.name != ACCOUNTS)


def load() -> list[dict]:
    rows: list[dict] = []
    for path in ledger_files():
        with path.open(encoding="utf-8", newline="") as handle:
            for number, row in enumerate(csv.DictReader(handle), 2):
                try:
                    float(row["amount"])
                except (KeyError, TypeError, ValueError):
                    print(f"{path.name}:{number}: bad amount, skipped", file=sys.stderr)
                    continue
                rows.append(row)
    return rows


def parse_date(value: str) -> datetime.date:
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        raise SystemExit(f"bad date: {value!r} (want YYYY-MM-DD)")


def cmd_record(args: argparse.Namespace) -> int:
    parse_date(args.date)
    amount = float(args.amount)
    path = LEDGER / f"{args.date[:7]}.csv"
    existing = load()  # read first: never open a data file for writing before reading it

    new_file = not path.exists()
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerow({
            "date": args.date,
            "amount": f"{amount:.2f}",
            "category": args.category,
            "account": args.account,
            "note": args.note or "",
        })

    print(f"recorded {amount:+.2f} in {args.category} ({len(existing) + 1} entries total)")
    return 0


def cmd_summary(args: argparse.Namespace) -> int:
    month = args.month or datetime.date.today().isoformat()[:7]
    rows = [r for r in load() if r["date"][:7] == month]
    if not rows:
        print(f"no entries in {month}")
        return 0

    by_category: dict[str, float] = {}
    by_account: dict[str, float] = {}
    for row in rows:
        amount = float(row["amount"])
        by_category[row["category"]] = by_category.get(row["category"], 0.0) + amount
        by_account[row["account"]] = by_account.get(row["account"], 0.0) + amount

    print(f"period {month} - {len(rows)} entries")
    print("\nby category")
    for name in sorted(by_category):
        print(f"  {name:<12} {by_category[name]:>10.2f}")
    print("\nby account")
    for name in sorted(by_account):
        print(f"  {name:<12} {by_account[name]:>10.2f}")
    print(f"\n  {'net':<12} {sum(by_category.values()):>10.2f}")
    return 0


def cmd_accounts(_: argparse.Namespace) -> int:
    path = LEDGER / ACCOUNTS
    if not path.exists():
        print("no accounts.csv")
        return 0
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            print(f"  {row.get('id', '?'):<12} {row.get('kind', ''):<8} {row.get('name', '')}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="ca-finance ledger")
    sub = parser.add_subparsers(dest="command", required=True)

    record = sub.add_parser("record", help="append one movement")
    record.add_argument("--date", required=True)
    record.add_argument("--amount", required=True, help="signed: negative is spending")
    record.add_argument("--category", required=True)
    record.add_argument("--account", required=True)
    record.add_argument("--note", default="")
    record.set_defaults(func=cmd_record)

    summary = sub.add_parser("summary", help="totals for one period")
    summary.add_argument("--month", help="YYYY-MM, default: this month")
    summary.set_defaults(func=cmd_summary)

    accounts = sub.add_parser("accounts", help="list accounts")
    accounts.set_defaults(func=cmd_accounts)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
