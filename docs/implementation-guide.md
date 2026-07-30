# Agent Harness Implementation Reference

Audience: agents and maintainers needing broad orientation while fitting this
framework to a target repo.

Use when: a cross-cutting implementation question remains after reading
`docs/installer.md` and the selected capability's source-of-truth files. This
is a map, not an installation checklist or a second procedure.

## Rule

Harness implementation is repo diagnosis plus collaborative workflow design,
not blind template installation.

Fit one dependency-valid Profile Change at a time. Select the smallest scope
that improves current human-agent work, validate its outcome, update the Current
Harness Profile only when evidence supports the claim, leave a durable handoff,
and stop.

## Source Of Truth Map

When sources conflict, update or trust the owner below rather than copying its
contract here.

- Maintenance decision lens: `docs/principles.md`
- Capability outcomes, boundaries, selection guidance, validation guidance,
  and prerequisites: `docs/capability-map.md`
- Framework concepts and rationale: `docs/framework.md`
- Profile Change workflow, human checkpoints, profile update, handoff, and
  sequencing: `docs/installer.md`
- Capability-specific procedure and gate: the selected checklist under
  `docs/install/`
- Canonical installable boundary: the selected capability manifest under
  `manifests/`
- Current target-repo state: `docs/harness/README.md`, created from
  `templates/profile/docs/harness/README.md`
- Proposal and installation record contract:
  `templates/profile/docs/harness/fit-proposal.md`
- Portable asset and adapter boundaries: `docs/portable-assets.md`
- Platform support: `docs/platform-support.md`, then only the relevant routed
  platform note
- Broad hook adapter design: `docs/hook-pattern.md`, only when the approved
  scope extends beyond Bounded Work Stop automation
- Work brief storage, fallback, sync, and progress guidance:
  `skills/core/harness-work-brief/`
- Implementation and review guidance: `skills/core/harness-implement/` and
  `skills/core/harness-review/`
- Focused Context routing templates: `templates/focused-context/`
- Maintainability Feedback policy and coordinator:
  `templates/maintainability-feedback/docs/harness/maintainability.md` and
  `skills/core/harness-maintainability/`
- Optional installable assets and adapters: `manifests/optional-assets.yml`

Do not maintain second copies of schemas, file lists, proposal fields,
checklists, commands, gates, or report formats in this reference.

## Implementation Routing

Use this sequence:

```text
principles -> Capability Map and Current Harness Profile -> installer
  -> one selected capability checklist and manifest
  -> manifest-named templates, skills, and narrow routed references
```

If no Current Harness Profile exists, Bounded Work is the only eligible first
addition. For any other addition, inspect the Capability Map's prerequisite
closure before reading realization sources. An absent prerequisite pauses the
selected change and requires its own separately approved Profile Change.

Read only sources needed for the current selection and exact proposed scope.
Record signals outside that scope as plain observations without preselecting
another capability or granting authority to edit it.

## Decision Lens

### Start Small

A small realization that is used is more valuable than broad harness machinery
that becomes ignored process. Select an exact outcome and scope from current
evidence or a credible anticipated need; do not install sibling capabilities
or every mechanism in a manifest merely because they exist.

### Surface Gaps Without Owning Every Gap

Installation may reveal missing tests, unclear CI, stale commands, no tracker
convention, weak secret handling, or scattered project docs. Surface those gaps
in the proposal or handoff, but do not turn a Profile Change into broad repo
modernization unless the human separately approves that work.

### Argue For Complexity

For each selected component, state the concrete failure, coordination cost, or
anticipated need it addresses; its beneficiary and expected value; its
maintenance or friction cost; Known Limits; and the signal that would justify
removing or simplifying it.

### Preserve Ownership

Keep universal operating guidance in the repo entrypoint, deterministic checks
in `scripts/repo-checks.sh`, phase-specific workflow in harness skills and
work-brief guidance, durable current state in the Current Harness Profile, and
tool-specific behavior in thin adapters.

## Common Routing Questions

Where do proposal fields and authorization come from?

Use `templates/profile/docs/harness/fit-proposal.md` together with the selected
checklist. The persisted, human-approved proposal authorizes only its named
files and behavior.

Where do acceptance and profile-update decisions come from?

Use the selected checklist's capability gate and `docs/installer.md`. Validate
the selected outcome, not merely file presence. Failed or incomplete validation
leaves the Current Harness Profile unchanged.

Where do lint, type-check, and test commands come from?

Use `docs/install/bounded-work.md` for discovery expectations and adapt
`templates/core/scripts/repo-checks.sh`. Keep actual commands in the target
repo's `scripts/repo-checks.sh`, not in descriptive docs.

Where does work-brief storage and progress guidance live?

Use `skills/core/harness-work-brief/`. Record target-repo storage, fallback,
sync, and durability decisions in the current proposal and harness docs.

Where do hook decisions live?

Bounded Work owns its selected narrow `repo-checks-on-stop` realization.
Secret guards, destructive-action controls, protected paths, or CI and
pre-commit parity belong to a separately approved Agent Action Boundaries
change unless they are merely thin adapters for already selected behavior.

Where do maintainability decisions and run records live?

Use `docs/install/maintainability-feedback.md` for selection and gate
requirements and `manifests/maintainability-feedback.yml` for the family and
asset boundary. Record selected mechanisms in the installed maintainability
policy and each run on its approved durable work surface. Do not create a
second debt backlog.

Where do final report and handoff fields come from?

Use `docs/installer.md` plus the selected capability checklist. Durable current
state belongs in `docs/harness/README.md`; the proposal and handoff preserve
change history without becoming competing profiles.

## Wording Check

Before finishing installed docs, verify that wording does not:

- imply a universal ranking, score, or exhausted capability domain,
- claim a selected capability outside its realized and validated scope,
- treat a Known Limit or approved proposal as validation evidence,
- imply agents should access, print, inspect, or directly handle sensitive
  values instead of validating secrets-management wiring,
- record machine-local framework or temporary proposal paths in durable docs,
- blur required behavior with optional or out-of-scope guidance,
- turn `AGENTS.md` into a product strategy document, historical note, or
  phase-specific procedure, or
- tell ordinary implementers to read `docs/harness/` when they need only the
  work brief, project docs, and code.

The goal is the smallest dependency-valid Harness Profile that improves current
human-agent work, with evidence and limits clear enough for a later operator to
change it deliberately.
