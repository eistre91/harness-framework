# Level 0 Installer Checklist

Audience: agents and maintainers installing the Level 0 foundation in a target
repo.

Use when: the current approved installation stage is Level 0. Start from
`docs/installer.md` first.

## Read For This Stage

Always read:

- `docs/principles.md`
- `docs/installer.md`
- `manifests/level-0.yml`
- the Level 0 templates, skills, and companion files named by the manifest

Read only if needed for this Level 0 stage:

- `docs/portable-assets.md`, when adaptation boundaries are unclear
- the `claude-entrypoint` entry in `manifests/optional-assets.yml`, followed by
  `templates/core/CLAUDE.md`, when the repo uses Claude Code or the human asks
  for the minimal Claude Code pointer

Do not read by default:

- `docs/maturity-model.md`
- `manifests/level-1.yml`
- the full `manifests/optional-assets.yml`
- platform adapter docs
- `docs/level-5-orchestration.md`
- `TODO.md`

If you read an out-of-stage source, record why in the proposal and stage
handoff.

## Scope

Level 0 installs the foundation that lets agents do ordinary work without
reconstructing prior planning conversation.

Use `manifests/level-0.yml` as the canonical asset list. Do not maintain a
second file list here.

Conceptually, the Level 0 foundation should give the target repo:

- a concise repo agent entrypoint,
- a canonical deterministic repo checks command,
- work-brief creation guidance,
- lightweight review guidance,
- a durable harness docs record.

Minimal Claude Code support may be included when needed to expose the shared
entrypoint. The `claude-entrypoint` optional manifest entry owns that asset
boundary. In that case, keep `CLAUDE.md` as a thin pointer to `AGENTS.md`. Do
not install platform hooks, native skill mirrors, `.codex/` config, or
pre-commit adapters in Level 0 unless the human explicitly expands the current
stage.

## Proposal

Prepare a Level 0 proposal before editing. The proposal authorizes Level 0
edits only.

Include:

- current stage: Level 0,
- installation mode: `canonical`, `starter`, or `overlay`,
- Level 0 asset completeness,
- expected Level 0 behavioral completeness,
- target-repo signals needed to adapt Level 0 assets,
- files to create or edit,
- work source and Agent Work Brief location,
- local fallback brief location and commit policy,
- repo checks command or honest placeholder,
- project context path, or `none yet`,
- existing entrypoint, skill, command, or harness-like component handling,
- minimal platform pointer decision, when relevant,
- gaps surfaced,
- current-stage deferrals,
- human decisions needed before editing,
- context used.

Out-of-stage observations may be recorded as plain observations. Do not map
them to future levels, propose later-stage assets, or ask for approval to
install them during the Level 0 stage.

## Human Checkpoint Before Editing

After writing and persisting the proposal, present the exact proposal text to
the human and wait for approval or corrections.

The approval should cover only:

- Level 0 installation mode,
- Level 0 files to create or edit,
- work brief storage and fallback policy,
- repo checks behavior,
- existing component handling,
- minimal platform pointer, when included,
- durable location for the Level 0 decision log or stage handoff.

Do not edit target-repo files before this checkpoint is resolved.

## Level 0 Gate

Level 0 passes when the installed harness is honest, usable, and auditable.

Check:

- `AGENTS.md` tells a fresh agent where work comes from, where briefs live, how
  to verify, what skills exist, where project context is or is not, and where
  harness docs live for intentional harness maintenance.
- `AGENTS.md` stays concise enough to be a repo entrypoint, not an encyclopedia.
- `scripts/repo-checks.sh` exists and either runs real inferred checks or
  clearly reports the missing-checks gap.
- The installed `harness-work-brief` and `harness-review` guidance is
  discoverable in the agreed skill location.
- `docs/harness/README.md` or the chosen durable decision log records
  provenance, installation mode, Level 0 stage completeness, installed pieces,
  existing component decisions, deferrals, and communication audit findings.
- Any introduced local fallback brief directory is gitignored.
- A fresh agent can do ordinary product work from the repo entrypoint, current
  work source, installed skills, project docs if any, and local code, without
  reading `docs/harness/` or framework internals.
- The stage report lists context used.
- The stage report confirms that higher-level manifests, optional asset
  manifests, adapter docs, and future-facing TODOs were not used for this stage
  unless explicitly listed and justified.

Missing checks, unclear trackers, or absent project docs do not automatically
fail Level 0. They fail only when hidden. Use honest placeholders or explicit
`none yet` decisions and record the gap.

## Stage Handoff

After installation and validation, report the Level 0 result and copy durable
stage state under `docs/harness/`. Use the canonical stage handoff fields in
`docs/installer.md`.

For Level 0, make sure the handoff also makes these details explicit:

- repo checks command and result,
- communication audit,
- recommended next action: stop, revise Level 0, or ask the human whether to
  begin next-stage inspection.

Do not inspect Level 1 guidance until the human chooses to begin the next
stage.
