# Capability Map Transition Plan

Audience: agents and maintainers replacing the implemented numbered maturity
model with the accepted Harness Capability Map.

Status: complete. The capability-based manifests, installer, Profile contracts,
documentation, existing-target migration path, validators, and tests have cut
over together. This plan remains as the completed migration record.

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

## How To Execute One Phase

Run each phase as a separate bounded work unit in a fresh primary-agent
context. Apply this loop to the current phase only; for the first run, "current
phase" means Phase 1. Do not begin the next phase in the same run.

1. Read `AGENTS.md`, `docs/principles.md`, `docs/capability-map.md`, the
   architectural decision, this plan, and the current phase's sources. Read
   earlier completion records for handoff evidence, but load later-phase
   sources only when the current phase explicitly requires them.
2. Confirm that every earlier phase is marked complete in the Phase Completion
   Ledger. If an earlier phase is incomplete or its evidence is insufficient
   for the current work, stop and report that dependency rather than silently
   repairing or combining phases.
3. Restate the current phase outcome, files or source owners likely to change,
   acceptance evidence, and explicit non-goals. Keep the work a semantic
   refactor and clarification. Do not introduce new framework behavior merely
   because the migration exposes an opportunity.
4. Implement only the current phase. Preserve one active installer taxonomy,
   the source-of-truth boundaries, and all Migration Invariants above.
5. Run focused verification while working and then run
   `./scripts/repo-checks.sh`. Gather concise evidence for the phase's
   mechanical and behavioral outcomes.
6. Draft the Phase Completion Ledger entry, but leave its status incomplete
   until independent review and finding resolution finish.
7. Spawn one fresh, non-forked `gpt-5.6-sol` subagent with high reasoning for a
   read-only completion review of the current phase. Give it a self-contained
   prompt containing:
   - the current phase number and full phase contract,
   - the target model, decision, Migration Invariants, and relevant earlier
     completion evidence,
   - the changed-file list and diff or equivalent exact work product,
   - verification results and drafted completion evidence,
   - instructions to inspect the repository directly, avoid edits, ignore
     style nits, and report only material incompleteness, semantic errors,
     source-of-truth conflicts, scope creep, or migration risks.
8. Resolve every material in-scope finding and rerun affected focused checks
   plus `./scripts/repo-checks.sh`. Do not implement reviewer suggestions that
   are stylistic, speculative, or unrelated to completing the current phase.
9. Ask the same reviewer to verify the resolutions. If a material finding needs
   a human decision, changes the accepted capability model, belongs to a later
   phase, or requires new framework behavior, leave the phase incomplete and
   request direction instead of broadening the work.
10. Mark the phase complete only after checks pass, the reviewer reports no
    unresolved material findings, and the ledger contains high-level completion
    evidence. Then stop. Do not start the next phase, commit, or push unless the
    human separately requests it.

High-level completion evidence should identify the source-of-truth contracts
changed, summarize mechanical and behavioral validation, state important
deferrals or limits, and record the independent-review verdict. It should not
duplicate complete diffs, file inventories, command logs, or implementation
details that future agents can inspect directly.

## Phase Completion Ledger

Update only the current phase's row. Use `complete` only after following the
full execution loop above. Use `incomplete` when work or material review
findings remain; put the blocker or next decision in the evidence cell.

