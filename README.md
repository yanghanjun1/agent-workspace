# agent-workspace

**The bot changes. The workspace doesn't.**

A workspace is a directory your agent opens: one small identity file, one manual per
life-domain, and two logs that keep the whole thing from rotting. Domains are generated
by the agent from a sentence, and conformance is checked by an assertion rather than by
vibes.

No dependencies. No build step. No vendor. Markdown and one standard-library script.

---

## The problem

An assistant that answers well and remembers nothing is a search engine with manners.
So people put everything in the system prompt — and after a few weeks the rules stop
being obeyed, because the file is 800 lines and every turn re-sends it.

Then, three months later, the second problem arrives: nobody remembers why anything is
the way it is, so every change forces a re-derivation, and two re-derivations disagree.
The assistant starts contradicting itself and everyone blames the model.

And when you switch tools, all of it is gone — because it lived in one product's
session store, not in a file.

## What this is

| | |
|---|---|
| **A spec** — `SPEC.md` | Seven MUSTs that define a conforming workspace. Normative, citable, small. |
| **A generator** — `aw new` | A need in your own words becomes a domain: manual, two axes, first decision entry, working reporter. |
| **A checker** — `aw check` | Every MUST is a function that can fail. Exit 1 means it did. |
| **Evidence** — `examples/` | Ten needs in, ten conforming workspaces out, on three operating systems in CI. |

It is **not** a bot, a plugin, a memory service, a RAG pipeline, or a framework. Those
are execution-layer choices. This is the layer a bot reads.

---

## Quickstart

```bash
git clone https://github.com/yanghanjun1/agent-workspace && cd agent-workspace

mkdir -p ../my-workspace
cp templates/AGENTS.md ../my-workspace/AGENTS.md     # the identity file: yours to write

python tools/aw new ca-reading \
  --need "track what I read each week" \
  --words "reading/book/pages" \
  --workspace ../my-workspace --yes

python tools/aw check ../my-workspace
```

Expected output of the last command:

```
workspace: .../my-workspace
domains:   1

  OK   --   conforming at level 2 (all MUST)

conforming.
```

Then open the workspace with whatever agent you use:

```bash
cd ../my-workspace && codex      # or dsh, or claude, or anything that reads a directory
> I read 30 pages of Sapiens today
```

If the agent opens `ca-reading/SKILL.md` on its own, the domain works. If it does not,
the problem is the `description` — not the model. `aw verify ca-reading` walks you
through the three acceptance questions.

---

## The three layers

```
identity     AGENTS.md          small, injected every turn, writes only routes
   │  routes by the words you actually use
   ▼
manuals      ca-*/SKILL.md      long, loaded on demand, holds the procedures
   │  reads and writes
   ▼
memory       event log · decision log · CURRENT.md
```

`WHY.md` explains what each layer answers, and what it costs. Short version: the
identity file is a **budget law** (it is re-sent every turn, so it may only hold what
must be true every turn), and the two logs are the difference between an assistant that
remembers and an assistant that stays *correct*.

---

## The seven rules

| | Rule | In one line |
|---|---|---|
| **M0** | One workspace, one root | A domain is never a workspace. Domains die; workspaces migrate. |
| **M1** | Identity writes routes | ≤200 lines, a routing table, no procedures, no secrets. |
| **M2** | A domain is a directory with a manual | `SKILL.md`, `name` = directory, `description` says *when*. |
| **M3** | Two axes, both non-empty | An empty log is not an axis. |
| **M4** | Append-only, except facts | History is immutable; wrong facts are corrected in place. |
| **M5** | Computation belongs in a script | A model that does arithmetic gives a different answer each time. |
| **M6** | One source per fact | Two copies of a rule is one copy plus a future contradiction. |

`SPEC.md` gives the rationale for each and says which ones a machine can check. M4b
cannot be checked; the spec says so instead of pretending.

---

## Portability

The test is mechanical, not aspirational:

> **A workspace is portable to a harness if that harness can start with the workspace as
> its working directory and read a file at the root.**

That is why there is nothing to install. `cd workspace && agent` — the agent is a
process, not a place. Harnesses without a working directory (web chat) are a different
tier, and `PORTABILITY.md` says what breaks there and which rules degrade.

---

## What it costs

- You write the identity file once, by hand. It says who the assistant is and what it
  owns; an agent writing its own job description writes one it likes. `aw new` refuses
  to run outside a workspace for the same reason.
- You keep two logs. Not writing them is the default, and the default degrades back into
  a chat window in about three weeks.
- A generated domain needs acceptance, not just creation. Three questions, one command.
- It is not smarter. It is only less forgetful — which removes most of what people blame
  on the model.

---

## Repository map

```
SPEC.md          the normative text: M0-M6, S1-S3, MAY patterns
WHY.md           five failure scenes, three layers, the cost
PORTABILITY.md   the mechanical criterion, tiers, degradation, measured matrix
templates/       the identity file and the domain skeleton (.zh.md variants for --lang zh)
tools/aw         check · new · verify · link  (standard library only)
examples/        golden fixtures (reading, finance) + ten input needs used by the tests
docs/            long-form guides: philosophy, layout, building a domain, memory, pitfalls, case study
tests/           22 tests: every MUST can fail, and ten needs conform
```

## Status

Draft 0.1. The spec is the part that should outlive everything else here; the tools are
its reference implementation and are allowed to be boring.

## Contributing

Read `CONTRIBUTING.md`. The bar is narrow on purpose: corrections, example inputs,
translations, and portability rows with a harness and a version.

## License

MIT.
