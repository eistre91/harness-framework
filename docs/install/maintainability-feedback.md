# Maintainability Feedback Installer Checklist

Audience: agents and maintainers adding, removing, or changing selected
Maintainability Feedback in a target repo.

Use when: Maintainability Feedback is the one human-selected Profile Change and
the Current Harness Profile already contains validated Bounded Work. Start from
`docs/installer.md` and complete its dependency check first.

## Read For This Change

Always read:

- `docs/principles.md`,
- `docs/installer.md`,
- the Maintainability Feedback section and Canonical Prerequisites table in
  `docs/capability-map.md`,
- `manifests/maintainability-feedback.yml`,
- required portable sources selected from that manifest,
- the target repo's Current Harness Profile and relevant feedback records,
- its installed agent entrypoint, work source, and executable-scope surface,
  and
- only the target-repo evidence relevant to the exact observation mechanisms
  in selected discovery scope.

Read only when current scope requires it:

- `skills/optional/harness-documentation-audit/SKILL.md`, for an approved
  documentation or semantic-drift observation,
- relevant platform or CI guidance when the selected mechanism uses it,
- existing tools, commands, reports, and architecture sources needed by the
  selected mechanism,
- `docs/portable-assets.md`, when adaptation seams are unclear.

Do not read sibling capability checklists or manifests, every candidate tool,
broad unrelated repo history, future-facing orchestration guidance, or
`TODO.md`. Record any exceptional source and why it was needed in the proposal
and handoff.

## Scope

Maintainability Feedback deliberately observes selected forms of accumulated
drift, preserves reviewable evidence, and supports operator disposition into
bounded follow-up work. Use `manifests/maintainability-feedback.yml` as the
canonical family boundary; inspect and realize only exact observation
mechanisms selected for this Profile Change.

One claim may contain one or several independently justified observations. It
does not imply that every family is installed or that the system is healthy.
If selected discovery justifies none, stop without changing the repo or Current
Harness Profile.

Classify a shared detector by purpose and effect:

- Maintainability Feedback observes across work or over time and feeds later
  operator judgment.
- Agent Action Boundaries guide, verify, or block one agent action or lifecycle
  transition.

The same detector may support both only when detection policy has one source
owner and each use declares its effect. Feedback is non-blocking by default.
Per-change observation must be separately justified as acceptably quiet, cheap,
and non-blocking.

This change may investigate, record, disposition, and shape proposed follow-up
work. It does not authorize repair, broad cleanup, tool installation unrelated
to the approved realization, external issue mutation, or new gates.

## Discovery

An exact observation is justified by either a concrete recurring or high-cost
drift signal or an operator-approved bounded experiment into a named risk or
uncertainty. Desire for a broader harness is not evidence.

Inspect only the human-selected families and measurements. For each candidate,
identify:

- beneficiary, signal or uncertainty, and smallest useful scope,
- evidence source and observation window,
- mechanism, trigger or cadence, operator, and durable record destination,
- expected runtime, cognitive cost, noise, blind spots, and false positives,
- a supervised trial that exercises the target environment, and
- evidence that would cause revision, pause, or removal.

Prefer existing repo tools and work surfaces. Do not invent architecture,
install a tool, prescribe a universal schedule, or create a second finding
database merely to discover whether an observation is useful.

Human-agent comprehension observations are experimental. Use bounded evidence
such as repeated clarification, conflicting explanations, unrecoverable recent
intent, context-routing failures, recent durable work records, and short
operator review. Record uncertainty prominently; do not introduce scores,
dashboards, synthetic probes, or claims of objective comprehension.

## Proposal

Use the Harness Fit Proposal contract and include only this one Maintainability
Feedback change. Complete its Selected Maintainability Feedback subsection and
apply these capability-specific decision rules:

- current Bounded Work prerequisite evidence and relevant Known Limits,
- exact discovery scope and the evidence or approved experiment justifying it,
- required policy and coordinator handling plus conditional specialists,
- existing tools and durable work surfaces to retain or adapt,
- exact files and behavior authorized,
- feedback families intentionally deferred, and
- context used.

