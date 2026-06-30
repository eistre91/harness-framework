# Platform-Independent Agent Hook Pattern

Audience: agents and maintainers installing or designing hook behavior for
multiple agent runtimes.

Use when: a target repo needs hooks beyond the narrow Level 0
`repo-checks-on-stop` adapter, or when the installer needs the full hook adapter
pattern as a reference. Do not read this for ordinary Level 0 installation
unless `docs/install/level-0.md` or the human-approved scope routes here.

This pattern keeps platform-specific files as thin adapters and puts shared
behavior in testable repo-local code. The platform adapter receives runtime hook
input, normalizes only the fields the shared policy needs, calls the shared
runner, and maps the neutral result back into the platform's output shape.

The pattern is portable across agent hosts. It does not make shell commands
automatically portable across operating systems. Replace example policies with
target-repo policies, and add Windows-specific command declarations only when
the target repo's contributors use Windows and the underlying checks can run
there.

## Official Hook Behavior

Current platform contracts are owned by the official docs:

- Codex hooks: `https://developers.openai.com/codex/hooks`
- Claude Code hooks: `https://code.claude.com/docs/en/hooks`

Re-check those docs before implementing a new adapter or hook schema. This
framework records adapter patterns, not the authoritative runtime schemas.

Both systems use the same broad shape:

1. A lifecycle event fires, such as `SessionStart`, `PreToolUse`, or `Stop`.
2. A matcher group decides whether a hook applies to the event, when that event
   supports matchers.
3. One or more hook handlers run.
4. Command handlers receive one JSON object on `stdin`.
5. Handlers communicate back through `stdout` JSON, selected exit codes, or no
   output.

There are important differences, so shared hooks should target the common
contract and keep platform-specific details at the edge.

| Area | Codex | Claude Code | Portable rule |
| --- | --- | --- | --- |
| Project hook location | `.codex/hooks.json` or `.codex/config.toml` can define project hooks when the project config layer is trusted. | `.claude/settings.json` can be committed for project hooks. | Commit one small declaration file per platform. |
| Config shape | `hooks` -> event -> matcher group -> hook handlers. | `hooks` -> event -> matcher group -> hook handlers. | Keep both declarations structurally similar where the event supports it. |
| Command input | Event JSON is passed on `stdin`. | Event JSON is passed on `stdin`. | Shared code should parse `stdin` once and tolerate missing or malformed JSON. |
| Repo root path | Codex command hooks run from the session `cwd`; repo-local hooks should resolve from the Git root because Codex may start in a subdirectory. | Claude supports `${CLAUDE_PROJECT_DIR}` for project paths. | Platform adapters should resolve the repo root before importing shared code. |
| Handler support | Codex command hooks are the portable baseline. | Claude supports command, HTTP, MCP tool, prompt, and agent hook handlers depending on event. | Use command hooks for cross-platform behavior. |
| Execution model | Multiple matching command hooks can run for the same event; do not rely on declaration order. | Matching hooks can run in parallel and may be deduplicated. | Hooks must be idempotent and must not depend on execution order. |
| `SessionStart` output | Plain text or `hookSpecificOutput.additionalContext` can add developer context. | `hookSpecificOutput.additionalContext` can add context at session start. | Emit the JSON `hookSpecificOutput` shape when practical. |
| `PreToolUse` output | `deny` blocks supported tool calls, `additionalContext` adds model-visible context, and `allow` with `updatedInput` can rewrite supported calls. Some legacy/common fields are parsed but unsupported. | `permissionDecision` can allow, deny, ask, or defer; `updatedInput` can rewrite tool arguments. Some outcomes are mode-specific. | Use `deny` for portable enforcement and no output for no decision. Add platform-specific branches for rewrites or approval flows. |
| Tool coverage | Codex `PreToolUse` currently covers Bash, file edits through `apply_patch`, and MCP tool calls; it does not cover every shell path or non-shell tool path. | Claude `PreToolUse` covers many named tools, including shell, file, web, agent, and MCP tools. | Do not assume identical coverage. Register useful matchers per platform and keep shared handlers defensive. |
| Stop output | `decision: "block"` continues the session with the reason instead of accepting the turn as complete. | `decision: "block"` makes Claude continue instead of ending the turn. | Use Stop JSON only in platform wrappers; keep repo checks output platform-neutral. When preventing a recursive Stop loop, report failures with a non-blocking platform message instead of blocking again. |
| Trust model | Project hooks load only after the `.codex/` layer is trusted; changed non-managed hooks may need review. | Project hooks can be controlled by settings and enterprise policy; command hooks run with user permissions. | Make hook behavior transparent, fast, and auditable. |

