# Minimal Agent Harness Framework

Date: 2026-06-14

This document defines a portable framework for applying a minimal agent
harness to a software repository.

The goal is not to install a large process system. The goal is to preserve the
smallest useful harness shape so it can be fitted to different repositories
and expanded only when the target repo proves that it needs more structure.

## Working Definition

A harness is the engineered control system around an agentic model that turns
short-lived, stochastic model sessions into reliable, inspectable,
long-horizon software work.

The important shift in this framework is to apply the same discipline to the
harness that we expect from application code:

- keep it small,
- make every piece justify its value,
- avoid speculative abstractions,
- add structure only when a real failure mode or coordination need appears,
- remove or simplify pieces that become maintenance burden.

In other words, KISS and YAGNI apply one layer up. A harness can accumulate
debt just like product code can.

## Context

Large agent harnesses can include many reusable ideas: skills, issue lifecycle
conventions, PRD flows, verification loops, context-routing docs, hooks,
review patterns, unattended runners, maintainability reports, and
documentation-audit workflows.

Those larger systems can be valuable for projects that have already grown
enough to need them. The target for this framework is different:

- a smaller project,
- any implementation stack,
- any work tracker or lightweight human-provided workflow,
- multiple humans and agents contributing together,
- a need to demonstrate value quickly to teammates,
- a desire to avoid selling a large agent-operating-system concept before
  people have seen practical benefits.

This means the starter harness must be modest. It should make agents better at
ordinary work immediately, while leaving clear extension points for later.

## Desired Outcome

The minimal harness should help a fresh agent:

1. orient quickly,
2. understand where work comes from,
3. transform external work into an executable local shape,
4. read only the context needed for the current task,
5. implement through verifiable steps,
6. avoid over-engineering,
7. produce mechanical and acceptance evidence,
8. support review of bugs, maintainability, scope, and design fit,
9. feed repeated failures back into harness, documentation, or code
   improvements.

The harness should not require the project to adopt any specific tracker,
language, framework, unattended runner, or mature domain-doc structure.

## Core Shape

The resulting core lifecycle is:

```text
bootstrap -> work brief -> implementation -> verification -> review -> feedback
```

A fuller version is:

```text
external work item
  -> agent work brief
  -> scoped implementation
  -> mechanical verification
  -> acceptance verification
  -> review
  -> closeout or follow-up work
  -> maintainability feedback when patterns repeat
```

The most important artifact is the **Agent Work Brief**. It becomes the local
abstraction that turns tracker tickets, issue comments, chat instructions, or
other external work sources into a shape that agents can reliably execute.

## Minimal Starting Layout

For an initial trial, the Level 0 default should be deliberately small. The
canonical file-level asset list lives in `manifests/level-0.yml`.

Conceptually, Level 0 provides:

- a repo agent entrypoint,
- a canonical verification command,
- a work brief template,
- a local harness owner manual,
- lightweight review guidance.

Optional pull-ins, depending on repo evidence and team tools:

- `docs/harness/component-brief.md`
- `docs/harness/maintainability.md`
- implementation or work-brief skills in `.agents/skills`, using
  self-explaining names such as `harness-implement` and
  `harness-work-brief` by default
- adapter-specific hook or settings files

The optional pieces should not be installed just because the template mentions
them. They should be added when the Harness Fit Proposal explains the value,
cost, and signal for each one.

## Maturity, Completeness, And Install Mode

Maturity level describes the behavior the repo is being fitted toward.
Installation completeness describes how much of the canonical manifest for that
level is actually installed or already satisfied. Installation mode describes
the shape of the install:

- `canonical`: install or adapt every required manifest asset and behavior for
  the target level unless an existing component already satisfies it.
- `starter`: install a deliberately partial subset with explicit deferrals.
- `overlay`: apply harness principles through existing repo conventions with
  little or no new asset creation.

Do not describe a partial starter as simply "Level 1." Use precise wording:

