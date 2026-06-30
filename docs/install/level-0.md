# Level 0 Installer Checklist

Audience: agents and maintainers installing the Level 0 bounded-work foundation
in a target repo.

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
- `docs/platform-support.md`, then only the relevant platform note, to install
  the required `repo-checks-on-stop` adapter for the target repo's desired
  hook-capable agent runtime(s) in current scope
- the `claude-entrypoint` entry in `manifests/optional-assets.yml`, followed by
  `templates/core/CLAUDE.md`, when the repo uses Claude Code or the human asks
  for the minimal Claude Code pointer

Do not read by default:

- `docs/maturity-model.md`
- `manifests/level-2.yml`
- the full `manifests/optional-assets.yml`
- platform adapter docs
- `docs/level-5-orchestration.md`
- `TODO.md`

If you read an out-of-stage source, record why in the proposal and stage
handoff.

## Scope

Level 0 installs the bounded-work foundation that lets agents do ordinary work
without reconstructing prior planning conversation.

Use `manifests/level-0.yml` as the canonical Level 0 asset and behavior list.
Do not maintain a second file list here.

Conceptually, the Level 0 foundation should give the target repo:

- a concise repo agent entrypoint,
- an actionable canonical deterministic repo checks command,
- work-brief creation guidance, including tiers, non-goals, ambiguity,
  boundary/interface, acceptance evidence, and progress/divergence guidance,
- lightweight implementation guidance,
- lightweight review guidance,
- a durable harness docs record.

Minimal Claude Code support may be included when needed to expose the shared
entrypoint. The `claude-entrypoint` optional manifest entry owns that asset
boundary. In that case, keep `CLAUDE.md` as a thin pointer to `AGENTS.md`. Do
not install native skill mirrors, broad platform hooks, or pre-commit adapters
in Level 0 unless the human explicitly expands the current stage.

Level 0 must install `scripts/repo-checks.sh`. For canonical Level 0
completeness, that script must run actionable, repo-derived deterministic
checks. The default Level 0 check set is lint, type checks, and tests. Include
each command when repo evidence shows it exists and is reasonably actionable.
If one member of that set is missing, unclear, too slow, flaky, or
inappropriate for the repo, raise that before editing and recommend whether to
omit it with a recorded reason, add or adapt it with human approval, or record
an explicit human waiver for this install.

Do not invent a verification stack during Level 0 installation. A placeholder
`scripts/repo-checks.sh` may honestly report a gap, but a placeholder-only
script is not full canonical Level 0 repo-checks completeness.

Level 0 includes a required `repo-checks-on-stop` behavior: install or adapt a
narrow Stop hook, or equivalent stop automation, for each desired hook-capable
agent runtime in current scope. The automation runs only `scripts/repo-checks.sh`
from the target repo root. This may require a thin platform adapter such as
`.codex/` or `.claude/` hook config. Broad hook policy, secret guards,
destructive-action controls, shared hook runners, cross-platform enforcement,
and CI or pre-commit parity remain selected deterministic controls beyond this
stage unless explicitly approved as separate current-stage scope.

If no hook-capable desired agent runtime is in scope, record that as a Level 0
gap and do not claim full canonical Level 0 asset or behavioral completeness.

## Proposal

Prepare a Level 0 proposal before editing. The proposal authorizes Level 0
edits only.

Include:

- current stage: Level 0,
- target maturity behavior: bounded work foundation,
- installation mode: `canonical`, `starter`, or `overlay`,
- Level 0 asset completeness,
- expected Level 0 behavioral completeness,
- target-repo signals needed to adapt Level 0 assets,
- files to create or edit,
- work source and Agent Work Brief location,
- local fallback brief location and commit policy,
- work-brief behavior for tiers, non-goals, ambiguity, decisions, boundaries,
  acceptance evidence, and progress/divergence notes,
- acceptance evidence standards for boundary-changing or externally visible
  behavior,
- repo checks command, including lint, type-check, and test coverage, plus any
  explicit omission reason, proposed addition, or human waiver,
