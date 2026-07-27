# Profile Change Harness Installer

Audience: agents and maintainers fitting this framework to a target repo.

Use when: adding, removing, or changing one capability realization in a target
repo's Harness Profile. The Capability Map and the selected manifest and
checklist are the conceptual and procedural installation owners.

If a target repo was installed under the retired numbered model and has not
yet established a Current Harness Profile, use
`docs/install/migrate-numbered-model.md` for the one-time documentation
migration. That path re-profiles installed behavior without authorizing a
capability installation or realization change. Return here only after the
migration handoff or when the human separately selects a Profile Change.

## Rule

Fit, approve, realize, and validate one Profile Change at a time.

The default path is:

```text
read current profile and prerequisites -> select one Profile Change ->
inspect only its scope -> persist proposal -> human approval -> realize ->
validate outcome -> update profile and hand off -> stop
```

If the repo has no installed Harness Profile, the only eligible addition is
Bounded Work. Install and validate that foundation, update the profile, hand
off, and stop before the human decides whether to consider another capability.

Eligibility is not approval. Repo evidence may suggest several useful
capabilities, but the current proposal authorizes only one addition, removal,
or realization change and its exact selected scope.

## Always-Read Sources

Before inspecting a Profile Change, read:

- `docs/principles.md`,
- this file,
- the Canonical Prerequisites table and selected domain in
  `docs/capability-map.md`,
- the target repo's Current Harness Profile in `docs/harness/README.md`, or
  establish that it has `No installed Harness Profile`, and
- the current or latest fit proposal only when it contains unresolved facts
  relevant to the selected change.

After the dependency check establishes that the change is eligible, read only:

- the selected capability checklist under `docs/install/`,
- the selected capability manifest, and
- current-change sources explicitly routed by that checklist, manifest, or
  human-approved scope.

Do not recursively open dependency manifests or checklists. The Capability Map
owns prerequisite semantics, manifests project direct prerequisites into
executable data, and the Current Harness Profile records whether those
prerequisites are realized and validated in this repo.

Do not load sibling capability manifests, optional-asset manifests, adapter
docs, future-facing TODOs, or exploratory Multi-Work Coordination guidance
unless the current checklist or human-approved scope explicitly requires a
bounded entry from one of them.

If a human selects a capability with no checklist or manifest, report the
missing installer source and stop that change. Do not infer an install path
from conceptual or future-facing docs.

## Dependency Check

Resolve the selected capability's complete prerequisite closure from the
Capability Map before inspecting its realization details.

For an addition or realization change:

1. Compare the closure with the Current Harness Profile.
2. If every prerequisite is current, continue with only the selected change.
3. If any prerequisite is absent, pause the selected change without drafting
   or approving its realization.
4. Offer one missing prerequisite as a separate current Profile Change.
5. Install, validate, update the profile, hand off, and stop before the human
   decides whether to return to the original capability.

Do not bundle prerequisite files or behavior into a dependent proposal. A
proposal may record why it paused, but it does not pre-authorize later work.

For a removal:

1. Resolve every current profile capability that directly or transitively
   depends on the selected capability.
2. Reject the removal while any such dependent remains current.
3. Offer a dependent's removal or realization change only as a separate
   Profile Change chosen by the human.
4. Recompute closure before approving the original removal.

Removing Bounded Work is eligible only when no dependent capability remains;
the resulting state is `No installed Harness Profile`.

## Source Routing

- Capability outcomes and prerequisites: `docs/capability-map.md`.
- Canonical installable boundaries and direct dependency projections:
  `manifests/`.
- Installation procedure, checkpoints, and handoff: this file and the selected
  checklist under `docs/install/`.
- Current repo-specific capability state: the Current Harness Profile in
  `docs/harness/README.md`.
- Proposed intent and exact edit authority: one Harness Fit Proposal, using
  `templates/profile/docs/harness/fit-proposal.md` as the portable contract.
- Portable adaptation rules: `docs/portable-assets.md`, only when the selected
  change needs its adaptation seam clarified.