```text
Target maturity: Level 1 bounded work execution.
Installation mode: starter.
Installation completeness: partial, not full canonical Level 1.
```

Harness-provided skills should avoid generic names that collide with platform,
personal, or team skills. Prefer names such as `harness-review`,
`harness-implement`, `harness-work-brief`, and `harness-diagnose`.

## Project Docs And Harness Docs

One important distinction emerged:

```text
docs/project/   # docs agents may read for product implementation work
docs/harness/   # docs agents read only when intentionally maintaining the harness
```

Project docs help agents change the product.

Harness docs help agents change the harness.

Normal product work should not route agents into `docs/harness/`. Harness work
should be intentional. An operator should explicitly point an agent at
`docs/harness/README.md` or a specific harness document when the task is to
modify the harness itself.

We discussed whether a router should explicitly say "do not read harness docs
unless doing harness work." The current conclusion is that this is probably
unnecessary at the start. If normal entrypoints never route to harness docs,
agents are unlikely to spend context there.

The escalation ladder is:

1. omit harness docs from normal routing,
2. add an explicit convention if agents wander into them,
3. add warning hooks if the problem repeats,
4. add blocking hooks only for proven recurring harm or sensitive files,
5. use sandbox/container separation only when risk justifies the machinery.

This keeps the starter harness simple while preserving a possible future path
for stronger file access boundaries.

## AGENTS.md

`AGENTS.md` should be a table of contents and operating entrypoint, not an
encyclopedia.

It should answer:

- where work comes from,
- where the Agent Work Brief template lives,
- how to verify work,
- where product context lives,
- what files or operations are sensitive,
- which skills exist for implementation and review,
- where harness-maintenance docs live when explicitly needed.

It should not attempt to encode every engineering standard. Many standards are
better enforced by scripts, hooks, review skills, or focused project docs.

### Value

Fresh agents become useful quickly.

### Add When

Always. Some repo-level entrypoint is needed as soon as agents work in the
project.

### Keep Small Because

Large always-loaded instructions consume context, go stale, and encourage
agents to carry irrelevant process around during implementation.

## SPEC-MAP.md

`SPEC-MAP.md` is optional in the smaller framework.

Its job is to route product implementation work to the smallest useful context:

```text
If working on API routes, read docs/project/api.md.
If working on auth, read docs/project/auth.md.
If changing external behavior, read the relevant ADR.
```

It should not route to `docs/harness/`.

### Value

It prevents agents from reading too broadly or rediscovering where context
lives.

### Add When

Add it when there are multiple product areas or docs and agents need routing
help.

### Do Not Add Yet When

Do not add it when there are not enough project docs to route between. A
premature router becomes busywork and may create semantic debt.

### Trade-Off

Routing docs can save context, but they also create another file that must be
kept current. If the project is small enough that agents can inspect the file
tree and obvious local patterns, `SPEC-MAP.md` can wait.

## CONTEXT.md

The initial recommendation included `CONTEXT.md`, but the refined decision was
to omit it from the starter harness for the new project.

`CONTEXT.md` can be useful as a short domain glossary and semantic compression
point, but a target repo may not yet have enough domain complexity to justify
it.

### Value

It gives agents shared vocabulary and prevents recurring conceptual
rediscovery.

### Add When

Add it when agents or humans repeatedly misunderstand the same domain terms,
when tickets assume vocabulary that is not obvious from code, or when domain
language starts drifting.

### Do Not Add Yet When

Do not add it just because the template has one. If the current domain is
simple, the file would become another artifact to maintain without immediate
payoff.

## Agent Work Brief

The Agent Work Brief is the central artifact of the minimal harness.

It is the local executable form of work. It can be produced from a tracker
ticket, issue, PRD, chat request, or planning conversation. The external work
source can remain the team source of truth, while the brief gives agents a
stable shape to work from.

This lets the harness stay tracker-neutral. A project can use Jira, GitHub
Issues, Linear, chat, docs, or no formal tracker for a small task. The
agent-facing shape remains consistent.

