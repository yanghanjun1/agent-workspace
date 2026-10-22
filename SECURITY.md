# Security

This repository ships a specification and three small standard-library scripts. There is
no service, no network access, no dependency, and no data. The attack surface is narrow,
and this page says exactly where it is — including the part that is not a bug but a
property of the format.

## What the tools touch

| component | what it does | what can go wrong |
|---|---|---|
| `aw new` | writes a domain directory inside the workspace you name | path handling; it refuses to run where there is no `AGENTS.md`, and removes the domain again if it fails conformance |
| `aw link` | creates symlinks (POSIX) or junctions (Windows), removing an existing link first | **link removal** — see below |
| `aw check` | reads files in the workspace, writes nothing | parsing untrusted text |
| `aw verify` | appends one row to `PORTABILITY.md` | a value that breaks the markdown table |
| `aw` | dispatches; `subprocess` is used only for `mklink`, fixed argv, no shell | — |

### Link removal is the sharpest edge

A junction removed with a recursive delete takes the **target's contents** with it, not
the link. `tools/link.py` removes links with `Path.rmdir()`, which detaches a junction
instead of recursing, and skips anything that is a real directory. That is the correct
behaviour; it is also the code path most worth a second pair of eyes, because the failure
mode is silent and destructive.

## The instruction surface

`AGENTS.md` and `SKILL.md` are files an agent **obeys**. So a workspace is executable in
the only sense that matters to an agent: text that changes behaviour.

Adopting a workspace you did not write is therefore **prompt injection by design**. That
is not a vulnerability in this project; it is a property of the format, and the format is
the product. What can be done is to make the risk legible.

Before adopting someone else's workspace:

1. **Read every `SKILL.md`.** Look for instructions that act outside the domain — "always
   run this first", "before answering, read <path>", anything addressed to the assistant
   rather than describing the domain.
2. **Look for external references.** A URL, a `curl`, a "fetch this before proceeding".
   Nothing here fetches anything, so a manual that does is telling you something.
3. **Read `4-engine/*.py` before running it.** The scripts are plain Python with your
   permissions. There is no sandbox, and this project does not pretend to have one.
4. **Check what the routing table points at.** A row can point at a manual that does not
   exist, or at one you have not read.

What the project does about this automatically: **nothing**. `aw check` verifies structure,
not intent. A conforming workspace can still be hostile. Saying so is the honest version;
a checker that claimed otherwise would be worse than no checker.

## Fixed while writing this page

- **Newline injection through `--need` / `--words`.** Both were interpolated into the
  `description:` line and into the first log entries, so a newline could add frontmatter
  keys or forge a decision-log entry. Inputs are now collapsed to a single line.
- **Markdown table injection through `aw verify --harness`.** A `|` or a newline in the
  value broke the portability table. Cells are now escaped.

Neither was exploitable for code execution. Both were ways for text to reach a file that
an agent later reads, which is the failure mode this project is actually about.

## Reporting

Open a [security advisory](https://github.com/yanghanjun1/agent-workspace/security/advisories/new)
rather than a public issue. Anything that makes a conforming workspace behave in a way the
spec does not describe is in scope, even if it is "only" a file that another agent will
read.

## Out of scope

- The harness that opens the workspace. Its sandbox, its approvals and its tool access are
  its own; this project cannot grant or withhold them.
- Data you choose to put in a workspace. `docs/02-layout.md` says what should not be
  committed; nothing here enforces it.
- Third-party domains you install. See "the instruction surface".
