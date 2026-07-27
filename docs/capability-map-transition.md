# Capability Map Transition Plan

Audience: agents and maintainers replacing the implemented numbered maturity
model with the accepted Harness Capability Map.

Status: planned. No migration phase beyond recording the target model and this
plan has begun. `docs/maturity-model.md` and the numbered installation sources
remain active until cutover.

Decision: `docs/adr/0001-replace-maturity-levels-with-capability-map.md`

Target model: `docs/capability-map.md`

## Outcome

Replace the framework-wide numbered maturity taxonomy with one capability map,
dependency-aware manifests and installer workflow, and target-repo Harness
Profiles that state selected scope, realization, evidence, and known limits.

The migration is complete when framework maintainers and installing agents can
select and install Bounded Work plus any justified dependency-valid capability
combination without numeric-order exceptions or maturity/completeness claims.

## Value

Humans and agents will reason directly about the outcomes a repo needs. The
framework can remain opinionated about prerequisites, fit, and evidence without
implying that every repo should climb one universal ladder.

## Non-Goals

- Do not redesign the installable behavior inside every current package unless
  migration exposes a contradiction with the accepted domain boundary.
- Do not create an installable Multi-Work Coordination package during this
  migration. Any such package is separate post-migration work requiring its
  own evidence, decision, scope, and authorization.
- Do not introduce scores, universal capability maturity, domain completeness,
  or a second profile taxonomy.
- Do not automatically rewrite historical target-repo install records.
- Do not reconcile course material unless a migration inventory finds an
  actual course dependency; if it does, follow `docs/course-maintenance.md` as
  a separately bounded reconciliation.

## Migration Invariants

- Keep one active installer taxonomy. The numbered model remains active until
  the capability-based sources cut over together.
- Preserve staged installation discipline: inspect one approved current change,
  persist the proposal, obtain human approval, edit only approved scope,
  validate, hand off, and stop before inspecting another capability.
- Bounded Work is the required foundation for every currently identified
  optional capability.
- A current profile is dependency-closed; future schema must allow an
  implemented capability to project more than one prerequisite from the
  Capability Map.
- Capability nodes name human-agent outcomes. Mechanisms and assets may support
  more than one domain.
- The Capability Map owns domain semantics and prerequisite relationships.
  Manifests own canonical installable boundaries and project the map's
  prerequisites into executable data. Validation must reject disagreement.
  Installer guidance owns procedure, and the target Harness Profile owns
  repo-specific current state.
- Proposed selection does not prove realization. A capability enters the
  current profile only after realization and validation provide evidence for
  its selected scope. Known limits may narrow that claim but cannot replace its
  evidence.
- Missing prerequisites and removal of selected prerequisites are handled as
  separate Profile Changes. Do not bundle prerequisite installation into a
  dependent capability's approval or remove a prerequisite while a current
  capability depends on it.
- Preserve explicit operator judgment for greenfield anticipated needs as well
  as brownfield observed signals.
- Keep current historical labels truthful during migration; do not rewrite a
  past Level 4 record as though it certified Focused Context or Agent Action
  Boundaries.

## Current-To-Target Mapping

| Current source | Target capability treatment |
| --- | --- |
| Level 0 | No installed Harness Profile; not a capability node or install stage |
| Level 1 | Bounded Work foundation |
| Level 2 | Focused Context |
| Level 3 selected controls | Agent Action Boundaries |
| Level 4 selected sensors | Maintainability Feedback |
| Level 5 sketch | Split by outcome: single-work continuity remains a Bounded Work realization; multi-unit concerns inform emerging Multi-Work Coordination; other ideas remain uncommitted |

This mapping guides migration but does not authorize mechanical relabeling.
Each source must be checked against the target domain boundary.

## Phase 1: Manifest Contract And Verification

Change the manifest model and its tests before moving canonical assets:

1. Replace level-specific definition metadata with capability-domain definition
   references.
2. Replace the singular prerequisite assumption with a dependency list that can
   represent future converging graph paths.