- `repo-checks-on-stop` installation or already-satisfied decision, including
  desired hook-capable agent runtime(s), adapter files, hook command, and
  unsupported-runtime gap when relevant,
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
- repo checks behavior, including included lint, type-check, and test commands
  and any explicit omissions or waivers,
- acceptance evidence standards,
- required `repo-checks-on-stop` adapter files and behavior,
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
- `scripts/repo-checks.sh` exists and runs actionable deterministic checks
  derived from repo evidence.
- The repo checks cover lint, type checks, and tests when those commands exist
  and fit the repo. Any missing, unclear, too slow, flaky, or inappropriate
  member of that set has a recorded reason, human-approved addition, or
  explicit human waiver.
- A placeholder-only `scripts/repo-checks.sh` records an honest gap but does
  not qualify as full canonical Level 0 repo-checks completeness.
- The installed `harness-work-brief`, `harness-implement`, and
  `harness-review` guidance is discoverable in the agreed skill location.
- `AGENTS.md` or the target repo's equivalent entrypoint tells agents to use
  work-brief, implementation, and review guidance by phase rather than as one
  combined reading list.
- The canonical work source and brief location remain explicit, including the
  local fallback and commit policy when a fallback exists.
- Standard or complex work has a clear place to record non-goals, ambiguities,
  accepted decisions, boundaries or interfaces, verification, and acceptance
  evidence.
- Work that spans sessions or diverges from the expected plan has a clear
  place to record current status, accepted divergence, latest evidence,
  blockers, and next action.
- Boundary-changing or externally visible work requires acceptance evidence in
  addition to mechanical verification.
- Implementation guidance tells agents to keep scope narrow, respect non-goals,
  use existing project patterns, run focused verification while iterating when
  practical, and run the canonical repo checks before claiming done.
- The review handoff names the brief or source, tier, changed files, behavior
  boundary, test surface, and known risks.
- `docs/harness/README.md` or the chosen durable decision log records
  provenance, installation mode, Level 0 stage completeness, installed pieces,
  existing component decisions, deferrals, and communication audit findings.
- Any introduced local fallback brief directory is gitignored.
- `repo-checks-on-stop` is installed, adapted, or explicitly satisfied for each
  desired hook-capable agent runtime in current scope, and runs only the
  canonical repo checks command from the repo root. If no supported desired
  runtime exists, the handoff records that gap and does not claim full
  canonical Level 0 completeness.
- A fresh agent can do ordinary product work from the repo entrypoint, current
  work source, installed skills, project docs if any, and local code, without
  reading `docs/harness/` or framework internals.
- The stage report lists context used.
- The stage report confirms that higher-level manifests, optional asset
  manifests, adapter docs, and future-facing TODOs were not used for this stage
  unless explicitly listed and justified.

Missing lint, type-check, or test commands; unclear trackers; or absent project
docs do not automatically fail a Level 0 install. They fail when hidden. Full
canonical Level 0 repo-checks completeness requires actionable deterministic
checks plus recorded reasons, additions, or explicit waivers for omitted
lint/type/test commands.

## Stage Handoff

After installation and validation, report the Level 0 result and copy durable
stage state under `docs/harness/`. Use the canonical stage handoff fields in
`docs/installer.md`.

For Level 0, make sure the handoff also makes these details explicit:

- repo checks command and result,
- included lint, type-check, and test commands, plus any omission reason,
  human-approved addition, or explicit waiver,
- `repo-checks-on-stop` adapter path, command, and result, or unsupported
  runtime gap,
- work-brief lifecycle and progress/divergence location,
- acceptance evidence rules for boundary-changing or externally visible work,
- representative communication audit result or reason it was not possible,
- recommended next action: stop, revise Level 0, or ask the human whether to
  begin context-routing inspection.

For communication evidence, use a representative standard or complex work item
when one is available. Confirm that a fresh agent could identify the tier,
brief location, implementation guidance, verification, acceptance evidence, and
review handoff path. If no representative work item is available, record that
the Level 0 communication audit is limited to installed-surface inspection.

Do not inspect Level 2 guidance, deterministic controls, or optional pull-ins
beyond this stage until the human chooses to begin that next stage or
explicitly changes the current approved scope.