## Layering

Use four layers:

1. Platform declarations
2. Platform wrapper scripts
3. Shared entrypoint or runner
4. Shared policy modules

Recommended layout for a target repo with broad shared hooks:

```text
.
+-- .claude/
|   +-- settings.json
|   +-- hooks/
|       +-- pre-tool-use.py
|       +-- session-start.py
+-- .codex/
|   +-- hooks.json
|   +-- hooks/
|       +-- pre-tool-use.py
|       +-- session-start.py
+-- scripts/
    +-- hooks/
        +-- __init__.py
        +-- common.py
        +-- entrypoint.py
        +-- pre_tool_use.py
        +-- session_start.py
```

The Level 0 Stop adapter is intentionally narrower than this layout. It uses
only `scripts/hooks/repo_checks_on_stop.py` plus one wrapper per platform.

Platform declaration files should only answer:

- which platform event should run,
- which platform matcher should trigger it,
- which tiny wrapper script should execute,
- what timeout or status message the platform should show.

They should not contain repository policy beyond matcher names and command
paths.

Wrapper scripts should only:

- resolve the repository root,
- put the repository root on the language import path,
- call the shared entrypoint with stable arguments such as event mode and
  platform,
- map the neutral shared result to the platform output schema.

Example wrapper:

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if __name__ == "__main__":
    from scripts.hooks.entrypoint import main

    raise SystemExit(main(["pre-tool-use", "codex"]))
```

The shared entrypoint should:

- read JSON from `stdin`,
- ignore malformed or missing input by returning no decision,
- dispatch by event mode,
- extract only the fields needed by the shared policy,
- convert the shared policy result into platform-compatible JSON,
- exit `0` after emitting a decision or no output.

The shared policy modules should:

- contain all repository-specific behavior,
- accept ordinary Python values instead of platform globals,
- return a small result object such as `deny_reason` or `additional_context`,
- be unit-testable without launching Claude Code or Codex,
- be idempotent and race-tolerant when they write files, update state, or call
  external processes.

## Shared Entrypoint Contract

A broad shared entrypoint can have this shape:

```python
from __future__ import annotations

import os
import sys

from .common import load_payload, pre_tool_use_output, repo_root, session_start_output
from .pre_tool_use import evaluate_pre_tool_use
from .session_start import evaluate_session_start


def main(argv: list[str] | None = None) -> int:
    args = list(argv or sys.argv[1:])
    if len(args) != 2:
        return 0

    mode, platform = args
    payload = load_payload()
    root = repo_root()

    if mode == "session-start":
        result = evaluate_session_start(root, env=os.environ, platform=platform)
        if result.additional_context:
            print(session_start_output(result.additional_context))
        return 0

    if mode == "pre-tool-use":
        tool_name = str(payload.get("tool_name", "") or "")
        tool_input = payload.get("tool_input")
        if not isinstance(tool_input, dict):
            tool_input = {}
        result = evaluate_pre_tool_use(
            root,
            env=os.environ,
            platform=platform,
            tool_name=tool_name,
            tool_input=tool_input,
        )
        if result.deny_reason:
            print(pre_tool_use_output(result.deny_reason))
        return 0

    return 0