- Platform support: `docs/platform-support.md`, then only the relevant platform
  note when the approved change includes that adapter.

Existing repo mechanisms may realize selected outcomes. Describe what is
retained, adapted, added, or removed; do not label the installation with a
mode or claim universal asset, behavioral, domain, or capability completeness.

## Fit Proposal

Inspect only enough target-repo context to fit the selected capability and
exact scope. Infer low-risk defaults from repo evidence and ask only questions
that materially affect the change.

Before editing target-repo files:

1. Write and persist the proposal outside the target-repo edit scope, usually
   under `/tmp` unless the human chose another planning location.
2. Present the exact proposal text to the human.
3. Wait for explicit approval or corrections.
4. Edit only the approved files and behavior.

Use `templates/profile/docs/harness/fit-proposal.md` as the required-field
owner. Complete every applicable section and mark irrelevant sections not
applicable; do not maintain a second proposal schema in installer guidance.

Out-of-scope observations remain plain observations. Do not classify them as a
future Profile Change, preselect another capability or asset, load its
implementation sources, or ask for approval to edit it.

## Entrypoint Compatibility Audit

When adding or changing Bounded Work or Focused Context, inspect every existing
always-loaded agent instruction surface in the selected repo scope. Confirm
that it does not silently broaden delegated authority, make broad project docs
default reads, duplicate the current work source, bypass focused routing, or
contradict the proposed entrypoint.

Record each conflicting surface and the approved handling in the fit proposal.
Do not rewrite unrelated entrypoints or platform files without including them
in the exact approved file scope. If an unapproved conflict would prevent the
selected outcome, validation is incomplete and the Current Harness Profile
must remain unchanged.

## Human Checkpoints

Pre-edit approval:

- The exact proposal is persisted and presented.
- The dependency check passed for this one change.
- The human approves or corrects its files, behavior, validation, limits, and
  deferrals.
- Scope changes after approval require a revised proposal and renewed approval.

Post-change decision:

- The installer reports realized files and behavior, deviations, mechanical
  verification, representative capability-outcome evidence, Known Limits,
  deferrals, context used, and plain out-of-scope observations.
- The Current Harness Profile is updated only when validation supports the
  selected claim or resulting removal state.
- The installer leaves a durable installation record or handoff and recommends
  stopping.
- The human later decides whether to select another Profile Change.

## Validation, Profile Update, And Handoff

Validate the selected outcome, not merely the presence of files. Use the
selected checklist's gate and representative evidence. Mechanical checks can
support the result but cannot by themselves prove a capability claim.

On passed validation:

1. Update only the affected claim in the Current Harness Profile.
2. Record selected scope, current realizations, evidence, Known Limits, and
   revisit or removal signals.
3. Confirm the resulting profile is dependency-closed.
4. Leave a durable installation and validation record or handoff.

On failed or incomplete validation, leave the Current Harness Profile
unchanged. Preserve the result, evidence, and next decision in the proposal or
handoff. A Known Limit may narrow a demonstrated claim; it cannot replace
evidence for one.

Canonical handoff fields:

- Profile Change and change type,
- proposal and approval record,
- files and behavior actually changed,
- deviations and human decisions,
- mechanical verification,
- capability-outcome evidence and validation result,
- Current Harness Profile decision and dependency-closure result,
- selected scope, realizations, Known Limits, and revisit or removal signals,
- deferrals,
- context used,
- out-of-scope observations, and
- recommended next action: stop by default, revise the current change, or wait
  for the human to select another change.

For large target repos, use the Profile Change boundary as a natural context
split. A fresh agent should be able to continue from the Current Harness
Profile, proposal, and handoff without relying on chat history.

## Implemented Capability Checklists

- Bounded Work: `docs/install/bounded-work.md`
- Focused Context: `docs/install/focused-context.md`
- Agent Action Boundaries: `docs/install/agent-action-boundaries.md`
- Maintainability Feedback: `docs/install/maintainability-feedback.md`

Multi-Work Coordination is emerging and has no installable package or
checklist. Do not inspect or install it through this workflow.
