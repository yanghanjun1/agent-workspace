# Decision log

> One line per decision: `date · from X to Y · because Z`.
> This is the object axis — why it is the way it is, not what happened that day.
> Append-only, with one exception: a factual error is corrected in place, and the
> correction itself gets a line (M4b).

## Storage

- 2026-08-20 · domain created · because the owner asked for: log every purchase and reconcile once a month
- 2026-08-20 · from "markdown table" to "one csv per month" · because a total cannot be computed from prose, and a prose table silently disagrees with itself
- 2026-08-21 · from "two columns, income and expense" to "one signed amount" · because two columns can disagree about the same row, one cannot

## Period

- 2026-08-25 · from "calendar month" to "a configured period start" · because the calendar month does not match when money actually arrives

## Safety

- 2026-09-02 · added "read before write" to the manual · because a script opened the ledger for writing before reading it and the file came back empty

## Categories

- 2026-09-10 · from "free text" to "a closed list in accounts.csv" · because two spellings of the same category produce two totals that both look right
