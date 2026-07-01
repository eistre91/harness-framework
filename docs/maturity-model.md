# Harness Maturity Model

Audience: agents and maintainers deciding how much harness structure a target
repo needs after the staged installer routes them here.

Use when: choosing or reviewing maturity, installation mode, asset completeness,
behavioral completeness, and deferrals for the current approved stage. For
ordinary installation, start with `docs/installer.md`.

Use this model diagnostically. Higher maturity is not automatically better. A
repo may be healthiest at Level 0 when it has no recurring agent-work need, and
a small repo may be healthiest at Level 1 for a long time once agents are doing
ordinary work there.

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
be aimed at Level 2 behavior without installing every canonical Level 2 asset.
Every stage proposal or install record should state three separate claims:

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

When an install is partial, do not describe the repo as simply "Level 2."
Prefer:

```text
Target maturity: Level 2 context routing.
Installation mode: starter.
Stage asset completeness: partial, not full canonical Level 2.
Deferred manifest assets are listed with reasons and revisit signals.
```

This document is the shared prose definition of the levels. File-level starter
assets are defined in manifests:

- Level 1 required bounded-work assets and behavior:
  `manifests/level-1.yml`
- Level 2 additive assets and behaviors: `manifests/level-2.yml`
- Other optional pull-ins and adapters: `manifests/optional-assets.yml`

Historical note: the old orientation-only Level 0 and bounded-work Level 1
stages have been collapsed. Level 0 now names the no-installed-harness baseline;
Level 1 is the first installable maturity level and owns the bounded-work
foundation.

## Level 0: No Installed Harness

Baseline for a repo with no installed harness assets or durable harness
workflow.

There is no Level 0 manifest or installer checklist. Use this label only to
describe a repo before fitting the harness, or when the human decides not to
install harness assets yet.

This may be enough when:

- agents are not expected to do recurring work in the repo,
- work is rare enough that chat context and local code inspection are
  sufficient,
- adding durable harness files would not yet pay for their maintenance cost.

Move beyond when:

- agents are going to work in the repo at all,
- recurring work needs a stable entrypoint, work source, verification command,
  or review expectation,
- handoff through chat history is already costing time or causing mistakes.

## Level 1: Bounded Work Foundation

Minimum for agents to receive, shape, implement, verify, and review ordinary
work without reconstructing prior planning discussion.

Default assets and behavior are defined in `manifests/level-1.yml`.

At this level, the harness should provide a repo agent entrypoint, canonical
deterministic repo checks command, work-brief skill bundle with a template,
local harness owner manual, lightweight implementation guidance, and
lightweight review guidance.

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
- implementation guidance for agents working from briefs or equivalent
  executable scope,
- review guidance that compares implementation to the brief, scope, evidence,
  and changed behavior boundary.

Asset boundary:

- `harness-work-brief` is Level 1 because the template and source-shaping
  guidance should travel together.
- `harness-implement` is Level 1 because ordinary harness use should include
  focused implementation guidance alongside work shaping and review.
- `harness-review` is Level 1 because every harness-managed change needs a
  reusable review lens.
- `harness-diagnose` is an optional Level 1 pull-in for debugging work, not
  part of the Level 1 required asset boundary.

Value:

- fresh agents know where to start,
- humans can hand off work in a consistent shape,
- agents know how to prove basic correctness,
- agents understand what not to build,
- humans and agents align on trade-offs before implementation,
- interface decisions happen before code generation,
- reviewers have a shared expectation for done and can compare the diff to a
  concrete brief or equivalent scope.

The Level 1 work-brief template includes richer optional sections. For tiny
work, the agent may only need source, goal, value target, context,
verification, and done criteria. Use the boundary, ambiguity, and acceptance
sections when scope or behavior could otherwise be misunderstood.

Add when:

- agents are going to work in the repo at all.

Required deterministic behavior:

- `scripts/repo-checks.sh` runs actionable deterministic checks derived from
  repo evidence,
- the default check set is lint, type checks, and tests, with an explicit
  omission reason, human-approved addition, or human waiver for any member of
  that set that is missing, unclear, too slow, flaky, or inappropriate for the
  repo,
- a narrow Stop hook, or equivalent stop automation, for each desired
  hook-capable agent runtime in current scope, running `scripts/repo-checks.sh`
  from the target repo root.

This is still a deterministic control, but it is small and central enough to be
part of the bounded-work foundation. It reinforces the Level 1 repo checks
contract without requiring a broader hook policy, shared runner, or
cross-platform enforcement system.

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

Default additive assets and behaviors are defined in `manifests/level-2.yml`.

Assets:

- `SPEC-MAP.md`,
- project-area briefs under `docs/project/areas/`,
- optional short `docs/project/intent.md` from
  `templates/optional/docs/project/intent.md`,
- optional `CONTEXT.md`,
- ADR or decision-log pointers.

Value:

- agents read the smallest useful context,
- product knowledge moves out of chat and into durable files,
- repeated conceptual explanations are compressed,
- implementation agents avoid navigating historical or harness docs.

`docs/project/intent.md`, when present, should be short and human-owned. It is
for planning, exploratory work, ambiguous scope decisions, and value-sensitive
review. Do not route ordinary implementation agents to it by default.

Add when:

- the project has multiple product areas,
- docs exist but agents do not know which ones matter,
- repeated planning or review decisions need a shared project north star,
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
- per-call safety decisions for operations that may be safe in one context but
  unsafe in another, including whether a command can run concurrently for this
  specific invocation,
- broader repo checks beyond the Level 1 lint/type/test contract, such as
  format, build/package, static analysis, generated-artifact validation, or
  adapter health checks when repo evidence justifies them,
- focused subsystem checks and CI-only verification records when full local
  parity is not practical,
- check performance, noise, and failure-clarity tuning,
- broader Stop hook or pre-commit enforcement beyond the required Level 1
  `repo-checks-on-stop` behavior,
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
- the Level 1 lint/type/test contract misses recurring deterministic failures,
- full-repo checks are too slow, noisy, flaky, or unclear for agent-stop
  feedback,
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
- validation itself needs orchestration,
- state is getting lost between agents.

## Level 5: Orchestration And Automation

For larger or more agent-heavy projects.

At this level, automation scales execution and coordination. It does not move
strategy, product meaning, architecture direction, priority, or acceptable risk
out of human ownership.

Complex work at this level often separates research, planning, implementation,
and validation into distinct context windows linked by durable artifacts. The
signals and operating model are still emerging; see
`docs/level-5-orchestration.md` for the current sketch.

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
- validation reports become structured,
- the harness itself can be tested and improved.

Add when:

- work spans many short-lived sessions,
- humans are routinely decomposing large work into many agent tasks,
- agents are operating unattended or semi-unattended inside bounded,
  human-approved intent,
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
