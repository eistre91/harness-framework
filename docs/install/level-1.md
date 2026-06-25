# Level 1 Installer Checklist

Audience: agents and maintainers installing bounded work execution in a target
repo.

Use when: Level 0 has been installed and validated, the human has chosen to
inspect the next stage, and the current approved installation stage is Level 1.
Start from `docs/installer.md` first.

## Read For This Stage

Always read:

- `docs/principles.md`
- `docs/installer.md`
- this checklist
- `manifests/level-1.yml`
- the Level 1 section of `docs/maturity-model.md`
- `skills/core/harness-implement/SKILL.md`
- the target repo's durable Level 0 handoff under `docs/harness/`
- the target repo's installed `AGENTS.md`, repo checks script, and existing
  work-brief, implementation, and review skill locations named by the Level 0
  handoff

Read only if needed for this Level 1 stage:

- `docs/portable-assets.md`, when adaptation boundaries or skill conflict
  handling are unclear
- `skills/core/harness-work-brief/SKILL.md` and
  `skills/core/harness-work-brief/work-brief-template.md`, when the installed
  Level 0 work-brief guidance is missing required Level 1 behavior or must be
  refreshed from source
- `docs/implementation-guide.md`, only for deeper work-brief lifecycle or hook
  background that this checklist does not answer
- `docs/platform-support.md`, then only the relevant platform note, when the
  Level 1 proposal includes the `repo-checks-on-stop` starter pull-in

Do not read by default:

- `manifests/level-0.yml`
- `manifests/optional-assets.yml`
- Level 2 or Level 3 manifests
- platform adapter docs
- `docs/level-5-orchestration.md`
- `TODO.md`

If you read an out-of-stage source, record why in the proposal and stage
handoff.

## Scope

Level 1 adds bounded work execution on top of a validated Level 0 foundation.

Use `manifests/level-1.yml` as the canonical additive asset and behavior list.
Do not maintain a second file list here.

Conceptually, Level 1 should let the target repo:

- distinguish tiny, standard, and complex work before implementation,
- use explicit non-goals when scope could sprawl,
- capture ambiguity and decisions that affect implementation or review,
- name boundaries and interfaces before changing consumed surfaces,
- require acceptance evidence for externally visible or boundary-changing
  behavior,
- record progress and accepted divergences in the canonical brief location when
  work spans sessions or departs from the original plan,
- give implementation agents focused guidance for executing from a brief.

The required additive installable asset is `harness-implement`, unless an
existing target-repo component is proven to satisfy the same behavior and the
handling decision is recorded.

Level 1 may also include the manifest's `repo-checks-on-stop` starter pull-in
when `scripts/repo-checks.sh` is real, reasonably fast, actionable, and the
team wants automatic feedback during agent sessions. Keep this pull-in narrow:
run the canonical repo checks command. Broad hook policy, secret guards,
destructive-action controls, shared hook runners, cross-platform enforcement,
and CI or pre-commit parity remain selected deterministic controls beyond this
stage unless explicitly approved as separate current-stage scope.

Do not install Level 2 context routers, Level 3 control systems, optional
diagnostic skills, `SPEC-MAP.md`, `CONTEXT.md`, `.harness.yml`, or
maintainability sensors during Level 1 just because the repo shows possible
future need. Record those as plain out-of-stage observations.

## Proposal

Prepare a Level 1 proposal before editing. The proposal authorizes Level 1
edits only.

Include:

- current stage: Level 1,
- target maturity behavior: bounded work execution,
- installation mode: `canonical`, `starter`, or `overlay`,
- Level 0 foundation status and any Level 0 gaps that affect Level 1,
- repo signals that justify Level 1 now,
- Level 1 asset completeness,
- expected Level 1 behavioral completeness,
- existing implementation skill, command, or workflow handling,
- `harness-implement` install, adaptation, merge, or already-satisfied
  decision,
