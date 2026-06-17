# Harness Maturity Model

Use this model diagnostically. Higher maturity is not automatically better. A
small repo may be healthiest at Level 0 or Level 1 for a long time.

## Harness Failure Signals

A harness may be failing when agents or humans repeatedly show the same
coordination, context, verification, or maintenance symptoms:

- agents miss requirements, overbuild, or need repeated clarification,
- agents forget checks or different contributors run different verification,
- reviewers repeatedly ask for the same evidence,
- work handoff depends on chat history or gets lost between sessions,
- individual agent contexts rot, read too broadly, miss important context, or
  hit compaction,
- docs mislead agents or drift from code,
- harness instructions, hooks, skills, or adapters duplicate truth or no longer
  help,
- product delivery slows because process surfaces create more work than value.

Use the level-specific "Add when" and "Move beyond when" sections below to
choose the smallest next harness change.

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
deterministic repo checks command, work-brief skill bundle with a template,
local harness owner manual, and lightweight review guidance.

Value:

- fresh agents know where to start,
- humans can hand off work in a consistent shape,
- agents know how to prove basic correctness,
- reviewers have a shared expectation for done.

The Level 0 work-brief template may include richer optional sections. For tiny
work, the agent may only need source, goal, value target, context,
verification, and done criteria. Filling the boundary, ambiguity, and
acceptance sections becomes more important at Level 1.

Add when:

- agents are going to work in the repo at all.

Move beyond when:

- agents miss requirements from vague tickets,
- agents forget repo checks commands,
- reviewers repeatedly ask for the same evidence,
- work handoff depends too heavily on chat history.

This may be enough when:

- tasks are small,
- the codebase is still easy to navigate,
- humans provide most context directly,
- agents can complete work without repeatedly asking where things live.

## Level 1: Bounded Work Execution

Adds stronger work shaping on top of Level 0.

Default additive assets are defined in `manifests/level-1.yml`.

Definition:

- intentional use of Agent Work Brief tiers,
- explicit non-goals when scope could sprawl,
- ambiguity and decision notes when product or interface choices affect
  implementation,
- boundary/interface sections for public APIs, CLIs, integrations, modules,
  jobs, file formats, or other consumed surfaces,
- acceptance evidence standards for externally visible or boundary-changing
  behavior,
- progress/divergence state in the canonical brief location when work spans
  sessions or departs from the original plan,
- implementation guidance for agents working from briefs.

Asset boundary:

- `harness-review` is Level 0 because every harness-managed change needs a
  reusable review lens.
- `harness-implement` is Level 1 because it guides bounded execution from a
  brief.
- `harness-work-brief` is Level 0 because the template and source-shaping
  guidance should travel together.
- `harness-diagnose` is an optional Level 1 pull-in for debugging work, not
  part of the Level 1 definition.

Value:

- agents understand what not to build,
- humans and agents align on trade-offs before implementation,
- interface decisions happen before code generation,
- review can compare the diff to a concrete brief.

Add when:

- tickets are too vague for direct implementation,
- changes affect APIs, modules, CLIs, integrations, or other boundaries,
- human-agent planning conversations are repeating the same questions,
- implementation spans more than one session or agent,
- agents overbuild beyond the requested value.

Common starter pull-in:

- a Stop hook that runs `scripts/repo-checks.sh` when the repo has a real, reasonably
  fast checks command and the team wants automatic feedback during agent
  sessions.

This is still a deterministic control, but it is small enough to pair with
Level 1 because it reinforces the Level 0 repo checks contract without
requiring a broader hook policy, shared runner, or cross-platform enforcement
system.

This may be enough when:

- most work is still local,
- acceptance examples are easy to state,
- a human can still route context manually,
- there are not many product docs to navigate.

Move beyond when:

- agents repeatedly read too much context,
- agents miss important local conventions,
- agents ask where relevant docs or modules are,
- task briefs become overloaded with routing details.

## Level 2: Context Routing

Adds product-context routing.

Assets:

- `docs/project/`,
- optional `SPEC-MAP.md`,
- optional `CONTEXT.md`,
- ADR or decision-log pointers.

Value:

