---
name: ca-finance
description: Use when the user mentions money, spending, a receipt, rent, the ledger, an account balance, or asks how much was spent this month.
---

# ca-finance — money in, money out, and no number that was not computed

> Fixture. The amounts are invented; the conventions are the ones that survived real use.
> This domain exists in the examples because M5 needs a domain where doing arithmetic in
> your head is obviously unacceptable.

## When to load

- "spent 40 on groceries, log it"
- "how much did I spend this month"
- "what is left in account A"
- "rent went out today"

## Record format

One row per movement, `0-ledger/YYYY-MM.csv`:

```csv
date,amount,category,account,note
2026-10-03,-1200.00,housing,account-a,rent
2026-10-05,-86.40,food,account-a,groceries
2026-10-08,3000.00,income,account-a,salary
```

| field | required | meaning |
|---|---|---|
| `date` | yes | the day the money moved |
| `amount` | yes | **signed**: negative is spending, positive is income |
| `category` | yes | one of the categories in `0-ledger/accounts.csv`, or a new one |
| `account` | yes | which account it left or entered |
| `note` | | one phrase |

## Rules

- **csv holds data, markdown holds rules.** Never put a table of amounts in a `.md` file;
  a number in prose cannot be recomputed and cannot be checked.
- **Every number comes from `4-engine/ledger.py`.** If the script cannot produce it, add a
  subcommand. Do not compute it in the conversation.
- **Read before write.** A script that opens a file for writing before reading it has
  already lost data — this happened once, to this very ledger.
- **One period, defined once.** The accounting period is a setting, not a habit; changing
  it is a decision-log entry, not a per-conversation choice.
- **Single source.** Balances that belong to another domain are referenced by pointer,
  never copied here. Two copies of a balance is one balance plus a future argument.
- **A refund offsets its original category**, positive amount, and is never income.

## How to work

```bash
python 4-engine/ledger.py summary --month 2026-10
python 4-engine/ledger.py record --date 2026-10-12 --amount -12.50 --category food --account account-a --note lunch
```

The model understands the request and explains the output. It never adds up the column.

## Maintenance

| when | do |
|---|---|
| after each entry batch | append a block to the event log |
| a convention changed | append one line to the decision log |