3. Replace optional-asset maturity labels with a representation that permits an
   asset to support zero, one, or multiple capability domains without making
   the asset taxonomy the capability taxonomy.
4. Rename level-boundary exclusion language to capability-scope language.
5. Preserve cycle detection, prerequisite-closure collision detection, source
   and target validation, selection contracts, and portable-path checks.
6. Add tests for multiple prerequisites, dependency closure, cycles, shared
   cross-domain mechanisms, and generic definition references.
7. Remove fixed assumptions about `level-N.yml`, level anchors, allowed maturity
   values, and the production manifest count.
8. Treat the Capability Map's canonical prerequisite table as the semantic
   owner and validate that every implemented manifest projects it exactly.

Keep the merged repository on one accepted manifest contract. If temporary
compatibility code is useful on a migration branch, remove it before cutover
rather than publishing two active schemas.

## Phase 2: Capability Manifests And Asset Paths

Create or rename canonical manifests around the implemented capabilities:

- Bounded Work,
- Focused Context,
- Agent Action Boundaries,
- Maintainability Feedback.

Do not create a Multi-Work Coordination manifest during this migration. Keep it
as an emerging conceptual node. Any installable package is separately
authorized post-migration work.

For each implemented capability:

1. Reconcile every existing asset and behavior against the accepted outcome and
   boundary.
2. Preserve independently selected control and feedback families rather than
   turning their domain manifests into universal bundles.
3. Move level-named template directories to capability-owned paths and update
   source references atomically.
4. Classify adapters and optional assets by the outcomes they support; allow
   cross-domain support where purpose and effect require it.
5. Keep bootstrap assets separate from capability selection when they are
   installer infrastructure rather than an installed capability outcome.

## Phase 3: Target-Repo Profile And Proposal Contract

Revise target-repo harness records so they distinguish current state from
future intent:

- The current Harness Profile lists only realized and validated capability
  claims, with local scope, realizations, evidence, known limits, and revisit
  signals.
- A Harness Fit Proposal describes one proposed profile change and authorizes
  only its files and behavior.
- Installation and validation records preserve what happened without becoming
  a second current profile.
- Historical level records remain historical. Current state is re-profiled from
  installed mechanisms and demonstrated behavior.
- A failed or incomplete validation does not update the current profile. Record
  it in the proposal, installation record, or handoff instead.

Before installer implementation begins, define the profile/proposal lifecycle,
required fields, and one durable target-repo owner for the current Harness
Profile. The exact path may be chosen during this phase. Reuse the existing
`docs/harness/` surfaces when practical; do not require a new registry or
ledger merely to represent the profile.

## Phase 4: Capability-Based Installer

Replace numbered stages with profile changes while preserving the valuable
staging constraints:

1. Install and validate Bounded Work before any dependent capability.
2. Read the current Harness Profile and the Capability Map's prerequisite
   closure before proposing a capability change.
3. If a prerequisite is absent, pause the dependent proposal. Offer the missing
   prerequisite as a separate current Profile Change, then install, validate,
   update the profile, and hand off before the human decides whether to return
   to the dependent capability.
4. Reject removal of a prerequisite while a current profile capability depends
   on it. Remove or change dependents through separately approved Profile
   Changes first.
5. Inspect only the one human-selected capability and exact scope currently
   under consideration.
6. Write and persist a proposal containing why now, selected scope, realization,
   files, validation, known limits, cost or friction, and revisit or removal
   signals.
7. Require explicit pre-edit approval for only that proposal.
8. Validate the selected outcome with representative evidence, update the
   current Harness Profile, leave a durable handoff, and recommend stopping.
   Do not update the current profile when validation does not establish the
   capability claim.
9. Run an entrypoint compatibility audit as fit validation when existing
   always-loaded instructions may undermine Bounded Work or Focused Context.
10. Record out-of-scope observations without preselecting another capability or
    loading its implementation sources.

Replace canonical/starter/overlay and asset/behavioral completeness claims with
plain descriptions of selected scope, current realization, evidence, known
limits, and explicit deferrals. Retain an overlay concept only if it continues
to clarify that existing repo mechanisms realize the selected outcome; do not
retain installation modes merely for compatibility.