Use one compact subsection per exact selected observation as the template
requires.
Persist and present the exact proposal, then wait for human approval before
editing target-repo files. Approval does not authorize findings repair,
external issue creation, new gates, or another capability.

For a realization change or removal, inspect only the affected selected
observations. Preserve unrelated current observations, validate changed
mechanisms and durable records, and update the profile claim only after the
resulting selected scope is demonstrated. If no observation remains after an
approved removal, remove the capability claim.

## Installation And Adaptation

Install or equivalently satisfy the selected target policy and coordinator.
Record exact observations rather than copying the framework's family menu.
Reuse the repo's current durable work surface for run records unless the human
approved a different destination.

Keep the coordinator thin. Point it to the installed policy, work source,
approved record surfaces, existing repo tools, and selected specialists. Keep
detailed procedures in source-owned mechanisms or specialist skills; do not
bake in a tracker, language, analyzer, CI provider, hook runtime, or agent
platform.

## Supervised Trial

Run one supervised trial for every added or materially changed observation
before claiming the selected outcome. Before each trial, restate its scope,
mechanism, evidence sources, expected cost and noise, Known Limits,
findings-only authority, and durable record destination. Obtain renewed human
approval if these facts differ materially from the proposal.

The trial must show that:

- the mechanism runs in the target environment and stays within approved
  scope,
- output is understandable and linked to evidence,
- runtime, cognitive cost, noise, and false positives are reviewable,
- Known Limits and uncertainty remain visible,
- results support operator disposition,
- the durable destination receives a run record, and
- the run neither gates changes nor mutates product or documentation.

A clean result is valid when the mechanism inspected what it claimed. Preserve
the clean result and unresolved coverage gaps. Chat-only output or a gitignored
local draft is not durable evidence.

## Capability Gate

Validation passes only when representative evidence supports the selected
Maintainability Feedback outcome. Check:

- The Current Harness Profile still contains validated Bounded Work.
- Every realized observation matches an approved proposal entry; no unapproved
  family or mechanism was added.
- The selected target policy and coordinator are installed or equivalently
  satisfied.
- Every added or changed observation completed a supervised target-environment
  trial and left a durable record for operator review.
- Each record includes scope and window, exact observation, evidence sources,
  findings or clean result, drift classification, impact, Known Limits,
  uncertainty, likely false positives, operator disposition, and approved
  follow-up links.
- Runtime, cognitive cost, noise, false positives, and limits are acceptable
  and recorded.
- Runs remained investigative and did not repair findings, create undelegated
  external issues, or gate changes.
- The resulting Current Harness Profile claim states exact selected scope,
  realizations, evidence, Known Limits, and revisit or removal signals without
  implying broad system health or exhaustive observation.
- The report lists context used and recommends stopping.

An unselected useful family does not fail this change. A selected observation
fails when it lacks approval, trial evidence, a durable record, operator
review, or honest limits, or when its normal run mutates or gates the repo.

## Profile Update And Handoff

On passed validation, add, update, or remove only the Maintainability Feedback
claim in `docs/harness/README.md`, confirm dependency closure, and complete the
durable proposal or handoff. On failed or incomplete validation, leave the
Current Harness Profile unchanged.

In addition to the template's Installation And Validation Record, record:

- each exact observation and approved proposal details,
- policy, coordinator, specialist, tool, and existing-surface handling,
- trial procedure and result,
- durable record locations and operator dispositions,
- runtime, cognitive cost, noise, false positives, and Known Limits,
- intentionally deferred observations and revisit signals,
- confirmation that runs did not repair, gate, or create undelegated external
  issues, and
- recommended next action: stop by default or revise this Maintainability
  Feedback change.

Do not inspect another capability after this handoff. Multi-Work Coordination
has no installable package; record long-horizon observations plainly without
loading or proposing that emerging domain.
