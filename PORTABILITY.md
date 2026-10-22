# PORTABILITY.md — what actually moves

"Works with any agent" is a claim that costs nothing to make and is easy to disprove.
This page replaces it with a criterion you can test in one command, and a matrix you can
disagree with.

---

## 1. The criterion

> A workspace is portable to a harness **if and only if** that harness can start with the
> workspace as its working directory and read a file at the workspace root.

That is the whole requirement. It is why there is no install step, no manifest, no plugin
API, and no registry: a workspace is *opened*, not *installed*.

The corollary matters more than the rule:

> **The agent is a process, not a place.**

So "plugging in" means `cd workspace && agent`. It never means copying the workspace into
some other tool's directory. Doing that creates two identity files, two task files and a
nested repository — a violation of M0, and the single most common way to break routing.

---

## 2. What moves, what adapts, what doesn't

| Layer | Portable? | Why |
|---|---|---|
| Identity, manuals, two axes, data, scripts | **yes** | Plain files in a git repository. |
| Discovery (how a harness finds a manual) | **adapts** | Directory watch vs declared registry. See `adapters/`. |
| Entry file name (`AGENTS.md` and friends) | **adapts** | Generate it, never hand-maintain two copies. |
| Rules that assume a capability | **no** | A rule that needs a subagent does nothing on a harness without one. |

The third row is the honest one, and almost nobody writes it down.

---

## 3. Tiers

| Tier | Condition | What works | What breaks |
|---|---|---|---|
| **T1** | Working directory + file reads + a shell | Everything: routing, on-demand manuals, script-computed numbers, both logs | — |
| **T2** | Working directory + file reads, no skill discovery | Routing and manuals by explicit path; scripts if it can run them | Nothing opens a manual automatically; you point at the file |
| **T3** | No working directory (web chat) | Copy-paste only | Everything except the text of the identity file |

T3 is not a failure of the workspace. It is a failure of the harness to have a working
directory, and no amount of spec-writing fixes it.

---

## 4. Degradation: which rules survive a weaker harness

A rule is not a file. Some rules need the harness to be able to *do* something. Tag them,
and say what happens when the tag cannot be satisfied.

| Rule | Requires | Without it |
|---|---|---|
| M0–M3, M6 | files only | always enforced |
| M5 (computation in a script) | shell | script still exists, agent cannot run it; you run it and paste the output |
| "Delegate exploration to a sub-session" | subagent support | degrade to: the agent reads conclusions only, the owner splits the work |
| "Receipt before an irreversible action" | an approval gate | degrade to: the owner confirms in chat before the agent proceeds |
| "Both lists on every delivery" | nothing, but it is a habit | enforced by review, not by code |

The point is not to make every rule work everywhere. The point is to **know which ones
are still true**, instead of assuming all of them are.

---

## 5. Measured matrix

Rows are produced by `aw verify <domain> --harness <name>`. A row without a harness
version is not a row.

| date | harness | domain | route | compute | write | verdict |
|---|---|---|---|---|---|---|
| 2026-10 | codex-cli 0.48.0 | owner's private workspace (6 domains) | yes | yes | yes | accepted — reported by the author |
| — | — | — | — | — | — | *your row here* |

What the author's row means in practice: the workspace is opened as the working directory,
the agent reads the identity file at session start, and a one-sentence request routes to
the right manual without any registration step. No skill registry was involved.

What it does **not** mean: that every harness behaves the same way. A harness that only
reads a global registry would need the adapter in `adapters/`, and the row would say so.

---

## 6. Adding a row

```bash
cd my-workspace
python /path/to/agent-workspace/tools/aw verify ca-reading --harness "codex-cli 0.48.0"
```

Three questions, answered by you, appended to the table above. If a question fails, the
row is still worth recording — a matrix of successes only is marketing.

---

## 7. What is deliberately not portable

- **The inbound receiver.** A small HTTP endpoint that validates a token, writes a file
  and reports a count. It is infrastructure; it should stay dumb and stay put. Do not
  abstract it into the workspace.
- **Scheduling.** Cron belongs to the host, not to the method.
- **Model choice.** Any rule that only holds for one model is a rule that will expire.

Writing down what you refuse to abstract is what keeps a method from turning into a
framework.
