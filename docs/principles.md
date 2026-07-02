# Principles

Audience: agents and maintainers changing this framework or fitting its assets
to a target repo.

Use when: deciding whether a harness component, document, adapter, skill,
script, or maturity claim earns its maintenance cost.

The following principles guide framework maintenance and target-repo harness
design. The framework should follow them itself; installed harnesses should
carry them into target repos. A principle may point at different artifacts in
each context, but the same decision test should hold in both.

When framework maintenance or harness installation work appears to conflict
with these principles, challenge it explicitly: name the conflict, state the
trade-off, and get human approval before proceeding with the conflicting work.

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

Humans own trajectory: intent, priorities, product judgment, trade-off decisions
and risk acceptance.

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

Context is engineered working state for the current task. Every piece of
context spends attention: stale, misleading, missing, or noisy material
competes with the information the agent needs to act well.

Agents work best from a context window that is correct, complete enough for the
current outcome, small enough to stay focused, and oriented toward the next
action.

Ask: does the agent have what it needs for the next action, without stale,
misleading, missing, or noisy material?

Remove incorrect context first, fill task-critical gaps next, then trim noise.
Split or hand off work when the scope no longer fits in a focused context.

### Single Source Of Truth

Shared facts and behavior that are meant to stay consistent should have one
source of truth.

Before adding something new, ask whether the system already has a source of
truth that can be reused, updated, or pointed to instead. This prevents drift,
keeps the system internally consistent, and makes behavior changes easier to
localize.

### Interfaces Provide A Shared Language

A good interface creates a shared language humans and agents can use to
communicate about the system. It lets humans steer through concepts while
agents work with implementation details when needed.

Interfaces increase leverage when they hide meaningful complexity and reduce
the context callers must carry. Every interface should earn its keep: it should
improve human-agent collaboration, expose useful concepts, and not exist
speculatively.

### Mechanical Work Belongs To Deterministic Tools

Deterministic tools provide repeatable guarantees and useful feedback. Their
results should be readily available and hard to miss: easy for humans to run,
run by CI, and fed into the agent loop through scripts or hooks.

Good deterministic checks keep codebases healthy, ground agents in the current
system state, and allow agents to focus on bounded investigation,
implementation, repair, and synthesis while receiving valuable information.

Reach for deterministic tools like tests, type checkers, and scripts when a
requirement can be checked or performed mechanically. Do not rely on an agent to
remember, infer, or enforce when a tool could verify directly.

A deterministic check should still earn its cost: keep it regularly used, acted
on, and connected to real requirements, useful signals, or known failure modes.

### Judgment Needs Reviewable Evidence

Some important quality questions are not mechanically decidable: whether scope
fits the request, an interface feels natural, an abstraction is earned, or the
result satisfies intent.

Do not treat implementation as proof that those calls were resolved. Use
structured review to name the question, compare the result against the brief,
examples, and project patterns, and surface findings or human decisions when
evidence is missing or trade-offs remain.

Review does not make judgment deterministic. It makes judgment explicit,
inspectable, and easier to correct.