| Phase | Status | High-level completion evidence | Independent completion review |
| --- | --- | --- | --- |
| 1. Manifest Contract And Verification | complete | Capability-oriented definition, dependency, asset-support, and scope fields now form the only accepted manifest schema; definition and dependency metadata are an enforced pair. Validation reads the Capability Map's canonical prerequisite table, requires exact direct projections, and preserves graph, collision, path, and selection checks; focused tests and `./scripts/repo-checks.sh` pass. Numbered filenames and asset paths remain intentionally deferred to Phase 2. | Passed after finding resolution and re-verification; no unresolved material findings. |
| 2. Capability Manifests And Asset Paths | complete | The four implemented capability domains now own canonical manifests and capability-named template paths; direct dependency projections remain Bounded Work-only, selected control and sensor families remain independent, and optional assets and adapters declare single- or cross-domain support according to current purpose and effect. Bootstrap remains separate, Multi-Work Coordination has no package, moved-path consumers resolve, focused validation passes, and `./scripts/repo-checks.sh` passes. | Passed with no material findings; manifests, moved paths, classifications, dependencies, branch independence, bootstrap separation, and Multi-Work Coordination exclusion are coherent. |
| 3. Target-Repo Profile And Proposal Contract | complete | Target profile and fit-proposal contracts are staged under `templates/profile/` without changing the active numbered installer sources. The future `docs/harness/README.md` is the sole durable owner of a dependency-closed current Harness Profile; one-change proposals preserve realization detail, authorize exact scope, and gate profile updates on outcome validation while records and historical levels remain non-current evidence. Focused validators and `./scripts/repo-checks.sh` pass; activation remains deferred to Phase 4. | Passed after resolving the active-contract sequencing finding; the same reviewer confirmed the dormant target contracts are complete and safely bounded with no unresolved material findings. |
| 4. Capability-Based Installer | complete | The active installer surfaces now expose one Profile Change workflow through capability-named checklists, Capability Map prerequisite closure, capability manifests, and the target Profile contracts. Bounded Work-first installation, separate missing-prerequisite changes, dependent-first removal, exact approval scope, entrypoint compatibility audits, representative outcome validation, evidence-gated profile updates, and stop handoffs are explicit; active bootstrap, portability, platform, hook, and README routes no longer publish numbered stages, installation modes, or completeness claims. Unreconciled broad conceptual prose is isolated as non-authoritative pending Phase 5. Focused contract tests and `./scripts/repo-checks.sh` pass. | Passed after resolving active-taxonomy and retired-mode findings; the same reviewer confirmed no unresolved material findings. |
| 5. Conceptual And Downstream Reconciliation | complete | The Capability Map and framework now own active conceptual language; the broad implementation reference, repository routes, portability, hook, platform, adapter, target-policy, and coordinator guidance use capability and Profile contracts. The numbered model and orchestration sketch are explicitly historical, retired core profile paths point to the sole current templates, classified residual taxonomy hits are historical records, negative tests, course language, or explicit guardrails, and focused tests plus `./scripts/repo-checks.sh` pass. Existing-target migration guidance and final transition cleanup remain deferred to Phases 6 and 7. | Passed with no material Standards or Spec findings; the reviewer confirmed active ownership, routes, installed-output language, historical classification, and phase boundaries, and independently re-ran equivalent focused and full checks. |
| 6. Existing Target-Repo Migration Guidance | complete | Active README and installer entrypoints route existing numbered installations to a bounded documentation-only re-profiling guide. The guide evaluates installed mechanisms and current outcome evidence without translating historical labels or completeness claims, preserves exact control and sensor scope and Known Limits, enforces Bounded Work dependency closure, distinguishes the current Capability Map contract from original installation provenance, requires approval of the exact proposed profile and history handling before edits, and stops without installing or repairing capabilities. Focused contract tests and `./scripts/repo-checks.sh` pass; final transition cleanup remains deferred to Phase 7. | Passed after resolving active-entrypoint routing and profile-provenance findings; the same reviewer confirmed no unresolved material findings. |
| 7. Cutover And Cleanup | complete | Capability-map, installer, and decision records describe the cutover as complete; the originating TODO points to the accepted decision; resolved migration choices no longer remain listed as deferred; capability-owned paths are current; and legacy manifest fields remain rejected. Focused checks and `./scripts/repo-checks.sh` pass, including manifest projection, source/target resolution, installer behavior, migration, and final-state contract coverage. | Passed after resolving two stale pre-cutover statements; the same reviewer confirmed no unresolved material findings and independently reran the full checks. |

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
