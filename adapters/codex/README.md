# Codex Adapter

Use when the target repo wants Codex-specific hooks or local configuration.

Before implementing Codex-specific hooks, project config, skill loading, or
other Codex adapter behavior, read:

- `docs/platform-support.md`
- `docs/platforms/codex.md`

Those files are the canonical source for Codex guidance. Keep this adapter
directory limited to Codex-specific assets that cannot live in shared
templates, such as config examples, hook adapters, or skill-loading wrappers.

## Level 0 Stop Hook

This adapter includes the narrow Codex side of the required Level 0
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

The Codex files declare the `Stop` hook, call the shared runner, and map the
neutral result to Codex Stop output. Verification behavior remains in the
target repo's `scripts/repo-checks.sh`.

The provided `hooks.json` command is POSIX-oriented and resolves the wrapper
from the Git root so it works when Codex starts in a subdirectory. For Windows,
`commandWindows` or TOML `command_windows` can call the same wrapper, but the
target environment must still be able to execute `scripts/repo-checks.sh`, for
example through Git Bash or WSL. If it cannot, record an unsupported-runtime gap
or add a target-specific Windows checks adapter with explicit approval.

## Not Included

Broader hook policies are not part of this adapter. Add secret guards,
destructive shell warning rules, tool policy, or bounded hook output formatting
only when the current approved scope includes those deterministic controls.
