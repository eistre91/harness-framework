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

- whether skills should be mirrored, symlinked, wrapped, or manually installed,
- which hooks are worth adding,
- whether project settings should be committed or kept local.

Potential future assets:

- Claude settings or hook examples,
- Claude-specific skill placement notes.
