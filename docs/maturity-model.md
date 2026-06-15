# Harness Maturity Model

Use this model diagnostically. Higher maturity is not automatically better. A
small repo may be healthiest at Level 0 or Level 1 for a long time.

Maturity level is not the same as installation completeness. A target repo can
be aimed at Level 1 behavior without installing every canonical Level 1 asset.
Every install should state three separate claims:

- target maturity: the behavior the repo is being fitted toward,
- asset completeness: whether the canonical manifest assets for that level are
  fully installed, partially installed, already satisfied, adapted, deferred, or
  excluded,
- behavioral completeness: whether humans and agents can actually follow the
  intended workflow with the installed surfaces.

Use these installation modes:

- `canonical`: install or adapt every required manifest asset and behavior for
  the target level unless the proposal proves an existing component already
  satisfies it.
- `starter`: install a deliberately partial subset that closes the highest
  value gaps, with explicit deferrals and revisit signals.
- `overlay`: apply harness principles through existing repo conventions with
  little or no new asset creation.

When an install is partial, do not describe the repo as simply "Level 1" or
"Level 2." Prefer:

```text
Target maturity: Level 1 bounded work execution.
Installation mode: starter.
Installation completeness: partial, not full canonical Level 1.
Deferred manifest assets are listed with reasons and revisit signals.
```

This document is the shared prose definition of the levels. File-level starter
assets are defined in manifests:

- Level 0 required starter assets: `manifests/level-0.yml`
- Level 1 additive assets and behaviors: `manifests/level-1.yml`
- Other optional pull-ins and adapters: `manifests/optional-assets.yml`

## Level 0: Table Stakes

Minimum for agents to work without reconstructing prior planning discussion.

Default assets are defined in `manifests/level-0.yml`.

At this level, the harness should provide a repo agent entrypoint, canonical
verification command, work brief template, local harness owner manual, and
lightweight review guidance.

The Level 0 work brief template may include richer optional sections. For tiny
work, the agent may only need source, goal, value target, context,
verification, and done criteria. Filling the boundary, ambiguity, and
acceptance sections becomes more important at Level 1.

Add when:

- agents are going to work in the repo at all.

Move beyond when:

- agents miss requirements from vague tickets,
- reviewers repeatedly ask for the same evidence,
- work handoff depends too heavily on chat history.

## Level 1: Bounded Work Execution

Adds stronger work shaping on top of Level 0.

Default additive assets are defined in `manifests/level-1.yml`.

Definition:

- intentional use of Agent Work Brief tiers,
- explicit non-goals when scope could sprawl,
- ambiguity and decision notes when product or interface choices affect
  implementation,
- boundary/interface sections for boundary-changing work,
- acceptance evidence standards for behavior changes,
- progress/divergence state in the canonical brief location when work spans
  sessions or departs from the plan,
- implementation guidance for agents working from briefs.

Asset boundary:

- `harness-review` is Level 0 because every harness-managed change needs a
  reusable review lens.
- `harness-implement` is Level 1 because it guides bounded execution from a
  brief.
- `harness-work-brief` is Level 1 when agents will help transform tickets,
  issues, or chat requests into executable briefs.
- `harness-diagnose` is an optional Level 1 pull-in for debugging work, not
  part of the Level 1 definition.

Add when:

- tickets are too vague for direct implementation,
- changes affect APIs, modules, CLIs, integrations, or other boundaries,
- implementation spans more than one session or agent,
- agents overbuild beyond the requested value.

## Level 2: Context Routing

Adds product-context routing.

Assets:

- `docs/project/`,
- optional `SPEC-MAP.md`,
- optional `CONTEXT.md`,
- ADR or decision-log pointers.

Add when:

- the project has multiple product areas,
- docs exist but agents do not know which ones matter,
- agents repeatedly rediscover the same context.

## Level 3: Deterministic Controls

Moves repeatable checks from agent memory into tools.

Assets:

- secret and sensitive-file guards,
- destructive-action warnings or blocks,
- tool-safety checklist for protected paths, protected commands, and
  ask/warn/block policy,
- Stop hook or pre-commit verification,
- CI parity with `scripts/verify.sh`,
- optional `.harness.yml` once multiple mechanisms need shared settings.

Add when:

- agents forget verification,
- contributors run different command sets,
- secret, local-state, destructive-command, or production-affecting mistakes
  are plausible,
- the same mechanical failure appears in review or CI.

## Level 4: Maintainability Sensors

Observes entropy without gating every change.

Assets:

- maintainability checklist,
- documentation quality audit,
- recurring failure ledger,
- optional duplicate/dead-code/complexity tools.

Add when:

- reviewers repeatedly see the same maintainability concerns,
- docs are stale enough to mislead,
- humans and agents no longer share the same model of the system.

## Level 5: Orchestration And Automation

For larger or more agent-heavy projects.

Assets:

- PRD lifecycle,
- tracker adapters,
- structured final-output protocols,
- unattended runners,
- verifier agents,
- multi-agent coordination rules,
- eval suites.

Add when:

- work spans many short-lived sessions,
- humans are routinely decomposing large work into many agent tasks,
- ordinary final messages are not reliable enough,
- multiple agents need explicit ownership, review, or integration boundaries.

## Use

1. Start with the smallest layer that supports current work.
2. Watch for repeated failures or coordination costs.
3. Add the smallest next component that addresses the observed signal.
4. Keep a component brief for each new harness part.
5. Remove or simplify components that stop earning their maintenance cost.
