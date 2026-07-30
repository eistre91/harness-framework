# Agent Action Boundaries Installer Checklist

Audience: agents and maintainers adding, removing, or changing selected Agent
Action Boundaries in a target repo.

Use when: Agent Action Boundaries is the one human-selected Profile Change and
the Current Harness Profile already contains validated Bounded Work. Start from
`docs/installer.md` and complete its dependency check first.

## Read For This Change

Always read:

- `docs/principles.md`,
- `docs/installer.md`,
- the Agent Action Boundaries section and Canonical Prerequisites table in
  `docs/capability-map.md`,
- `manifests/agent-action-boundaries.yml`,
- the target repo's Current Harness Profile and relevant boundary records,
- the installed agent entrypoint and `scripts/repo-checks.sh`, and
- only the target-repo mechanisms and evidence relevant to the exact boundary
  families in selected discovery scope.

Read only when current scope requires it:

- `docs/platform-support.md`, then only the relevant platform note, for a
  selected runtime hook or config,
- `docs/hook-pattern.md`, for hook design beyond an existing adapter,
- `adapters/pre-commit/README.md`, when pre-commit is selected,
- the exact optional-asset or adapter manifest entry routed by selected scope,
- `docs/portable-assets.md`, when adaptation seams are unclear.

Do not read sibling capability checklists or manifests, every possible control
family, broad CI/CD or enterprise-tooling docs, unrelated historical sources,
future-facing orchestration docs, or `TODO.md`. Record any exceptional source
and why it was needed in the proposal and handoff.

## Scope

Agent Action Boundaries keep selected agent actions within explicit repo
operating limits at the point where consequential violations can be guided,
verified, or prevented. Use `manifests/agent-action-boundaries.yml` as the
canonical family boundary; inspect and realize only exact boundaries selected
for this Profile Change.

One claim may contain one or several independently justified boundaries. It is
not a bundle or a promise of comprehensive safety. Every boundary must earn its
friction through a concrete risk, recurring correction, or operator decision.

Bounded Work continues to own semantic delegation and the ordinary
`scripts/repo-checks.sh` plus narrow stop-automation contract. Agent Action
Boundaries own separately selected operational constraints around commands,
files, artifacts, and lifecycle transitions. A broad drift detector belongs to
Maintainability Feedback unless its selected purpose is to constrain one agent
action at a named lifecycle point.

## Discovery

Inspect only the boundary families in human-selected discovery scope. Ask:

- Which agent action creates expensive cleanup, exposure, data loss, broken
  history, or repeated review correction?
- At which event can feedback still change that action?
- What repo rule or source establishes the expected behavior?
- Should the mechanism observe, guide, block, or verify?
- What is the cheapest useful mechanism, and what safe path must remain easy?
- What friction, bypass pressure, noise, and coverage limit will it introduce?
- What evidence would cause the repo to revise or remove it?

Use these portable modes:

- `observe`: record or report a signal without preventing the action.
- `guide`: provide just-in-time direction and allow continuation.
- `block`: prevent the action or transition until its stated condition changes.
- `verify`: run a deterministic check and use pass/fail as evidence.

Do not use `ask` as a portable mode. A human decision can be a block with an
actionable next step or a platform-native approval flow explicitly selected by
the adapter. `warn` is a tone inside guide, not a separate mode.

Choose the narrowest effective lifecycle seam. Keep shared policy under one
owner and platform adapters thin. Secret controls must validate wiring by
names, declarations, aliases, and permissions without reading, printing, or
persisting secret values. Record bypass limits rather than claiming complete
prevention.

## Proposal

Use the Harness Fit Proposal contract and include only this one Agent Action
Boundaries change. In addition to the common fields in `docs/installer.md`,
record one compact row for every exact selected boundary:

| Boundary | Why now | Event | Mode | Mechanism | Files | Validation | Friction risk | Known limits | Revisit or removal signal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  | observe / guide / block / verify |  |  |  |  |  |  |

Also make explicit:

- current Bounded Work prerequisite evidence and relevant Known Limits,
- exact discovery scope and operator decisions,
- existing controls and shared policy to retain or adapt,
- manifest entries included, adapted, already satisfied, deferred, or
  excluded,
- exact files and behavior authorized,
- expected output, human-decision wording, safe path, and rollback when a
  selected boundary blocks or changes shared hooks,
- validation commands or smoke tests,
- control families intentionally deferred, and
- context used.

Persist and present the exact proposal, then wait for human approval before
editing target-repo files. Do not install unapproved boundaries merely because
they share a hook, script, detector, or adapter with an approved boundary.

For a realization change or removal, inspect only the affected selected
boundaries. Preserve unrelated current boundaries, validate every changed safe
and constrained path, and update the profile claim only after the resulting
selected scope is demonstrated. If no boundary remains after an approved
removal, remove the capability claim.

## Capability Gate

Validation passes only when representative evidence supports the selected
Agent Action Boundaries outcome. Check:

- The Current Harness Profile still contains validated Bounded Work.
- Every installed or retained boundary matches an approved proposal row; no
  unapproved family or behavior was added.
- Each selected boundary has an event, mode, mechanism, validation method,
  friction risk, Known Limits, and revisit or removal signal.
- Each changed boundary has deterministic command evidence, a wrapper or hook
  smoke test, or a documented reason why only static inspection was possible.
- Expected safe paths remain usable, and guide/block/failure output is
  actionable while pass output is quiet.
- Shared policy is not duplicated across adapters, hooks, docs, and scripts
  without a clear owner.
- Platform-specific files remain thin adapters when shared policy is
  practical.
- Secret controls do not expose or direct agents to inspect secret values and
  state known bypass limits.
- Destructive-command and protected-path controls are narrow enough that
  routine work does not encourage bypass.
- `scripts/repo-checks.sh` remains focused rather than becoming an unrelated
  CI/CD or maintainability bundle.
- The resulting Current Harness Profile claim states exact selected
  boundaries, realizations, evidence, Known Limits, friction, and revisit or
  removal signals without implying exhaustive coverage.
- The report lists context used.

An unselected useful boundary does not fail this change. A selected boundary
fails when it is hidden, unvalidated, noisy enough to invite bypass, blocks its
expected safe path, or overclaims coverage.

## Profile Update And Handoff

On passed validation, add, update, or remove only the Agent Action Boundaries
claim in `docs/harness/README.md`, confirm dependency closure, and complete the
durable proposal or handoff. On failed or incomplete validation, leave the
Current Harness Profile unchanged.

In addition to the canonical handoff fields in `docs/installer.md`, record:

- selected boundary rows realized or already satisfied,
- validation evidence for each changed boundary and its safe path,
- hook, script, Git hook, adapter, or repo-checks mechanisms used,
- Known Limits, friction, and expected operator cost,
- families intentionally deferred or excluded, and
- recommended next action: stop by default or revise this Agent Action
  Boundaries change.

Do not inspect another capability or boundary family after this handoff. The
human may select a new Profile Change in a later work unit.
