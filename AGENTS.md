# Agent Instructions

## Start Here

This is the source repo for the Agent Harness Framework. Work in this repo is
framework maintenance, not target-repo harness installation.

Keep context focused. Read only what the current framework change requires, and
prefer source-of-truth files over broad background docs.

## Required Reading

For any framework change, read `docs/principles.md` first.

Then route by task:

- Installer workflow changes: `docs/installer.md`, then the relevant
  `docs/install/*.md` checklist.
- Framework concepts or maturity language: `docs/framework.md` and, when
  needed, `docs/maturity-model.md`.
- Asset boundary changes: the relevant manifest in `manifests/`.
- Target-repo installable content: the source template under `templates/` or
  skill under `skills/`.
- Platform adapter guidance: `docs/platform-support.md`, then only the relevant
  platform note or adapter README.
- Deferred ideas: `TODO.md`; treat it as a work record, not active guidance.

Do not load future-facing docs such as `docs/level-5-orchestration.md` unless
the task is about that topic.

## Source Of Truth

- Principles live in `docs/principles.md`.
- Installer routing lives in `docs/installer.md` and `docs/install/`.
- Maturity definitions live in `docs/maturity-model.md`.
- Asset lists live in `manifests/`.
- Installable templates live in `templates/`.
- Reusable skill bodies live in `skills/`.
- Mechanical verification for this repo lives in `scripts/repo-checks.sh`.

Avoid maintaining second copies of schemas, file lists, commands, or policy.
Docs should point to the owner instead.

## Editing Rules

Keep framework changes small and justified by a current need or recorded
failure signal. Avoid speculative process, optional assets, adapters, or
automation.

When changing installer docs, preserve staged installation: current stage first,
human approval before edits, validation and handoff before next-stage
inspection.

When changing target-repo templates or skills, keep them portable. Repo-specific
commands, paths, trackers, and policies should be adaptation points, not baked
into the framework source.

## Verification

Before claiming framework work is complete, run:

```sh
./scripts/repo-checks.sh
```

Report the command result. If it fails, report the failure and do not claim the
work is complete.
