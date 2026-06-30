# Codex Platform Support

Audience: agents and maintainers adding Codex-specific harness support.

Use when: implementing Codex hooks, Codex project config, Codex-specific skill
loading, or other Codex adapter behavior.

Read `docs/platform-support.md` first when the target repo needs the same
behavior to work across multiple platforms.

## Current Public Docs Checked

Checked on 2026-06-30 against the OpenAI Codex manual:

- `https://developers.openai.com/codex/skills.md`
- `https://developers.openai.com/codex/guides/agents-md.md`
- `https://developers.openai.com/codex/config-advanced.md`
- `https://developers.openai.com/codex/hooks`

Re-check those docs before implementing a new adapter or hook schema.

## Guidance Files

Codex reads `AGENTS.md` files as project guidance. Keep shared repo behavior in
`AGENTS.md` only when every Codex agent in the repo needs it for ordinary work.
Use nested guidance only when a subtree genuinely needs a different rule.

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

Codex can use the shared `.agents/skills/<skill>/SKILL.md` files directly. Do
not install a second Codex-specific copy unless the target repo needs a real
Codex-only wrapper or plugin package.

When a Codex skill needs explicit invocation policy, keep Codex sidecar
metadata at `.agents/skills/<skill>/agents/openai.yaml`. For example,
`policy.allow_implicit_invocation: false` marks the skill as explicitly invoked
only. If the same skill is mirrored to Claude Code, the Claude adapter
translates that policy into Claude-specific frontmatter rather than copying the
sidecar.

Use self-explaining harness skill names such as `harness-review`,
`harness-implement`, `harness-work-brief`, and `harness-diagnose` by default.
Before installing them, audit existing `.agents/skills` entries for generic or
overlapping names such as `review`, `implement`, `debug`, `diagnose`, `run`,
or `verify`, and record whether the harness skill is merged, adapted,
supersedes the existing skill, or is deferred.

If the same shared skill also needs a Claude Code native skill, keep
`.agents/skills/<skill>/SKILL.md` as the source of truth and sync
`.claude/skills/<skill>/SKILL.md` as a Claude mirror. Preserve Claude-specific
frontmatter in the mirror. The `.agents` skill source should not absorb
Claude-only metadata such as `model`, `allowed-tools`, or other Claude-only
frontmatter.

## Project Config

Codex project config lives under `.codex/`:

- `.codex/config.toml`
- `.codex/hooks.json`

Project-local config and hooks load only when the project `.codex/` layer is
trusted. User and system config remain separate.

Do not add `.codex/` files during a starter install unless Codex is the target
repo's desired hook-capable agent runtime in current scope for the required
Level 0 `repo-checks-on-stop` behavior, or the target repo otherwise needs
Codex-specific config, hooks, or policy.

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

## Level 0 Stop Adapter

For the required Level 0 `repo-checks-on-stop` behavior, use the standard
shared runner from `adapters/common-hooks` plus the Codex declaration and
wrapper from `adapters/codex`.

Default target paths:

```text
scripts/hooks/repo_checks_on_stop.py
.codex/hooks.json
.codex/hooks/repo-checks-on-stop.py
```

The Codex declaration should be a single `Stop` command hook. Do not add a
matcher; Codex ignores matchers for `Stop`.

Minimal JSON shape:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/repo-checks-on-stop.py\"",
            "timeout": 600,
            "statusMessage": "Running repo checks"
          }
        ]
      }
    ]
  }
}
```

Codex passes one JSON object on stdin to command hooks. The shared fields include
`session_id`, `cwd`, and `hook_event_name`; `Stop` also includes fields such as
`turn_id`, `stop_hook_active`, and `last_assistant_message`. The standard
wrapper leaves payload interpretation to the shared runner, which uses
`stop_hook_active` to avoid recursive Stop blocking while still reporting check
failures, then maps the neutral result to Codex Stop output.

The standard Codex wrapper exits `0` with no output when
`scripts/repo-checks.sh` passes. Keep that script quiet on pass; Stop hook
output should be limited to actionable failures, missing setup, or next steps.
When the command fails on an ordinary Stop event, the wrapper exits `0` with
Stop JSON:

```json
{
  "decision": "block",
  "reason": "scripts/repo-checks.sh failed at Stop..."
}
```

For Codex `Stop`, `decision: "block"` continues the session with the reason
rather than ending the turn. Do not make `scripts/repo-checks.sh` emit platform
hook JSON; keep all Codex output mapping in the hook adapter.

When Codex sends `stop_hook_active: true`, the standard wrapper still runs
`scripts/repo-checks.sh`, but maps failures to non-blocking JSON:

```json
{
  "systemMessage": "scripts/repo-checks.sh failed at Stop..."
}
```

That reports the actionable check output without starting another Stop-hook
continuation loop.

Project `.codex/` hooks load only after the project config layer is trusted.
Changed non-managed hooks may need to be reviewed and trusted again before they
run.

For Windows support, `commandWindows` in `hooks.json` or `command_windows` in
TOML can invoke the same `.codex/hooks/repo-checks-on-stop.py` wrapper, but the
shared runner still executes `scripts/repo-checks.sh`. Use this adapter on
Windows only when the target repo has POSIX shell support such as Git Bash or
WSL, or record an unsupported-runtime gap until the target repo approves a
Windows-specific checks adapter.

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
- Codex is a desired hook-capable agent runtime for the required Level 0
  `repo-checks-on-stop` behavior,
- the repo needs Codex hooks or project config,
- Codex needs a platform-specific path or setting to expose shared harness
  behavior.

Do not add Codex support when Codex is not in current scope for required Stop
automation and `AGENTS.md`, shared skills, and `scripts/repo-checks.sh` are
enough for Codex users.
