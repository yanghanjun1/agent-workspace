# adapters/

One file per harness, describing the only thing that differs: how that harness discovers
a manual.

JSON, not YAML, because the tools are standard-library only and a YAML parser would be
the first dependency. These files are read by humans today and by `aw link` where an
install action exists.

```json
{
  "harness": "dsh",
  "tier": "T1",
  "entry_file": "AGENTS.md",
  "discovery": "directory-watch",
  "install": [{"action": "link", "to": "{workspace}/.dsh/skills/{domain}"}],
  "notes": ["..."]
}
```

`tier` follows `PORTABILITY.md`. `discovery` is one of:

- `workspace-read` — the agent reads the entry file at the working directory root and
  follows paths. No registration; nothing to install.
- `directory-watch` — the harness scans a fixed directory for skills.
- `declared-registry` — each skill must be declared in a config file.
- `none` — no file access; T3.
