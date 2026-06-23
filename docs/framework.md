# Agent Harness Framework

Audience: agents and maintainers changing this framework or deciding which
harness concepts belong in a target repo.

Use when: understanding the framework shape and rationale. For installation
steps, use `docs/implementation-guide.md`.

This document defines the conceptual shape of a portable agent harness that is
fit to the target repo's current purpose and grown as new needs are discovered.
It intentionally avoids being the source of truth for installable file lists,
templates, or detailed installation procedure.

## Source Of Truth Map

- Principles: `docs/principles.md`
- Maturity definitions and failure signals: `docs/maturity-model.md`
- Bootstrap, Level 0, Level 1, and optional assets:
  `manifests/bootstrap.yml`, `manifests/level-0.yml`,
  `manifests/level-1.yml`, and `manifests/optional-assets.yml`
- Installation procedure: `docs/implementation-guide.md`
- Portable versus repo-specific assets: `docs/portable-assets.md`
- Platform adapter guidance: `docs/platform-support.md` and
  `docs/platforms/*.md`
- Work brief template:
  `skills/core/harness-work-brief/work-brief-template.md`
- Harness fit proposal template:
  `templates/core/docs/harness/fit-proposal.md`
- Component brief template:
  `templates/optional/docs/harness/component-brief.md`
- Level 5 orchestration sketch, exploratory:
  `docs/level-5-orchestration.md`

## Mission

The mission of the harness is to maximize human leverage by keeping humans in
control of software strategy while agents expand tactical execution,
investigation, and review. It translates human intent into bounded,
inspectable work agents can carry forward without silently making product,
architecture, domain, priority, or risk decisions. A good harness makes humans
and agents together more capable than either alone while preserving human
responsibility for what the software is, how it evolves, and what it should
become.

## Working Definition

A harness is the engineered control system around an agentic model that turns
short-lived, stochastic model sessions into reliable, inspectable,
long-horizon software work.

The framework applies the same discipline to the harness that we expect from
application code:

- keep it small,
- make every piece justify its value,
- avoid speculative abstractions,
- add structure only when a real failure mode or coordination need appears,
- remove or simplify pieces that become maintenance burden.

KISS and YAGNI apply one layer up. A harness can accumulate debt just like
product code can.

## Target Shape

Large agent harnesses can include issue lifecycle conventions, PRD flows,
validation loops, context routers, hooks, review patterns, unattended
runners, maintainability reports, and documentation-quality-audit workflows.

Those systems can be valuable when a repo has grown enough to need them. This
framework starts smaller. It should help the human-agent system:

1. let fresh agents orient quickly,
2. understand where work comes from,
3. transform external work into an executable local shape,
4. read only the context needed for the current task,
5. implement through verifiable steps,
6. avoid over-engineering,
7. produce mechanical and acceptance evidence,
8. support review of bugs, maintainability, scope, and design fit,
9. feed repeated failures back into harness, documentation, or code
   improvements.

The harness should not require the project to adopt a specific tracker,
language, framework, unattended runner, or mature domain-doc structure.

The core lifecycle is:

```text
bootstrap -> work brief -> implementation -> validation -> feedback
```

A fuller lifecycle is:

```text
external work item
  -> agent work brief
  -> scoped implementation
  -> validation: verification, review, and human checkpoints as needed
  -> closeout or follow-up work
  -> maintainability feedback when patterns repeat
```

## Primitive Agent Work Verbs

The lifecycle above is one concrete expression of a smaller conceptual model:

```text
research -> plan -> implement -> validate
```

These verbs are primitives for reasoning about agent work, not mandatory
ceremony. Tiny work may collapse all four into one short context. Standard work
may combine research and planning, then implement from the resulting brief.
Complex work often benefits from isolating each phase into separate context
windows with explicit handoff artifacts.

Each phase can be understood as an input/output function:

- Research gathers the code, docs, prior decisions, human context, and external
  references needed to act on the intent.
- Plan shapes intent and research into executable scope: what will change, what
  will not change, what boundary is affected, and how completion will be
  checked.
- Implement produces the requested artifact inside the delegated scope. When
  reality falsifies the plan, the implementer should record the divergence or
  return to planning or human decision rather than silently changing direction.
