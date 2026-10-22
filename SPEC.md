# SPEC.md — Workspace Conformance

**Status:** draft 0.1 · normative text is English; long-form guides under `docs/` are Chinese.

The key words MUST, MUST NOT, SHOULD and MAY are used as in RFC 2119.

This document specifies what a *workspace* is and the minimum an implementation must
satisfy to call itself conforming. It deliberately says nothing about which agent reads
the workspace, which model runs it, or how data is stored — those are execution-layer
choices, and the whole point is that they can change.

---

## 0. Terms

- **Workspace** — a directory an agent opens, normally the root of a git repository. It
  holds one identity file, zero or more domains, and a task file.
- **Domain** — a subdirectory holding one manual (`SKILL.md`), two logs, and whatever data
  that domain needs. A domain is a plugin: add a directory, get a capability.
- **Identity file** — `AGENTS.md`. Injected at the start of every session.
- **Manual** — a domain's `SKILL.md`. Loaded on demand, never injected by default.
- **Event log / decision log** — the two axes. What happened, and why it is the way it is.

---

## 1. M0 — One workspace, one root

> A workspace root is the repository root and contains exactly one identity file.
> Domains are subdirectories of a workspace and MUST NOT themselves be workspaces.
> A workspace MUST NOT be nested inside another workspace.

**Why.** A domain has a manual; a workspace has a *routing table*. Load-on-demand only
means something when there is a choice to make, and only the workspace can hold that
choice. A domain also has no task file and no ownership boundary, so cross-domain work
has nowhere to land.

The structural reason is lifecycle: **domains die, workspaces migrate.** A domain is
archived when it stops being used (`mv ca-x ../archive/`, delete two rows from the
identity file). A workspace is the root — it is moved, never archived. Two objects with
different lifecycles cannot sit at the same level.

**Checked.** The checker walks the parent chain: an identity file in any ancestor is a
violation. Domain directories with no identity file beside them are a violation.

---

## 2. M1 — The identity file writes routes, not procedures

> The identity file MUST be at most 200 lines, MUST contain a routing table that maps the
> user's own words to a domain, and MUST NOT contain procedures, domain rules, amounts,
> credentials, or session data.

**Why.** The identity file is re-sent every turn. Its cost is paid on every request, and
every line added dilutes the lines already there. This is a budget law, not a style
preference: at 800 lines, roughly a third of the rules stop being obeyed and the failure
looks like "the model got worse".

The left column of the routing table must be **what the user actually says**, not a
domain name. `"coffee / pour-over / beans"` routes; `"ca-coffee"` does not, because the
user never says that.

**Checked.** Line count; presence of a table with at least two rows; secret patterns
(`sk-…`, private-key blocks, 11-digit phone numbers); the user-words column is present.

---

## 3. M2 — A domain is a directory with a manual

> Every domain MUST contain `SKILL.md` with YAML frontmatter. `name` MUST equal the
> directory name. `description` MUST state *when to use this manual* in the user's
> vocabulary, and MUST be at least 12 characters.

**Why.** The model decides whether to open a manual from the `description` alone. A
description that says what the domain *is* ("coffee domain operations manual") is never
matched. One that says when to use it, using the words the user actually types, is
matched reliably.

**Checked.** Frontmatter parse; name/directory equality; description length; presence of
`Use when` or CJK trigger words.

---

## 4. M3 — Two axes, both non-empty

> Every domain MUST contain an event log and a decision log. Both MUST be non-empty.
> An empty file does not satisfy this.

**Why.** One timeline answers "what did I do last week". It never answers "why is the
period the 20th instead of the calendar month" — and three months later, that is the
question that matters. Without the second axis, every large change forces you to
re-derive the reasoning, and the assistant starts contradicting itself.

**Checked.** Presence and non-emptiness after stripping headings and comments. This is
the rule most generators fail, because an empty log is the cheapest thing to emit.

---

## 5. M4 — The decision log is append-only, except for facts

> **M4a.** Every entry in the decision log MUST match `- YYYY-MM-DD · … · because …`
> (the separator may be `·` or `|`).
> **M4b.** History MUST NOT be rewritten — except factual errors, which MUST be corrected
> in place, with a correction entry recording what changed and why.

**Why M4b.** Almost every memory system says "append-only" and therefore accumulates
wrong facts that nobody dares touch. A log that protects its own errors stops being
usable. The judgement is one question: *if I leave this, will I later act on something
false?* If yes, fix it and log the correction. If no, append.

**Checked.** M4a is machine-checked line by line. **M4b cannot be checked by a machine**
— it is a manual review item, and pretending otherwise would be the exact dishonesty
this spec exists to prevent.

---

## 6. M5 — Computation belongs in a script

> If a manual describes producing a number (totals, summaries, reconciliation, reports),
> it MUST reference a script that exists inside the domain.

**Why.** A language model re-derives arithmetic differently each time it is asked. Numbers
that come out of a conversation are not data, they are a rumour. The model's job is to
understand the request and explain the result; the script's job is to produce it.

**Checked.** Keyword scan of the manual; every referenced script path must resolve.

---

## 7. M6 — One source per fact

> The identity file MUST NOT repeat, verbatim, any line of twelve characters or more from
> a domain manual.

**Why.** Two copies of a rule is one copy plus a future contradiction. The failure is
silent: you update the manual, the identity file keeps the old version, and behaviour
depends on which one the model happened to read first.

**Checked.** Line-level comparison between the identity file and every manual.

---

## 8. SHOULD

- **S1.** One scratch zone (`_scratch/`) for throwaway scripts and intermediate data, and
  every delivery names two lists: discardable artifacts and named artifacts. A workspace
  where nothing may be deleted becomes a workspace nobody dares touch.
- **S2.** Volatile numbers (balances, counts, prices) are not copied into status
  summaries. A summary number starts expiring the moment it is written, and it looks like
  a fact.
- **S3.** An irreversible action gets a receipt first: what changes, what it affects, how
  to undo it.

---

## 9. MAY — patterns, not requirements

These come from one particular deployment. Copy the shape, not the content.

- **X1.** Permission tiers (read / scratch-write / owner-files / real-world-action).
- **X2.** Multi-party review: the same question put to several independent passes before
  a decision.
- **X3.** An inbound receiver on a public host that validates a token, writes the payload,
  and reports a count — and knows nothing about the domain it feeds.

---

## 10. Conformance levels

| Level | Requirement |
|---|---|
| **1 — structured** | M0, M2, M3 |
| **2 — conforming** | all MUST (M0–M6) |
| **3 — disciplined** | all MUST + all SHOULD |

Claim the highest level your checker passes, and say which rules you cannot check.

---

## 11. Out of scope

Harness, model, storage engine, language of filenames, sync mechanism, encryption,
whether the agent runs locally or in the cloud. A workspace that needs a specific vendor
to be readable has already failed M0 in spirit.
