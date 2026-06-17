## Principles

The following principles guide the framework.

### Relentlessly Pursue Value

The harness should help agents deliver useful work, not admire its own
structure. Every component should answer what value it provides now or what
specific failure it prevents.

### KISS And YAGNI Apply To The Harness

Do not introduce `CONTEXT.md`, `SPEC-MAP.md`, `.harness.yml`, full PRD flows,
unattended runners, or structured protocols just because they are useful in a
larger system. Add them when the project has signals that justify them.

### Code Is The Source Of Truth

Documentation compresses truth or records intended direction. It rots quickly.
Prefer code, tests, scripts, and executable examples where possible.

### Documentation Is Compression

Docs are valuable when they reduce repeated inference cost. They are harmful
when agents must parse too much stale or irrelevant material before doing the
work.

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
