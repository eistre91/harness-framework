# Harness Fit Proposal

This file proposes and records one Profile Change against the current Harness
Profile. It is durable repo documentation when the repo chooses this separate
record instead of embedding the final decision in another durable harness
document. Do not record machine-local paths or temporary installation-session
proposal paths here.

Keep exactly one addition, removal, or realization change in this proposal.
The exact approved proposal authorizes only the files and behavior named here.
Approval records future intent; it does not prove realization and does not
update the Current Harness Profile.

After implementation, complete the installation and validation record below.
Update the profile only when validation demonstrates the selected outcome in
the approved scope. On failed or incomplete validation, leave the profile
unchanged and preserve the result here or in the linked handoff. Preserve
historical level records as historical; do not rewrite them as capability
evidence.

## Proposal Identity

- Profile Change:
- Change type: add capability / remove capability / change realization
- Capability domain:
- Current Harness Profile owner: `docs/harness/README.md`
- Proposal status: draft / awaiting approval / approved / implemented /
  validation passed / closed without profile update
- Durable record path:

## Why Now

- Observed signal or credible anticipated need:
- Human or agent beneficiary:
- Expected outcome and value:
- Expected cost or friction:
- Revisit or removal signal:

## Current Profile And Dependency Check

Do not copy the full current profile here. Record only the facts needed to
evaluate this change and link to its durable owner.

- Current profile reviewed at:
- Relevant current capability claims:
- Capability Map source/version reviewed:
- Required capability domains:
- Dependency closure result:
- Current dependents, for a removal:

If an addition has an absent prerequisite, pause this proposal. Offer the
missing prerequisite as a separate Profile Change and do not include its files
or behavior here. Reject removal of a prerequisite while a current capability
depends on it.

## Selected Scope And Proposed Realization

- Selected outcome and scope:
- Proposed practices, assets, tools, and behavior:
- Existing mechanisms to retain or adapt:
- Explicitly excluded behavior:
- Expected Known Limits:
- Revisit or removal signals:

## Existing Harness Component Decisions

Record only components relevant to this Profile Change.

| Component | Appears to do | Handling | Reason and human decision |
| --- | --- | --- | --- |
|  |  | thread through / adapt / supersede / leave alone / defer |  |

## Skill And Command Conflict Decisions

Harness-provided skills use the `harness-` prefix by default so their
provenance is visible and they do not collide with generic platform or team
skills.

| Platform or path | Skill or command | Overlap | Decision |
| --- | --- | --- | --- |
|  |  | review / implement / work brief / diagnose-debug / run-checks / other |  |

For Claude Code, record whether bundled skills such as `/code-review`,
`/debug`, `/run`, and `/verify` remain enabled, are secondary to repo-specific
guidance, or are disabled by user or project settings. If native skill mirrors
are installed, record the mirror and shared-source paths, sync command, and
platform-owned frontmatter that must be preserved.

## Entrypoint Compatibility Audit

Required when adding or changing Bounded Work or Focused Context. Inspect every
always-loaded agent instruction surface in selected repo scope. Record `not
applicable` for other changes.

| Surface | Always-loaded effect | Conflict with selected outcome | Handling | Authorized file |
| --- | --- | --- | --- | --- |
|  |  | authority / work source / broad context / routing / none | retain / adapt / supersede / defer |  |

An unresolved unapproved conflict that prevents the selected outcome leaves
validation incomplete and the Current Harness Profile unchanged.

## Selected Manifest Scope

Use the current capability manifest as the canonical installable boundary.
Keep only rows relevant to this Profile Change; do not preselect assets or
behavior from another capability.

| Asset or behavior | Status | Reason | Revisit signal |
| --- | --- | --- | --- |
|  | include / adapt / already satisfied / defer / exclude |  |  |

## Capability-Specific Realization Details

Keep only the subsections relevant to this Profile Change. These details
refine the selected scope; they do not authorize another capability.

### Project Context And Intent

- Existing project context docs:
- Existing project intent source:
- `docs/project/intent.md` decision: include / adapt existing / defer / exclude
- Reason and revisit signal:
- Routing boundary:

### Work Brief Storage

- Canonical location:
- Local fallback when the canonical store is unavailable:
- Commit policy for brief instances:
- Sync rule back to the canonical location:
- Durability rationale:
- Stale brief mitigation when briefs are committed:

### Tests, Lint, And Type Checking

| Check | Existing command | Decision | Reason or future default |
| --- | --- | --- | --- |
| Tests |  | include / add / omit with reason / waiver |  |
| Lint |  | include / add / omit with reason / waiver |  |
| Type check |  | include / add / omit with reason / waiver |  |

### Bounded Work Stop Automation

- Desired hook-capable runtime or runtimes in scope:
- Decision: already satisfied / install / adapt / unsupported gap
- Adapter source and files to create or edit:
- Hook event and command:
- Repo-root handling:
- Output and blocking behavior:
- Validation command and result:
- Runtime Stop event tested or wrapper smoke-tested:
- Human decision or Known Limit:
- Revisit signal:

### Selected Agent Action Boundaries

Mode: observe / guide / block / verify.

| Boundary | Why now | Event | Mode | Mechanism | Files | Validation | Friction risk | Known limits | Revisit or removal signal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |

### Selected Maintainability Feedback

- Required policy or coordinator handling:
- Default durable run-record surface:

Add one short subsection per exact observation mechanism:

#### <Observation family: exact mechanism>

- Why now, beneficiary, and intended drift categories:
- Repo surface, observation scope, and observation window:
- Mechanism and evidence sources:
- Trigger or cadence:
- Operator or decision owner:
- Durable record destination:
- Expected runtime, cognitive cost, and noise:
- Known limits and false-positive risk:
- Supervised trial command or procedure:
- Revisit or removal signal:

## Authorized Files And Behavior

Anything not listed here remains out of scope for this proposal.

Create:

-

Edit:

-

Remove:

-

Behavior authorized:

-

## Validation Plan

Validation must demonstrate the selected capability outcome, not merely that
files exist. Include representative evidence where available and name any case
that cannot be exercised.

| Outcome or risk | Command or evidence | Expected result |
| --- | --- | --- |
|  |  |  |

## Acceptance Criteria

-

## Known Limits And Deferrals

Known limits narrow the proposed claim. Deferrals and failed validation do not
become profile claims.

| Limit or deferral | Effect on selected scope | Revisit signal |
| --- | --- | --- |
|  |  |  |

## Context Used

Framework sources:

-

Target repo sources:

-

Sources outside this change's scope and justification:

-

## Human Approval

- Exact proposal presented:
- Decision: approved / revise / rejected
- Approved by and date:
- Approved amendments, if any:

Do not edit target-repo files until the exact proposal is approved. If scope
changes after approval, revise and re-present the proposal before continuing.

## Installation And Validation Record

Complete this section after the approved work. It records what happened but is
not a second Current Harness Profile.

- Files and behavior actually changed:
- Deviations from the approved proposal and decisions:
- Mechanical verification:
- Capability-outcome evidence:
- Validation result: passed / failed / incomplete
- Known limits demonstrated by validation:
- Current Harness Profile decision: updated / unchanged
- Profile update and exact evidence location:
- Human decisions:
- Handoff or related record:
- Recommended next action:

Update the Current Harness Profile only after a passed result establishes the
claim in its selected scope. A removal updates the profile only after the
approved removal is realized, validation supports the resulting profile, and
dependency closure still holds.

## Out-Of-Scope Observations

Record plain observations without preselecting another capability or granting
authority to edit it.

-
