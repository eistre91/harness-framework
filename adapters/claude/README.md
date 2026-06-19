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
templates, such as settings examples, hook adapters, or skill-loading notes.

Unclear until a target repo needs it:

- which hooks are worth adding,
- whether project settings should be committed or kept local.

## Native Skill Mirrors

When Claude Code should discover harness skills natively, prefer the generated
mirror pattern documented in `docs/platforms/claude-code.md`:
`.agents/skills/<skill>/SKILL.md` owns the portable workflow body and support
files, while `.claude/skills/<skill>/SKILL.md` owns Claude Code frontmatter.

Install `scripts/sync_claude_skills.py` when using generated mirrors. Do not
let install overwrite Claude-specific fields such as model choices or tool
permissions like `allowed-tools` with shared `.agents` frontmatter. Thin
wrappers with `@` imports remain an explicit exception when the target repo
chooses that adapter shape deliberately.

Potential future assets:

- Claude settings or hook examples,
- Claude-specific skill placement notes.
