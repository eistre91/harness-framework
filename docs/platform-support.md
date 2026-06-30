# Platform Support

Audience: agents and maintainers adding or changing platform-specific harness
support.

Use when: the target repo needs Codex, Claude Code, pre-commit, CI, or another
runtime to load skills, settings, hooks, or other adapter-specific behavior.

Do not read this for ordinary Level 0 installation until the Level 0 checklist
routes here for the required `repo-checks-on-stop` adapter or for another
platform-specific behavior in current scope. Start with `docs/installer.md`,
the current stage checklist, and the current stage manifest first.

## Read Next

- Codex-specific support: `docs/platforms/codex.md`
- Claude Code-specific support: `docs/platforms/claude-code.md`
- Pre-commit support: `adapters/pre-commit/README.md`

## Principle

Shared behavior should have one owner.

Prefer these shared surfaces:

- `AGENTS.md` for repo-wide agent operating guidance,
- `scripts/repo-checks.sh` for canonical deterministic repo checks,
- the `harness-work-brief` skill bundle for executable work shape,
- shared skill source for reusable task workflows,
- one shared hook runner when multiple platforms enforce the same check.

Platform-specific files should be thin adapters. They may declare where a
platform loads config, skills, or hooks, and they may translate platform input
and output formats. They should not re-encode the policy itself.

An adapter can be as small as a pointer file, a generated skill mirror, a hook
config plus wrapper script, or a pre-commit/CI entry that calls
`scripts/repo-checks.sh`. The adapter's purpose is to expose the shared harness to a
specific runtime, not to become another copy of the harness.

## Decision Flow

1. Identify the platforms that need first-class support now.
2. Install or adapt the core harness first.
3. Read only the platform docs for the platforms in scope.
4. If a platform-specific feature duplicates shared behavior, add a thin
   adapter instead of another copy of the behavior.
5. Record the adapter, its value, and its removal or expansion signal in the
   target repo's harness docs.

If the repo uses Claude Code only for instruction loading and another primary
runtime owns the required Stop automation, support can often be just the
conditional pointer file `CLAUDE.md` containing `@AGENTS.md`.

## Level 0 Repo Checks Stop Hook

Level 0 requires `repo-checks-on-stop` for each desired hook-capable agent
runtime in current scope. The canonical behavior is:

```text
platform Stop hook declaration
  -> platform wrapper script
  -> shared scripts/hooks/repo_checks_on_stop.py
  -> scripts/repo-checks.sh
  -> neutral pass or block result
  -> platform wrapper maps result back to platform Stop output
```

The shared contract is deliberately narrow:

- `scripts/repo-checks.sh` owns verification behavior.
- Platform hook files only declare when and how the runtime calls the hook.
- Platform wrappers resolve the repo root, import the shared runner, and map
  its neutral result into platform Stop output.
- `scripts/hooks/repo_checks_on_stop.py` runs only
  `scripts/repo-checks.sh` from the repo root and returns a neutral pass or
  block result.
- Broad hook policy, secret guards, destructive-action rules, tool policy, and
  CI or pre-commit parity remain later deterministic controls unless
  explicitly approved in current scope.

Copy the target-independent shared runner from:

```text
adapters/common-hooks/scripts/hooks/__init__.py
adapters/common-hooks/scripts/hooks/repo_checks_on_stop.py
```

to:

```text
scripts/hooks/__init__.py
scripts/hooks/repo_checks_on_stop.py
```

Then copy or adapt the platform declaration and wrapper for each runtime in
scope:

| Runtime | Adapter source | Default target |
| --- | --- | --- |
| Codex | `adapters/codex/hooks.json` | `.codex/hooks.json` |
| Codex | `adapters/codex/hooks/repo-checks-on-stop.py` | `.codex/hooks/repo-checks-on-stop.py` |
| Claude Code | `adapters/claude/settings.json` | `.claude/settings.json` |
| Claude Code | `adapters/claude/hooks/repo-checks-on-stop.py` | `.claude/hooks/repo-checks-on-stop.py` |

The standard platform wrappers exit silently when `scripts/repo-checks.sh`
passes. When checks fail, each wrapper emits Stop JSON with
`decision: "block"` and a reason that tells the agent to fix the failures
before ending the turn. For both Codex and Claude Code, a blocked Stop
continues the agent session instead of accepting the turn as finished.

Keep platform differences at the adapter edge:

| Difference | Codex | Claude Code |
| --- | --- | --- |
| Config path | `.codex/hooks.json` or `.codex/config.toml` | `.claude/settings.json` |
| Stop matcher | No matcher; Stop is turn-scoped | No matcher; Stop ignores matchers |
| Repo-root command | Resolve from Git root because Codex may start in a subdirectory | Use `${CLAUDE_PROJECT_DIR}` for project paths |
| Trust/settings | Project `.codex` config and changed non-managed hooks must be trusted | Project settings can be disabled or limited by managed policy |
| Windows command | `commandWindows` or TOML `command_windows` can call the wrapper, but the checks command still needs POSIX shell support | Use explicit shell or a Windows wrapper only when `scripts/repo-checks.sh` can run |

