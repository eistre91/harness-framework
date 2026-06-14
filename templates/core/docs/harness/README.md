# Harness Docs

Audience: agents and maintainers intentionally changing this repo's agent
harness.

Use when: maintaining harness files, changing agent workflow, raising harness
maturity, or understanding why these files exist.

Normal product work should start from `AGENTS.md`, the current Agent Work
Brief, project docs, and local code. Do not read harness docs for ordinary
implementation unless the task is about the harness itself.

## Provenance

Source framework:
Installed on:
Installed by:
Harness Fit Proposal plan:

For significant harness changes, consult the source framework docs or run a
fresh harness-fit pass before adding process.

## Current Harness Maturity

Target level:

Why:

Intentionally deferred:

## Installed Harness Pieces

Update this section during installation so it records the target repo's actual
installed harness. It is a local inventory, not the source framework's
canonical asset list.

- `AGENTS.md`: repo entrypoint for agents. Keep it short and focused on where
  work comes from, how verification runs, where context lives, and what safety
  rules apply.
- `scripts/verify.sh`: canonical local verification command. Keep it aligned
  with existing repo checks and CI where practical.
- `docs/harness/README.md`: this local owner’s manual for the harness.
- `docs/harness/work-brief.md`: template for turning work into an executable
  agent brief with goal, scope, context, verification, and acceptance evidence.
- `.agents/skills/review/SKILL.md`: findings-led review lens for checking
  scope, bugs, tests, maintainability, evidence, and review independence.

## Conditional Platform Pointers

- `CLAUDE.md`: install only when Claude Code support is desired. Keep it as
  `@AGENTS.md` so shared behavior stays in one entrypoint.

## Level 1 Additive Components

Install these when the target maturity is Level 1.

- `.agents/skills/implement/SKILL.md`: implementation guidance for working
  from briefs.
- `.agents/skills/work-brief/SKILL.md`: guidance for turning tracker items,
  issues, or chat requests into Agent Work Briefs when agents will shape work.

## Optional Components

Before installation, use the source framework manifests to decide which
optional components are justified. After installation, keep only the optional
components that matter to this repo.

- `docs/harness/component-brief.md`: use before adding a harness component.
  Record value, add signal, cost, and remove/simplify signal.
- `docs/harness/maintainability.md`: lightweight periodic sensor for repeated
  technical, harness, cognitive, or semantic debt.
- `.agents/skills/diagnose/SKILL.md`: disciplined debugging loop.
- `.agents/skills/documentation-quality-audit/SKILL.md`: audit active docs for
  stale or misleading guidance.
- `SPEC-MAP.md`: optional implementation task router. Add only when project
  docs are numerous enough that agents need routing help.
- `CONTEXT.md`: optional short glossary. Add only when domain vocabulary causes
  repeated confusion.

## Maintenance Rules

- Add the smallest component that addresses a repeated failure or coordination
  cost.
- Record why a new harness component exists and when it should be simplified or
  removed.
- Keep shared behavior in `AGENTS.md`, `scripts/verify.sh`, work brief
  templates, and shared skills. Keep tool-specific adapters thin.
- Prefer executable checks and concrete acceptance evidence over prose.
- If project docs are added later, give active docs a short audience and use
  trigger so future agents can tell quickly whether they are reading the right
  file.
