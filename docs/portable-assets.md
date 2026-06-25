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
  target repo when the current stage or optional pull-in justifies it.
- `behavior`: a required or optional harness capability that may be satisfied
  by existing repo conventions, adapted files, scripts, hooks, or documented
  workflow instead of a single copied file.
- `optional-reference`: optional reference material that supports a stage when
  evidence justifies the extra context, but is not part of the required
  current-stage asset boundary.
- `adapter`: platform-specific support that exposes shared harness behavior to
  a tool such as Codex, Claude Code, pre-commit, CI, or another runtime.

Fields such as `maturity`, `category`, `common_starter_pull_ins`, and
`excluded_from_level_asset_boundary` qualify selection or grouping. They are
not asset types.

## Bootstrap Assets

Bootstrap assets help install the harness. They usually should not remain in
the target repo after installation.

`manifests/bootstrap.yml` owns the canonical bootstrap asset boundary.
Conceptually, bootstrap assets include the principles, staged installer,
current-stage checklists, broad reference docs, platform notes, stage
manifests, optional-asset manifest, and installer support scripts used while
fitting a target repo.

Use `docs/installer.md` first. Read the stage checklist and manifest for the
current approved stage, then load other bootstrap assets only when the staged
installer path routes you there.

## Core Installable Assets

The default Level 0 trial assets are defined in `manifests/level-0.yml`.
Treat that manifest as the canonical file-level list.

The additive Level 1 assets and behaviors are defined in
`manifests/level-1.yml`. Treat that manifest as the canonical Level 1 asset
boundary.

The additive Level 2 assets and behaviors are defined in
`manifests/level-2.yml`. Treat that manifest as the canonical Level 2 asset
boundary.

## Optional Installable Assets

Install optional assets only when repo evidence or human preference justifies
them. Treat `manifests/optional-assets.yml` as the canonical optional asset
list.

Use the current-stage manifest for required stage assets. Read
`manifests/optional-assets.yml` only when the stage checklist or
human-approved scope routes to an optional pull-in.

## Repo-Specific Adaptation

Every installation should adapt:

- work source,
- canonical Agent Work Brief location,
- local work brief fallback and commit policy,
- repo checks commands,
- project context paths,
- Level 2 task-intent routes and project-area brief paths,
- sensitive file patterns,
- project-specific skill guidance under `.agents/skills`, using
  self-explaining harness names such as `harness-review` unless adapting to an
  existing convention,
- Claude Code skill mirrors under `.claude/skills` when installed, preserving
  Claude-specific frontmatter while syncing bodies and support files from
  `.agents/skills`,
- existing platform skill or command conflicts,
- adapter choice,
- acceptance evidence standards.

If the target repo uses multiple agentic coding tools, every adapter should
preserve the same verification, safety, and reporting expectations unless a
documented tool limitation prevents it.

Do not copy optional assets into the target repo merely because they exist.
Each installed asset should have a reason, a cost, and a signal for later
expansion or removal.
