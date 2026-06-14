# Claude Code Platform Support

Audience: agents and maintainers adding Claude Code-specific harness support.

Use when: implementing Claude Code hooks, settings, native skills, or
Claude-specific instruction loading.

Read `docs/platform-support.md` first when the target repo needs the same
behavior to work across multiple platforms.

## Current Public Docs Checked

Checked on 2026-06-14 against Anthropic Claude Code docs:

- `https://code.claude.com/docs/en/memory`
- `https://code.claude.com/docs/en/skills`
- `https://code.claude.com/docs/en/settings`
- `https://code.claude.com/docs/en/hooks`

Re-check those docs before implementing a new adapter or hook schema.

## Guidance Files

Claude Code reads `CLAUDE.md`, not `AGENTS.md`. If a repo uses `AGENTS.md` as
the shared agent entrypoint, keep `CLAUDE.md` as a thin import:

```md
@AGENTS.md
```

Add Claude-specific text below that import only when the behavior is genuinely
Claude-specific. Do not duplicate the shared harness in both files.

Claude treats `CLAUDE.md` as context, not an enforcement layer. Use settings or
hooks for behavior that must be mechanically enforced.

## Skills

Claude Code project skills are loaded from `.claude/skills/` in the starting
directory and parent directories up to the repo root. Claude can also discover
nested `.claude/skills/` directories on demand when working in subdirectories.

Skills can be invoked by the user or selected by Claude from their
descriptions. Keep descriptions clear, scoped, and front-loaded with the
trigger condition.

If the harness keeps portable skill source under `.agents/skills`, expose that
source to Claude Code with the smallest adapter the target repo can maintain:

- a generated copy,
- a symlink where that is practical,
- a thin wrapper skill that points to the shared source,
- or a documented install step.

Do not manually maintain separate Claude and Codex skill bodies unless a real
platform limitation requires it.

## Settings

Claude Code project settings live under `.claude/`:

- `.claude/settings.json` for shared project settings,
- `.claude/settings.local.json` for local, gitignored settings.

Most settings, including hooks and permissions, reload during a running
session. Keep committed project settings minimal and avoid writing personal or
machine-specific policy into shared files.

## Hooks

Claude Code hooks are configured under `hooks` in settings JSON. Project hooks
can reference scripts relative to the project root with `${CLAUDE_PROJECT_DIR}`.

Command hooks receive event JSON on stdin. Hook output can use exit codes or
JSON decisions, depending on the event. `PreToolUse` and `Stop` are common
events for enforcing command policy or verification, but the current hook docs
should be checked before implementing exact schemas.

If the same policy must also run in Codex, pre-commit, or CI, the Claude hook
should dispatch to a shared runner and translate only Claude-specific input and
output.

## Adapter Pattern

Prefer this shape:

```text
.claude/settings.json
  -> .claude/hooks/<event>-adapter
  -> shared hook runner
```

The Claude adapter should own:

- Claude hook event declarations,
- matcher syntax,
- Claude JSON input and output mapping,
- Claude path placeholders such as `${CLAUDE_PROJECT_DIR}`.

The shared runner should own:

- verification behavior,
- command or path policy,
- user-facing messages,
- pass, warn, or block decisions.

## Install Guidance

Add Claude Code support when:

- the team actually uses Claude Code for repo work,
- the repo needs Claude Code hooks or project settings,
- native Claude skill discovery needs a `.claude/skills` adapter,
- the repo needs the conditional `CLAUDE.md` pointer so Claude Code loads the
  shared `AGENTS.md` guidance.

For a Claude Code Level 0 trial, a one-line `CLAUDE.md` pointer should be
enough. Keep it as `@AGENTS.md` unless there is a genuine Claude-specific
behavior to document.
