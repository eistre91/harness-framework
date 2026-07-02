# Staged Harness Installer

Audience: agents and maintainers fitting this framework to a target repo.

Use when: installing the harness in a target repo. For conceptual framework
design, use `docs/framework.md`. For broad installation reference, use
`docs/implementation-guide.md` after this staged entrypoint routes you there.

## Rule

Install and validate the harness one maturity stage at a time.

The default path is:

```text
inspect -> Level 1 proposal -> human approval -> Level 1 install ->
validation and handoff -> human decision to stop or inspect context routing
```

Do not turn eligibility for a later level into approval to install that later
level. A target repo may show signs that Level 2 context routing or selected
deterministic controls will be useful, but the installer should first install a
clear Level 1 bounded-work foundation and validate that ordinary agent work can
start there.

## Always-Read Sources

Read these before any staged install:

- `docs/principles.md`
- this file
- the current stage checklist under `docs/install/`, when one exists
- the current stage manifest

The current stage checklist names any additional current-stage templates,
skills, or reference docs to read. Do not load higher-level manifests, optional
asset manifests, adapter docs, future-facing TODOs, or exploratory docs unless
the current stage checklist or human-approved scope explicitly requires them.

If the human asks to inspect a next stage and no checklist exists for that
stage, do not infer the path silently. Say that the stage checklist is missing,
then use the stage manifest if one exists, `docs/maturity-model.md`, and
`docs/implementation-guide.md` as provisional references only after the human
confirms that next-stage inspection should proceed. Record the missing checklist
or manifest as a framework follow-up in the stage handoff.

If you need a broad conceptual answer while installing, prefer the smallest
relevant source. Use `docs/framework.md` only when the staged installer docs and
principles do not answer a harness-design question.

## Source Routing

- Asset boundaries: manifests own what can be installed for each stage.
- Installation sequence and checkpoints: this staged installer path owns the
  workflow.
- Portable adaptation rules: `docs/portable-assets.md`, when a stage needs
  repo-specific adaptation boundaries clarified.
- Platform-specific support: `docs/platform-support.md`, then the specific
  platform note, only when the current approved stage includes that adapter.
- Broad hook adapter design: `docs/hook-pattern.md`, only when the current
  approved scope includes hooks beyond the narrow Level 1 Stop adapter or the
  platform docs route there for a design question.
- Mature or future-facing orchestration: do not read during ordinary Level 1
  installation.

## Stage Proposals

Each stage gets its own proposal. The proposal authorizes only the current
stage's edits.

Before editing target-repo files:

1. Inspect only enough target-repo context to fit the current stage.
2. Write and persist the stage proposal, usually under `/tmp` unless the human
   chose another temporary planning location.
3. Present the exact proposal text to the human.
4. Wait for explicit approval or corrections.

Inspect first, infer low-risk defaults from repo evidence, and ask only
questions that materially affect the current-stage harness shape.

The proposal should include:

- current stage,
- target maturity behavior for this stage,
- installation mode: `canonical`, `starter`, or `overlay`,
- asset completeness for this stage,
- behavioral completeness expected after this stage,
- files to create or edit,
- adaptation decisions,
- placeholders or gaps that are allowed for this stage,
- current-stage deferrals,
- human decisions needed before editing,
- context used.

Use plain out-of-stage observations only when evidence appears while doing
current-stage work. Do not classify those observations by future maturity level,
preselect future assets, load optional manifests, or ask the human to approve
later-stage edits in the current-stage proposal.

## Required Human Checkpoints

Each stage has two human checkpoints.

Pre-edit approval:

- The installer has written and persisted the stage proposal.
- The human approves or corrects only the current stage's planned edits.
- The installer edits only the approved files and behavior.

Post-stage decision:

- The installer reports validation results, context used, installed files,
  placeholders, gaps, deferrals, communication audit findings, and out-of-stage
  observations.
- The human decides whether to stop or begin inspection for the next stage.

## Stage Validation And Handoff

Every completed stage leaves a lightweight handoff artifact. The final
post-stage report can serve as that artifact when it is copied into the durable
target-repo harness record.

Record the durable stage state under `docs/harness/`. A simple install can put
the decision log in `docs/harness/README.md`; a larger install may use
`docs/harness/fit-proposal.md` or `docs/harness/install-log.md` with sections
per stage.

Canonical stage handoff fields:

- stage completed,
- installation mode,
- stage asset completeness,
- stage behavioral completeness,
- files installed or edited,
- validation result,
- mechanical verification,
- acceptance or communication evidence,
- context used,
- human decisions,
- placeholders and gaps,
- deferrals,
- out-of-stage observations,
- recommended next action.

For large target repos, treat a stage boundary as a natural context-window
split. A fresh agent should be able to continue from the durable stage handoff
without relying on chat history.

## Level 1 First

Most installs should begin with Level 1. Use `docs/install/level-1.md` for the
current Level 1 stage checklist.

Level 1 includes bounded work execution: work-brief shaping, implementation
guidance, review guidance, verification expectations, and the skill-use rules
for ordinary harness work. Level 0 is the no-installed-harness baseline, not an
installer stage.

## Level 2 Context Routing

After Level 1 has been installed and validated, ask whether to stop or inspect
context routing. If the human chooses Level 2 inspection, use
`docs/install/level-2.md` for the current Level 2 stage checklist.

Do not inspect Level 3 deterministic controls, maintainability sensors, or
future orchestration guidance during Level 2 unless the human explicitly
changes the current approved stage or the Level 2 checklist routes to a narrow
current-stage pull-in.

## Level 3 Selected Deterministic Controls

Selected deterministic controls may be inspected after Level 1 has been
installed and validated when the human chooses that stage or when the human
explicitly approves a selected Level 3 pull-in as the current scope. Use
`docs/install/level-3.md` for the current Level 3 stage checklist.

Level 3 is a selected-control menu, not a required bundle. Do not treat a
signal that one control family may help as approval to inspect or install every
Level 3 family. Each selected control needs its own proposal row, human
approval, validation, known limits, friction risk, and revisit or removal
signal.

Level 3 does not replace Level 1 repo checks. Level 1 owns
`scripts/repo-checks.sh` and the narrow `repo-checks-on-stop` behavior. Level 3
owns separately approved deterministic controls that constrain risky or
repeatedly missed agent actions beyond that foundation.
