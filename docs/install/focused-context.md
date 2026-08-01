# Focused Context Installer Checklist

Audience: agents and maintainers adding, removing, or changing the Focused
Context realization in a target repo.

Use when: Focused Context is the one human-selected Profile Change and the
Current Harness Profile already contains validated Bounded Work. Start from
`docs/installer.md` and complete its dependency check first.

## Read For This Change

Always read:

- `docs/principles.md`,
- `docs/installer.md`,
- the Focused Context section and Canonical Prerequisites table in
  `docs/capability-map.md`,
- `manifests/focused-context.yml`,
- the target repo's Current Harness Profile and relevant Focused Context change
  records,
- the target repo's installed agent entrypoints and current work source,
- its existing project-context index if any, and
- only enough repo evidence to locate project-area docs, ADRs, decision logs,
  glossaries, and other routes relevant to the selected scope.

Read only when current scope requires it:

- the selected manifest sources under `templates/focused-context/`,
- the `project-intent` entry in `manifests/optional-assets.yml` and its source
  when repeated value or direction decisions justify it,
- `docs/portable-assets.md`, when adaptation seams are unclear.

Do not read sibling capability checklists or manifests, broad historical or
provenance docs, unrelated platform guidance, future-facing orchestration
sources, or `TODO.md`. Record any exceptional source and why it was needed in
the proposal and handoff.

## Scope

Focused Context lets the human-agent system recover and load context relevant
to the current purpose without relying on chat history, repeated rediscovery,
or broad irrelevant reading. Use `manifests/focused-context.yml` as the
canonical asset and behavior boundary; do not maintain a second file list here.

A typical selected realization routes work through:

```text
repo entrypoint -> Agent Work Brief -> SPEC-MAP.md -> project-area brief ->
trigger-matched deep references -> focused code and tests
```

Existing routers or area docs may satisfy this outcome. Keep the seam clear:

- `SPEC-MAP.md` or its approved equivalent routes current task intent; it is
  not a roadmap, broad encyclopedia, historical index, or work brief.
- Project-area briefs provide quick orientation and route to deep references
  only when a trigger matches.
- A glossary owns shared domain language when one exists; routers and briefs
  use that language without redefining it.
- ADRs, decision logs, plans, and historical records are not default reads
  unless current purpose routes to them.

Create or adapt only the routes and area briefs justified by selected scope.
Do not add documentation audits, broad link enforcement, action controls,
maintainability sensors, or a universal project-doc hierarchy through this
change.

## Entrypoint Compatibility Audit

Inspect every always-loaded agent instruction surface in selected repo scope.
Confirm that it points to one context-routing start without duplicating the
router, requiring broad project-doc reads, bypassing trigger-matched routes, or
contradicting the current work source and Bounded Work lifecycle.

Record each relevant surface and its approved handling in the fit proposal.
If an unapproved conflict would keep a fresh agent from loading the smallest
useful context, validation is incomplete and the Current Harness Profile must
remain unchanged.

## Proposal

Use the Harness Fit Proposal contract and include only this one Focused Context
change. Complete its applicable sections and make these capability-specific
decisions explicit:

- current Bounded Work prerequisite evidence and relevant Known Limits,
- observed routing failures or credible anticipated need that justify the
  selected scope,
- existing context docs, routers, ADRs, decision logs, glossaries, maps, and
  area docs to retain, adapt, supersede, leave alone, or defer,
- router installation or existing-router decision,
- project-area brief location and exact initial briefs or routes,
- optional project-intent or glossary decision when relevant,
- routing boundary and broad-doc exclusions,
- entrypoint compatibility audit findings,
- exact files and behavior authorized,
- representative routing validation plan,
- expected Known Limits and broken-route handling,
- revisit or removal signals, and
- deferrals, human decisions, and context used.

Persist and present the exact proposal, then wait for human approval before
editing target-repo files. Do not install sibling capability behavior merely
because discovery exposes it.

For a realization change, inspect only the affected routes and preserve
unrelated current scope. For removal, remove or change only the approved
realizations, validate the resulting entrypoint and Bounded Work behavior, and
remove the Focused Context profile claim only after that evidence passes.

## Capability Gate

Validation passes only when representative evidence supports the selected
Focused Context outcome. Check:

- The Current Harness Profile still contains validated Bounded Work.
- The target entrypoint names one context-routing start without becoming a
  broad project encyclopedia.
- The entrypoint compatibility audit found no unresolved always-loaded
  instruction that forces broad reading or bypasses selected routes.
- The installed router is adapted to target-repo task intents and states its
  own boundary, trigger-matched deep references, missing-route behavior, and
  update triggers.
- The area-brief guide or approved equivalent records the expected brief shape
  and scanability guidance.
- Each selected area brief names audience and triggers, what to read first,
  deep-reference triggers, important modules or surfaces, core invariants,
  common wrong turns, useful tests or searches, and update triggers.
- The router reaches every area brief in selected scope, and installed routes
  do not point to missing files.
- A representative current purpose reaches the first useful area brief and
  only the needed deep references.
- Historical and broad planning sources remain opt-in unless current purpose
  explicitly routes to them.
- Optional project intent, glossary, and existing context docs are included
  only with evidence and a maintenance owner.
- When a glossary exists, selected routes use its terms without duplicating
  definitions.
- Missing or stale routes found during validation are recorded as Known Limits
  or separately bounded follow-up; they are not silently ignored.
- No sibling capability behavior was installed through this change.
- The resulting Current Harness Profile claim can state selected scope,
  realizations, evidence, Known Limits, and revisit or removal signals.
- The report lists context used.

For representative routing evidence, record the chosen purpose, selected
area brief, deep references opened or skipped, and every missing or stale route.
If no representative task exists, record that validation was limited to an
installed-surface walkthrough and narrow the claim accordingly.

## Profile Update And Handoff

On passed validation, add, update, or remove only the Focused Context claim in
`docs/harness/README.md`, confirm dependency closure, and complete the durable
proposal or handoff. On failed or incomplete validation, leave the Current
Harness Profile unchanged.

In addition to the template's Installation And Validation Record, record:

- router installation or existing-router handling,
- selected area-brief location, briefs, and routes,
- project-intent, glossary, ADR, and decision-log decisions,
- representative routing evidence,
- entrypoint compatibility audit result,
- broken or missing routes and Known Limits, and
- recommended next action: stop by default or revise this Focused Context
  change.

Do not inspect another capability after this handoff. The human may select a
new Profile Change in a later work unit.
