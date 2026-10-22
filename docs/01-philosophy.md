# 01 · Why assistants rot, and what three layers answer

## Five failure scenes

Not model failures. Structural ones, each reproducible within a week.

**1. It reintroduces itself every morning.**
Open a chat, explain the context, talk, close it, repeat tomorrow. Nothing survives the
session, so the assistant is permanently new.

**2. The prompt grows until the rules stop working.**
The obvious fix is to put everything in the system prompt. It works for two weeks. Then
the file is 800 lines, a third of the rules are quietly ignored, and changing one word
invalidates the cached prefix. The symptom reads as "the model got worse".

**3. Three months later it contradicts itself.**
You ask why the accounting period starts on the 20th. Nobody knows; the answer was in a
conversation in July. A single timeline of *what happened* cannot answer *why it is like
this*, so every large change forces a re-derivation — and two re-derivations disagree.

**4. Wrong facts live forever.**
Every memory system says *append-only*. So a mistyped number from March is still being
used in September, and nobody dares touch it, because the rule says history is immutable.
The log ends up protecting its own errors.

**5. Switching tools means starting over.**
Everything lived in one product's session store. It changes its pricing, its model, its
terms — and eight months of context is gone, because it was never a file.

## Three layers

```
identity     AGENTS.md          small, injected every turn, writes only routes
   │  routes by the words you actually use
   ▼
manuals      ca-*/SKILL.md      long, loaded on demand, holds procedures and rules
   │  reads and writes
   ▼
memory       event log · decision log · CURRENT.md
```

- **A small identity file** answers (2). It is a **budget law**: re-sent every turn, so it
  may only hold what must be true every turn.
- **Manuals loaded on demand** answer the other half of (2), and give each domain its own
  conventions without cross-contamination.
- **Two axes** answer (1) and (3). The event log says what happened; the decision log says
  why it is the way it is. Only the second one survives a redesign.
- **The correction rule** answers (4). History is append-only — *except for facts*.
- **Everything is a file in a git repo** answers (5). A workspace is opened by an agent,
  never owned by one.

## Why a domain is a plugin, not a feature

Because everyone's domains differ, and one person's domains differ across time.

A domain as "a directory plus one manual" means: adding a domain is adding a directory,
with no change to the skeleton; a domain can be deleted, moved, or handed to someone else
whole; a domain's data and its rules live together. And the skeleton stays clean.

This is why the repository ships a skeleton and a generator rather than a set of domains:
**your domains are your asset, mine are worth nothing to you.**

## Why no vector database

The assumption is a memory of a few hundred files and a few hundred thousand words.

At that scale, "filename plus directory convention plus one index per manual" is more
reliable than embedding retrieval, because you can `grep` it and see exactly what the
assistant read. Reach for retrieval when you have hundreds of thousands of files, not
before.

## The cost, honestly

- You write the identity file once. It is the one artifact an agent must not generate.
- You keep two logs. Not writing them is the default, and the default degrades back into a
  chat window within three weeks.
- A generated domain needs acceptance, not just creation.
- It is not smarter, only less forgetful — and being less forgetful removes most of what
  people blame on the model.
