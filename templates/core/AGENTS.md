# Agent Instructions

## Start Here

Use this file as the repo entrypoint. Keep context focused and read only what
the current task requires.

This file is for instructions every agent in this repo needs for ordinary work.
Put phase-specific workflow in skills, deterministic checks in scripts,
product/domain context in routed project docs, and detailed standards in
focused docs, tests, hooks, or review guidance.

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

Use harness skills by phase, not as one combined reading list. Shape ambiguous
or acceptance-heavy work with `harness-work-brief`, implement from the agreed
brief or scope with `harness-implement`, then review against that brief or scope
with `harness-review`. For non-trivial work, keep implementation and review in
separate context windows when practical.

## Review Independence

For standard or complex work, prefer an independent review in a separate context
window or by a separate agent. If the implementer reviews the same change, label
it as a self-review and treat it as lower-confidence.

Scale review depth to the work and its ambient risk: Tiny checks outcome, diff,
obvious regressions, evidence, and scope; Standard also checks requirements,
design fit, boundaries, tests, security implications, and conventions; Complex
or elevated-risk work also challenges premises and relevant consumers,
dependencies, migration or negative cases, and cross-boundary effects.

## Project Context

Project docs: `<path or "none yet">`

If project docs are not enough, inspect local code patterns before adding new
documentation.

## Harness Docs

Harness docs live in `docs/harness/`. Do not read them for ordinary
implementation or to learn how to use the harness during product work. Use this
entrypoint, the current request or agreed brief, installed skills, project docs,
and local code instead.

Read `docs/harness/` only when the task is to inspect, audit, maintain, or
extend the harness itself.

## Safety

Do not read, print, commit, or copy secrets. Treat `.env*`, credentials, local
databases, and private operator state as sensitive unless the human explicitly
directs otherwise.

Do not revert unrelated user changes.
