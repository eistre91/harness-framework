# Harness Docs

Audience: agents and maintainers intentionally inspecting, auditing,
maintaining, or extending this repo's agent harness.

Use when: maintaining harness files, changing agent workflow, raising harness
maturity, auditing harness behavior, or understanding why these harness files
exist.

Normal product work should start from `AGENTS.md`, the current Agent Work
Brief, project docs, and local code. Do not read harness docs for ordinary
implementation or to learn how to use the harness unless the task is about the
harness itself.

## Provenance

Source framework: harness-framework
Source version or commit, if known:
Installed on:
Installed by:
Durable Harness Fit Proposal or decision log:

Use portable source names in committed docs. Do not record machine-local paths
or temporary proposal paths in durable harness docs.

For significant harness changes, consult the source framework docs or run a
fresh staged fit pass with the installer before adding process.

## Current Harness Stage

Current stage:
Target level:
Installation mode: canonical / starter / overlay
Stage asset completeness:
Stage behavioral completeness:

Why:

Intentionally deferred:

Use precise maturity wording. If this is a partial starter install, do not
describe the repo as simply "Level 2." Prefer:

```text
Target maturity: Level 2 context routing.
Installation mode: starter.
Stage asset completeness: partial, not full canonical Level 2.
```

## Existing Harness Components

Record overlapping pre-existing components and the decision made during
installation.

| Component | Appears to do | Harness principle satisfied | Handling | Revisit signal |
| --- | --- | --- | --- | --- |
|  |  |  | thread through / adapt / supersede / leave alone / defer |  |

## Skill And Command Conflict Decisions

Harness-provided skills use the `harness-` prefix by default so their
provenance is visible and they do not collide with generic platform or team
skills.

| Platform or path | Skill or command | Overlap | Decision |
| --- | --- | --- | --- |
|  |  | review / implement / work brief / diagnose-debug / run-checks / other |  |

For Claude Code, record whether bundled skills such as `/code-review`,
`/debug`, `/run`, and `/verify` should remain enabled, be documented as
secondary to repo-specific guidance, or be disabled by user or project Claude
Code settings.

If Claude Code native skill mirrors are installed, record the `.claude/skills`
mirror path, the shared `.agents/skills` source path, the sync command, and the
Claude-specific frontmatter that must be preserved, such as `model`,
`allowed-tools`, `effort`, `context`, `hooks`, or `paths`. Treat
`.agents/skills` as the source of truth for skill bodies and support files;
the mirror frontmatter remains platform-owned adapter metadata.

## Installed Harness Pieces

Update this section during installation so it records the target repo's actual
installed harness. It is a local inventory, not the source framework's
canonical asset list.

Populate this table from the final Harness Fit Proposal or decision log. If the
source framework manifests are needed later, use the provenance above to locate
the same framework version; do not assume bootstrap manifest files remain in the
target repo.

| Piece | Status | Purpose | Notes |
| --- | --- | --- | --- |
|  | installed / already satisfied / adapted / deferred / excluded |  |  |

Record the required `repo-checks-on-stop` behavior explicitly, including the
desired hook-capable agent runtime(s), adapter path, command, and result. If no
desired hook-capable runtime is in current scope, record the unsupported-runtime
gap and do not claim full canonical Level 0 completeness.

## Conditional Platform Pointers

- `CLAUDE.md`: install only when Claude Code support is desired. Keep it as
  `@AGENTS.md` so shared behavior stays in one entrypoint.

## Deferred Or Excluded Components

Use the final Harness Fit Proposal or decision log to populate this table. Do
not copy the canonical manifest here.

| Component | Status | Reason | Revisit signal |
| --- | --- | --- | --- |
|  | deferred / excluded |  |  |

## Maintenance Rules

- Add the smallest component that addresses a repeated failure or coordination
  cost.
- Record why a new harness component exists and when it should be simplified or
  removed.
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

## Communication Audit

Update after installation and after significant harness changes.

- A fresh agent can now understand:
- A fresh agent may still misunderstand:
- Terms that need clearer wording:
- Deferred decisions that must not be mistaken for completed maturity:

## Stage Handoff

Update after each completed installation stage. Use the canonical stage handoff
fields from the staged installer.

- Stage completed:
- Installation mode:
- Stage asset completeness:
- Stage behavioral completeness:
- Files installed or edited:
- Validation result:
- Mechanical verification:
- Acceptance or communication evidence:
- Context used:
- Human decisions:
- Placeholders and gaps:
- Deferrals:
- Out-of-stage observations:
- Recommended next action:
