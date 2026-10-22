# Contributing

This repository does one thing: it makes a method copyable. The bar is narrow on purpose.

## Accepted

- **Corrections to the spec.** Especially where a MUST is unenforceable, or enforceable
  in a way that punishes a legitimate workspace. `SPEC.md` is the artifact that should
  outlive everything else here.
- **Example inputs.** `examples/inputs/` holds needs in plain language. A new one is a
  new proof that the generator generalizes. Non-English inputs are welcome as locale
  coverage — add them with `--lang` and a test, not only as a file.
- **Portability rows.** A row in `PORTABILITY.md` needs a harness, a version, and a date.
  A failing row is worth more than a passing one.
- **Translations.** The repository is English. The `--lang` flag and the `.zh.md` templates
  exist because a workspace's filenames and headings are an implementation choice, not a
  spec requirement. A third locale follows the same pattern.
- **Bug fixes** in `tools/` — encoding, paths, Windows behaviour. These are the bugs
  users actually hit.

## Not accepted

- **Personal data.** Examples must be invented. A PR with a real name, phone number or
  account is rejected without discussion.
- **Third-party dependencies.** `tools/` is standard library only. This is not a
  preference: the checker has to run on a machine where nothing is installed. A YAML
  parser is why `adapters/` is JSON.
- **Rules that are "smarter" but harder to obey.** A rule nobody follows is worse than
  no rule, because it teaches people to ignore the file.
- **Vendor-specific features.** If it only works on one harness, it belongs in
  `adapters/`, as a note — not in the spec.

## Before a PR

```bash
python -m unittest discover -s tests -v      # 21 tests, no install step
python tools/aw check <a workspace you own>  # optional, but tell us the result
grep -rniE 'sk-[A-Za-z0-9]{16,}|1[3-9][0-9]{9}' . --exclude-dir=.git
```

If you add a MUST, add a test that fails without it. If you add a rule that cannot be
tested, say so in the spec — the honesty is the feature.

## Discussing

Open an issue with the concrete situation first: what your domain covers, where it broke,
what you expected. Proposals without a situation tend to be closed, because the value of
a skeleton is what it refuses to add.
