# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning: [SemVer](https://semver.org/). The spec and the tools version together.

## [Unreleased]

### Fixed
- Newline injection through `aw new --need/--words`: both were interpolated into the
  `description:` line and the first log entries, so a newline could add a frontmatter key
  or forge a decision-log entry. Inputs are collapsed to one line, with a test.
- Markdown table injection through `aw verify --harness`: a pipe or newline broke the
  portability row. Cells are escaped, with a test.

### Added
- `SECURITY.md` — what the tools touch, why link removal is the sharpest edge, and the
  instruction-surface problem: a workspace is a set of files an agent obeys, so adopting
  someone else's workspace is prompt injection by design. `aw check` verifies structure,
  not intent, and the page says so.
- `SETUP.md` — setup with an agent: a copy-paste prompt that ends at `aw check` instead
  of at "done!", what the agent may touch, the four ways it goes wrong, and how to undo.
- `README.md` — setup split into "manually" and "with an agent", with the bootstrap
  prompt inline.
- `examples/golden/ca-review/` — a domain whose output is a judgement rather than a
  record: blind passes, the disagreement kept, one dated verdict. The third domain shape,
  and the one `CONTRIBUTING.md` had been asking for.
- `examples/golden/ca-finance/` — a domain where every number must come from a script.
  Signed amounts, csv for data and markdown for rules, read-before-write, a refund that
  offsets its category. This is the fixture that makes M5 obvious instead of fussy.
- `examples/golden/README.md` — fixtures are not a recommended domain set.
- `docs/06-case-study.md` — eight months, six domains, and the failures that produced
  each rule. The provenance of the spec, which is the one thing a reader cannot get from
  the spec itself.
- `WHY.md` — "two complaints, three rules": hallucination and context loss mapped to the
  rules that answer them.

## [0.1.0] — 2026-10-23

First draft. The spec is the part meant to outlive the tools.

### Added

- `SPEC.md` — seven MUSTs (M0–M6), three SHOULDs, MAY patterns, conformance levels.
- `WHY.md` — five failure scenes, the three layers that answer them, and the cost.
- `PORTABILITY.md` — the mechanical portability criterion, three tiers, a rule
  degradation table, and a measured matrix.
- `tools/aw` — one entry point: `check`, `new`, `verify`, `link`. Standard library only.
- `templates/` — identity file, domain skeleton, both axes, a working reporter.
- `examples/golden/ca-reading/` — the golden fixture, i.e. a domain after a week of use.
- `examples/inputs/` — ten needs in plain language.
- `tests/` — 22 tests: every MUST can fail, and ten needs produce conforming workspaces.
- CI on three operating systems and two Python versions, with no install step.

### Decisions

- **Identity is never generated.** It states who the assistant is and what it owns; an
  agent writing its own job description writes one it likes. `aw new` refuses to run
  outside a workspace for the same reason.
- **M4 is split.** The entry format is machine-checked; "correct factual errors in place"
  is not, and the spec says so instead of pretending.
- **No shell scripts.** One Python entry point decides symlink vs junction, so the Windows
  path cannot silently degrade into a copy — which is the failure that made the previous
  attempt unusable on Git Bash.
- **JSON adapters, not YAML.** A YAML parser would be the first dependency.

[0.1.0]: https://github.com/yanghanjun1/agent-workspace/releases/tag/v0.1.0
