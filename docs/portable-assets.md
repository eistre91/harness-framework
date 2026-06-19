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

## Bootstrap Assets

Bootstrap assets help install the harness. They usually should not remain in
the target repo after installation.

- `docs/framework.md`
- `docs/principles.md`
- `docs/implementation-guide.md`
- `docs/maturity-model.md`
- `docs/platform-support.md`
- `docs/platforms/*.md`
- `manifests/bootstrap.yml`
- `manifests/level-0.yml`
- `manifests/level-1.yml`
- `manifests/optional-assets.yml`

Use these while creating the Harness Fit Proposal and selecting assets.

## Core Installable Assets

The default Level 0 trial assets are defined in `manifests/level-0.yml`.
Treat that manifest as the canonical file-level list.

The additive Level 1 assets and behaviors are defined in
`manifests/level-1.yml`. Treat that manifest as the canonical Level 1 asset
boundary.

## Optional Installable Assets

Install optional assets only when repo evidence or human preference justifies
them. Treat `manifests/optional-assets.yml` as the canonical optional asset
list.

Selection manifests:

- `manifests/level-0.yml`
- `manifests/level-1.yml`
- `manifests/optional-assets.yml`

## Repo-Specific Adaptation

Every installation should adapt:

- work source,
- canonical Agent Work Brief location,
- local work brief fallback and commit policy,
- repo checks commands,
- project context paths,
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
