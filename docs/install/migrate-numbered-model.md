# Existing Numbered-Model Migration

Audience: agents and maintainers re-profiling a target repo that was installed
under the retired numbered harness model.

Use when: the target repo has durable numbered-stage records or installed
harness behavior from that model but does not yet have a Current Harness
Profile. Start from `docs/installer.md`, then use this guide instead of a
capability installation checklist.

## Outcome

Establish one dependency-closed Current Harness Profile from the target repo's
currently installed behavior and evidence, with human approval before any
current-state harness documentation is replaced.

This is a bounded documentation migration. It does not install, remove, or
change a realization; convert a historical label into evidence; or authorize a
later Profile Change. Stop after the migration record, profile decision, and
handoff.

## Read Scope

Read:

- `docs/principles.md`,
- `docs/installer.md`,
- the Canonical Prerequisites table and candidate domains in
  `docs/capability-map.md`,
- this guide,
- the target repo's installed harness surfaces,
- its durable numbered-stage proposals, handoffs, validation records, and
  original framework provenance, and
- `docs/maturity-model.md` only to interpret a historical label or record whose
  meaning is otherwise unclear.

Do not read current capability manifests or installation checklists merely to
compare package contents. Migration evaluates outcomes already realized in the
target repo; it does not certify asset parity with the current framework.
Inspect a current source only when it is necessary to interpret current
Capability Map semantics or evidence and record why it was needed.

Treat historical handoffs as leads and provenance, not proof of current
behavior. Inspect the actual installed surfaces and check whether cited
commands, routes, controls, sensors, and records still exist and behave as
described. Do not trust a level number, installation mode, or historical asset
or behavioral completeness statement as a current capability claim.

## Establish The Migration Boundary

Before detailed inspection, confirm with the human that the current work is
limited to re-profiling and documentation replacement. Record:

- the current-state harness document to establish or replace,
- the historical records that must remain truthful and recoverable,
- the allowed inspection and representative validation scope,
- the intended durable migration record or handoff location, and
- any actions that require separate operator approval because they have cost,
  side effects, or access beyond ordinary read-only inspection.

Do not repair gaps, update installed mechanisms, add missing assets, or run a
state-changing validation as part of this migration. Record those needs as
plain gaps. A human may later select one as a separate Profile Change.

## Inventory Installed State And Evidence

Inventory mechanisms before proposing claims. For each installed surface,
record its path or location, observed purpose and effect, the historical record
that describes it when one exists, current mechanical evidence, representative
outcome evidence, and any drift or uncertainty.

Use the historical labels only as investigation routes:

| Historical route | Candidate treatment | Required migration judgment |
| --- | --- | --- |
| Level 0 | No installed Harness Profile | It supplies no capability claim. |
| Level 1 | Bounded Work | Claim only the currently demonstrated foundation, not the historical level. |
| Level 2 | Focused Context | Claim only current, purpose-specific context routing; evaluate Bounded Work independently. |
| Level 3 | Agent Action Boundaries | Preserve and evaluate each selected control, its lifecycle effect, friction, evidence, and limits; do not infer Focused Context. |
| Level 4 | Maintainability Feedback | Preserve and evaluate each selected sensor, observation scope, run evidence, operator disposition path, cost or noise, and limits; do not infer either sibling branch. |
| Level 5 material | No direct migration claim | Treat it as historical or future-facing. Single-work continuity may support Bounded Work evidence; do not infer Multi-Work Coordination or an installable package. |

The numbered model's old cumulative wording does not override these judgments.
No optional capability is required merely because the repo once recorded a
higher number.

## Evaluate Candidate Claims

Build a migration evidence table before drafting the profile:

| Candidate capability | Selected scope | Current realizations | Current outcome evidence | Known limits or gaps | Profile result |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  | include / narrow / omit |

For each candidate, apply the Capability Map's outcome, boundary, and
validation guidance to a representative current use:

1. Confirm that the realization still exists and its observed effect belongs
   to the candidate domain.
