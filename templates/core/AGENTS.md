# Agent Instructions

## Start Here

Use this file as the repo entrypoint. Keep context focused and read only what
the current task requires.

## Work Source

Primary work source: <Jira / GitHub Issues / human-provided brief / other>.

Canonical work brief location: <Jira ticket/comment / repo file / PR
description / chat for tiny work>.

Allowed temporary draft location: <none / .agent/work / docs/work / other>.

Lifecycle/status updates: <where Draft -> Ready For Implementation ->
Implemented -> Verified -> Reviewed is recorded>.

Before implementation, make sure the work has an Agent Work Brief or enough
equivalent detail to answer:

- goal,
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
