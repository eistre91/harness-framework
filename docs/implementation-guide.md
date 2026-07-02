# Agent Harness Implementation Reference

Audience: agents and maintainers needing broad orientation while fitting this
framework to a target repo.

Use when: `docs/installer.md` or a stage checklist routes you here for context
that the current source-of-truth file does not answer.

For ordinary installation, start with `docs/installer.md`, then the current
stage checklist and manifest. This file is a map, not an installation
checklist. Do not use it to approve edits, define completion, select assets, or
override a stage checklist, manifest, template, or skill.

## Rule

Harness implementation is repo diagnosis plus collaborative workflow design,
not blind template installation.

Install the smallest current-stage harness that lets humans and agents work
better now. Record gaps and revisit signals instead of expanding scope because
a later-stage asset exists.

## Source Of Truth Map

When sources conflict, update or trust the owner below rather than copying its
procedure here.

- Principles and maintenance decision lens: `docs/principles.md`
- Framework concepts and maturity language: `docs/framework.md`
- Maturity definitions and level capabilities: `docs/maturity-model.md`
- Staged installation workflow, human checkpoints, stage handoff fields, and
  post-stage sequencing: `docs/installer.md`
- Level 1 bounded-work installation procedure, gate, and handoff details:
  `docs/install/level-1.md`
- Level 2 context-routing installation procedure, gate, and handoff details:
  `docs/install/level-2.md`
- Level 3 selected-control installation procedure, gate, and handoff details:
  `docs/install/level-3.md`
- Bootstrap, Level 1, Level 2, Level 3, and optional asset boundaries:
  `manifests/bootstrap.yml`, `manifests/level-1.yml`,
  `manifests/level-2.yml`, `manifests/level-3.yml`, and
  `manifests/optional-assets.yml`
- Portable asset and adapter boundaries: `docs/portable-assets.md`
- Platform support: `docs/platform-support.md`, then only the relevant
  platform note routed by the current stage
- Broad hook adapter design: `docs/hook-pattern.md`, only when current approved
  scope includes hook design beyond the narrow Level 1 Stop adapter
- Proposal and durable decision-log schema:
  `templates/core/docs/harness/fit-proposal.md`
- Installed harness docs template: `templates/core/docs/harness/README.md`
- Target-repo checks template: `templates/core/scripts/repo-checks.sh`
- Work brief storage, fallback, sync, and progress guidance:
  `skills/core/harness-work-brief/`
- Implementation and review phase guidance:
  `skills/core/harness-implement/` and `skills/core/harness-review/`
- Level 2 routing templates: `templates/level-2/`

Do not maintain second copies of those assets, schemas, file lists, proposal
fields, checklists, commands, gates, or report formats in this guide.

## Installation Routing

Use this sequence:

```text
principles -> staged installer -> current stage checklist -> current stage
manifest -> manifest-named templates and skills -> narrow routed references
```

Read broader or later-stage sources only when the current checklist or
human-approved scope routes to them. If a later-stage signal appears during a
current-stage install, record it as a plain out-of-stage observation unless the
human chooses to begin that stage or approve a selected pull-in.

The current stage proposal owns authorization to edit target-repo files. The
stage checklist owns what that proposal, checkpoint, gate, and handoff must
cover.

## Decision Lens

Use this lens when the source-of-truth procedure leaves room for judgment.

### Start Small

Most target repos should begin with the Level 1 bounded-work foundation. A
small harness that is used is more valuable than a broad harness that becomes
ignored process.

### Surface Gaps Without Owning Every Gap

Harness installation may reveal missing tests, unclear CI, stale README
commands, no tracker convention, weak secret handling, or scattered project
docs. Surface those gaps in the current-stage proposal or handoff, but do not
turn harness installation into a broad modernization project unless the human
approves that scope.

### Argue For Complexity

When proposing a component beyond the current stage, state the concrete
failure or coordination cost it addresses, the evidence that the repo needs it
now, the maintenance cost it adds, the simpler option considered, and the
signal that would justify removing or simplifying it later.

### Preserve Ownership

Keep universal operating guidance in the repo entrypoint, deterministic checks
in `scripts/repo-checks.sh`, phase-specific workflow in harness skills and
work-brief guidance, durable harness decisions in `docs/harness/`, and
tool-specific behavior in thin adapters.

## Common Routing Questions

Where do proposal fields come from?

Use the current stage checklist and
`templates/core/docs/harness/fit-proposal.md`.

Where do acceptance and completion checks come from?

Use the current stage gate and handoff sections in `docs/install/`.

Where do lint, type-check, and test commands come from?

Use `docs/install/level-1.md` for discovery expectations and adapt
`templates/core/scripts/repo-checks.sh`. Keep actual command details in the
target repo's `scripts/repo-checks.sh`, not in docs.

Where does work-brief storage and progress guidance live?

Use `skills/core/harness-work-brief/` and the current stage checklist. Record
target-repo storage, fallback, and sync decisions in the stage proposal and
durable harness docs.

Where do hook decisions live?

Level 1 owns only the narrow `repo-checks-on-stop` behavior described in
`docs/install/level-1.md` and `manifests/level-1.yml`. Broader hook policy,
secret guards, destructive-action controls, and CI or pre-commit parity require
separate approved Level 3 scope through `docs/install/level-3.md`.

Where do final report and handoff fields come from?

Use `docs/installer.md` plus the current stage checklist. The durable target
repo record belongs under `docs/harness/`.

## Wording Check

Before finishing installed docs, verify that wording does not:

- claim a maturity level that is only a target,
- describe partial starter or overlay completeness as full canonical
  completeness,
- imply agents should access, print, inspect, or directly handle sensitive
  values instead of validating secrets-management wiring,
- record machine-local paths such as a framework checkout path or `/tmp`
  proposal file in durable docs,
- blur required current-stage behavior with optional or later-stage guidance,
- turn `AGENTS.md` into a product strategy document, historical note, or
  phase-specific procedure,
- tell ordinary implementers to read `docs/harness/` when they only need the
  work brief, project docs, and code.

The goal is not maximum harness maturity. The goal is the smallest installed
harness that improves current human-agent work and makes the next useful layer
obvious when the project earns it.
