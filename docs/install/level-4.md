# Level 4 Installer Checklist

Audience: agents and maintainers installing selected maintainability sensors in
a target repo.

Use when: Level 1 has been installed and validated, the human has chosen to
inspect maintainability sensing, and the current approved installation stage is
Level 4. Start from `docs/installer.md` first.

## Read For This Stage

Always read:

- `docs/principles.md`
- `docs/installer.md`
- this checklist
- `manifests/level-4.yml`
- the Level 4 section of `docs/maturity-model.md`
- the required portable policy and coordinator sources named by the manifest
- the target repo's durable Level 1 handoff under `docs/harness/`
- the target repo's installed agent entrypoint
- the target repo's canonical work source and Agent Work Brief location or
  equivalent executable-scope surface
- only the target-repo evidence relevant to the exact sensors in current scope

Read only if needed for this Level 4 stage:

- `skills/optional/harness-documentation-audit/SKILL.md`, when the selected
  documentation or semantic-drift scope benefits from that specialist
- relevant platform or CI guidance, only when an approved sensor mechanism uses
  that platform or CI surface
- existing maintainability tools, commands, and reports, only for selected
  sensor families
- `docs/portable-assets.md`, when adaptation boundaries are unclear
- `docs/implementation-guide.md`, only for a design question this checklist
  does not answer

Do not read by default:

- Level 5 guidance
- `TODO.md` or `docs/ignored/`
- the full `manifests/optional-assets.yml`
- broad product, historical, or provenance docs outside the selected scope
- every candidate tool for a selected sensor family

If you read an out-of-stage source, record why in the proposal and stage
handoff.

## Scope And Level 3 Boundary

Level 4 installs a selected operating protocol for observing accumulated drift
across work or sessions, leaving durable evidence, and helping the operator
shape bounded follow-up work. Use `manifests/level-4.yml` as the canonical
sensor-family menu. Do not maintain a second full family list here.

A Level 4 pass installs one or more justified exact sensors; it does not install
every family by default. If inspection justifies none, stop without installing
Level 4 or claiming Level 4 completeness. Canonical completeness means that the
required policy, coordinator, records, and supervised evidence are complete for
the approved sensor scope; it does not mean that the full menu is installed.

Level 4 requires a validated Level 1 bounded-work foundation so approved
findings can become executable work. It does not require or certify Level 2
context routing or Level 3 deterministic controls.

Classify a mechanism by purpose and effect:

- Level 4 observes broader health, trends, or accumulated drift and feeds later
  triage.
- Level 3 guides, verifies, or blocks a particular agent action or lifecycle
  transition.

The same detector may support both uses only when detection policy has one
source owner and each use declares its effect. A Level 4 use is non-blocking by
default. Per-change observation must be separately justified as acceptably
quiet, cheap, and non-blocking.

The stage investigates, records, dispositions, and shapes approved work. It
does not repair findings, perform broad cleanup, install or reconfigure tools,
create or edit external issues, change enforcement, or inspect unrelated repo
areas without separate explicit delegation.

## Discovery And Eligibility

A repo is eligible for a selected sensor only when it has either:

- a concrete recurring or high-cost maintainability signal, or
- an operator-approved bounded experiment addressing a named uncertainty or
  risk.

Wanting a higher level is not evidence. For each candidate, identify who
benefits, how, the exact signal or uncertainty, the smallest observation scope,
available evidence, expected cost and noise, known limits, and what would cause
the sensor to be removed.

Inspect only the families and exact measurements in current approved discovery
scope. Prefer existing repo tools and work surfaces. Do not install a new tool,
invent an architecture expectation, prescribe a universal schedule, or create
a record system while discovering whether a sensor is valuable.

Use these questions:

- What repeated drag, drift, uncertainty, or risk is expensive enough to
  observe now?
- Which exact measurement or review would provide decision-useful evidence?
- What repo surface and observation window are sufficient without broadening
  the audit?
- Which existing command, report, work record, human check, or specialist can
  gather the evidence?
- Who will operate the sensor and who owns disposition decisions?
- Where will the run record survive chat, agent context, and local workspace
  cleanup?
- What runtime, cognitive cost, noise, blind spots, and false positives are
  likely?
- What supervised trial can show whether the mechanism works in the target
  environment?
- What evidence would cause the repo to revise, pause, or remove the sensor?

Human-agent comprehension sensing is experimental. Use bounded evidence such as
repeated clarification, conflicting explanations, unrecoverable recent intent,
context-routing failures, recent durable work records, and a short operator
review. Record uncertainty prominently; do not propose scores, dashboards,
synthetic probes, or claims of objective comprehension measurement.

## Selected-Sensor Proposal

Prepare and persist a Level 4 proposal before editing. It authorizes only the
exact sensors and portable assets listed for this pass.

Include a compact stage summary:

- current stage: Level 4,
- target behavior: selected maintainability sensing,
- installation mode: usually `starter` or `overlay`; use `canonical` only when
  selected-scope completeness is explicit,
- durable Level 1 handoff status and relevant gaps,
- repo evidence or approved experiment that justifies Level 4 now,
- Level 4 asset completeness for the approved selected scope,
- expected Level 4 behavioral completeness for that scope,
- required policy/coordinator handling and any conditional specialist,
- files to create or edit,
- current-stage deferrals,
- human decisions needed before editing, and
- context used.

For every exact sensor, record short per-sensor detail:

