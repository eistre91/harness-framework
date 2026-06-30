# Common Hook Adapter

Use when a target repo installs the Level 0 `repo-checks-on-stop` behavior for
Codex, Claude Code, or both.

Install these files into the target repo:

```text
scripts/hooks/__init__.py
scripts/hooks/repo_checks_on_stop.py
```

The shared runner is target-repo independent. It accepts the target repo root
from the platform wrapper, runs `scripts/repo-checks.sh` from that root, and
returns a neutral pass or block result. Platform wrappers decide how to express
that result to the runtime.

Keep repository verification behavior in `scripts/repo-checks.sh`. Do not add
lint, type-check, test, or project policy commands to the hook runner.

This adapter assumes the target environment can execute the POSIX shell script
`scripts/repo-checks.sh`. Native Windows repos without Git Bash, WSL, or
equivalent shell support need a target-specific checks adapter or should record
an unsupported-runtime gap.

Pair this common adapter with the narrow platform declarations in:

- `adapters/codex`
- `adapters/claude`

For installation guidance, read `docs/platform-support.md` and only the
platform note for the runtime in scope.