### Why This Matters

Work trackers are optimized for human coordination, not necessarily for agent
execution. Tickets can be vague, political, incomplete, or written for people
who already know the context. Agents need an execution contract:

- what to build,
- what not to build,
- what boundaries are changing,
- what context to read,
- what trade-offs have been accepted,
- what evidence will prove the task is complete.

The brief is also the place where lightweight "grill me" behavior belongs. A
planning agent should use brief creation to surface ambiguities, ask focused
questions, propose alternatives, and help the human make decisions before
implementation begins.

The brief is not a transcript of that planning discussion. The planning agent
should distill its gathered context into the decisions, constraints,
source-of-truth references, and acceptance evidence that the implementation
agent and reviewer need.

The goal is not to turn every ticket into a full PRD. The goal is to get
agent, human, and future reviewer aligned enough that implementation work can
proceed with less ambiguity.

### Suggested Template

```md
# Agent Work Brief

Fill only the sections that reduce risk for the current task.

Source:
Owner:
Status: Draft
Tier: Tiny / Standard / Boundary-changing
Agent-runnable: yes / no / blocked by human decision

## Goal
What user or system outcome should change?

## Value / Scope Discipline
- Smallest valuable outcome:
- Why this scope is enough now:
- Extra structure, cleanup, abstraction, or dependency explicitly not justified:

## Non-Goals
What should not be changed?

## Ambiguities / Decisions
- Open ambiguity that blocks implementation:
- Decision made that affects implementation or review:
- Accepted trade-off the implementer or reviewer must know:

## Progress / Divergences
Use when work spans more than one session or the implementation differs from
the original expectation. Keep this current in the canonical brief location or
post it back there before removing a temporary local draft.

- Current status:
- Plan changes:
- Divergences from expected approach:
- Why the divergence was accepted:
- Blockers:
- Latest evidence:
- Next action:

## Boundary / Interface
Required only when adding or changing a boundary.

- New or changed interface:
- Inputs:
- Outputs:
- Error cases:
- Consumers:
- Dependencies:
- Explicitly not solving yet:

## Context To Read
- Files:
- Docs:
- Prior decisions:

## Implementation Guidance
- Preferred existing patterns:
- Constraints:
- Things to avoid:

## Verification
Mechanical:
- Commands:
- Negative proof for removals/moves/cleanup:

Acceptance examples:
- Given:
- When:
- Then:
- Evidence expected:

Docs impact: none / maybe / required

## Done When
-
```

### Tiers

To avoid overloading small tasks, the brief should have tiers.

Record the tier in the brief so later implementation and review can tell how
much planning depth was intended.

```text
Tiny:
  bug fix or obvious local change
  includes goal, context, verification

Standard:
  normal feature or behavior change
  includes goal, non-goals, context, verification, done criteria

Boundary-changing:
  adds interface section, alternatives/trade-offs, acceptance examples
```

The interface section is not required for every bug fix. It is needed when a
task introduces or changes a boundary, public behavior, module interface, API,
CLI, integration, or other surface consumed by other code or people.

The progress/divergence section is not a substitute for a formal long-term
state store. Its job is narrower: when a work brief is the executable unit for
the current task, keep enough current status, plan change history, evidence,
blockers, and next action for a future agent or reviewer to understand why the
work no longer looks exactly like the initial plan. If the brief was drafted in
a temporary local file, post the durable update back to the chosen tracker or
remote store before removing the local draft.

### Human Decision Guardrail

A common failure mode in agent-human collaboration is that the agent presents a
large confident plan, the human experiences decision fatigue, and the plan is
accepted without enough scrutiny. The cost is paid later as technical debt.

The brief-creation process should therefore surface bounded choices:

```text
Recommended approach:
Alternative A:
Alternative B:
Trade-off:
Decision needed:
Default if human does not care:
```

The planning agent should help the human make decisions, not bury the human in
undifferentiated options.

