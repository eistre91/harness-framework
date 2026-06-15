# Harness Docs

Audience: agents and maintainers intentionally changing this repo's agent
harness.

Use when: maintaining harness files, changing agent workflow, raising harness
maturity, or understanding why these files exist.

Normal product work should start from `AGENTS.md`, the current Agent Work
Brief, project docs, and local code. Do not read harness docs for ordinary
implementation unless the task is about the harness itself.

## Provenance

Source framework: harness-framework
Source version or commit, if known:
Installed on:
Installed by:
Temporary Harness Fit Proposal path, if any:
Durable Harness Fit Proposal or decision log:

Use portable source names in committed docs. Keep local paths such as
`../harness-framework` in temporary proposals or transcripts only.

For significant harness changes, consult the source framework docs or run a
fresh fit pass with the implementation guide before adding process.

## Current Harness Maturity

Target level:
Installation mode: canonical / starter / overlay
Installation completeness:
Behavioral completeness:

Why:

Intentionally deferred:

Use precise maturity wording. If this is a partial starter install, do not
describe the repo as simply "Level 1." Prefer:

```text
Target maturity: Level 1 bounded work execution.
Installation mode: starter.
Installation completeness: partial, not full canonical Level 1.
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
|  |  | review / implement / work brief / diagnose-debug / run-verify / other |  |

For Claude Code, record whether bundled skills such as `/code-review`,
`/debug`, `/run`, and `/verify` should remain enabled, be documented as
secondary to repo-specific guidance, or be disabled by the human's Claude Code
settings.

## Installed Harness Pieces

Update this section during installation so it records the target repo's actual
installed harness. It is a local inventory, not the source framework's
canonical asset list. For the canonical source asset list, consult the source
framework manifests:

- `manifests/level-0.yml`
- `manifests/level-1.yml`
- `manifests/optional-assets.yml`

| Piece | Status | Purpose | Notes |
| --- | --- | --- | --- |
|  | installed / already satisfied / adapted / deferred / excluded |  |  |

## Conditional Platform Pointers

- `CLAUDE.md`: install only when Claude Code support is desired. Keep it as
  `@AGENTS.md` so shared behavior stays in one entrypoint.

## Deferred Or Excluded Components

Use the final Harness Fit Proposal or source framework manifests to populate
this table. Do not copy the canonical manifest here.

| Component | Status | Reason | Revisit signal |
| --- | --- | --- | --- |
|  | deferred / excluded |  |  |

## Maintenance Rules

- Add the smallest component that addresses a repeated failure or coordination
  cost.
- Record why a new harness component exists and when it should be simplified or
  removed.
- Keep shared behavior in `AGENTS.md`, `scripts/verify.sh`, work brief
  templates, and shared skills. Keep tool-specific adapters thin.
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
