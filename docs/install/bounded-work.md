# Bounded Work Installer Checklist

Audience: agents and maintainers adding, removing, or changing the Bounded Work
realization in a target repo.

Use when: Bounded Work is the one human-selected Profile Change. Start from
`docs/installer.md` and complete its dependency check first.

## Read For This Change

Always read:

- `docs/principles.md`,
- `docs/installer.md`,
- the Bounded Work section and Canonical Prerequisites table in
  `docs/capability-map.md`,
- `manifests/bounded-work.yml`,
- the templates, skills, and companion files selected from that manifest,
- `templates/profile/docs/harness/fit-proposal.md`, and
- the target repo's Current Harness Profile and relevant current Bounded Work
  records, when they exist.

Read only when current scope requires it:

- `docs/portable-assets.md`, when adaptation seams are unclear,
- `docs/platform-support.md`, then only the relevant platform note, for each
  desired hook-capable runtime in the selected `repo-checks-on-stop` scope,
- `docs/hook-pattern.md`, only for custom hook adapter design beyond copying or
  adapting a standard Stop adapter, and
- the `claude-entrypoint` entry in `manifests/optional-assets.yml`, followed by
  `templates/core/CLAUDE.md`, when a minimal Claude Code pointer is selected.

Do not read sibling capability checklists or manifests, the full optional-asset
manifest, unrelated platform docs, future-facing orchestration sources, or
`TODO.md`. Record any exceptional source and why it was needed in the proposal
and handoff.

## Scope

Bounded Work lets the human-agent system shape intent into one coherent work
unit, execute and validate it within delegated authority, and reach a
reviewable completion decision. Use `manifests/bounded-work.yml` as the
canonical asset and behavior boundary; do not maintain a second file list here.

A typical realization provides:

- a concise repo agent entrypoint,
- an actionable deterministic repo-checks command,
- work-brief creation guidance for scope, non-goals, ambiguity, interfaces,
  decisions, acceptance evidence, and divergence,
- focused implementation and review guidance,
- a durable Current Harness Profile and change record, and
- stop automation for desired hook-capable runtimes in selected scope.

Existing mechanisms may satisfy some or all selected behavior. Record how they
are retained or adapted. Do not install every optional skill, platform adapter,
project-context surface, or action boundary merely because it is available.

## Repo Checks And Stop Automation

Install or adapt `scripts/repo-checks.sh`. Derive its actionable commands from
repo evidence. The expected default set is tests, lint, and type checks when
those commands exist and are reasonably actionable. For each missing, unclear,
too slow, flaky, or inappropriate member, propose an omission with a reason, a
human-approved addition or adaptation, or an explicit waiver.

Keep output quiet on success and actionable on failure. Do not invent a broad
verification stack merely to fill a gap. A placeholder script can be an honest
Known Limit, but it does not demonstrate that deterministic verification works
for ordinary selected work.

For each desired hook-capable agent runtime in scope, install, adapt, or record
an existing narrow Stop hook or equivalent automation that runs only
`scripts/repo-checks.sh` from the target repo root. Prefer the shared runner in
`adapters/common-hooks` and the relevant thin platform adapter. If no supported
desired runtime exists, record that limitation and narrow the selected claim;
do not silently imply stop automation works.

Broad hook policy, secret guards, destructive-action controls, generated-file
gates, and CI or pre-commit parity are not part of this change unless the
Capability Map places the behavior in Bounded Work and the current manifest
selects it. Potential Agent Action Boundaries remain out-of-scope observations.

## Entrypoint Compatibility Audit

Inspect every always-loaded agent instruction surface in selected repo scope,
including root and nested agent files and tool-specific pointer files. Confirm
that the resulting entrypoint:

- names the current work source, brief location, verification command, and
  phase-specific skills,
- does not silently broaden delegated outcome or file authority,
- does not require broad project or harness docs for ordinary work,
- does not present stale or conflicting work and completion rules, and
- keeps tool-specific files thin when shared guidance is practical.

Record each relevant existing surface and its approved handling in the fit
proposal. An unresolved contradiction that prevents representative work from
following the selected lifecycle leaves validation incomplete.

