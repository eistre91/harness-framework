# Claude Adapter

This adapter is intentionally a guidance placeholder, not a complete install
package.

Use when the target repo uses Claude Code conventions.

Before implementing Claude Code-specific hooks, settings, native skill support,
or instruction loading, read:

- `docs/platform-support.md`
- `docs/platforms/claude-code.md`

Those files are the canonical source for Claude Code guidance. Keep this
adapter directory limited to Claude-specific assets that cannot live in shared
templates, such as settings examples, hook adapters, or skill-loading wrappers.

Unclear until a target repo needs it:

- which hooks are worth adding,
- whether project settings should be committed or kept local.

## Native Skill Wrappers

When Claude Code should discover harness skills natively, prefer a thin wrapper
under `.claude/skills/<skill>/SKILL.md` that keeps Claude Code frontmatter and
imports the shared `.agents/skills/<skill>/SKILL.md` body with `@`.

Do not let install copy only the shared `.agents` skill into `.claude/skills`
when that would drop Claude-specific fields such as model choices or tool
permissions like `allowed-tools`. The shared `.agents` skill owns the portable
workflow body; the `.claude` wrapper owns Claude Code metadata.

Potential future assets:

- Claude settings or hook examples,
- Claude-specific skill placement notes.
