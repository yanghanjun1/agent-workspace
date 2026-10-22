# 02 · Layout

## A workspace is not a domain

This is the easiest thing to get wrong and the most expensive (M0).

```
<workspace>/              ← repo root = workspace root, exactly one AGENTS.md
├── AGENTS.md             ← identity: the routing table lives here
├── CURRENT.md            ← open work (single source)
├── _scratch/             ← throwaway artifacts (.gitignore)
└── ca-<domain>/          ← a domain: manual + two axes + data + scripts
```

**A domain cannot be a workspace.** Three reasons:

| A workspace has | A domain has |
|---|---|
| a routing table (words → manual) | one manual, and no choice to make |
| `CURRENT.md` | nowhere to put cross-domain work |
| an ownership boundary | an agent that invents other domains' work |

The structural reason is lifecycle: **domains die, workspaces migrate.** A domain that
stops being used is `mv`-ed to an archive and two rows come out of the identity file. A
workspace is the root — it is moved, never archived. Two objects with different lifecycles
cannot sit at the same level.

So do not put a workspace inside another workspace either: that yields two identity files,
two task files and a nested repository, and routing becomes ambiguous immediately.
**Switching agents means switching launchers, not moving house.**

## Inside a domain

```
ca-<domain>/
├── SKILL.md          ← the manual (required; frontmatter has name + description)
├── log.md            ← event axis
├── decisions.md      ← object axis
├── 0-raw/            ← raw inputs (usually .gitignore'd)
├── 1-data/           ← structured data (csv/jsonl/md)
└── 4-engine/         ← this domain's scripts
```

The numeric prefixes are not fussiness: **sorting is semantics.** Raw material first,
scripts last. Filenames may be English or any other language — the spec governs meaning,
the implementation governs naming.

## Where things go

| Thing | Where |
|---|---|
| one-off scripts, intermediate data, debug output | `_scratch/`, and say "discardable" at delivery |
| a domain's real data | that domain's `1-data/` |
| a domain's raw input | that domain's `0-raw/` (personal data stays out of git) |
| conventions, rules, procedures | that domain's `SKILL.md`, **not** `AGENTS.md` |
| keys, tokens, session stores | environment or the OS keychain, **never** git |

## Does data belong in git?

One criterion: **would leaking it hurt someone?**

- Yes (health, money, identity, chat logs) → `.gitignore` it, or use a separate private repo
- No (scripts, templates, general knowledge) → commit it

But "not in git" is not "not backed up": a local repo plus a private remote is a different
question.

## What CURRENT.md looks like

```markdown
# CURRENT.md

## State
- 2026-10-21 · <one line describing where things stand>

## OPEN_LOOPS
- [ ] <an actionable next step> · <domain> · <when>
```

Two disciplines: **keep only what is live** (finished items move to an archive — not
deleted, just not in the table), and **one line per item**.
