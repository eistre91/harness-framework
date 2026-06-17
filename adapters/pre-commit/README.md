# Pre-Commit Adapter

This adapter is intentionally a guidance placeholder, not a complete install
package.

Use when the target repo already uses pre-commit or the team wants deterministic
checks before commit.

Before wiring pre-commit into a multi-platform harness, read
`docs/platform-support.md`.

Default guidance:

- do not introduce pre-commit as part of a starter harness unless the human
  wants that workflow,
- prefer wiring existing checks into `scripts/repo-checks.sh` first,
- avoid noisy or slow hooks until the project has evidence they are needed,
- keep pre-commit behavior aligned with agent-tool hooks and CI where those
  tools are also used.

Adapter purpose:

- let human local commits and agent workflows share the same verification
  contract,
- call `scripts/repo-checks.sh` or narrower shared scripts instead of duplicating
  command lists,
- make deterministic checks run before commit when the team wants that gate.

Unclear until a target repo needs it:

- whether the repo already has pre-commit,
- whether `scripts/repo-checks.sh` is fast enough for commit-time use,
- which checks belong in pre-commit rather than CI or manual verification.

Potential future assets:

- pre-commit config snippets that call `scripts/repo-checks.sh`,
- secret-file guard examples,
- formatting/linting hook examples for common stacks.
