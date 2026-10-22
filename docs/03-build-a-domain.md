# 03 · Build a domain (let the agent do it)

A domain should not be typed out by hand. You supply three things; the generator writes
the rest; then you accept it.

## The three things you supply

1. **What it covers**, in one sentence.
2. **How you actually talk about it** — your own words, including slang, abbreviations and
   situations.
3. **Where the data comes from** — typed by hand, pushed from a phone, imported.

The second one matters most: it becomes the `description`, and the description is the only
thing the model sees when it decides whether to open the manual.

## One command

```bash
python tools/aw new ca-coffee \
  --need "record every cup and how much caffeine this week" \
  --words "coffee/pour-over/beans/another one" \
  --workspace ~/my-workspace --yes --register
```

What it does:

1. Prints a **receipt** — which files, which name, the draft description. Without `--yes`
   it waits for you.
2. Generates `SKILL.md`, both axes, and `4-engine/report.py`.
3. Writes the first decision entry: `domain created · because the owner asked for: …`
4. Runs `aw check` itself; if the new domain introduces violations it **removes it**,
   rather than leaving a half-dead directory behind.
5. With `--register`, inserts the two rows into `AGENTS.md` (keeping a `.bak`).

Without `--register` it prints the rows for you to paste:

```markdown
| ca-coffee | `ca-coffee/` | coffee and caffeine | `ca-coffee/SKILL.md` |

| coffee / pour-over / beans / another one | `ca-coffee` |
```

**The identity file is never generated.** It states who the assistant is and what it owns
— an agent writing its own job description writes one it likes. `aw new` refuses to run
outside a workspace for exactly the same reason.

## Then accept it (three questions)

```bash
python tools/aw verify ca-coffee --harness "codex-cli 0.48.0"
```

1. **Route** — say it the way you normally would. Did the agent open the manual on its own?
2. **Compute** — ask for a number. Did it run the script, or do arithmetic itself?
3. **Write** — ask it to record one item. Did both axes each gain a line?

**Until all three pass, the domain is not built.** It is a folder. The answers are written
into the matrix in `PORTABILITY.md`.

## When it does not work

| Symptom | Almost always | Fix |
|---|---|---|
| The manual is never opened | the `description` uses your system vocabulary, not your speech | put your own words in the description |
| Opened, but behaviour is wrong | the manual has no conventions, or they contradict the identity file (M6) | move conventions into the manual; leave a pointer in the identity file |
| Nothing was written down | the manual never says "append a block after each run" | add the maintenance section |
| Numbers differ each time | the manual let the model compute (M5) | point it at a script under `4-engine/` |

## When to split one domain into two

- the manual passes 150 lines
- the two things store data differently
- the words you use for them do not overlap at all

Conversely, if one phrase ("how am I doing?") reaches three domains, they should be one.

## When a domain dies

Do not `rm -rf`.

1. `mv ca-x ../archive/ca-x-<date>`
2. delete its two rows from `AGENTS.md`
3. delete the link from the skills directory, if you made one
4. append one line to the skeleton's decision log: `domain ca-x retired · because …`

**History is an asset; attention is scarce.** Move it, do not erase it.
