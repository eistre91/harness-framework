# Codex Adapter

This adapter is intentionally a guidance placeholder, not a complete install
package.

Use when the target repo wants Codex-specific hooks or local configuration.

Before implementing Codex-specific hooks, config, or skill-loading behavior,
read:

- `docs/platform-support.md`
- `docs/platforms/codex.md`

Default guidance:

- keep `scripts/verify.sh` as the verification contract,
- add Codex hooks only when the human wants automatic enforcement or repeated
  failures show agents forget verification,
- keep Codex hook behavior aligned with Claude Code, pre-commit, and CI where
  those tools are also used,
- prefer Codex hooks that call shared scripts rather than reimplementing
  policy inside Codex-specific files,
- keep Codex-specific files out of the core harness when the target repo does
  not use Codex.

Adapter purpose:

- add Codex project config only when shared `AGENTS.md`, `.agents/skills`, and
  `scripts/verify.sh` are not enough,
- map Codex hook input and output to shared hook runners when automatic checks
  are justified,
- keep Codex-specific trust, matcher, and event-shape details out of portable
  harness docs.

Unclear until a target repo needs it:

- which hooks are worth adding,
- whether project-local `.codex/` config should be committed,
- how hook output should be shaped against current Codex docs.

Potential future assets:

- Stop hook wrapper for `scripts/verify.sh`,
- secret or sensitive-file guard,
- destructive shell warning rules,
- bounded hook output formatting.
