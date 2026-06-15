# Agent Instructions

## Start Here

Use this file as the repo entrypoint. Keep context focused and read only what
the current task requires.

## Work Source

Primary work source: <Jira / GitHub Issues / human-provided brief / other>.

Canonical work brief location: <Jira ticket/comment / repo file / PR
description / chat for tiny work>.

Allowed temporary draft location: <none / .agent/work / docs/work / other>.

Commit policy for work brief instances: <commit / gitignore / explicit approval
required>.

If the canonical brief location is external and unavailable, use the local
fallback only as temporary state. Copy durable progress, evidence, blockers,
and plan changes back to the canonical location before handoff.

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

Work brief template: `docs/harness/work-brief.md`

## Verification

Before claiming implementation is complete, run:

```sh
./scripts/verify.sh
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

Harness-provided skills, if installed, use the `harness-` prefix, such as
`harness-review`, `harness-implement`, `harness-work-brief`, or
`harness-diagnose`. Existing platform-native skills or commands may also be
available; use the repo-specific decision recorded during installation.

## Review Independence

For standard or boundary-changing work, prefer an independent review in a
separate context window or by a separate agent. If the implementer reviews the
same change, label it as a self-review and treat it as lower-confidence.

## Project Context

Project docs: `<path or "none yet">`

If project docs are not enough, inspect local code patterns before adding new
documentation.

## Harness Docs

Harness docs live in `docs/harness/`.

Read them when the task is to maintain or extend the harness. Normal product
work should use the work brief, project docs, and local code.

## Safety

Do not read, print, commit, or copy secrets. Treat `.env*`, credentials, local
databases, and private operator state as sensitive unless the human explicitly
directs otherwise.

Do not revert unrelated user changes.