- Validate decides whether the output satisfies the intent at acceptable risk.
  Validation includes deterministic verification, judgment-heavy review, and
  human-required checkpoints when intent, trade-offs, residual risk, or
  long-living decisions need human input.

Human intent is the initial input, but it is not assumed to be complete. Any
phase may discover ambiguity, missing context, or a decision that requires a new
injection of human intent or another source artifact.

## Intent Layers

Semantic intent may live at several layers. The framework should name these
layers without prescribing one storage system:

- Project intent: the high-level direction, audience, constraints, and value
  proposition for the product or system.
- Initiative intent: feature, PRD, design, or larger body-of-work intent that
  decomposes into work units.
- Work-unit intent: the local goal, scope, non-goals, acceptance evidence, and
  constraints for an agent-executable task.
- Implementation intent: local design choices inside the approved work unit,
  such as the immediate boundary, test surface, and code path.

The storage can be a tracker, repo docs, PRD, issue, Agent Work Brief, or other
durable project source. The important property is that future agents and humans
can recover the relevant intent without relying on chat history.

## Starter Harness

For an initial trial, the canonical Level 0 file-level asset list lives in
`manifests/level-0.yml`.

Conceptually, Level 0 provides:

- a repo agent entrypoint,
- a canonical deterministic repo checks command,
- a work-brief skill bundle with a template,
- a local harness owner manual,
- lightweight review guidance.

Level 1 adds bounded work execution. Its canonical additive asset and behavior
list lives in `manifests/level-1.yml`; the prose definition lives in
`docs/maturity-model.md`.

Optional pull-ins should not be installed just because they exist. Use
`manifests/optional-assets.yml` and the Harness Fit Proposal to justify their
value, cost, and revisit signal.

Harness-provided skills should avoid generic names that collide with platform,
personal, or team skills. Prefer names such as `harness-review`,
`harness-implement`, `harness-work-brief`, and `harness-diagnose`.

## Maturity And Completeness

The maturity model is diagnostic. Higher maturity is not automatically better.
A small repo may be healthiest at Level 0 or Level 1 for a long time.

`docs/maturity-model.md` owns:

- level definitions,
- harness failure signals,
- installation modes,
- asset completeness,
- behavioral completeness,
- level-specific "Add when" and "Move beyond when" guidance.

Do not describe a partial starter install as simply "Level 1" or "Level 2."
Record the target maturity, install mode, installed asset completeness,
behavioral completeness, deferrals, and revisit signals.

The levels describe common growth pressure, not a strict installation order. A
repo may add a narrow Stop hook during a Level 1 starter install, or add secret
guards from Level 3 before it needs a Level 2 context router, when the proposal
explains the evidence.

## Documentation Boundaries

The framework uses this distinction:

```text
docs/project/   # docs agents may read for product implementation work
docs/harness/   # docs agents read only when intentionally maintaining the harness
```

Project docs help agents change the product. Harness docs help agents change
the harness.

Normal product work should not route agents into `docs/harness/`. Harness work
should be intentional. An operator should explicitly point an agent at
`docs/harness/README.md` or a specific harness document when the task is to
modify the harness itself.

The repo entrypoint should state that ordinary work routes through the
canonical work source, installed skills, project docs, and local code.

The escalation ladder for harness-doc over-reading is:

1. omit harness docs from normal routing,
2. state the convention in the repo entrypoint,
3. add warning hooks if the problem repeats,
4. add blocking hooks only for recurring harm or sensitive files,
5. use sandbox or container separation only when risk justifies the machinery.

## Routing Surfaces

`AGENTS.md` is the repo operating entrypoint. It should answer:

- where work comes from,
- where the Agent Work Brief skill/template bundle lives,
- how to verify work,
- where project context lives,
- what files or operations are sensitive,
- which skills exist for implementation and review,
- where harness-maintenance docs live when explicitly needed.

`AGENTS.md` should contain only instructions that every agent in the repo needs
for ordinary work. It should stay short enough to function as a bootloader, not
an encyclopedia. Phase-specific workflow belongs in skills, deterministic
commands belong in scripts, product or domain context belongs in routed project
docs, and detailed engineering standards usually belong in focused docs,
review skills, hooks, tests, or examples.

