# Portable Harness Assets

Audience: agents and maintainers selecting framework assets for a target repo.

Use when: distinguishing bootstrap docs, installable assets, optional pull-ins,
adapters, and repo-specific adaptations.

This repo separates portable harness assets from repo-specific adaptations.

## Rule

Concepts, templates, and skill bundles transfer. Final file contents, commands,
paths, tracker locations, and adapters are fitted to the target repo.

Adapters should preserve shared behavior across tools. Put common policy in
portable assets, then make tool-specific adapters call or point to those
assets.

## Asset Types

Manifests own the canonical asset inventory. Use these asset type definitions
when reading or editing manifests:

- `bootstrap`: temporary framework material used while fitting a harness to a
  target repo. Bootstrap assets usually should not remain installed after the
  harness is fitted.
- `installable`: a file or file bundle that can be copied or adapted into a
  target repo when the current Profile Change or optional pull-in justifies it.
- `behavior`: a required or optional harness capability that may be satisfied
  by existing repo conventions, adapted files, scripts, hooks, or documented
  workflow instead of a single copied file.
- `optional-reference`: optional reference material that supports a capability
  realization when
  evidence justifies the extra context, but is not part of the required
  selected manifest boundary.
- `adapter`: platform-specific support that exposes shared harness behavior to
  a tool such as Codex, Claude Code, pre-commit, CI, or another runtime.

Fields such as `supports_capability_domains`, `category`,
`common_starter_pull_ins`, and `excluded_from_capability_scope` qualify support,
selection, or grouping. An asset may support zero, one, or multiple capability
domains without becoming a capability domain itself. These fields are not asset
types.

## Bootstrap Assets

Bootstrap assets help install the harness. They usually should not remain in
the target repo after installation.

`manifests/bootstrap.yml` owns the canonical bootstrap asset boundary.
Conceptually, bootstrap assets include the principles, Profile Change
installer, capability checklists and manifests, Capability Map, optional-asset
manifest, platform notes, and installer support scripts used while fitting a
target repo.

Use `docs/installer.md` first. After its dependency check, read only the
checklist and manifest for the current human-selected capability, then load
other bootstrap assets only when that Profile Change routes to them.

## Bounded Work Assets

Bounded Work assets and behavior are defined in
`manifests/bounded-work.yml`. Treat that manifest as the canonical core asset and
behavior boundary.

## Focused Context Assets

Focused Context assets and behaviors are defined in
`manifests/focused-context.yml`. Treat that manifest as the canonical selected
asset and behavior boundary.

## Selected Capability Assets

Selected Agent Action Boundaries are defined in
`manifests/agent-action-boundaries.yml`. Selected Maintainability Feedback and
its installable policy/coordinator assets are defined in
`manifests/maintainability-feedback.yml`. Treat each manifest as the canonical
boundary for explicitly approved scope; do not infer that every family is
selected.

## Optional Installable Assets

Install optional assets only when repo evidence or human preference justifies
them. Treat `manifests/optional-assets.yml` as the canonical optional asset
list.

Use the current capability manifest for its selected assets. Read
`manifests/optional-assets.yml` only when the capability checklist or exact
human-approved scope routes to an optional pull-in.

## Repo-Specific Adaptation

Adapt only the selected assets. For each one, use the adaptation points in its
manifest and the approved Profile Change rather than applying a universal
installation checklist.

Typical seams include repo paths, commands, work surfaces, existing
conventions or conflicts, runtime mappings, and acceptance evidence or Known
Limits. The manifests own the exact list for each asset.

If the target repo uses multiple agentic coding tools, every adapter should
preserve the same verification, safety, and reporting expectations unless a
documented tool limitation prevents it.

Do not copy optional assets into the target repo merely because they exist.
Each installed asset should have a reason, a cost, and a signal for later
expansion or removal.
