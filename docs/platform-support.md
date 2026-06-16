# Platform Support

Audience: agents and maintainers adding or changing platform-specific harness
support.

Use when: the target repo needs Codex, Claude Code, pre-commit, CI, or another
runtime to load skills, settings, hooks, or other adapter-specific behavior.

Do not read this for ordinary Level 0 installation unless platform-specific
support is part of the requested harness shape. Start with
`docs/implementation-guide.md` and the manifests first.

## Read Next

- Codex-specific support: `docs/platforms/codex.md`
- Claude Code-specific support: `docs/platforms/claude-code.md`
- Pre-commit support: `adapters/pre-commit/README.md`

## Principle

Shared behavior should have one owner.

Prefer these shared surfaces:

- `AGENTS.md` for repo-wide agent operating guidance,
- `scripts/verify.sh` for canonical mechanical verification,
- the `harness-work-brief` skill bundle for executable work shape,
- shared skill source for reusable task workflows,
- one shared hook runner when multiple platforms enforce the same check.

Platform-specific files should be thin adapters. They may declare where a
platform loads config, skills, or hooks, and they may translate platform input
and output formats. They should not re-encode the policy itself.

An adapter can be as small as a pointer file, a generated skill mirror, a hook
config plus wrapper script, or a pre-commit/CI entry that calls
`scripts/verify.sh`. The adapter's purpose is to expose the shared harness to a
specific runtime, not to become another copy of the harness.

## Decision Flow

1. Identify the platforms that need first-class support now.
2. Install or adapt the core harness first.
3. Read only the platform docs for the platforms in scope.
4. If a platform-specific feature duplicates shared behavior, add a thin
   adapter instead of another copy of the behavior.
5. Record the adapter, its value, and its removal or expansion signal in the
   target repo's harness docs.

If the repo uses Claude Code and no hooks or native skills are needed, support
can often be just the conditional pointer file `CLAUDE.md` containing
`@AGENTS.md`.

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

- which verification command to run,
- which paths or commands are sensitive,
- what counts as pass, warn, or block,
- how messages should be phrased for humans and agents.

## Skill Pattern

Keep reusable workflow content in one source location. If a platform requires a
different discovery path, add a mirror, wrapper, symlink, generator, or install
step rather than manually maintaining two skill bodies.

Harness-provided skills should use self-explaining names such as
`harness-review`, `harness-implement`, `harness-work-brief`, and
`harness-diagnose` unless the target repo has a stronger naming convention.
Avoid generic names such as `review` when they could collide with platform,
plugin, personal, or team skills.

During installation, audit existing platform skills and commands for overlap
with review, implementation, work-brief, diagnose/debug, run, and verify
workflows. Record whether each overlapping item is merged, adapted,
superseded, left alone, or deferred.

Skill descriptions are part of the runtime contract. Keep them concise and
front-load the trigger condition so platforms can select the right skill from
frontmatter or metadata without always loading the full instructions.

## What To Avoid

- Copying full hook policy into `.codex/`, `.claude/`, pre-commit, and CI.
- Maintaining separate review or implementation skill text for each runtime.
- Adding hooks before `scripts/verify.sh` defines the command contract.
- Installing platform files for tools the team does not use.
- Treating platform docs as always-loaded product context.

## Source Freshness

Platform behavior changes. Before implementing a new adapter or hook schema,
check the current official platform docs and update the platform note if the
framework guidance has drifted.