During installation, treat an oversized or over-routed existing entrypoint as a
harness-fit signal. For example, an `AGENTS.md` with hundreds of lines,
historical notes, product strategy, one-off standards, or instructions that
apply only to rare tasks should usually be split into narrower surfaces instead
of copied forward as universal context.

`SPEC-MAP.md` is optional. Add it when there are enough product areas or docs
that agents need routing help. It should route product implementation work to
the smallest useful context and should not route to `docs/harness/`.

`CONTEXT.md` is not part of the starter harness by default. It can be useful as
a short domain glossary and semantic compression point when agents or humans
repeatedly misunderstand the same domain terms.

`docs/project/intent.md` is an optional Level 2 project-intent document, not a
default entrypoint dependency. When it exists, planning and value-sensitive
review skills may consult it for strategic, exploratory, product, or scoping
work. Ordinary implementation agents should read it only when the work brief
explicitly routes them there.

## Agent Work Brief

The Agent Work Brief is the central artifact of the starter harness.

It is the local executable form of work. It can be produced from a tracker
ticket, issue, PRD, chat request, or planning conversation. The external work
source can remain the team source of truth, while the brief gives agents a
stable shape to work from.

The brief should capture only the implementation and review context that
matters:

- what to build,
- what not to build,
- what boundary or interface is changing,
- what context to read,
- what trade-offs have been accepted,
- what human-required checkpoints exist,
- what evidence will prove the task is complete.

For most Level 0 and Level 1 work, the Agent Work Brief is the minimal plan. It
is not a planning transcript. The planning agent should distill context into
accepted decisions, constraints, source-of-truth references, and acceptance
evidence.

The canonical template lives at
`skills/core/harness-work-brief/work-brief-template.md`. Do not maintain a
second copy here.

Use tiers to avoid overloading small tasks:

- Tiny: contained bug fix, docs tweak, prompt copy change, or test-only
  cleanup. It may only need source, goal, context, verification, and done
  criteria.
- Standard: behavior change inside an existing pattern or interface. It should
  include goal, non-goals, context, verification, and done criteria.
- Complex: boundary/interface change, cross-area work, multi-session work,
  sequencing, migration/backcompat concern, or product/design ambiguity. It
  should include interface notes, accepted decisions, trade-offs, and
  acceptance examples when relevant.

Add the boundary/interface section when a task introduces, changes, or depends
on a public behavior, module interface, API, CLI, integration,
configuration/schema contract, schedule, job, file format, or other consumed
surface.

Add progress/divergence notes when work spans more than one session or departs
from the original expectation. If the brief was drafted in a temporary local
file, copy durable status, evidence, blockers, and accepted plan changes back
to the canonical work source before handoff.

Add human-required checkpoints when a human must clarify intent, approve a
plan, approve an interface, accept residual risk, or evaluate acceptance before
the work should move forward. Use checkpoints deliberately; too many gates
create decision fatigue, while too few allow semantic drift and hidden risk.

During planning, surface bounded choices:

```text
Recommended approach:
Alternative A:
Alternative B:
Trade-off:
Decision needed:
Default if human delegates the choice:
```

The planning agent should help the human make decisions, not bury the human in
undifferentiated options.

## Interface Thinking

The framework keeps one major design idea: boundaries matter more than
implementation details.

"Interface" can mean:

- API endpoint,
- CLI command,
- function,
- module export,
- service boundary,
- database-access boundary,
- UI component contract,
- job or worker input and output,
- file format,
- external integration surface.

Interfaces create task boundaries, reduce cognitive load, provide natural test
targets, support parallel work, and make review easier.

The harness should encourage interface design without forcing premature
abstraction. Define the smallest useful boundary for the current value, make
inputs and outputs clear, test behavior at the boundary, and allow the
interface to evolve when the project learns more.

## Validation

In this framework, validation is the umbrella activity for deciding whether the
work satisfies intent at acceptable risk. It has three recurring mechanisms:

