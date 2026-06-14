# Claude Adapter

This adapter is intentionally a guidance placeholder, not a complete install
package.

Use when the target repo uses Claude Code conventions.

Before implementing Claude Code-specific hooks, settings, or native skill
support, read:

- `docs/platform-support.md`
- `docs/platforms/claude-code.md`

Default guidance:

- `templates/core/CLAUDE.md` is a conditional pointer for repos that want
  Claude Code support,
- keep `CLAUDE.md` as `@AGENTS.md`,
- do not duplicate the whole harness in multiple agent entrypoints,
- use this adapter only for Claude-specific settings or hooks beyond that
  pointer file,
- keep Claude-specific behavior aligned with Codex, pre-commit, and CI where
  those tools are also used.

Adapter purpose:

- expose shared `AGENTS.md` guidance to Claude Code through `CLAUDE.md`,
- expose shared skills to Claude Code when `.agents/skills` is not enough for
  the desired workflow,
- map Claude Code hook input and output to shared hook runners when automatic
  checks are justified.

Unclear until a target repo needs it:

- whether skills should be mirrored, symlinked, wrapped, or manually installed,
- which hooks are worth adding,
- whether project settings should be committed or kept local.

Potential future assets:

- Claude settings or hook examples,
- Claude-specific skill placement notes.