## Interface Thinking

The framework keeps one major design idea: boundaries matter more than
implementation details.

For many tasks, the most important design question is:

> What interface is this feature or change asking us to create or modify?

Here "interface" does not only mean a formal language construct. It can mean:

- API endpoint,
- CLI command,
- function,
- module export,
- service boundary,
- database-access boundary,
- UI component contract,
- job/worker input and output,
- file format,
- external integration surface.

Interfaces are valuable because they:

- create task boundaries,
- reduce cognitive load,
- help agents work locally,
- provide natural test targets,
- support parallel work by multiple people or agents,
- make review easier.

The harness should encourage interface design without forcing premature
abstraction. Agents often try to nail a final architecture too early. The
desired behavior is different:

- define the smallest useful boundary for the current value,
- make inputs and outputs clear,
- test behavior at the boundary,
- allow the interface to evolve when the project learns more.

This balances interface discipline with YAGNI.

## Verification

The framework separates verification into two categories.

```text
Mechanical verification:
  deterministic checks such as lint, format, typecheck, unit tests,
  integration tests, build/package checks, static analysis

Acceptance verification:
  concrete evidence that the requested behavior works and matches the brief
```

This maps to the broader distinction between computational and inferential
controls.

Mechanical verification should be automated as much as practical.

Acceptance verification should be structured so humans and review agents can
evaluate whether the change actually satisfies the intended behavior.

### scripts/verify.sh

`scripts/verify.sh` is the canonical verification entrypoint.

It answers:

> What does this repo consider basic verification?

It can be used by:

- agents before claiming done,
- Stop hooks,
- humans locally,
- CI,
- reviewers who want reproducible evidence.

Hooks answer when verification runs automatically. `verify.sh` defines what
verification is.

Keeping the verification contract in a script has several benefits:

- agents do not need to infer commands from README prose,
- hooks and CI can share the same entrypoint,
- command changes happen in one place,
- final reports can cite one canonical command,
- future stack-specific details stay behind a stable interface.

### What Hooks Cannot Fully Verify

Even if `verify.sh` runs on a Stop hook, not everything can be reduced to that
mechanical gate.

Hooks cannot reliably answer:

- whether the implementation stayed in scope,
- whether the abstraction is warranted,
- whether a boundary fits the rest of the project,
- whether the human's intended feature was actually implemented,
- whether live behavior works in a particular environment,
- whether the acceptance examples are convincing.

The Agent Work Brief should therefore include acceptance examples for
externally visible or boundary-level behavior.

### Acceptance Evidence

A central unresolved problem in agent work is:

> How do we know the agent implemented the feature we expected?

This cannot be answered fully deterministically. Humans also fail at this when
reviewing code. The framework's answer is to require concrete examples where
they matter.

For an API endpoint:

```text
Request:
Expected response:
Error case:
How verified:
Evidence:
```

For a CLI:

```text
Command:
Input/state:
Expected output:
How verified:
Evidence:
```

For an internal interface:

```text
Function/interface:
Input:
Expected output or side effect:
Test proving it:
```

This does not guarantee correctness, but it gives reviewers a concrete
behavioral expectation instead of forcing them to infer intent from a diff.

## Hooks

The minimal hook posture is conservative.

Start with:

- guard secrets,
- warn or block destructive actions,
- optionally run `scripts/verify.sh` on Stop or pre-commit.

At the checklist level, tool safety should identify:

- protected paths such as `.env*`, credentials, local databases, and private
  operator state,
- protected commands or command families such as destructive filesystem,
  database, deployment, or production-affecting actions,
- which operations should ask, warn, block, or remain manual,
- whether a command is safe to run concurrently for this specific call, not
  merely for the tool name.

Hook behavior should be cross-tool where practical. If a repo uses both Claude
Code and Codex, shared policy should live in portable scripts and docs, while
tool-specific hooks should be thin adapters that call the same underlying
commands and enforce the same rules.