- work-brief behavior changes needed for tiers, non-goals, ambiguity,
  decisions, boundaries, acceptance evidence, and progress/divergence notes,
- canonical brief lifecycle and where Level 1 progress updates are written,
- acceptance evidence standards for boundary-changing or externally visible
  behavior,
- `repo-checks-on-stop` decision: include, exclude, or defer, with evidence and
  revisit signal,
- files to create or edit,
- current-stage deferrals,
- human decisions needed before editing,
- context used.

Out-of-stage observations may be recorded as plain observations. Do not map
them to future levels, propose later-stage assets, or ask for approval to
install them during the Level 1 stage.

## Human Checkpoint Before Editing

After writing and persisting the proposal, present the exact proposal text to
the human and wait for approval or corrections.

The approval should cover only:

- Level 1 installation mode,
- Level 1 files to create or edit,
- `harness-implement` installation or existing-component handling,
- any work-brief, repo entrypoint, or harness-doc updates needed for Level 1
  behavior,
- acceptance evidence standards,
- whether to include the narrow `repo-checks-on-stop` starter pull-in,
- durable location for the Level 1 decision log or stage handoff.

Do not edit target-repo files before this checkpoint is resolved.

## Level 1 Gate

Level 1 passes when bounded work execution is usable, not merely when a skill
file exists.

Check:

- The durable Level 0 handoff exists and either remains accurate or is updated
  by this stage.
- `harness-implement` is installed, adapted, or explicitly satisfied by an
  existing component with the handling decision recorded.
- `AGENTS.md` or the target repo's equivalent entrypoint tells agents to use
  work-brief, implementation, and review guidance by phase rather than as one
  combined reading list.
- The canonical work source and brief location remain explicit, including the
  local fallback and commit policy when a fallback exists.
- Standard or complex work has a clear place to record non-goals, ambiguities,
  accepted decisions, boundaries or interfaces, verification, and acceptance
  evidence.
- Work that spans sessions or diverges from the expected plan has a clear place
  to record current status, accepted divergence, latest evidence, blockers, and
  next action.
- Boundary-changing or externally visible work requires acceptance evidence in
  addition to mechanical verification.
- Implementation guidance tells agents to keep scope narrow, respect non-goals,
  use existing project patterns, run focused verification while iterating when
  practical, and run the canonical repo checks before claiming done.
- The review handoff names the brief or source, tier, changed files, behavior
  boundary, test surface, and known risks.
- If `repo-checks-on-stop` is installed, it runs only the canonical repo checks
  command and its inclusion is justified by real, reasonably fast, actionable
  checks plus human approval.
- If `repo-checks-on-stop` is not installed, the handoff records the reason and
  revisit signal.
- Level 2 or Level 3 assets were not installed unless the human explicitly
  changed the current approved stage.
- The stage report lists context used.
- The stage report confirms that optional manifests, broad adapter docs,
  deterministic-control policy, and future-facing docs were not used for this
  stage unless explicitly listed and justified.

For communication evidence, use a representative standard or complex work item
when one is available. Confirm that a fresh agent could identify the tier,
brief location, implementation guidance, verification, acceptance evidence, and
review handoff path. If no representative work item is available, record that
the Level 1 communication audit is limited to installed-surface inspection.

## Stage Handoff

After installation and validation, report the Level 1 result and copy durable
stage state under `docs/harness/`. Use the canonical stage handoff fields in
`docs/installer.md`.

For Level 1, make sure the handoff also makes these details explicit:

- `harness-implement` install or existing-component handling,
- work-brief lifecycle and progress/divergence location,
- acceptance evidence rules for boundary-changing or externally visible work,
- `repo-checks-on-stop` decision and result, when installed,
- representative communication audit result or reason it was not possible,
- recommended next action: stop, revise Level 1, or ask the human whether to
  begin selected next-stage inspection.

Do not inspect Level 2 guidance, Level 3 deterministic controls, or optional
pull-ins until the human chooses to begin that next stage or explicitly changes
the current approved scope.
