# Claude Adapter

Use when the target repo uses Claude Code conventions.

Before implementing Claude Code-specific hooks, settings, native skill support,
or instruction loading, read:

- `docs/platform-support.md`
- `docs/platforms/claude-code.md`

Those files are the canonical source for Claude Code guidance. Keep this
adapter directory limited to Claude-specific assets that cannot live in shared
templates, such as settings examples, hook adapters, or skill-loading notes.

## Level 0 Stop Hook

This adapter includes the narrow Claude Code side of the required Level 0
`repo-checks-on-stop` behavior. Copy these source files to the default targets:

```text
adapters/claude/settings.json -> .claude/settings.json
adapters/claude/hooks/repo-checks-on-stop.py -> .claude/hooks/repo-checks-on-stop.py
```

Install the shared runner from `adapters/common-hooks` at the same time:

```text
scripts/hooks/__init__.py
scripts/hooks/repo_checks_on_stop.py
```

The Claude files declare the `Stop` hook, call the shared runner, and map the
neutral result to Claude Code Stop output. Normal failures become
`decision: "block"`; recursive Stop failures with `stop_hook_active` become a
non-blocking `systemMessage` so the agent does not get stuck in a Stop loop.
Verification behavior remains in the target repo's `scripts/repo-checks.sh`.

The provided settings command uses exec-form `args` with
`${CLAUDE_PROJECT_DIR}` to reference the project wrapper without breaking on
project paths that contain spaces. For Windows, the command can call the same
wrapper, but the target environment must still be able to execute
`scripts/repo-checks.sh`, for example through Git Bash or WSL. If it cannot,
record an unsupported-runtime gap or add a target-specific Windows checks
adapter with explicit approval.

Keep `scripts/repo-checks.sh` quiet when checks pass. Its output should be
limited to actionable failures, missing setup, or next steps the agent or human
needs to act on.

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

## Not Included

Broader hook policies are not part of this adapter. Add secret guards,
destructive shell warning rules, tool policy, or additional Claude-specific
settings only when the current approved scope includes those deterministic
controls.
