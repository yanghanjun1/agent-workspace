# SETUP.md — letting an agent do the setup

A copy-paste prompt is the most convenient way to bootstrap a workspace, and it is also
the easiest place for a project like this one to contradict itself. So, first:

> **A setup prompt is not a dependency.** It runs once, writes files, and exits. The
> workspace it leaves behind contains no record of which agent wrote it, and every later
> session can use a different one. That is the whole point of ending the prompt at
> `aw check` instead of at "done!".

The prompt is also deliberately short on rules. It tells the agent to **read `SPEC.md`
and follow it** rather than restating the spec in the prompt — a prompt that repeats the
spec becomes a second source, and second sources drift (M6).

---

## The prompt

Paste everything between the fences into your agent.

```text
Set up an agent workspace for me from the agent-workspace repository.

1. Read SPEC.md and docs/03-build-a-domain.md in that repository. Follow them.
   Do not summarize them back to me.
2. Ask me which directory to use as the workspace. Create nothing yet.
3. Tell me what you will create, where, and how I undo it. Wait for my yes.
4. Copy templates/AGENTS.md into that directory as AGENTS.md. Then interview me for
   the three things you cannot know, and fill the file in from my answers only:
     - what my first domain covers
     - the words I actually use when I talk about it
     - where that domain's data will come from
5. Run:
   python <path-to-repo>/tools/aw new <name> --need "<my answer>" \
     --words "<my words>" --workspace <dir> --yes --register
6. Run: python <path-to-repo>/tools/aw check <dir>
   If it fails, show me the failures and stop. Do not edit the spec to make it pass.
7. Ask me the three acceptance questions one at a time, then record my answers with:
   python <path-to-repo>/tools/aw verify <name> --harness "<your name and version>"
8. Report what exists, what passed, what failed, and what you did not do.

Do not create a second domain. Do not write outside the workspace directory.
```

---

## What the agent is allowed to touch

| Allowed | Not allowed |
|---|---|
| create the workspace directory you named | touch any other directory |
| write `AGENTS.md` from your answers | invent content for `AGENTS.md` |
| run `aw new`, `aw check`, `aw verify` | edit `SPEC.md` to make a check pass |
| create exactly one domain | create a second "while it is here" |

The second row is the one that matters. The identity file says who the assistant is and
what it owns; an agent writing its own job description writes one it likes. That is why
the prompt says *interview me and fill it from my answers only* — and why `aw new` refuses
to run outside a workspace.

---

## What a good run looks like

The agent should produce a receipt before writing anything:

```
workspace:   /home/me/assistant
will create: AGENTS.md, ca-reading/{SKILL.md, log.md, decisions.md, 4-engine/report.py}
description: Use when the user mentions reading/book/pages, or needs to track what I read each week
undo:        rm -rf /home/me/assistant
```

…then the check, then three questions, then a short report. If the receipt is missing,
stop and ask for it. If the report claims success without showing `aw check` output,
treat it as a failure.

---

## Four ways this goes wrong

**1. It writes the identity file by itself.**
Symptom: `AGENTS.md` is full of plausible routing rows you never said.
Why it hurts: routing is matched against *your* vocabulary; an invented table routes
nothing, and you will not know until the first real request fails.
Fix: delete the file, re-run step 4 with the interview.

**2. It creates three domains "to be helpful".**
Symptom: `ca-notes/`, `ca-tasks/`, `ca-ideas/`, all empty.
Why it hurts: this is the six-half-dead-domains failure in `docs/06-case-study.md`. One
domain, used for a week, teaches you what the second should be.
Fix: `mv` the extras out, delete their rows from `AGENTS.md`.

**3. It skips the check.**
Symptom: "Done! Your workspace is ready."
Why it hurts: a workspace that fails M3 looks identical to one that passes, until the
first request needs the decision log.
Fix: run `aw check <dir>` yourself. It takes a second.

**4. It "fixes" a failing check by weakening the rule.**
Symptom: the spec, the templates, or the checker has been edited.
Why it hurts: the rules are the product; a passing check that was bought by editing the
spec is a lie with a green light.
Fix: `git -C <path-to-repo> status` should be clean. If it is not, `git checkout .`.

---

## Undo

Nothing here is irreversible:

```bash
rm -rf <workspace>          # a fresh workspace is just a directory
git -C <path-to-repo> checkout .   # if the agent edited the repository
```

If you ran `--register`, `aw new` left `AGENTS.md.bak` beside the file it edited. Restore
that if the two inserted rows are wrong.

---

## If you already have a folder of notes

The common case, and the one the prompt does not cover. Do not hand it to an agent and
say "organize this" — that is how a workspace ends up with six half-dead domains.

Do this instead:

1. Run the prompt above and get **one** domain working.
2. Move the notes that belong to it into that domain's `1-data/`, in the format the
   manual already describes.
3. Only when that domain has been used for a week, add the second.

Converting everything at once is a migration with no rollback and no acceptance test.