## Proposal

Use the Harness Fit Proposal contract and include only this one Bounded Work
change. In addition to the common fields in `docs/installer.md`, make these
decisions explicit:

- current Bounded Work claim or `No installed Harness Profile`,
- source framework provenance,
- exact selected outcome and Known Limits,
- work source and Agent Work Brief location,
- local fallback location, commit policy, and stale-brief mitigation,
- work-brief behavior for tiers, scope, non-goals, ambiguity, decisions,
  interfaces, acceptance evidence, status, and divergence,
- acceptance evidence for interface-changing or externally visible work,
- test, lint, and type-check commands plus omissions, additions, or waivers,
- selected `repo-checks-on-stop` runtimes, files, commands, validation, and
  unsupported-runtime limits,
- existing entrypoint, skill, command, and harness-component handling,
- entrypoint compatibility audit findings,
- optional platform pointer decision when relevant,
- exact files and behavior authorized,
- representative work validation plan, and
- deferrals, human decisions, and context used.

Persist and present the exact proposal, then wait for human approval before
editing target-repo files. Approval covers only its named files, behavior,
validation, limits, and deferrals.

For a realization change, inspect only the affected selected scope and preserve
unrelated current realizations. For removal, first confirm that no current
profile capability depends on Bounded Work. Removal must validate the resulting
state and update the profile to `No installed Harness Profile`; it does not
authorize deleting unrelated repo-owned mechanisms.

## Capability Gate

Validation passes only when representative evidence supports the selected
Bounded Work outcome. Check:

- The installed entrypoint is concise and tells a fresh agent where work comes
  from, where briefs live, how to verify, which phase-specific guidance exists,
  where project context starts if any, and where harness maintenance records
  live.
- The entrypoint compatibility audit found no unresolved always-loaded
  instruction that undermines the selected work lifecycle or authority.
- `scripts/repo-checks.sh` exists and its demonstrated commands and omissions
  match the proposal.
- Selected test, lint, and type-check behavior is actionable, or each uncovered
  case is an explicit Known Limit with a human decision.
- Work-brief, implementation, and review guidance is discoverable and loaded
  by purpose rather than as one broad reading list.
- Standard or complex work has a durable place for scope, non-goals,
  ambiguities, decisions, interfaces, verification, acceptance evidence,
  status, divergence, blockers, and next action.
- Interface-changing or externally visible work requires acceptance evidence
  in addition to mechanical verification.
- Each desired hook-capable runtime in selected scope has demonstrated Stop
  automation, an approved existing equivalent, or an explicit unsupported
  Known Limit.
- Any local fallback brief directory introduced by the change is gitignored.
- A representative fresh-agent walkthrough can recover intent and boundaries,
  use the relevant guidance, run verification, and produce a reviewable
  completion decision without hidden chat history.
- The resulting Current Harness Profile claim can name selected scope,
  realizations, evidence, Known Limits, and revisit or removal signals without
  relying on an installation label or universal completion claim.
- The report lists context used and confirms sibling capability sources were
  not loaded unless explicitly justified.

If no representative work item exists, an installed-surface walkthrough may
provide limited evidence, but record the unexercised behavior as a Known Limit.
Missing verification commands, placeholder checks, unclear trackers, or absent
project docs are not hidden by a label; validation passes only for the narrower
scope actually demonstrated.

## Profile Update And Handoff

On passed validation, add or update the Bounded Work claim in
`docs/harness/README.md`, confirm dependency closure, and complete the durable
proposal or handoff. On failed or incomplete validation, leave the Current
Harness Profile unchanged.

In addition to the canonical handoff fields in `docs/installer.md`, record:

- source framework version or commit, or `unknown` with a reason,
- repo-checks command, result, selected test/lint/type-check commands, and
  omissions or waivers,
- Stop adapter paths, commands, and results for each selected runtime,
- work-brief lifecycle and progress/divergence location,
- representative communication evidence,
- entrypoint compatibility audit result,
- Known Limits that narrow the claim, and
- recommended next action: stop by default or revise this Bounded Work change.

Do not inspect another capability after this handoff. The human may select a
new Profile Change in a later work unit.