Avoid aggressive hooks that create too much noise or interrupt useful
development flow before the project has proven that it needs them.

### Value

Hooks leave deterministic actions to deterministic tools.

### Add When

Add a hook when a failure is common, cheap to detect, and expensive enough to
prevent automatically.

### Do Not Add Yet When

Do not add a hook if it encodes judgment better handled by review, if it is
noisy, or if developers will quickly learn to bypass it.

### Trade-Off

Hooks are powerful because they fire without agent memory. They are dangerous
when they become noisy, slow, or too clever. The starter harness should favor
simple, reliable hooks over sophisticated control systems.

When behavior cannot be made identical across tools, document the divergence in
the relevant adapter and explain the practical effect on agents using that
tool.

## Review

A minimal review skill should be findings-led.

It should prioritize:

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
are better applied after the agent has produced a concrete change.

This reduces implementation context while still preserving quality pressure.

## Maintainability Lifecycle

The maintainability lifecycle should start as a periodic sensor, not a gate on
every change.

Its purpose is to detect rot and turn recurring drag into bounded improvement
work.

The lightweight cycle is:

```text
observe signal -> classify debt -> decide whether to act -> create bounded repair work
```

The debt categories discussed were:

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

### Value

It protects the project from entropy without slowing every feature.

### Add When

Add maintainability checks when repeated review findings, agent confusion,
large files, duplicate code, stale docs, or recurring verification failures
start appearing.

### Do Not Add Yet When

Do not add a full maintainability workflow before there are signals worth
tracking. Start with manual checks and simple notes.

### Tooling

Tools such as repowise may be useful for detecting code smells, dead code, and
duplicate code. These tools should be treated as sensors, not unquestioned
authorities.

DRY matters, but YAGNI balances it. Duplicating a little code while an
interface is still evolving may be better than extracting the wrong abstraction
too early.

## Harness Component Brief

Every harness component should justify itself using a small component brief.

```md
# Component Name

Value:
What failure does this prevent, or what capability does this unlock?

Use when:
When should an agent or human reach for this?

Add when:
What recurring signal proves the project now needs this?

Do not add yet when:
What would make this premature?

Cost:
What cognitive, maintenance, or workflow burden does this introduce?

Simplify/remove when:
What signs show this part has become harness debt?
```

This applies to:

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

The component brief is a guard against harness bloat.

## .harness.yml

`.harness.yml` was identified as an interesting possible future layer, not an
immediate requirement.

Its purpose would be shared machine-readable harness configuration.

Example:

```yaml
verify:
  default: ./scripts/verify.sh
  quick: ./scripts/verify.sh --quick

guards:
  protected_paths:
    - .env
    - .env.*
    - secrets/*
  block_secret_reads: true

tracker:
  system: jira
  work_brief_required: true

maintainability:
  command: null
  cadence: manual
```

### Value

It prevents scripts, hooks, and skills from duplicating configuration.

### Add When

Add it when two or more harness mechanisms need the same settings:

- scripts and hooks duplicate command lists,
- protected paths are repeated in multiple places,
- different agent modes need different verification behavior,
- tracker settings need to be consumed by scripts,
- maintainability tooling needs shared configuration.

### Do Not Add Yet When

Do not add it while simple scripts can hold the configuration. A config file
without multiple consumers is speculative abstraction.

## Tracker Strategy

The harness should not fight the team's current work tracker at the start.

The practical strategy is:

- keep the existing tracker or work source as the team source of truth,
- avoid requiring tracker automation initially,
- use tracker APIs, CLIs, or MCP tools only when they clearly help seed or
  update the Agent Work Brief,
- define the work item contract independently of any specific tracker,
- add tracker adapters later if useful.

This means the harness is tracker-neutral at the agent execution layer.

Possible tracker modes:

```text
tracker: jira
tracker: github
tracker: linear
tracker: markdown
tracker: chat
```

### Reasoning