The shared hook behavior is portable across Codex and Claude Code, but the
Level 0 checks command is `scripts/repo-checks.sh`. The provided declarations
are POSIX-oriented examples and require an environment that can execute that
script, such as POSIX shell, Git Bash, or WSL. On native Windows without that
support, changing only `commandWindows`, `command_windows`, or the Claude
settings command is not enough. Record an unsupported-runtime gap, or add a
target-specific Windows check adapter with explicit approval.

Validate the adapter before claiming Level 0 completeness:

1. Run `scripts/repo-checks.sh` directly from the target repo root.
2. Run each wrapper from the repo root with a Stop-shaped payload, for example
   `printf '%s\n' '{"hook_event_name":"Stop"}' | python3 .codex/hooks/repo-checks-on-stop.py`.
3. Run each wrapper from a subdirectory using the same repo-root command form
   declared in the platform config, for example
   `python3 "$(git rev-parse --show-toplevel)/.codex/hooks/repo-checks-on-stop.py"`.
4. Record whether an actual runtime Stop event was tested or only the wrapper
   was smoke-tested.
5. Record the adapter path, hook command, repo-root handling, blocking
   behavior, and validation result in `docs/harness/`.

## Hook Pattern

When multiple runtimes need the same hook behavior, use this shape:

```text
platform hook config
  -> platform adapter script
  -> shared hook runner
  -> platform adapter maps result back to platform output
```

The shared runner should receive a normalized input shape, for example:

```json
{
  "platform": "codex",
  "event": "PreToolUse",
  "cwd": "/repo",
  "tool_name": "Bash",
  "tool_input": {},
  "raw": {}
}
```

The shared runner should return a small neutral result, for example:

```json
{
  "status": "pass",
  "message": ""
}
```

Platform adapters own the unstable parts:

- hook declaration syntax,
- hook event names,
- platform JSON input schema,
- platform JSON or exit-code output schema,
- path placeholders and environment variables,
- trust or permission behavior.

The shared runner owns the stable policy:

- which repo checks command to run,
- which paths or commands are sensitive,
- what counts as pass, warn, or block,
- whether an operation is safe for this specific hook event or tool call,
  including whether a command can run concurrently in the current context,
- how messages should be phrased for humans and agents.

## Skill Pattern

Keep reusable workflow content in one source location. If a platform requires a
different discovery path, add a mirror, wrapper, symlink, generator, or install
step rather than manually maintaining two skill bodies.

Separate reusable skill instructions from platform-owned skill metadata. The
shared skill source should hold the portable workflow body and the metadata
needed by the shared skill format. If a platform requires additional
frontmatter or sidecar metadata, such as model selection, allowed tools, or
runtime-specific discovery fields, keep that metadata in the platform adapter
instead of stripping it or copying it into the shared skill body.

For repos that use both `.agents/skills` and Claude Code native skills, the
standard harness adapter is a generated Claude mirror: `.agents/skills` owns
the reusable body and support files, while `.claude/skills` owns
Claude-specific frontmatter. Read `docs/platforms/claude-code.md` for the
sync command, drift check, and wrapper-import exception.

Harness-provided skills should use self-explaining names such as
`harness-review`, `harness-implement`, `harness-work-brief`, and
`harness-diagnose` unless the target repo has a stronger naming convention.
Avoid generic names such as `review` when they could collide with platform,
plugin, personal, or team skills.

During installation, audit existing platform skills and commands for overlap
with review, implementation, work-brief, diagnose/debug, run, and verify
workflows. Record whether each overlapping item is merged, adapted,
superseded, left alone, or deferred.

When native skill mirrors are installed for a platform, record where the shared
skill source lives, where the mirror lives, what platform frontmatter is
intentionally present, and which sync or check command prevents drift.

Skill descriptions are part of the runtime contract. Keep them concise and
front-load the trigger condition so platforms can select the right skill from
frontmatter or metadata without always loading the full instructions.

## What To Avoid

- Copying full hook policy into `.codex/`, `.claude/`, pre-commit, and CI.
- Maintaining separate review or implementation skill text for each runtime.
- Adding hooks beyond the required repo-checks Stop adapter before
  `scripts/repo-checks.sh` defines the command contract.
- Installing platform files for tools the team does not use.
- Treating platform docs as always-loaded product context.

## Source Freshness

Platform behavior changes. Before implementing a new adapter or hook schema,
check the current official platform docs and update the platform note if the
framework guidance has drifted.