```text
Verification:
  deterministic checks such as lint, format, typecheck, unit tests,
  integration tests, build/package checks, static analysis

Review:
  judgment-heavy checks such as scope fit, design fit, maintainability,
  security posture, over-engineering, and acceptance satisfaction

Human-required checkpoints:
  human clarification, decision, approval, or evaluation when the harness cannot
  own the product intent, trade-off, long-living decision, or residual risk
```

Mechanical verification should be automated as much as practical. Acceptance
evidence should be concrete enough for humans and review agents to evaluate
whether the change satisfies the intended behavior.

`scripts/repo-checks.sh` is the canonical deterministic checks entrypoint for a
target repo. It answers:

```text
What deterministic checks should run before claiming repo work is complete?
```

Hooks decide when checks run automatically. `repo-checks.sh` defines the repo's
local lint, typecheck, test, build, package, or static-analysis command set.

Even if `repo-checks.sh` runs on a Stop hook, hooks cannot fully verify:

- whether the implementation stayed in scope,
- whether the abstraction is warranted,
- whether a boundary fits the rest of the project,
- whether the human's intended feature was actually implemented,
- whether live behavior works in a particular environment,
- whether the acceptance examples are convincing.

The Agent Work Brief should include acceptance examples for externally visible
or boundary-level behavior. Examples should name the request, command, input,
expected output or side effect, and evidence.

## Hooks

The minimal hook posture is conservative. A starter install should not add
hooks just because hook adapters exist.

Add hooks when a failure is common, cheap to detect, and expensive enough to
prevent automatically. Start with narrow, high-signal checks:

- guard secrets or sensitive files,
- warn or block destructive actions,
- optionally run `scripts/repo-checks.sh` on Stop or pre-commit.

For broader Level 3 controls, the safety policy should also identify protected
paths, protected command families, ask/warn/block behavior, and whether an
operation is safe for the specific call, including whether a command can run
concurrently in the current context.

Do not add hooks that encode judgment better handled by review, are noisy, or
will be bypassed quickly.

When a repo uses multiple tools, keep shared policy in portable scripts and
docs. Tool-specific hooks should be thin adapters that call the same underlying
commands and enforce the same practical rules. When behavior cannot be
identical across tools, document the divergence in the adapter and explain its
effect.

## Review

A minimal review skill should be findings-led. It should prioritize:

- bugs,
- missed requirements,
- untested behavior,
- over-engineering,
- unnecessary dependencies,
- misuse of existing project patterns,
- unclear boundaries,
- interfaces that are too broad or too narrow,
- abstractions that are premature,
- implementation that exceeds or misses the brief.

Review is where many inferential checks belong. The harness should not force
every engineering principle into implementation instructions. Some standards
are better applied after the agent has produced a concrete change. Review
should also surface latent product, architecture, domain, priority, or risk
decisions that were not explicit in the brief and should return those decisions
to human ownership.

## Resteering

Resteering is feedback that changes the trajectory of the human-agent system
when new information shows that the work is drifting from intent, quality, or
acceptable risk.

At small scale, resteering can be a failed test, type error, hook warning, or
review comment that sends implementation back for correction. At larger scales,
it can be a human clarification, maintainability finding, production signal,
design review, or product evaluation that changes the plan, creates follow-up
work, or updates durable intent.

Resteering should inject enough new information to correct the trajectory
without flooding the active context. The goal is not perfection; it is enough
confidence that the work is complete for the current risk tolerance, with
residual risks made visible to the humans who own them.

## Maintainability Lifecycle

Maintainability should start as a periodic sensor, not a gate on every change.
Its purpose is to detect rot and turn recurring drag into bounded improvement
work.

The lightweight cycle is:

```text
observe signal -> classify debt -> decide whether to act -> create bounded repair work
```

The debt categories are:

```text
Technical debt:
  code structure, duplication, missing tests, unsafe abstractions,
  overly complex implementation

Harness debt:
  instructions, hooks, scripts, skills, or workflows that no longer help

Cognitive debt:
  humans and agents no longer share a clear model of what the system does

Semantic debt:
  docs, tickets, decisions, or requirements no longer match reality
```