Agents may work better with some tracker tooling than others, but adoption
matters. A starter harness should fit the team's current workflow before
arguing for different tools.

The Agent Work Brief provides the abstraction that keeps tracker decisions
reversible.

## Progressive Disclosure

The framework treats context windows as precious. Large context windows,
compaction, and broad document loading are signals that the harness may be
failing.

The progressive-disclosure question is:

> Under what conditions does an agent need this information?

Related questions:

- Does this belong in always-loaded instructions?
- Should it live in project docs routed by task area?
- Is it better captured in the work brief?
- Can the agent infer it from local code patterns?
- Is it historical context that belongs in an ADR or decision log?
- Is it harness-maintenance context that belongs in `docs/harness/`?

This is another place where KISS/YAGNI applies. Not every useful fact belongs
in the harness.

The framework uses four verbs for context movement:

- **Select**: load the smallest useful context for the current task, just in
  time.
- **Write**: persist decisions, state, evidence, or reusable guidance outside
  chat when future agents should not rediscover it.
- **Compress**: summarize older or broader context when a session grows too
  large, while preserving current objective, decisions, files, evidence, and
  next step.
- **Isolate**: keep delegated, review, or exploratory work in separate context
  when mixing it into the main session would add noise or bias.

These verbs are first a vocabulary for evaluating harness design. They become
mechanical only when a repo adds supporting mechanisms such as a context router,
handoff template, compaction convention, subagent workflow, or orchestration
runner.

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

## Harness Maturity Model

The framework uses a maturity model: a harness should not be applied as one
large package. It should be layered in as project conditions justify each new
surface.

This maturity model is not a status ladder where "higher" is automatically
better. A small project may be healthiest at an earlier level for a long time.
The point is to make the next useful layer obvious when the current harness
starts failing.

### Level 0: Table Stakes

This is the minimum required for agents to work in a repo without reconstructing
prior planning discussion.

Includes:

- a small `AGENTS.md`,
- a canonical verification command such as `scripts/verify.sh`,
- a basic Agent Work Brief template,
- a lightweight review checklist or skill.

Value:

- fresh agents know where to start,
- humans can hand off work in a consistent shape,
- agents know how to prove basic correctness,
- reviewers have a shared expectation for done.

Add when:

- agents are going to work in the repo at all.

Signs this is enough:

- tasks are small,
- the codebase is still easy to navigate,
- humans provide most context directly,
- agents can complete work without repeatedly asking where things live.

Signs to move beyond it:

- agents miss requirements from vague tickets,
- agents forget verification commands,
- reviewers repeatedly ask for the same evidence,
- work handoff depends too heavily on chat history.

### Level 1: Bounded Work Execution

This layer makes work more executable and reduces implementation sprawl.

Includes:

- tiered Agent Work Briefs,
- explicit non-goals,
- ambiguity and decision notes when product or interface choices affect
  implementation,
- boundary/interface sections for boundary-changing work,
- acceptance evidence standards,
- progress/divergence state in the canonical brief location when work spans
  sessions or departs from the plan,
- lightweight implementation guidance.

The additive Level 1 assets and behaviors are defined in
`manifests/level-1.yml`. Review guidance remains Level 0 because every
harness-managed change needs a review lens.

Value:

- agents understand what not to build,
- humans and agents align on trade-offs before implementation,
- interface decisions happen before code generation,
- review can compare the diff to a concrete brief.

Add when:

- tickets are often too vague for direct implementation,
- changes affect APIs, modules, CLIs, integrations, or other boundaries,
- human-agent planning conversations are repeating the same questions,
- agents overbuild beyond the user's requested value.

Signs this is enough:

- most work is still local,
- acceptance examples are easy to state,
- a human can still route context manually,
- there are not many product docs to navigate.

Signs to move beyond it:

- agents repeatedly read too much context,
- agents miss important local conventions,
- agents ask where relevant docs or modules are,
- task briefs become overloaded with routing details.

