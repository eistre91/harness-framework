# Harness Docs

Audience: agents and maintainers intentionally inspecting, auditing,
maintaining, or extending this repo's agent harness.

Use when: maintaining harness files, changing agent workflow, auditing harness
behavior, or understanding why these harness files exist.

Normal product work should start from `AGENTS.md`, the current Agent Work
Brief, project docs, and local code. Do not read harness docs for ordinary
implementation or to learn how to use the harness unless the task is about the
harness itself.

## Current Harness Profile

This section is the durable owner of the repo's current Harness Profile. A fit
proposal, installation record, validation report, or handoff may explain a
change, but none of those records is a second statement of current profile
state.

List only capability claims whose selected scope is currently realized and
supported by validation evidence. A Known Limit may narrow a claim but cannot
replace evidence that the claimed outcome works. If validation is failed,
incomplete, or absent, leave the claim out and record the result in the
relevant proposal or handoff.

A nonempty profile must include Bounded Work and every prerequisite of every
other claimed capability. Check dependency closure against the Capability Map
identified by the current profile-contract provenance below. If this repo has
no realized and validated Bounded Work foundation, state
`No installed Harness Profile` and do not add another capability claim.

Profile last updated:
Dependency-closure evidence:

Copy the following subsection once for each current capability claim. Use the
Capability Map's domain name; do not add ranks, scores, or universal
completeness labels.

### <Capability domain>

- Selected scope:
- Current realizations:
- Validation evidence:
- Known limits:
- Revisit or removal signals:

## Profile Change Lifecycle

Future intent belongs in one Harness Fit Proposal for one Profile Change. An
approved proposal authorizes only its named files and behavior; approval does
not itself update the Current Harness Profile.

After implementation, validate the selected outcome. Update the profile only
when the realization and evidence support the claim in its selected scope,
then leave a durable installation record or handoff. If validation fails or is
incomplete, keep the current profile unchanged and preserve the result in the
proposal, installation record, or handoff.

Treat each addition, removal, or realization change as a separate Profile
Change. Install an absent prerequisite through its own completed change before
returning to a dependent proposal. Do not remove a prerequisite while a
current capability depends on it.

Use the capability-based installer and checklist for each change. Recommend
stopping after its validation, profile decision, and handoff; another
capability requires a later human-selected Profile Change.

## Framework Provenance

Current profile contract source: harness-framework
Capability Map and profile contract version or commit: record the framework
commit/tag used to establish or last reconcile this profile, or `unknown`
Current source version unknown reason: required only when current version is
`unknown`

Use portable source names in committed docs. Do not record machine-local paths
or temporary proposal paths in durable harness docs.

For significant harness changes, consult the source framework docs or run a
fresh fit pass with the installer before adding process.

## Related Change Records

Current or latest Harness Fit Proposal:
Installation and validation record or handoff:
Earlier durable harness records:

These records preserve decisions and events; they do not override the Current
Harness Profile.

## Maintenance Rules

- Add the smallest component that addresses a repeated failure, credible
  anticipated need, or coordination cost.
- Record why a new harness component exists and when it should be simplified
  or removed.
- Keep universal operating guidance in `AGENTS.md`, deterministic checks in
  `scripts/repo-checks.sh`, and phase-specific behavior in work-brief bundles
  and shared skills. Keep tool-specific adapters thin.
- Prefer executable checks and concrete acceptance evidence over prose.
- For secrets management changes, verify declarations, aliases, permissions,
  redaction, and runtime wiring without printing, revealing, inspecting, or
  directly handling secret values.
- If project docs are added later, give active docs a short audience and use
  trigger so future agents can tell quickly whether they are reading the right
  file.
