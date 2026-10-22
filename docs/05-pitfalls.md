# 05 · Pitfalls

Ordered by how often they happen. Every one of these actually did.

## 1. The manual is built, and the agent never opens it

**Symptom:** you ask something related and it does not read the manual.
**Cause:** the `description` says what the domain *is* ("coffee domain operations manual")
instead of *when to use it*.
**Fix:** put your own words in it — slang, abbreviations, situations
(`Use when the user mentions coffee/pour-over/another one/caffeine this week`).
**Check order:** description → is the manual inside the workspace → is it registered in the
identity file.

## 2. Copy instead of link

**Symptom:** you edit `ca-x/SKILL.md` and nothing changes.
**Cause:** the skills directory holds a copy. Two files, and you edited the one that does
not run.
**Fix:** delete the copy, use a link. `aw link --target dsh` handles the Windows junction
fallback. Note that `ln -s` in Git Bash on Windows is **not** a symlink by default — it
silently copies, which is the easiest way to step on this.

## 3. A workspace inside a workspace

**Symptom:** routing works sometimes; two `CURRENT.md` files overwrite each other; git shows
a nested repository.
**Cause:** the whole workspace was moved into another tool's working directory.
**Fix:** one identity file per working directory (M0). Switching agents means `cd` into the
workspace and starting the agent there — not copying the workspace over. `aw check` walks
the parent chain and reports the first ancestor that also holds an identity file.

## 4. The identity file grows

**Symptom:** rules start being missed; editing it is expensive.
**Cause:** procedures, SOPs and history were written into it.
**Test:** past 200 lines it needs splitting (M1). Two piles: keep routing, boundaries and
per-turn triggers; move "how to do it" into a manual.

## 5. The same thing written in two places

**Symptom:** two documents disagree about one convention, and either could be the one the
agent read.
**Typical:** both `AGENTS.md` and `SKILL.md` state "the period starts on the 20th"; later
only one is updated.
**Fix:** one source per fact, pointers elsewhere (M6 — `aw check` compares lines and reports
verbatim duplication).

## 6. Six domains on day one

**Symptom:** all six are half-dead, each with one manual and two records.
**Cause:** the number of domains is not the value; each one needs data, both axes and upkeep.
**Advice:** run one domain for a month. Once one works, you know what the second should look
like.

## 7. A generated domain that was never accepted

**Symptom:** the files exist, `aw check` is green, and it still does nothing when you ask.
**Cause:** the checker proves structure, not behaviour. This is the second thing a machine
cannot verify, next to M4b.
**Fix:** `aw verify` — route, compute, write. Failing any of them means it is a folder.

## 8. Letting the model do arithmetic

**Symptom:** totals do not add up, and asking twice gives two answers.
**Cause:** computation was handed to a language model.
**Fix:** computation in a script (M5); the model understands and explains. `aw new` ships a
working `report.py` so there is no excuse.

## 9. No rollback point before a big change

**Symptom:** it breaks, and there is nowhere to go back to.
**Fix:** commit before editing rule-like files; prototype a big refactor in a branch or a
separate directory. **"If you can start a scratch file, you may not edit the original"** —
cheaper than any backup.

## 10. `_scratch/` becomes a landfill

**Symptom:** 3 GB of one-off scripts six months later, and nobody dares delete them.
**Fix:** at delivery, say which artifacts are discardable and which are named; delete the
discardable ones on the spot. **The cost is not disk, it is that you stop touching files.**

## 11. Leaking history when open-sourcing

**Symptom:** making a private repo public, or "deleting the sensitive files, then pushing".
**Why it always fails:** after `git rm` the file is still in history; `git log -p` shows it.
Deleting a working-tree file is not deleting history.
**Do this instead:** create a new directory, `git init` a fresh repository, copy only the
cleaned files. The original stays private and untouched. Run `gitleaks detect` and read
`git log --stat` yourself before publishing.

## 12. Treating the conversation as memory

**Symptom:** closing the session equals it never happened.
**Fix:** anything that will matter later is written down at the time: conventions into the
manual, facts into the data, decisions into the decision log, next steps into `CURRENT.md`.
**The primary carrier of attention is a file, not a chat log.**
