# Codex Platform Support

Audience: agents and maintainers adding Codex-specific harness support.

Use when: implementing Codex hooks, Codex project config, Codex-specific skill
loading, or other Codex adapter behavior.

Read `docs/platform-support.md` first when the target repo needs the same
behavior to work across multiple platforms.

## Current Public Docs Checked

Checked on 2026-06-14 against the OpenAI Codex manual:

- `https://developers.openai.com/codex/skills.md`
- `https://developers.openai.com/codex/guides/agents-md.md`
- `https://developers.openai.com/codex/config-advanced.md`
- `https://developers.openai.com/codex/hooks.md`

Re-check those docs before implementing a new adapter or hook schema.

## Guidance Files

Codex reads `AGENTS.md` files as project guidance. Keep shared repo behavior in
`AGENTS.md`, and use nested guidance only when a subtree genuinely needs a
different rule.

Do not put a platform-specific inventory of skills into `AGENTS.md`. Codex
discovers available skills from skill metadata and loads the full skill only
when selected.

## Skills

Codex skills are directories containing `SKILL.md` plus optional scripts and
references. The `name` and `description` frontmatter are required.

Codex uses progressive disclosure: the initial context contains skill names,
descriptions, and paths; the full `SKILL.md` is read only when Codex selects
that skill. A skill can be selected explicitly or implicitly from its
description.

For repo-scoped skills, Codex scans `.agents/skills` from the working directory
up to the repository root. Keep shared harness skills there unless the target
repo has a stronger local convention.

## Project Config

Codex project config lives under `.codex/`:

- `.codex/config.toml`
- `.codex/hooks.json`

Project-local config and hooks load only when the project `.codex/` layer is
trusted. User and system config remain separate.

Do not add `.codex/` files during a starter install unless the target repo
needs Codex-specific config, hooks, or policy.

## Hooks

Codex hooks can be declared in `hooks.json` or inline `[hooks]` tables in
`config.toml`. Use one representation per layer to avoid drift.

Useful events include:

- `PreToolUse`
- `PermissionRequest`
- `PostToolUse`
- `UserPromptSubmit`
- `Stop`
- `SubagentStart`
- `SubagentStop`
- `PreCompact`
- `PostCompact`

Codex command hooks run from the session `cwd`. For repo-local hooks, resolve
from the git root rather than relying on a relative path from the launch
directory.

Command hooks receive JSON on stdin. The hook adapter should treat Codex's
event-specific JSON and output behavior as platform-owned. In particular, do
not make the shared runner parse transcripts or depend on convenience fields
that are not part of the stable policy. Normalize the incoming event, branch on
the hook event name, and map the shared runner result back to the current Codex
exit-code or JSON response shape for that event.

If the same policy must also run in Claude Code, pre-commit, or CI, the Codex
hook should dispatch to a shared runner and translate only Codex-specific input
and output.

## Adapter Pattern

Prefer this shape:

```text
.codex/hooks.json or .codex/config.toml
  -> .codex/hooks/<event>-adapter
  -> shared hook runner
```

The Codex adapter should own:

- Codex hook event declarations,
- matcher syntax,
- Codex JSON input and output mapping,
- Codex trust or project-config assumptions.

The shared runner should own:

- verification behavior,
- command or path policy,
- user-facing messages,
- pass, warn, or block decisions.

## Install Guidance

Add Codex support when:

- the team actually uses Codex for repo work,
- the repo needs Codex hooks or project config,
- Codex needs a platform-specific path or setting to expose shared harness
  behavior.

Do not add Codex support when `AGENTS.md`, shared skills, and
`scripts/verify.sh` are enough.
