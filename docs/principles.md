# Principles

Audience: agents and maintainers changing this framework or fitting its assets
to a target repo.

Use when: deciding whether a harness component, document, adapter, skill,
script, or maturity claim earns its maintenance cost.

The following principles guide the framework.

### Relentlessly Pursue Value

Value is the central principle.

Work produces value when it helps a real human or agent achieve a concrete
outcome.

Valuable work answers the question: who is better off, and how?

This applies both to the framework as a maintained product and to the outcomes
each installed harness helps deliver.

Tasks that cannot name the concrete outcome they improve are speculative waste.
Defer, simplify, or remove them.

### Design For The Human-Agent System

The harness exists to make humans and agents together more capable than either
alone.

Humans own trajectory: intent, priorities, product judgment, and risk acceptance.

Agents drive progress: bounded investigation, implementation, verification, and
synthesis within delegated intent, explicit constraints, and reviewable evidence.

### The Harness Is A System Too

The harness is subject to the same failure modes as the codebase it supports. It
can rot, accumulate debt, and become too hard for humans or agents to understand.

Everything in a harness adds system surface area and should earn its maintenance
cost the same way application code does.

When changing the harness, ask: if this were application code, what engineering
concern would we notice?

KISS and YAGNI apply to the harness too. Add structure when a real failure mode
or coordination need appears. Simplify or remove structure when it stops serving
its purpose.

### Code Is The Source Of Truth

Documentation compresses truth or records intended direction. It rots quickly.
Prefer code, tests, scripts, and executable examples where possible.

### Documentation Is Compression

Docs are valuable when they reduce repeated inference cost. They are harmful
when agents must parse too much stale or irrelevant material before doing the
work.

### Context Is Precious And Focused

An agent's context window is a limited working set, not a storage layer. Good
context is correct, complete enough for the current task, small enough to stay
focused, and oriented toward the next action.

Bad context is usually worse than missing context, and missing context is
usually worse than noisy context. The harness should bias toward removing stale
or misleading claims first, then filling task-critical gaps, then reducing
irrelevant volume.

Too little context makes agents guess. Too much context creates context rot:
stale claims, irrelevant history, duplicated guidance, and noisy reading paths
crowd out the instructions and evidence that matter.

The harness should route agents to the smallest sufficient context and preserve
progress through explicit handoffs. Intentional compression into briefs,
handoffs, research notes, or validation reports is useful. Unplanned automatic
compaction is a failure of context engineering, not a planned workflow.

### Shared Behavior Has One Owner

This is drifting into being lower level than a principle.

The principle is that shared behavior has one owner. Behavior?

I think this should more be that there should be a source of truth
and where possible everything refers to that source of truth.
Do not duplicate source of truth.

Each reusable harness behavior, schema, template, or policy should have one
canonical home. Explanatory docs should point to that owner instead of
maintaining second copies. Use manifests for asset boundaries, the maturity
model for level definitions, skill bundles for executable workflows and
templates, scripts for mechanical command contracts, and adapters as thin
wrappers over shared behavior.

### Interfaces Are Natural Boundaries

Agents and humans work better when boundaries are explicit. Interfaces reduce
cognitive burden, support parallel work, and guide testing. But interfaces
should be allowed to evolve; do not overdesign them too early.

### Deterministic Work Belongs To Deterministic Tools

Linting, formatting, type checking, tests, secret guards, and static checks
should not rely on the agent remembering them. Put them behind scripts, hooks,
or CI.

### Judgment Belongs In Structured Review

What is this trying to say?

Did this arise out of the separation between what can be done deterministically
and that which cannot?

Scope fit, interface quality, over-engineering, abstraction timing, and
acceptance satisfaction are not fully deterministic. The harness should provide
briefs, examples, and review skills that make judgment easier.

### Harness Docs Are Not Product Docs

This might not need to raise to the level of a principle.

This is more guidance.

The principle might more be that we want clear separation of concerns.

Agents doing product work should not need to understand the harness internals.
Agents changing the harness should read harness docs intentionally.

### Start With Manual Sensors Before Automatic Gates

Automation prevents known failure modes in repeatable ways.

We write tests and run them because we know that software is better with them.

I think what I don't like here is that it focuses on adoption. Which is true but downstream of a principle.

The principle is that you shouldn't automate for the sake of automation. Everything should have purpose.

Maintainability and documentation drift matter, but noisy gates can damage
adoption. Begin with manual or periodic review, then automate once signals are
clear and detection is reliable.