```

The `platform` argument may be unused at first. Keep it anyway. It gives the
shared implementation an escape hatch for real platform differences without
duplicating policy in wrappers.

Use a small result object instead of returning platform JSON from policy code:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class HookResult:
    additional_context: str = ""
    deny_reason: str = ""

    @property
    def should_inject_context(self) -> bool:
        return bool(self.additional_context)

    @property
    def should_deny(self) -> bool:
        return bool(self.deny_reason)
```

This keeps decisions separate from transport. The policy says "deny because
this path is sensitive"; the output builder decides how to express that denial
to Codex or Claude Code.

## Event Flow

For `SessionStart`, the flow should look like this:

1. Platform starts or resumes a session.
2. Platform runs its configured command hook.
3. Wrapper imports the shared entrypoint.
4. Entrypoint calls `evaluate_session_start(repo_root, env=...)`.
5. Shared policy performs a fast setup or environment check.
6. Shared policy returns either no context or an `additional_context` string.
7. Entrypoint prints `hookSpecificOutput.additionalContext`.

For `PreToolUse`, the flow should look like this:

1. Platform prepares a supported tool call.
2. Matcher selects the wrapper for that tool.
3. Entrypoint reads `tool_name` and `tool_input` from `stdin`.
4. Shared policy evaluates the operation.
5. If allowed, the hook exits `0` with no output.
6. If denied, the entrypoint prints JSON with `permissionDecision: "deny"` and
   one actionable reason.

Important coverage note: a Claude `PreToolUse` matcher for `Read` does not have
a direct Codex equivalent today. For portable enforcement, prefer checks on
paths that flow through shell commands, file edits, MCP tools, Git hooks, CI, or
underlying filesystem permissions. Treat agent-runtime `PreToolUse` as a useful
local guardrail, not a complete interception layer.

## Declaration Examples

Claude Code project hooks can live in `.claude/settings.json`. The shell-form
example below matches a POSIX-style environment. If project paths can contain
spaces or the team uses Windows, prefer the platform's exec-form command
configuration with separate arguments where available:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": [
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/session-start.py"
            ],
            "timeout": 10
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3",
            "args": [
              "${CLAUDE_PROJECT_DIR}/.claude/hooks/pre-tool-use.py"
            ],
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