Use the Level 4 guidance in `docs/maturity-model.md` to decide when a target
repo has enough repeated maintainability, harness, cognitive, or semantic debt
signals to add maintainability checks.

Tools such as repowise can help detect code smells, dead code, duplicate code,
or dependency issues. Treat their output as signal for inspection, not
automatic proof that refactoring is needed.

## Harness Governance

Every harness component should justify itself. The component brief template
lives at `templates/optional/docs/harness/component-brief.md`.

Use a component brief for new or evolving harness surfaces such as:

- `SPEC-MAP.md`,
- `CONTEXT.md`,
- `.harness.yml`,
- hooks,
- skills,
- tracker adapters,
- maintainability reports,
- structured outputs,
- unattended runners,
- harness docs.

`.harness.yml` is a possible future layer, not an immediate requirement. Add it
only when two or more harness mechanisms need the same settings, such as check
commands, protected paths, tracker settings, or maintainability tooling
configuration.

## Tracker Strategy

The harness should not fight the team's current work tracker at the start.

The practical strategy is:

- keep the existing tracker or work source as the team source of truth,
- avoid requiring tracker automation initially,
- use tracker APIs, CLIs, or MCP tools only when they clearly help seed or
  update the Agent Work Brief,
- define the work item contract independently of any specific tracker,
- add tracker adapters later if useful.

The Agent Work Brief provides the abstraction that keeps tracker decisions
reversible.

## Progressive Disclosure

Context windows are a limited working set, not a storage layer. The central
question is:

```text
Under what conditions does an agent need this information?
```

Related questions:

- Does this belong in always-loaded instructions?
- Should it live in project docs routed by task area?
- Is it better captured in the work brief?
- Can the agent infer it from local code patterns?
- Is it historical context that belongs in an ADR or decision log?
- Is it harness-maintenance context that belongs in `docs/harness/`?

Use four verbs for context movement:

- Select: load the smallest useful context for the current task, just in time.
- Write: persist decisions, state, evidence, or reusable guidance outside chat
  when future agents should not rediscover it.
- Compress: summarize older or broader context when a session grows too large,
  while preserving current objective, decisions, files, evidence, and next
  step.
- Isolate: keep delegated, review, or exploratory work in separate context when
  mixing it into the main session would add noise or bias.

These verbs are first a vocabulary for evaluating harness design. They become
mechanical only when a repo adds supporting mechanisms such as a context
router, handoff template, compaction convention, subagent workflow, or
orchestration runner.

## Inclusion Criteria

Something belongs in the harness when one or more are true:

1. multiple agents need it,
2. it prevents a repeated failure,
3. it protects secrets, data, production, or team coordination,
4. it reduces context required for common work,
5. it gives deterministic feedback,
6. it preserves decisions outside chat,
7. it defines a boundary that keeps work from sprawling.

Something probably does not belong when:

- the code already makes it obvious,
- it only applies once,
- it is a personal preference,
- it bloats implementation context,
- it tries to encode every engineering standard upfront,
- it does not have a clear owner or maintenance trigger.

## Starter Deferrals

The starter package should not begin with:

- `CONTEXT.md`,
- `SPEC-MAP.md`,
- `.harness.yml`,
- unattended runners,
- full PRD lifecycle,
- strict harness-doc blocking,
- always-on maintainability gates,
- automated documentation reconciliation.

Add these only when the maturity model signals, repo evidence, or human
preference justifies them, and record the decision in the Harness Fit Proposal
or installed harness docs.

## Summary

The agent harness framework starts from a small set of control surfaces:

- a tiny repo entrypoint,
- a local executable work brief,
- a canonical deterministic repo checks command,
- lightweight review guidance,
- lightweight implementation guidance when Level 1 is selected,
- optional safety hooks when signals justify them,
- optional project context routing,
- an optional maintainability feedback loop that starts manual.

The strongest idea is the Agent Work Brief. It converts external work into
agent-executable work, creates a natural moment for human-agent design
alignment, captures interface and boundary decisions when needed, and requires
concrete acceptance evidence for behavior changes.

Harnesses should evolve the way good code evolves: start small, respond to
observed signals, add the least structure that solves the real problem, and
keep removing or simplifying anything that stops earning its place.