### Level 2: Context Routing

This layer introduces explicit product-context routing.

Includes:

- `docs/project/` for product docs,
- optional `SPEC-MAP.md`,
- optional `CONTEXT.md` if domain vocabulary has become meaningful,
- ADR or decision-log pointers when decisions matter for implementation.

Value:

- agents read the smallest useful context,
- product knowledge moves out of chat and into durable files,
- repeated conceptual explanations are compressed,
- implementation agents avoid navigating historical or harness docs.

Add when:

- the project has multiple product areas,
- agents repeatedly rediscover the same context,
- domain vocabulary causes confusion,
- docs exist but agents do not know which ones matter for a task.

Signs this is enough:

- context routing is short,
- agents rarely need more than the routed docs and local code,
- docs are current enough to reduce confusion,
- implementation context remains focused.

Signs to move beyond it:

- docs drift from code,
- agents read stale docs and make bad changes,
- maintainability problems recur across tasks,
- reviewers repeatedly identify the same code or documentation debt.

### Level 3: Deterministic Controls

This layer moves repeatable checks from agent memory into tools.

Includes:

- secret and sensitive-file guards,
- destructive-action warnings or blocks,
- tool-safety checklists for protected paths, protected commands, and
  ask/warn/block policy,
- Stop hook or pre-commit verification,
- CI parity with `scripts/verify.sh`,
- optional shared config such as `.harness.yml` once multiple mechanisms need
  the same settings.

Value:

- common failures are caught automatically,
- verification does not depend on agent memory,
- humans and agents share one command contract,
- safety boundaries are enforced consistently.

Add when:

- agents forget verification,
- contributors run different command sets,
- secret or local-state mistakes are plausible,
- the same mechanical failure appears in review or CI,
- scripts and hooks start duplicating configuration.

Signs this is enough:

- hooks are fast and quiet,
- failures are actionable,
- people do not routinely bypass the checks,
- mechanical defects are caught before review.

Signs to move beyond it:

- quality problems are not mechanical,
- code organization is degrading,
- documentation usefulness is degrading,
- agents close tasks but require too many review cycles.

### Level 4: Maintainability Sensors

This layer observes entropy without turning every change into a process-heavy
event.

Includes:

- manual maintainability checklist,
- periodic documentation audit,
- recurring failure ledger,
- optional tools for duplicate code, dead code, complexity, or dependency
  drift,
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
- humans no longer share the same model of the system,
- objective tools reveal duplicate, dead, or overly complex code.

Signs this is enough:

- maintainability work is periodic, bounded, and useful,
- sensors produce few false alarms,
- repair work is scoped as normal tickets,
- product delivery is not slowed by constant process.

Signs to move beyond it:

- multiple agents need to coordinate long-horizon work,
- work spans many short-lived sessions,
- verification itself needs orchestration,
- state is getting lost between agents.

### Level 5: Orchestration And Automation

This layer is for larger or more agent-heavy projects. It should not be part
of the starter harness.

Includes:

- PRD lifecycle,
- tracker adapters,
- structured final-output protocols,
- unattended runners,
- verifier agents,
- eval suites,
- harness modes,
- stricter file access controls.

Value:

- long-horizon work survives fresh-context sessions,
- multiple agents can coordinate through durable artifacts,
- verification reports become structured,
- the harness itself can be tested and improved.

Add when:

- humans are routinely decomposing large work into many agent tasks,
- agents are operating unattended or semi-unattended,
- ordinary final messages are not reliable enough,
- work state is too large for one session or ticket,
- harness behavior itself needs regression testing.

Do not add yet when:

- a human is still closely guiding most work,
- tasks are small enough for one agent session,
- a work brief and verification script solve most coordination needs,
- the team has not yet adopted the lower layers.

### How To Use The Model

The maturity model should be used diagnostically:

