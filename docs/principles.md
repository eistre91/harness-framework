# Principles

Audience: agents and maintainers changing this framework or fitting its assets
to a target repo.

Use when: deciding whether a harness component, document, adapter, skill,
script, or maturity claim earns its maintenance cost.

The following principles guide the framework.

### Relentlessly Pursue Value

Value is the goal; harness structure, metrics, checks, docs, and agent output
are only attempts to steer toward it. The harness should maximize human
leverage and help implementation pursue human-defined value, not admire its own
ceremony or produce work because it is easy to generate.

Every harness component should answer which repo need it serves now or what
specific failure it prevents. Every agent-executable task should stay aimed at
the smallest valuable outcome instead of broad cleanup, speculative
abstraction, or measurable-but-misaligned activity.

### The Harness Is A System Too

The harness is subject to the same failure modes as the codebase it supports. It
can rot, overfit old workflows, duplicate truth, hide complexity, accumulate
dead paths, and become too hard for humans or agents to understand.

Keep the harness fit to purpose, explicit, and easy to change. The harness
should satisfy KISS/YAGNI: do not introduce harness components, maturity levels,
automation, protocols, or adapters without demonstrated need. Add them when the
project has signals that justify them, and simplify or remove them when they
stop earning their maintenance cost.

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

Scope fit, interface quality, over-engineering, abstraction timing, and
acceptance satisfaction are not fully deterministic. The harness should provide
briefs, examples, and review skills that make judgment easier.

### Harness Docs Are Not Product Docs

Agents doing product work should not need to understand the harness internals.
Agents changing the harness should read harness docs intentionally.

### Start With Manual Sensors Before Automatic Gates

Maintainability and documentation drift matter, but noisy gates can damage
adoption. Begin with manual or periodic review, then automate once signals are
clear and detection is reliable.
