# Principles

Audience: agents and maintainers changing this framework or fitting its assets
to a target repo.

Use when: deciding whether a harness component, document, adapter, skill,
script, or maturity claim earns its maintenance cost.

The following principles guide framework maintenance and target-repo harness
design. The framework should follow them itself; installed harnesses should
carry them into target repos. A principle may point at different artifacts in
each context, but the same decision test should hold in both.

### Relentlessly Pursue Value

Value is the central principle.

Work produces value when it helps a real human or agent achieve a concrete
outcome.

Valuable work answers the question: who is better off, and how?

Apply that test to framework changes and to the target-repo outcomes each
installed harness helps deliver.

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

### Prefer Executable Evidence

Prefer executable evidence over documentation when determining current behavior.

Code and other executable artifacts show what the system does now. Documentation
can record why the system works that way, where it should go next, or which
gaps are known, but those records are not proof of current behavior.

When sources conflict, trust the artifact closest to execution for current
behavior and update the conflicting record.

### Descriptive Documentation Compresses

Good descriptive documentation provides durable guidance that saves recurring
inference cost. It should be slow-changing and avoid repeating implementation
details.

It is a compressed map of the system, not the territory. Keep it short and
rewrite or remove docs that duplicate what agents should inspect directly.

### Context Is Precious And Focused

Context is engineered working state for the current task. Agents work best from
a context window that is correct, complete enough for the current outcome, small
enough to stay focused, and oriented toward the next action.

Ask: does the agent have what it needs for the next action, without stale,
misleading, missing, or noisy material?

Remove incorrect context first, fill task-critical gaps next, then trim noise.
Split or hand off work when the scope no longer fits in a focused context.

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

When refining this principle, consider framing it as: separate harness concerns
from product concerns.

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
