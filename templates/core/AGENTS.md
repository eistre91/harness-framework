# Agent Instructions

## Start Here

Use this file as the repo entrypoint. Keep context focused and read only what
the current task requires.

## Work Source

Primary work source: <Jira / GitHub Issues / human-provided brief / other>.

Canonical work source and brief location: <Jira ticket/comment / repo file /
PR description / chat for tiny work>.

Allowed local fallback draft location: <none / .agent/work / other gitignored
path>.

Local fallback draft policy: do not commit local fallback brief instances. If
the team wants versioned in-repo briefs, use an explicit durable path such as
`docs/work/` as the canonical brief location.

Durability policy: committed repo briefs are shared work records and may be
useful for collaboration, but they can go stale. If this repo uses committed
briefs, keep source, status, owner, progress, and supersession/archive state
clear enough that future agents do not treat stale work records as current
project guidance.

Availability means the current agent session can read and update the canonical
source through the configured tool, such as an MCP server, API, CLI, or browser
workflow. If the canonical source is external and unavailable, use the local
fallback only as temporary state. Copy durable progress, evidence, blockers, and
accepted plan changes back to the canonical location before handoff.

Lifecycle/status updates: <where Draft -> Ready For Implementation ->
Implemented -> Verified -> Reviewed is recorded>.

Before implementation, make sure the work has an Agent Work Brief or enough
equivalent detail to answer:

- goal,
- smallest valuable outcome,
- non-goals,
- context to read,
- verification,
- acceptance evidence for behavior changes.

For tiny work, a ticket, issue, or chat request can be enough when it states the
source, goal, context, verification, and done criteria.

Work brief skill/template: `.agents/skills/harness-work-brief/`

## Repo Checks

Before claiming implementation is complete, run the canonical deterministic
repo checks:

```sh
./scripts/repo-checks.sh
```

If the command fails, report the failure and do not claim the work is done.

Report both mechanical verification and acceptance evidence. If behavior did
not change, say acceptance evidence is not applicable.

Also report manual evidence when behavior changes externally visible output,
runtime boundaries, secrets management, schedules, deployment behavior, or
integrations. For secrets management changes, verify declarations, aliases,
permissions, redaction, and runtime wiring without printing, revealing,
inspecting, or directly handling secret values.

## Skills

Reusable harness skills are installed in platform-neutral `.agents/skills/` by
default. Use those repo-specific skills when their descriptions match the task.
The singular `.agent/` path, when configured, is for local gitignored drafts and
state, not committed shared skills.

Use harness skills by phase, not as one combined reading list. Shape ambiguous
or acceptance-heavy work with `harness-work-brief`, implement from the agreed
brief or scope with `harness-implement`, then review against that brief or scope
with `harness-review`. For non-trivial work, keep implementation and review in
separate context windows when practical.

## Review Independence

For standard or boundary-changing work, prefer an independent review in a
separate context window or by a separate agent. If the implementer reviews the
same change, label it as a self-review and treat it as lower-confidence.

## Project Context

Project docs: `<path or "none yet">`

If project docs are not enough, inspect local code patterns before adding new
documentation.

## Harness Docs

Harness docs live in `docs/harness/`. Do not read them for ordinary
implementation or to learn how to use the harness during product work. Use this
entrypoint, the canonical work source, installed skills, project docs, and local
code instead.

Read `docs/harness/` only when the task is to inspect, audit, maintain, or
extend the harness itself.

## Safety

Do not read, print, commit, or copy secrets. Treat `.env*`, credentials, local
databases, and private operator state as sensitive unless the human explicitly
directs otherwise.

Do not revert unrelated user changes.
