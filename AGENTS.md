# Agent Instructions

## Start Here

This is the source repo for the Agent Harness Framework and its learning
course. Work in this repo is framework maintenance or course development, not
target-repo harness installation.

Keep context focused. Read only what the current work requires, and prefer
source-of-truth files over broad background docs.

## Required Reading

For framework changes, read `docs/principles.md` first.

For learning-course development or intentional course/framework
reconciliation, read `docs/course-maintenance.md`, then only the relevant
lesson or framework sources it identifies. Do not load course material for
ordinary framework maintenance, or framework sources for ordinary course work.

Then route framework work by task:

- Installer workflow changes: `docs/installer.md`, then the relevant
  `docs/install/*.md` checklist.
- Framework concepts: `docs/framework.md`; capability outcomes and
  prerequisites: `docs/capability-map.md`.
- Asset boundary changes: the relevant manifest in `manifests/`.
- Target-repo installable content: the source template under `templates/` or
  skill under `skills/`.
- Platform adapter guidance: `docs/platform-support.md`, then only the relevant
  platform note or adapter README.
- Deferred ideas: `TODO.md`; treat it as a work record, not active guidance.

Do not load historical or future-facing docs such as
`docs/level-5-orchestration.md` unless the task is about that topic.

## Source Of Truth

- Principles live in `docs/principles.md`.
- Course purpose and its relationship to the framework live in
  `docs/course-maintenance.md`.
- Installer routing lives in `docs/installer.md` and `docs/install/`.
- Capability definitions and prerequisites live in `docs/capability-map.md`.
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

When changing installer docs, preserve staged installation as one Profile
Change at a time: dependency check first, human approval before edits, then
validation and handoff before another capability is inspected.

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