Codex project hooks can live in `.codex/hooks.json` or `.codex/config.toml`.
The POSIX example below resolves from the Git root so hooks still work when the
session starts in a subdirectory:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/session-start.py\"",
            "timeout": 10,
            "statusMessage": "Checking repository setup"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/pre-tool-use.py\"",
            "timeout": 10,
            "statusMessage": "Checking command policy"
          }
        ]
      }
    ]
  }
}
```

Keep these examples short. Add more matchers only when the platform officially
supports the event/tool combination you need or when current behavior has been
verified. For Windows support, add the platform's Windows command field for
each command hook, and avoid relying on `python3`, POSIX command substitution,
or unquoted shell-expanded paths.

## Policies That Fit This Pattern

This pattern works best for deterministic, fast, local decisions:

- blocking reads of sensitive local files,
- blocking unsafe command flags,
- ensuring required local setup exists before a commit or deploy command,
- injecting concise setup guidance at session start,
- enforcing repo-local conventions that do not require model judgment,
- warning about generated files, read-only directories, or required test paths.

Hook output should be quiet on pass and actionable on failure. Pass banners and
routine success chatter spend context without telling the agent what to do next.

Avoid using hooks as the only security boundary for policies that need complete
coverage. Platform hook coverage differs, especially for tool interception. Use
hooks as one layer alongside file permissions, repository permissions, CI
checks, server-side controls, and Git hooks.

## State And Side Effects

Do not assume matching hooks run one at a time or in declaration order. Design
side effects as if two hook processes might start nearly at the same time.

For portable hook code:

- make setup writes idempotent,
- detect and preserve unmanaged user files instead of overwriting them,
- use atomic file writes or file locks for shared state that cannot tolerate
  concurrent writes,
- keep per-session state keyed by the platform session identifier when the
  event payload provides one,
- avoid cross-hook dependencies where one hook must finish before another hook
  starts,
- make failures local so one optional hook cannot corrupt state needed by a
  later hook invocation.

## Adding A New Shared Hook

Use this process when adding an event or rule:

1. Read the current official docs for each target platform.
2. Confirm the event exists on each platform, or decide which platform should
   declare it.
3. Add or update one shared evaluator in `scripts/hooks/`.
4. Add output helpers only if the existing JSON response helpers do not cover
   the event.
5. Add or update the tiny wrappers for each platform.
6. Add platform declaration entries with the narrowest practical matcher.
7. Add unit tests for the shared evaluator and entrypoint dispatch.
8. Manually smoke-test the hook in each platform if the change affects user
   workflow or enforcement.

Do not copy policy code into `.claude/hooks/` and `.codex/hooks/`. If the new
rule needs platform-specific handling, branch inside the shared evaluator on the
explicit `platform` argument and leave a short comment explaining why.

## Testing Strategy

Test the shared code directly:

- `load_payload()` returns `{}` for empty, malformed, or non-object JSON.
- Output helpers produce valid JSON with the expected hook event name.
- `SessionStart` policy returns setup context only when setup is missing or was
  changed.
- `PreToolUse` policy denies only the intended tool inputs.
- Path normalization handles absolute paths, relative paths, missing files,
  subdirectories, and paths outside the repo.
- Shell command parsing handles quoting, environment assignments, command
  prefixes, and malformed commands.
- Platform wrappers can import the shared runner from the repository root.
- Recursive Stop payloads still run checks and report failures without blocking
  again.

Also keep one or two sample `stdin` fixtures per event. They let maintainers
run the same payload through multiple wrappers:

```sh
printf '%s\n' '{"tool_name":"Bash","tool_input":{"command":"git status"}}' \
  | python3 .claude/hooks/pre-tool-use.py

printf '%s\n' '{"tool_name":"Bash","tool_input":{"command":"git status"}}' \
  | python3 .codex/hooks/pre-tool-use.py
```

Expected allow behavior is no stdout and exit code `0`. Expected deny behavior
is stdout JSON and exit code `0`, unless the specific platform/event docs require
a different exit-code contract.

## Security Guidance

Command hooks run locally and can access what the user account can access. Treat
hook code as privileged repository automation:

- keep hook code reviewed and committed,
- keep platform declarations small enough to audit quickly,
- validate all JSON fields before using them,
- do not trust paths or shell commands from hook input,
- normalize paths against the repository root before classifying them,
- avoid shell string construction in shared policy code,
- prefer structured parsers such as `json` and `shlex` over ad hoc string
  splitting,
- keep timeouts short for hooks that run in the interactive path,
- emit concise denial reasons that tell the agent what to do instead,
- never print secret values, tokens, environment dumps, or full sensitive paths
  unless they are already safe to expose,
- add CI or pre-commit checks for the same policy when the policy must hold
  outside interactive agent sessions.

## Porting Checklist

When applying this pattern to another repository:

1. Create `.claude/settings.json` and `.codex/hooks.json`, or the platform
   subset actually in scope.
2. Add one wrapper script per platform/event.
3. Add a shared `scripts/hooks/` package.
4. Implement shared payload loading and JSON output helpers.
5. Implement one policy evaluator at a time.
6. Keep wrappers platform-specific but behavior-free.
7. Keep platform JSON declarative and behavior-free.
8. Unit-test shared policy with platform-shaped payloads.
9. Smoke-test each platform from the repository root and a subdirectory.
10. Document the repository's hook policy and how to bypass or repair it, if any
    bypass or repair path exists.

The success criterion is that a reviewer can answer "what behavior changed?" by
reading `scripts/hooks/`, and can answer "when does it run on this platform?" by
reading only `.claude/settings.json` or `.codex/hooks.json`.
