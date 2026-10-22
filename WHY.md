# WHY.md — five failures, three layers, one cost

## The five ways an assistant rots

Not model failures. Structural ones, and every one of them is reproducible in a week.

**1. It reintroduces itself every morning.**
Open a chat, explain the context, talk, close it, repeat tomorrow. Nothing survives the
session, so the assistant is permanently new. This is the one everybody notices.

**2. The prompt grows until the rules stop working.**
The obvious fix is to put everything in the system prompt. It works for two weeks. Then
the file is 800 lines, a third of the rules are quietly ignored, and changing one word
invalidates the whole cached prefix. The failure looks like "the model got worse".

**3. Three months later it contradicts itself.**
You ask why the accounting period starts on the 20th. Nobody knows. The answer was in a
conversation in July. A single timeline of "what happened" cannot answer "why is it like
this", so every large change forces a re-derivation — and two re-derivations disagree.

**4. Wrong facts live forever.**
Every memory system says *append-only*. So a mis-typed number from March is still being
used in September, and nobody dares edit it because the rule says history is immutable.
The log ends up protecting its own errors.

**5. Switching tools means starting over.**
Everything lived in one product's session store. The product changes its pricing, its
model, or its terms — and eight months of context is gone, because it was never a file.

---

## The three layers

```
identity     AGENTS.md          small, injected every turn, writes only routes
   │  routes by the user's own words
   ▼
manuals      ca-*/SKILL.md      long, loaded on demand, holds the procedures
   │  reads and writes
   ▼
memory       event log · decision log · CURRENT.md
```

Each layer answers one of the failures above, and none of them is a feature:

- **A small identity file** answers (2). It is a budget law: the file is re-sent every
  turn, so it may only contain what must be true every turn.
- **Manuals loaded on demand** answer the "one giant prompt" half of (2) and give each
  domain its own rules without cross-contamination.
- **Two axes** answer (1) and (3). The event log says what happened; the decision log says
  why it is the way it is. Only the second one survives a redesign.
- **The correction rule** (M4b) answers (4). History is append-only *except for facts*.
- **Everything is a file in a git repo** answers (5). The workspace is opened by an agent,
  not owned by one. Switching agents is `cd` and a different command.

---

## What this costs

Honest list, because a method that hides its cost gets abandoned at the first hard week.

- **You write the identity file once, by hand.** It is the one artifact an agent must not
  generate, because it says who the assistant is and what it owns — letting the agent
  write its own job description produces a job description it likes.
- **You keep two logs.** Not writing them is the default, and the default degrades the
  system back into a chat window within three weeks.
- **Domains need acceptance, not just creation.** A generated domain that was never
  exercised is a folder with good intentions. The acceptance test is three questions:
  does it route, does it compute with a script, does it write both axes.
- **It is not smarter.** It is only less forgetful. Being less forgetful removes most of
  the friction people blame on the model.

---

## What this is not

- **Not a bot.** A bot is an execution-layer product. This is the layer a bot reads.
- **Not a memory plugin.** Plugins remember inside one harness; a workspace is readable by
  any harness that can open a directory.
- **Not a RAG pipeline.** Retrieval finds similar text. This needs the *right* text at the
  *right* moment, and a file tree plus a routing table is a more reliable index at the
  scale a single person generates — a few hundred files, a few hundred thousand words.
- **Not a framework.** No dependency, no build step, no runtime. Markdown and one
  standard-library script.

---

## The claim

> The bot changes. The workspace doesn't.

That is the whole thesis. Everything else in this repository is the maintenance cost of
keeping it true.
