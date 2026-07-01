# Claude Code Platform Support

Audience: agents and maintainers adding Claude Code-specific harness support.

Use when: implementing Claude Code hooks, settings, native skills, or
Claude-specific instruction loading.

Read `docs/platform-support.md` first when the target repo needs the same
behavior to work across multiple platforms.

## Current Public Docs Checked

Checked on 2026-06-30 against Anthropic Claude Code docs:

- `https://code.claude.com/docs/en/memory`
- `https://code.claude.com/docs/en/skills`
- `https://code.claude.com/docs/en/commands`
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
source to Claude Code with a generated mirror by default. Install
`scripts/sync_claude_skills.py` from this framework when the target repo wants
Claude Code native skills for the same harness skills that live in
`.agents/skills`.

Do not manually maintain separate Claude and Codex skill bodies unless a real
platform limitation requires it.

The generated mirror pattern treats `.agents/skills/<skill>/SKILL.md` as the
source of truth for the skill body and support files. The corresponding
`.claude/skills/<skill>/SKILL.md` owns Claude-specific frontmatter. The sync
script preserves existing Claude frontmatter, replaces the body with the
`.agents` body, copies support files, and rejects orphaned Claude files that no
longer have a `.agents` source.

When a shared skill includes Codex invocation policy at
`.agents/skills/<skill>/agents/openai.yaml`, the sync script translates
`policy.allow_implicit_invocation: false` into Claude frontmatter
`disable-model-invocation: true`. The Codex sidecar remains Codex metadata and
is not copied into `.claude/skills`.

Add this to the target repo's canonical checks when the mirror adapter is
installed:

```sh
python3 -m scripts.sync_claude_skills --check
```

Run this after changing `.agents/skills` or adding a Claude skill mirror:

```sh
python3 -m scripts.sync_claude_skills
```

Thin wrapper skills with `@` imports remain acceptable only when the target
repo deliberately chooses wrappers over generated mirrors. When using a thin
wrapper skill, keep Claude Code frontmatter in the wrapper even though the
instruction body delegates to the shared source. This prevents installers from
losing Claude-specific discovery metadata, model choices, `allowed-tools`
declarations, or other Claude Code fields.

Recommended wrapper shape:

```md
---
name: harness-review
description: Reviews implementation against the repo's Agent Work Brief.
model: <Claude model, when the target repo wants one>
allowed-tools: <Claude tools, when pre-approved for this skill>
---

@../../../.agents/skills/harness-review/SKILL.md
```

When adapting an existing Claude skill, preserve or intentionally adapt
platform-specific fields such as `model`, `allowed-tools`, `disallowed-tools`,
`effort`, `context`, `hooks`, or `paths`. Do not silently replace them with the
shared skill frontmatter.

### Bundled Skills

Claude Code ships bundled skills and workflows such as `/code-review`,
`/debug`, `/run`, `/verify`, `/batch`, `/loop`, and `/claude-api`. These may
overlap with harness-provided review, diagnose, run, or verification guidance.

During a harness install, tell the human when a bundled skill overlaps with a
repo-specific or harness-specific skill. Record one of these decisions:

- leave bundled skills enabled and document which command is preferred,
- leave bundled skills enabled but treat them as secondary to repo-specific
  guidance,
- disable bundled Claude Code skills or workflows through Claude Code settings
  when the team wants project guidance to be the only available path.

Claude Code supports `disableBundledSkills: true` in settings, or the
equivalent `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS=1` environment variable. This
removes bundled skills and workflows. It does not disable project skills in
`.claude/skills/` or legacy project commands in `.claude/commands/`.

Do not change a user's personal Claude Code settings during harness
installation unless the human explicitly asks for that. Project settings affect
the whole team and should be proposed as a deliberate adapter decision.

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

## Level 1 Stop Adapter

For the required Level 1 `repo-checks-on-stop` behavior, use the standard
shared runner from `adapters/common-hooks` plus the Claude Code declaration and
wrapper from `adapters/claude`.

Default target paths:

```text
scripts/hooks/repo_checks_on_stop.py
.claude/settings.json
.claude/hooks/repo-checks-on-stop.py
```

The Claude Code declaration should be a single `Stop` command hook. Do not add
a matcher; Claude Code ignores matchers for `Stop`.

Minimal project settings shape:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": [
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/repo-checks-on-stop.py"
            ],
            "timeout": 600,
            "statusMessage": "Running repo checks"
          }
        ]
      }
    ]
  }
}
```

Claude Code passes one JSON object on stdin to command hooks. The shared fields
include `session_id`, `cwd`, and `hook_event_name`; `Stop` also includes
`stop_hook_active`. The standard wrapper leaves payload interpretation to the
shared runner, which uses `stop_hook_active` to avoid recursive Stop blocking
while still reporting check failures, then maps the neutral result to Claude
Code Stop output.

The standard Claude Code wrapper exits `0` with no output when
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

For Claude Code `Stop`, `decision: "block"` makes Claude continue instead of
ending the turn. Do not make `scripts/repo-checks.sh` emit Claude hook JSON;
keep all Claude output mapping in the hook adapter.

When Claude Code sends `stop_hook_active: true`, the standard wrapper still
runs `scripts/repo-checks.sh`, but maps failures to non-blocking JSON:

```json
{
  "systemMessage": "scripts/repo-checks.sh failed at Stop..."
}
```

That reports the actionable check output without starting another Stop-hook
continuation loop.

Project `.claude/settings.json` is team-shared. Personal settings can disable
or override hooks, and managed settings can restrict project hooks entirely.
Record an unsupported-runtime gap if the target environment cannot load project
Stop hooks.

For Windows support, the project settings command can invoke the same
`.claude/hooks/repo-checks-on-stop.py` wrapper, but the shared runner still
executes `scripts/repo-checks.sh`. Use this adapter on Windows only when the
target repo has POSIX shell support such as Git Bash or WSL, or record an
unsupported-runtime gap until the target repo approves a Windows-specific
checks adapter.

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

For Claude Code instruction loading, a one-line `CLAUDE.md` pointer should be
enough. Keep it as `@AGENTS.md` unless there is a genuine Claude-specific
behavior to document. If Claude Code is a desired hook-capable agent runtime in
current scope, Level 1 also needs the required `repo-checks-on-stop` behavior
through a narrow Claude Code Stop hook adapter when supported.
