---
name: {{name}}
description: {{description}}
---

# {{name}} — {{summary}}

> A manual, not a procedure dump. Loaded on demand, so it may be long — but past
> ~150 lines ask whether two domains are hiding in one.

## When to load

- {{need}}
- <more trigger situations, in the owner's words>

## Record format

One line per record, `1-data/{{name}}-YYYY-MM.jsonl`:

```json
{"date": "YYYY-MM-DD", "what": "...", "note": "..."}
```

| field | required | meaning |
|---|---|---|
| `date` | yes | the day it happened, not the day it was written |
| `what` | yes | one noun phrase |
| `note` | no | one sentence |

## Rules

- <a convention someone would get wrong without being told>
- <what counts as one record vs two>

## How to work

Numbers come from a script under `4-engine/`; the model understands the request and
explains the result. It never does the arithmetic itself.

```bash
python 4-engine/report.py --week
```

## Maintenance

| when | do |
|---|---|
| after each run | append one block to the event log |
| a rule changed | append one line to the decision log |
