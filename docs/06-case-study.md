# 06 · Case study: eight months, six domains, and the times it rotted

The workspace this spec came from is private and stays private. What follows is its
shape, not its contents: the failures that produced each rule, with the situation
stripped out and the lesson kept.

Roughly 1,200 files across six domains, used daily for about eight months. No rule in
`SPEC.md` was designed in advance. Every one of them is a scar.

---

## What broke, and what grew out of it

| What broke | The scene | What it produced |
|---|---|---|
| Rules quietly stopped being obeyed | The identity file reached ~800 lines; about a third of it was no longer followed, and every edit invalidated the cached prefix | **M1** — identity writes routes only, 200-line budget |
| Numbers disagreed with themselves | Totals were produced in conversation; asking twice gave two answers | **M5** — computation belongs in a script |
| Nobody remembered why anything was the way it was | The logs said what was done each day, and nothing said why a convention existed | **M4** — the decision log |
| A wrong figure survived for months | "Append-only" protected it, and nobody dared edit history | **M4b** — facts are corrected in place, with a correction line |
| Editing a manual changed nothing | The skills directory held a copy, and the copy was not the one being read | pitfall 2, and `aw link` falling back to a junction on Windows |
| Switching tools meant starting from zero | Everything lived in one product's session store | **M0**, and the portability criterion |
| Routing drifted after a move | The workspace was copied into another tool's directory, leaving two identity files | **M0** — no nested workspaces |
| Two repositories, constant conflicts | A cloud repository and a local one, syncing into each other | one workspace, one source per fact (**M6**) |
| A ledger file was emptied | A script opened it for writing before reading it | read before write; and numbers never come from a conversation |
| Six domains in the first month | All six half-dead, each with one manual and two records | run one domain for a month before the second |

The last two are worth reading twice. The ledger one is why M5 exists in the shape it
does: the danger is not only a model doing arithmetic, it is any code path that writes
before it reads. The six-domains one is why `CONTRIBUTING.md` rejects features: the
failure mode of this method is never "too few domains", it is "six folders with good
intentions".

---

## Two motives, in the spec's own words

The reason this exists is usually stated as "agents hallucinate and lose the thread".
That is two different problems, and they have different structural answers:

| The complaint | What it actually is | The rule |
|---|---|---|
| It makes things up | a model producing numbers it never computed | **M5**; and **M4b** once a wrong number is already written down |
| It forgets the middle of a long session | rules competing for a fixed context budget | **M1**, plus manuals loaded on demand instead of injected |
| I cannot move it to another tool | the working state lives inside a vendor | **M0**, and the portability criterion in `PORTABILITY.md` |

None of those is fixed by a better prompt. All three are fixed by moving the thing out of
the conversation and into a file with a rule about it.

---

## What did not survive contact

Worth recording, because a method that only lists what worked is a sales pitch.

- **A second identity file.** It began with two (`SOUL.md` and `AGENTS.md`). Two files
  describing the same assistant is one file plus a future contradiction. One was retired.
- **The cloud as a second assistant.** It started as a duplicate that also did work.
  It ended as infrastructure only: an inbound receiver and a way to get back in. No
  scheduled aggregation, no second brain. The business moved back to the machine with the
  data on it.
- **Two repositories.** Cloud domain and local domain, merged into one. The conflicts cost
  more than the separation bought.
- **Building domains in bulk.** See above.
- **One big prompt.** The whole reason M1 exists.

---

## What this case study does not claim

- Not that eight months is long. It is long enough to hit the second failure (the slow
  rot) and not long enough to hit the third.
- Not that these domains are a recommended set. They are one person's life. See
  `examples/golden/README.md`.
- Not that the rules are sufficient. M4b is unenforceable by machine, and the spec says so
  rather than pretending.
- Not that this works for a team. Every rule here assumes one owner, one workspace, one
  person who can say "this is mine".

The claim is narrow and it holds: **the failures above are structural, so the answers can
be structural too.**