1. Start with the smallest layer that supports current work.
2. Watch for repeated failures or coordination costs.
3. Add the smallest next component that addresses the observed signal.
4. Keep the component brief for every new harness part.
5. Remove or simplify layers that stop earning their maintenance cost.

The model also allows partial adoption. A project might add secret guards from
Level 3 before it needs `SPEC-MAP.md` from Level 2. The levels describe common
growth pressure, not a strict installation order. When partial adoption is
chosen, record the target maturity, install mode, installed asset
completeness, behavioral completeness, deferrals, and revisit signals.

## Adoption Phases

The starter path should be phased so teammates can adopt practical value
without buying into the whole operating-system concept at once.

### Phase 0

- the canonical Level 0 assets from `manifests/level-0.yml`, or a starter
  subset with explicit deferrals when existing repo components already satisfy
  some behavior

### Phase 1

- the additive Level 1 assets and behaviors from `manifests/level-1.yml`, or
  selected Level 1 behavior with explicit "partial starter" wording
- acceptance evidence standard
- optional secret/destructive-action guards
- Stop hook or pre-commit integration for `scripts/verify.sh`

### Phase 2

- `SPEC-MAP.md` if project docs have grown
- project docs routing
- maintainability checklist
- optional docs-audit skill

### Phase 3

- `.harness.yml`
- tracker adapters
- stronger hooks
- structured final-output protocols
- maintainability tooling such as repowise

### Later

- unattended runners,
- eval suites,
- harness modes,
- file access blocking for non-secret but distracting areas,
- full PRD lifecycle,
- automated documentation reconciliation.

## Deferred Or Rejected For The Starter Harness

### Unattended Runners

Deferred. Valuable for larger long-horizon automation, but too much for the
starter harness.

### Full PRD Lifecycle

Deferred. The Agent Work Brief captures the immediate value at a smaller scale.

### `CONTEXT.md`

Deferred until repeated domain-language confusion appears.

### `SPEC-MAP.md`

Deferred until there are enough product docs to route between.

### `.harness.yml`

Deferred until multiple harness mechanisms need shared machine-readable
configuration.

### Strict Harness-Docs Blocking

Deferred. Omit harness docs from normal routing first. Add warnings or blocks
only if agents repeatedly waste context there or if sensitive files require
hard protection.

### Always-On Maintainability Gate

Deferred. Maintainability begins as a periodic or manual sensor. Automatic
gates should wait until they are accurate enough not to become noise.

## Harness Fit Proposal Schema

The canonical Harness Fit Proposal schema lives at
`templates/core/docs/harness/fit-proposal.md`. Do not maintain a second full
question list here. The proposal must capture the repo signals, existing
component decisions, skill or command conflicts, target maturity, installation
mode, installation completeness, work brief storage and fallback, verification
and validation, tests/lint-format/type-check decisions, deferrals, proposed
files, human decisions, and communication audit.

## Proposed First Artifact Set

The Level 0 trial default is defined in `manifests/level-0.yml`.

The additive Level 1 default is defined in `manifests/level-1.yml`.

Optional pull-ins are defined in `manifests/optional-assets.yml`. Install them
only when project readiness, repo evidence, or human preference justifies the
extra surface.

The package should not start with `CONTEXT.md`, `SPEC-MAP.md`, `.harness.yml`,
unattended runners, or a full PRD system.

## Summary

The minimal harness framework is not a large process. It is a small set of
control surfaces:

- a tiny repo entrypoint,
- a local executable work brief,
- a canonical verification command,
- lightweight implementation and review guidance,
- optional safety hooks,
- optional project context routing,
- an optional maintainability feedback loop that starts manual.

The framework's strongest idea is the Agent Work Brief. It converts external
work into agent-executable work, creates a natural moment for human-agent
design alignment, captures interface and boundary decisions when needed, and
requires concrete acceptance evidence for behavior changes.

The broader principle is that harnesses should evolve the way good code
evolves: start small, observe failure modes, add the least structure that
solves the real problem, and keep removing or simplifying anything that stops
earning its place.
