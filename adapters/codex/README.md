# Codex Adapter

Use when the target repo wants Codex-specific hooks or local configuration.

Before implementing Codex-specific hooks, project config, skill loading, or
other Codex adapter behavior, read:

- `docs/platform-support.md`
- `docs/platforms/codex.md`

Those files are the canonical source for Codex guidance. Keep this adapter
directory limited to Codex-specific assets that cannot live in shared
templates, such as config examples, hook adapters, or skill-loading wrappers.

## Bounded Work Stop Hook

This adapter includes the narrow Codex side of the selected Bounded Work
`repo-checks-on-stop` behavior. Copy these source files to the default targets:

```text
adapters/codex/hooks.json -> .codex/hooks.json
adapters/codex/hooks/repo-checks-on-stop.py -> .codex/hooks/repo-checks-on-stop.py
```

Install the shared runner from `adapters/common-hooks` at the same time:

```text
scripts/hooks/__init__.py
scripts/hooks/repo_checks_on_stop.py
```

The Codex files declare the hook, resolve the wrapper from the Git root, and map
the shared runner's neutral result to Codex output. See the Bounded Work Stop
Adapter section of `docs/platforms/codex.md` for Codex schemas, trust behavior,
and Windows support. Shared Stop semantics and validation belong to
`docs/platform-support.md`.

## Not Included

Broader hook policies are not part of this adapter. Add secret guards,
destructive shell warning rules, tool policy, or bounded hook output formatting
only when the current approved scope includes those deterministic controls.
