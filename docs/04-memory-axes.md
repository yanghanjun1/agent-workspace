# 04 · Two axes: the event log and the decision log

## Why two lines

One timeline answers "what did I do last week". It never answers "why is it like this".

The questions you ask three months later are almost all the second kind:

- Why does the accounting period start on the 20th instead of the calendar month?
- Why did this domain move from the cloud back to local?
- Why does the task list no longer read that file directly?

None of those are in ninety blocks of "what I did today". One line in the decision log
answers each of them. **So the axes are separate documents, not one document written twice.**

```
event log      ←→  time axis: one block per day
decision log   ←→  object axis: each thing's own history
```

## The event log

The block date is **the day you did the work**, not the day the thing happened (put that
in the body).

Five fixed fields; drop one and it stops being readable:

```markdown
## 2026-10-21
- did:
- artifacts: (full paths)
- blocked / open:
- next:
- handoff: (commit / backup / how to roll back)
```

Newest on top. Four rules of thumb:

| Situation | How to write it |
|---|---|
| You only looked something up, changed nothing | do not write a block (do not invent one to fill a grid) |
| The data is from the 4th but entered today | block date is today, body says "entries for the 4th" |
| You changed a convention | event log says what you did; decision log says what it became |
| Several unrelated things in one day | one block, several lines |

## The decision log

One line per decision, grouped by object, three parts:

```
date · from "old" to "new" · because …
```

```markdown
## Accounting period
- 2026-09-12 · from "calendar month" to "the 20th" · because salary lands on the 20th and the calendar month does not match cash flow
```

What counts as an object: a rule, a mechanism, a structure, a decision.

The test: **if someone asks "why is it like this", can this line answer in one sentence?**

---

## 🔴 Append-only, except for facts

This is the rarest rule in the whole method, and the one almost every memory system gets
wrong.

**History layers** (both axes) are append-only: if a judgement is overturned, do not edit
the original — add a new line.
**Live tables** (`CURRENT.md` OPEN_LOOPS, per-domain state) keep only what is live: move
finished items to an archive.

**But "append-only" protects historical facts, not errors.**

A mistyped number, a wrong path, a reversed fact — **fix it in place**, then record one
correction line in the decision log: `correction: X to Y, because …`.

One test decides it:

> **If I leave this, will I later act on something false?**

Yes → fix it. No → append.

A log that protects its own errors stops being trusted within three weeks.

---

## Anti-patterns

| Anti-pattern | Consequence |
|---|---|
| The event log becomes a diary ("felt good today") | three months of noise, and you cannot find what you did |
| The decision log becomes a changelog (grouped by date) | a second timeline; the object axis is lost |
| Closed loops pile up in OPEN_LOOPS | live items drown, and two contradictory rows appear in one batch |
| Events without decisions | every large change re-derives the reasoning from scratch |
| Only saying it in the conversation | closing the session equals it never happening |
