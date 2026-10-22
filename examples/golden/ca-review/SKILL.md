---
name: ca-review
description: Use when the user asks for a second opinion, says "review this", "argue both sides", "is this plan sound", or keeps going back and forth on a decision.
---

# ca-review — a domain whose output is a judgement, not a record

> Fixture. The other two examples append rows. This one produces a decision, which is a
> different shape: several independent passes over the same evidence, the disagreements
> kept, and exactly one dated verdict.

## When to load

- "review this before I send it"
- "argue both sides of this"
- "I keep going back and forth on X"
- "is this plan sound?"

## The protocol

1. **Frame it.** Write the question in one sentence and the decision it feeds. If you
   cannot name the decision, there is nothing to review yet — stop here.
2. **Independent passes.** Run several passes over the same evidence, each with a
   different brief and **none of them seeing the others**: argue for, argue against,
   assume it failed in six months and explain why.
3. **Keep the disagreement.** Where the passes disagree is the real uncertainty. Where
   they agree is not evidence — three passes written by the same model share its blind
   spots.
4. **One verdict.** The owner decides. A review ends with a dated decision line, not a
   pile of recommendations.

## Rules

- **Passes must be blind to each other.** A model criticising its own answer three times
  produces one opinion in three costumes.
- **Evidence before opinion.** Every claim names the file, entry or event it rests on.
  "It feels risky" is not a finding.
- **No new facts in the verdict.** If the verdict needs something the passes did not
  establish, the review is incomplete — go back to the evidence.
- **"It depends" is a failed review.** "It depends on X, and X will be known by date Y"
  is a decision.
- **A verdict carries its date.** Quoting a conclusion without the date turns it into
  folklore within a month.

## Record format

One file per review, `1-reviews/YYYY-MM-DD-<slug>.md`:

```markdown
# <the question, one sentence>
decides: <the decision this feeds> · owner: <who> · date: YYYY-MM-DD

## Evidence
- <file, entry or event, with the specific line>

## Passes
### A — argue for
### B — argue against
### C — assume it failed in six months; why

## Where they disagree
- <the disagreement, and what would settle it>

## Verdict
- YYYY-MM-DD · <one line>
```

## Maintenance

| when | do |
|---|---|
| after each review | append a block to the event log |
| the protocol changed | append one line to the decision log |