- agents read the smallest useful context,
- product knowledge moves out of chat and into durable files,
- repeated conceptual explanations are compressed,
- implementation agents avoid navigating historical or harness docs.

Add when:

- the project has multiple product areas,
- docs exist but agents do not know which ones matter,
- domain vocabulary causes confusion,
- agents repeatedly rediscover the same context.

This may be enough when:

- context routing is short,
- agents rarely need more than the routed docs and local code,
- docs are current enough to reduce confusion,
- implementation context remains focused.

Move beyond when:

- docs drift from code,
- agents read stale docs and make bad changes,
- maintainability problems recur across tasks,
- reviewers repeatedly identify the same code or documentation debt.

## Level 3: Deterministic Controls

Moves repeatable checks from agent memory into tools.

Assets:

- secret and sensitive-file guards,
- destructive-action warnings or blocks,
- tool-safety checklist for protected paths, protected commands, and
  ask/warn/block policy,
- broader Stop hook or pre-commit enforcement beyond the early
  `scripts/repo-checks.sh` pull-in,
- CI parity with `scripts/repo-checks.sh`,
- optional `.harness.yml` once multiple mechanisms need shared settings.

Value:

- common failures are caught automatically,
- verification does not depend on agent memory,
- humans and agents share one command contract,
- safety boundaries are enforced consistently.

Add when:

- agents forget verification,
- contributors run different command sets,
- secret, local-state, destructive-command, or production-affecting mistakes
  are plausible,
- the same mechanical failure appears in review or CI,
- scripts and hooks start duplicating configuration.

This may be enough when:

- hooks are fast and quiet,
- failures are actionable,
- people do not routinely bypass the checks,
- mechanical defects are caught before review.

Move beyond when:

- quality problems are not mechanical,
- code organization is degrading,
- documentation usefulness is degrading,
- agents close tasks but require too many review cycles.

## Level 4: Maintainability Sensors

Observes entropy without gating every change.

Assets:

- maintainability checklist,
- documentation quality audit,
- recurring failure ledger,
- optional duplicate/dead-code/complexity tools,
- issue creation for bounded repair work.

Value:

- technical debt becomes visible,
- harness debt becomes visible,
- cognitive and semantic drift are named,
- recurring failures become repair work instead of review folklore.

Add when:

- reviewers repeatedly see the same maintainability concerns,
- agents struggle to close similar work without extra verification cycles,
- docs are stale enough to mislead,
- humans and agents no longer share the same model of the system,
- objective tools reveal duplicate, dead, or overly complex code.

This may be enough when:

- maintainability work is periodic, bounded, and useful,
- sensors produce few false alarms,
- repair work is scoped as normal tickets,
- product delivery is not slowed by constant process.

Move beyond when:

- multiple agents need to coordinate long-horizon work,
- work spans many short-lived sessions,
- verification itself needs orchestration,
- state is getting lost between agents.

## Level 5: Orchestration And Automation

For larger or more agent-heavy projects.

Assets:

- PRD lifecycle,
- tracker adapters,
- structured final-output protocols,
- unattended runners,
- verifier agents,
- multi-agent coordination rules,
- eval suites,
- harness modes,
- stricter file access controls.

Value:

- long-horizon work survives fresh-context sessions,
- multiple agents can coordinate through durable artifacts,
- verification reports become structured,
- the harness itself can be tested and improved.

Add when:

- work spans many short-lived sessions,
- humans are routinely decomposing large work into many agent tasks,
- agents are operating unattended or semi-unattended,
- ordinary final messages are not reliable enough,
- multiple agents need explicit ownership, review, or integration boundaries,
- work state is too large for one session or ticket,
- harness behavior itself needs regression testing.

Do not add yet when:

- a human is still closely guiding most work,
- tasks are small enough for one agent session,
- a work brief and verification script solve most coordination needs,
- the team has not yet adopted the lower layers.

## Use

1. Start with the smallest layer that supports current work.
2. Watch for repeated failures or coordination costs.
3. Add the smallest next component that addresses the observed signal.
4. Keep a component brief for each new harness part.
5. Remove or simplify components that stop earning their maintenance cost.
