# Event log

> One block per working day. The block date is the day you worked, not the day the
> thing happened (put that in the body). Newest on top. Append; never rewrite history.

## 2026-09-02

- did: rebuilt the ledger after a script emptied it; added the read-before-write rule
- artifacts: `ca-finance/0-ledger/2026-09.csv`, `ca-finance/4-engine/ledger.py`
- blocked / open: three entries from August were reconstructed from memory, not from data
- next: check whether any other script opens a data file for writing first
- handoff: -

## 2026-08-20

- did: created ca-finance for: log every purchase and reconcile once a month
- artifacts: `ca-finance/SKILL.md`, `ca-finance/log.md`, `ca-finance/decisions.md`
- blocked / open: no real entries yet
- next: enter one week of real spending, then run the summary
- handoff: -