- sensor family and exact sensor or measurement,
- why now: evidence, risk, or bounded experiment, including the beneficiary,
- intended primary and possible secondary debt categories,
- repo surface, observation scope, and observation window,
- mechanism and evidence sources,
- trigger or cadence,
- operator or decision owner,
- durable record destination,
- expected runtime, cognitive cost, and noise,
- known limits and false-positive risk,
- supervised trial command or procedure, and
- revisit or removal signal.

Use a compact summary plus per-sensor sections rather than one unreadably wide
table. Out-of-stage observations remain plain observations; do not use this
proposal to authorize repair, external issue creation, new gates, or Level 5
inspection.

The proposal and installed policy entry normally satisfy the Harness Component
Brief requirement. Use a separate component brief only for an unusually complex
sensor with its own lifecycle, dependencies, or governance.

## Human Checkpoint Before Editing

Present the exact persisted proposal to the human and wait for approval or
corrections.

The approval covers only:

- Level 4 installation mode and selected-scope completeness claim,
- required portable assets and equivalent existing surfaces,
- exact sensor families, measurements, and observation scopes,
- mechanisms and evidence sources,
- files to create or edit,
- triggers or cadences and operators,
- durable record destinations,
- supervised trial commands or procedures,
- expected runtime, cognitive cost, noise, limits, and false-positive risks,
  and
- revisit or removal signals.

Do not edit target-repo files before this checkpoint is resolved. Approval does
not authorize findings repair, external issue creation, new gates, or Level 5
inspection.

## Installation And Adaptation

Install or equivalently satisfy the required target policy and
`harness-maintainability` coordinator. Add only the selected sensor behaviors
and conditional specialist approved in the proposal.

Adapt the target maintainability policy to record selected exact sensors, not
the framework's full family menu. Reuse the repo's canonical work surface for
run records by default. Add a repo-specific report location only when no
existing durable surface is suitable and the operator approved it.

Keep the coordinator thin. Point it to the installed policy, canonical work
source, approved durable record surfaces, existing repo tools, and selected
specialists. Keep detailed sensor procedures in specialist skills or repo-owned
mechanisms. Do not bake in a tracker, language, static-analysis tool, CI
provider, hook runtime, or agent platform.

For each sensor, record trigger or cadence, operator, expected cost and noise,
known limits, trial procedure and result, and revisit or removal signal. A
target may begin with human-invoked or manually scheduled runs and later change
the mechanism only through a separately approved proposal.

## Supervised Trial

Run one supervised trial for every selected sensor before claiming behavioral
completeness.

Before each trial, restate the exact sensor, scope, mechanism, evidence sources,
expected cost/noise, known limits, findings-only authority, and durable record
destination. Obtain operator confirmation when the trial details changed from
the approved proposal.

The trial must demonstrate that:

- the mechanism runs in the target environment,
- its actual scope matches the approved proposal,
- output is understandable and linked to evidence,
- runtime, cognitive cost, and noise are acceptable to the operator,
- known limits and likely false positives are recorded,
- results can be classified and dispositioned,
- the chosen work surface receives a durable run record, and
- the run neither gates changes nor mutates product code or documentation.

A clean trial is valid when the sensor inspected what it claimed to inspect.
Record the clean result and any unresolved coverage gap. A chat-only result or
gitignored local draft does not satisfy the durable-record gate.

## Level 4 Gate

Level 4 passes only for the approved selected scope. Check:

- The durable Level 1 handoff establishes the prerequisite foundation.
- Every installed sensor matches an approved proposal entry, and no unapproved
  family or measurement was installed.
- The target policy and coordinator behavior are installed or equivalently
  satisfied.
- Every selected sensor completed a supervised trial in the target environment.
- Every trial left a durable record and received operator review.
- Each record includes scope and observation window; selected family and exact
  sensor; mechanisms and evidence sources; findings and evidence pointers, or
  a clean result or unresolved gap when no actionable finding is retained; debt
  classifications; concrete impact and affected surface; known limits,
  uncertainty, and likely false positives; operator dispositions; and approved
  follow-up links.
- Runtime, cognitive cost, noise, false positives, and known limits are
  acceptable and recorded.
- The runs remained investigative and did not perform repairs, create
  undelegated external issues, or gate changes.
- Asset and behavioral completeness are stated for selected scope only.
- Deferrals and revisit or removal signals are durable.
- The handoff recommends stopping by default.

Missing unselected families do not fail the gate. An installed sensor fails the
gate when it lacks approval, trial evidence, a durable record, operator review,
or honest limits, or when it mutates or gates the target repo during a normal
run.

## Stage Handoff And Default Stop

After installation and trials, copy durable stage state under `docs/harness/`
using the canonical handoff fields in `docs/installer.md`.

Also record:

- each selected sensor and its approved proposal details,
- Level 4 asset and behavioral completeness for selected scope,
- policy, coordinator, specialist, tool, and existing-surface handling,
- trial procedure and result for each sensor,
- durable run-record locations and operator dispositions,
- runtime, cognitive cost, noise, false positives, and known limits,
- intentionally deferred sensors and revisit signals,
- confirmation that runs did not repair findings, gate changes, or create
  undelegated external issues, and
- plain out-of-stage long-horizon coordination or state-loss observations.

Recommend stopping after the Level 4 handoff. Level 5 remains exploratory and
has no implemented stage package. Inspect it only after an explicit human
request, following the staged installer's missing-stage fallback. Do not begin
Level 5 inspection as part of this handoff.
