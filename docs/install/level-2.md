# Level 2 Installer Checklist

Audience: agents and maintainers installing product context routing in a target
repo.

Use when: Level 1 has been installed and validated, the human has chosen to
inspect the next stage or selected context routing, and the current approved
installation stage is Level 2. Start from `docs/installer.md` first.

## Read For This Stage

Always read:

- `docs/principles.md`
- `docs/installer.md`
- this checklist
- `manifests/level-2.yml`
- the Level 2 section of `docs/maturity-model.md`
- `templates/level-2/SPEC-MAP.md`
- `templates/level-2/docs/project/areas/README.md`
- the target repo's durable Level 1 handoff under `docs/harness/`
- the target repo's installed `AGENTS.md`, canonical work source, existing
  project context index if any, and only enough repo evidence to identify ADR,
  decision-log, project-doc, or area-doc locations

Read only if needed for this Level 2 stage:

- `docs/portable-assets.md`, when adaptation boundaries are unclear
- the `project-intent` entry in `manifests/optional-assets.yml`, followed by
  `templates/optional/docs/project/intent.md`, when repeated planning,
  exploratory, scope, or value-sensitive review decisions need a shared project
  north star
- `docs/implementation-guide.md`, only for deeper installation background that
  this checklist does not answer

Do not read by default:

- Level 3 or later manifests
- platform adapter docs
- broad historical, plan, discussion, or provenance docs in the target repo
- `docs/level-5-orchestration.md`
- `TODO.md`

If you read an out-of-stage source, record why in the proposal and stage
handoff.

## Scope

Level 2 adds product context routing on top of bounded work execution.

Use `manifests/level-2.yml` as the canonical additive asset and behavior list.
Do not maintain a second file list here.

Conceptually, Level 2 should let the target repo route ordinary implementation
work through this path:

```text
repo entrypoint -> Agent Work Brief -> SPEC-MAP.md -> project-area brief
  -> trigger-matched deep references -> focused code and tests
```

The required additive installable assets are:

- `SPEC-MAP.md`, the task-intent router,
- `docs/project/areas/README.md`, the area-brief guide and template,
- target-specific project-area briefs or equivalent existing docs for the
  areas that justified Level 2.

`SPEC-MAP.md` should route implementation intent. It is not a live roadmap,
historical index, broad product encyclopedia, or substitute for the work brief.
It should point agents to the first useful area brief and then to optional deep
references only when a trigger matches the current change.

Project-area briefs should stay short enough to scan. The default target is
roughly 80 to 150 lines per brief. Split a brief or move details into deep
references when it stops being quick to use.

Optional `docs/project/intent.md`, a domain glossary such as `CONTEXT.md`, or
an existing ADR or decision-log index may be included only when current-stage
evidence justifies them. Do not install `CONTEXT-MAP.md`, documentation quality
audits, maintainability sensors, broad doc-link enforcement, `.harness.yml`, or
Level 3 controls during Level 2 unless the human explicitly changes the
current approved stage.

When a domain glossary exists, keep the boundary clean: the glossary owns
canonical language and `SPEC-MAP.md` uses that language to route implementation
intent. Do not duplicate glossary definitions inside `SPEC-MAP.md` or area
briefs.

## Proposal

Prepare a Level 2 proposal before editing. The proposal authorizes Level 2
edits only.

Include:

- current stage: Level 2,
- target maturity behavior: context routing,
- installation mode: `canonical`, `starter`, or `overlay`,
- Level 1 bounded-work foundation status and any Level 1 gaps that affect
  Level 2,
- repo signals that justify Level 2 now,
- Level 2 asset completeness,
- expected Level 2 behavioral completeness,
- existing project docs, ADRs, decision logs, glossaries, maps, or area docs
  and how they will be used, adapted, superseded, or left alone,
- `SPEC-MAP.md` install, adaptation, or existing-router decision,
- project-area brief path decision, defaulting to `docs/project/areas/` unless
  the repo has a better existing equivalent,