## Phase 5: Conceptual And Downstream Reconciliation

Update active references after the manifest and installer contracts are stable:

1. Make the capability map the active conceptual source and retire
   `docs/maturity-model.md` as an active taxonomy.
2. Reconcile `docs/framework.md`, `docs/installer.md`, the capability-specific
   checklists, and `docs/implementation-guide.md`.
3. Reconcile README and repository agent instructions.
4. Update portable-assets, hook, platform, and adapter guidance where it routes
   by level.
5. Update installed templates and skills that write level, maturity,
   completeness, stage, or future-level language into target repos.
6. Update source-of-truth maps and path references after file moves.
7. Search the repository for remaining active `Level N`, `level-N`, maturity,
   completeness, and numbered-stage language. Retain only intentional historical
   references that are explicitly labeled as historical.

Do not perform this as a broad search-and-replace. Classify every occurrence by
meaning: domain semantics, manifest ownership, installer procedure, target
profile state, historical record, or unrelated ordinary language.

## Phase 6: Existing Target-Repo Migration Guidance

Add a bounded migration path for repos installed under the numbered model:

1. Inspect the actual installed harness and durable level handoffs.
2. Map Level 1 behavior to Bounded Work when evidence supports the current
   foundation.
3. Select Focused Context, Agent Action Boundaries, and Maintainability Feedback
   only when their actual installed realizations and evidence support them.
4. Preserve selected control and sensor scope and known limits.
5. Record gaps honestly instead of translating partial or historical
   completeness labels.
6. Present the proposed current Harness Profile for human approval before
   replacing current target-repo harness documentation.

No target repo should be required to add an unneeded capability merely to
migrate its terminology.

## Phase 7: Cutover And Cleanup

Cut over only when the new manifests, installer, profile surfaces, docs,
validator, and tests agree:

1. Remove or retire numbered manifests, installer checklists, and level-owned
   template paths in the same bounded change that updates their consumers.
2. Remove manifest-schema compatibility for maturity and level metadata.
3. Mark the capability map active and this plan complete or superseded.
4. Update the originating TODO work record so it points to the completed
   decision rather than continuing to describe the change as deferred.
5. Run the repository's full mechanical checks and a fresh-agent documentation
   walkthrough.

## Acceptance Evidence

Mechanical:

- `./scripts/repo-checks.sh` passes.
- Manifest tests cover multiple prerequisites, cycles, dependency closure,
  cross-domain assets, and capability definition references.
- Repository search finds no unintended active numbered-level, maturity,
  completeness, or numbered-stage taxonomy references.
- Every manifest source and default target resolves after capability-owned path
  moves.

Behavioral:

- A fresh installer can fit Bounded Work and stop.
- A fresh installer can add any one implemented optional capability without
  reading or implying installation of its sibling capabilities.
- A proposed downstream capability automatically brings its prerequisite
  closure into view without granting approval to edit those prerequisites;
  each absent prerequisite requires its own completed Profile Change.
- An installer rejects removal of a prerequisite until its current dependents
  have been removed or changed through separate approved Profile Changes.
- A target repo can express its current Harness Profile without a number,
  maturity score, or universal completeness claim.
- The current Harness Profile contains no capability whose selected scope lacks
  realization and validation evidence.
- Greenfield anticipated need and brownfield observed evidence can both justify
  selection while preserving value, cost, validation, and revisit reasoning.
- Existing target repos can migrate without rewriting historical records or
  claiming capabilities they never installed.

## Remaining Implementation Decisions

These decisions are intentionally deferred to the bounded migration work that
has the relevant files and tests in context:

- final capability manifest filenames and metadata field names,
- the durable target-repo file that owns the current Harness Profile,
- the smallest useful representation for assets supporting multiple domains,
- whether any installation-mode language remains valuable after completeness
  is removed,
- the final public label for Multi-Work Coordination if implementation evidence
  reveals a clearer outcome name.