2. Prefer current executable or behavioral evidence. A still-relevant
   historical validation record may support the investigation, but its label
   does not substitute for checking current behavior.
3. Include the claim only when the outcome is demonstrated in an explicit
   selected scope.
4. Narrow the selected scope and state Known Limits when the demonstrated
   outcome remains useful but bounded.
5. Omit the claim when evidence is absent, stale, failed, or insufficient to
   demonstrate the outcome. Record why in the migration record rather than
   translating the old completeness statement.

Preserve exact control and sensor scope. Do not turn selected controls into a
claim about all agent actions, or selected sensors into a claim about overall
system health. Preserve known bypasses, unsupported lifecycle points, noise,
false positives, operator costs, and other material limits even when the old
record called its selected scope complete.

## Enforce Dependency Closure

Every nonempty proposed profile must contain demonstrated Bounded Work. If the
foundation is not supported, propose `No installed Harness Profile`; record
evidence for other installed mechanisms only as migration findings, not current
capability claims.

For every included optional capability, verify the complete prerequisite
closure against the Capability Map. Omit a claim whose prerequisite is absent.
Do not install or assume the prerequisite during migration, and do not add an
unneeded sibling capability to make the historical sequence look cumulative.

## Human Checkpoint Before Documentation Edits

Persist the migration proposal outside the target-repo edit scope, normally
under `/tmp` unless the human chooses another planning location. Present its
exact text and wait for explicit approval before editing target-repo harness
documentation.

The proposal must state:

- the exact proposed Current Harness Profile text, including selected scope,
  realizations, evidence, Known Limits, and revisit or removal signals;
- the dependency-closure result;
- the inventory and evidence table, including omitted candidates and honest
  gaps;
- the exact documentation files to create, edit, retain, or move;
- how every historical numbered record will remain truthful, labeled as
  historical, and recoverable;
- mechanical and representative outcome validation already performed;
- inspection or validation limits;
- the durable migration record or handoff location;
- the current Capability Map and profile-contract source version, kept distinct
  from the original installation provenance; and
- confirmation that no harness behavior or capability realization will change.

Approval authorizes only those documentation edits. New evidence, a changed
claim, a new file operation, or a proposed harness repair requires a revised
proposal and renewed approval.

## Establish The Current Profile

After approval, use `templates/profile/docs/harness/README.md` as the shape for
the target repo's sole current-state owner at `docs/harness/README.md`. Copy
only approved claims from the evidence table. Record the current framework
version used for the Capability Map and profile contract separately from the
original installation framework version. Use `unknown` with a reason when
either version cannot be recovered; an old installation version does not
identify the current Capability Map used for dependency closure.

Do not rewrite an old stage proposal, handoff, validation result, installation
mode, or completeness statement as though it were authored under the
Capability Map. Leave a separate historical record unchanged apart from an
explicit historical label or link approved in the proposal. If the old record
occupies `docs/harness/README.md`, retain it in a clearly historical section or
move it to an approved historical path without changing what it originally
claimed.

Link the migration record and retained historical records from Related Change
Records. They explain provenance and decisions but do not become competing
current profiles.

## Verify And Hand Off

After the approved documentation edits:

1. Confirm that `docs/harness/README.md` is the sole Current Harness Profile.
2. Recheck every claim against the evidence table and every prerequisite
   against the Capability Map.
3. Confirm that omitted or narrowed claims, gaps, and Known Limits remain
   visible in the migration record.
4. Confirm that historical records remain recoverable and are not presented as
   current capability evidence.
5. Run the target repo's canonical mechanical checks when the approved edit
   scope and environment permit it; otherwise record the exact limitation.
6. Record the approved profile text, files changed, verification, evidence
   locations, closure result, preserved history, gaps, limits, and human
   decisions in the durable migration handoff.

Recommend stopping. The terminology migration neither proves that omitted
capabilities should be added nor authorizes work on recorded gaps. Any later
addition, removal, or realization change starts from `docs/installer.md` as a
separately selected and approved Profile Change.