- initial task intents and area briefs to create or adapt,
- source-of-truth order for code, tests, work briefs, ADRs, project docs, and
  historical records,
- optional `project-intent` or glossary decision, when relevant,
- files to create or edit,
- current-stage deferrals,
- human decisions needed before editing,
- context used.

Out-of-stage observations may be recorded as plain observations. Do not map
them to future levels, propose later-stage assets, or ask for approval to
install them during the Level 2 stage.

## Human Checkpoint Before Editing

After writing and persisting the proposal, present the exact proposal text to
the human and wait for approval or corrections.

The approval should cover only:

- Level 2 installation mode,
- Level 2 files to create or edit,
- `SPEC-MAP.md` installation or existing-router handling,
- project-area brief location and initial briefs,
- optional `project-intent` or glossary inclusion, when proposed,
- source-of-truth order and historical-doc routing,
- durable location for the Level 2 decision log or stage handoff.

Do not edit target-repo files before this checkpoint is resolved.

## Level 2 Gate

Level 2 passes when a fresh implementation agent can find the smallest useful
project context without bulk-reading broad docs.

Check:

- The durable Level 1 handoff exists and either remains accurate or is updated
  by this stage.
- `AGENTS.md` or the target repo's equivalent entrypoint tells agents where
  project context routing starts without turning the entrypoint into a broad
  project encyclopedia.
- `SPEC-MAP.md` exists, is adapted to target-repo task intents, and includes
  how to use it, source-of-truth order, task-intent routing, trigger-matched
  deep references, and update triggers.
- `docs/project/areas/README.md` or an approved equivalent area-brief guide
  exists and includes the brief size and shape guidance.
- Each installed project-area brief is short enough to scan, names its audience
  and use-when triggers, lists what to read first, uses trigger-matched deep
  references, names important modules or surfaces, records core invariants,
  lists common wrong turns, points to useful tests or searches, and says when
  docs should be updated.
- `SPEC-MAP.md` routes to every installed project-area brief.
- A representative current task can be routed from task intent to the first
  useful area brief and only the needed deep references.
- ADRs, decision logs, historical notes, broad plans, and provenance records
  are not default implementation reads unless a route, brief, work brief, or
  human request triggers them.
- Installed routes do not point to missing files. If a route is useful but
  cannot be fixed in this stage, the stage handoff records it as a gap and does
  not claim full canonical Level 2 asset or behavioral completeness.
- Missing routes discovered during the representative routing audit are
  reported as cleanup work rather than silently ignored.
- Optional `project-intent`, glossary, or existing context docs are included
  only when the proposal records the evidence and maintenance owner.
- If a glossary exists, `SPEC-MAP.md` and project-area briefs use its domain
  terms without redefining them.
- Level 3 or later controls were not installed unless the human explicitly
  changed the current approved stage.
- The stage report lists context used.

For communication evidence, use a representative task from the repo when one
is available. Record the chosen task intent, selected area brief, deep
references opened or skipped, and any missing route. If no representative task
is available, record that the Level 2 communication audit is limited to
installed-surface inspection.

## Stage Handoff

After installation and validation, report the Level 2 result and copy durable
stage state under `docs/harness/`. Use the canonical stage handoff fields in
`docs/installer.md`.

For Level 2, make sure the handoff also makes these details explicit:

- `SPEC-MAP.md` install or existing-router handling,
- project-area brief location,
- installed or adapted area briefs,
- source-of-truth order,
- optional `project-intent`, glossary, ADR, or decision-log routing decisions,
- representative routing audit result or reason it was not possible,
- broken or missing route cleanup,
- recommended next action: stop, revise Level 2, or ask the human whether to
  begin selected next-stage inspection.

Do not inspect Level 3 deterministic controls, maintainability sensors, or
optional pull-ins beyond this stage until the human chooses to begin that next
stage or explicitly changes the current approved scope.
