# examples/golden/

**These are fixtures, not a recommended set.**

They exist because the checker needs something to check and the tests need something to
break. Each one is a *shape*, not a topic:

| fixture | shape it demonstrates |
|---|---|
| `ca-reading/` | a domain whose output is an appended record, with a reporter |
| `ca-finance/` | a domain where every number must come from a script (M5) |

Your domains will not look like these, and they should not. If you are looking for how to
build one, read `docs/03-build-a-domain.md` and let `aw new` do it — the fixtures are what
the generator's output should resemble after a week of use, not a menu to choose from.
