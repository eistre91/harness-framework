# Harness Capability Map

Audience: agents and maintainers designing the framework or deciding which
harness outcomes a target repo should support.

Status: accepted target model; framework migration is pending. Until the
transition plan is completed, `docs/maturity-model.md`, the numbered manifests,
and the numbered installer checklists remain the active installation sources.
Do not install a target-repo harness from this document yet.

Use when: reasoning about the target shape that will replace the numbered
maturity model. The migration plan lives in
`docs/capability-map-transition.md`.

## Purpose

The capability map describes what outcomes an installed harness helps the
human-agent system achieve. It does not prescribe one universal progression or
rank repos by how much harness machinery they have.

The current map has one foundation with independent branches:

```text
Bounded Work  [foundation]
├── Focused Context
├── Agent Action Boundaries
├── Maintainability Feedback
└── Multi-Work Coordination  [emerging]
```

Each line from Bounded Work means that the dependent capability requires
Bounded Work. The prose for the dependent capability explains why. Future
capabilities may depend on a branch or on multiple existing capabilities; the
current hub-and-spokes topology is not a permanent constraint.

The Capability Map is the canonical owner of prerequisite relationships.
Implemented capability manifests project those relationships into executable
installer data; they do not independently define them. Manifest validation
must detect any disagreement between that projection and this map.

## Canonical Prerequisites

| Capability domain | Required capability domains |
| --- | --- |
| Bounded Work | None |
| Focused Context | Bounded Work |
| Agent Action Boundaries | Bounded Work |
| Maintainability Feedback | Bounded Work |
| Multi-Work Coordination | Bounded Work |

Changing this table is a capability-model decision. A manifest-only change
cannot add, remove, or reinterpret a prerequisite.

## Language

**Capability Domain**:
A bounded area of outcomes that the installed harness enables for the
human-agent system. A domain names what the system can do, not the mechanisms
used to do it.

**Harness Capability Map**:
The framework-wide set of capability domains and their prerequisite
relationships.

**Harness Profile**:
The target repo's current, deliberate set of realized and validated capability
claims, including selected scope, current realizations, supporting evidence,
and known limits. A profile includes every prerequisite of each claimed
capability.

**Realization**:
The target-specific combination of practices, assets, tools, and behavior that
supports a selected capability outcome.

**Known Limit**:
An explicit boundary, evidenced coverage gap, accepted trade-off, or unsupported
case in the current realization. A known limit can narrow a validated
capability claim; it cannot substitute for evidence that the claimed outcome
works in its selected scope.

**Profile Change**:
A candidate or approved addition, removal, or realization change proposed
against the current Harness Profile. Future intent belongs in a fit proposal
or other work record until the change is installed and validated.

Capability domains do not have universal completeness or maturity states. A
domain can have a clear boundary without a finite end state. A particular
installation change, approved scope, or validation run can finish, but the
framework does not claim that a repo has exhausted a capability domain.

## Capability Domain Shape

Each domain should answer only the questions needed to understand and select
it:

1. Outcome: what can the human-agent system do?
2. Value: who is better off, and how?
3. Boundary: what adjacent concerns does the domain not own?
4. Prerequisites: which capabilities does the framework require, and why?
5. Selection guidance: what observed signals or anticipated needs justify it,
   and when should it be deferred?
6. Validation: what evidence supports the selected capability claim?

Manifests and installer guidance own realization details and procedure. Assets
may support more than one capability domain; the map must not force a
one-asset-to-one-domain taxonomy.

## Bounded Work

Outcome:
The human-agent system can shape human intent into one coherently bounded,
agent-executable work unit, carry out and validate the work appropriate to its
outcome, and reach a reviewable completion decision without silently expanding
delegated authority.

Value:
Humans can delegate coherent scope while retaining trajectory and decision
ownership. Agents can make meaningful progress with explicit constraints and
produce evidence that supports acceptance, correction, or resteering.

Boundary:
Bounded Work does not select broader project context for each purpose, govern
arbitrary agent actions at execution time, discover accumulated
maintainability drift, or coordinate multiple work units toward a larger
outcome. A work unit may produce implementation, investigation, planning,
review, or another valuable outcome; it need not produce user-facing behavior.

Prerequisites:
None. Bounded Work is the foundation of every nonempty Harness Profile.

Selection guidance:
Select when agents will perform work in the repo. Defer the entire harness when
agent work is absent or too rare to justify durable harness surfaces.

Validation:
Use a representative work unit when available. Confirm that a fresh agent can
recover its intent and boundaries, carry out the appropriate work, produce the
required evidence, and reach a reviewable completion decision without relying
on hidden chat history.

Owned concept:
A **work unit** is one coherently bounded, agent-executable outcome with a
reviewable completion decision.

## Focused Context

Outcome:
The human-agent system can recover and load context relevant to the current
purpose without relying on chat history, repeatedly rediscovering project
knowledge, or loading broad irrelevant material.

Value:
Agents spend attention on the smallest useful context for the current action.
Recurring project orientation becomes durable and recoverable without turning
every document into universal context.

Boundary:
Focused Context does not define work scope, guarantee that every routed source
remains truthful, preserve general organizational memory, or coordinate
execution state across multiple work units. Durable context and routing are
means of achieving focus, not separate capability domains by default.

Prerequisites:
Requires Bounded Work because relevance is evaluated against a current outcome,
scope, phase, or decision boundary.

Selection guidance:
Select when agents repeatedly read too broadly, miss important local context,
rediscover the same project knowledge, or need predictable routing across
product areas. A greenfield repo may select it for a credible near-term
multi-area operating model, but should defer broad context infrastructure that
has no concrete use yet.

Validation:
Route a representative purpose from its work source to the smallest useful
current context. Record missing, stale, misleading, or unnecessarily broad
routes rather than claiming universal context coverage.

## Agent Action Boundaries

Outcome:
The human-agent system can keep selected agent actions within explicit,
repo-specific operating boundaries, steering, verifying, or preventing
consequential violations at the point where they occur while keeping known
limits visible.

Value:
Repeated or high-cost operational mistakes can be constrained where agents can
act on the feedback, reducing reliance on human memory and late review.

Boundary:
Agent Action Boundaries govern operational means such as commands, files,
artifacts, and lifecycle transitions. Bounded Work owns semantic delegation:
the authorized outcome, scope, non-goals, and completion evidence. This domain
does not promise comprehensive safety or justify installing every available
control.

Prerequisites:
Requires Bounded Work so operational restrictions augment an intentional work
lifecycle rather than becoming a speculative collection of gates.

Selection guidance:
Select an exact boundary when a concrete risk, recurring correction, or
operator decision justifies its friction. Defer controls whose cost, noise, or
bypass pressure would exceed their value.

Validation:
Demonstrate that each selected boundary acts at the intended lifecycle point,
produces actionable behavior, preserves expected safe paths, and states its
coverage limits honestly.

## Maintainability Feedback

Outcome:
The human-agent system can deliberately observe selected forms of accumulated
drift, preserve evidence for operator judgment, and turn approved findings into
bounded improvement work.

Value:
Technical, harness, cognitive, and semantic drift can become reviewable
evidence and intentional work rather than recurring review folklore.

Boundary:
Maintainability Feedback observes across work or over time; it does not govern
one current agent action, prove that repair is required, automatically repair
findings, or claim comprehensive system health. Raw findings and dispositions
belong to this domain; approved follow-up becomes Bounded Work.

Prerequisites:
Requires Bounded Work so operator-approved findings have a path into
intentionally scoped improvement work.

Selection guidance:
Select an exact feedback scope for a recurring or high-cost drift signal, or
for an operator-approved bounded experiment into a named uncertainty or risk.
Do not install a universal sensor stack merely because mechanisms exist.

Validation:
Run a supervised observation that stays within approved scope, produces
understandable evidence, leaves a durable record, supports operator
disposition, states cost and uncertainty, and does not perform undelegated
repair or gating.

Owned concepts:
A **finding** is reviewable evidence of possible drift. A **disposition** is
the operator's judgment about whether and how that finding should affect the
system's trajectory.

## Multi-Work Coordination

Status: emerging capability; no installable framework package is yet implied.

Outcome:
The human-agent system can decompose a larger outcome into multiple bounded
work units and coordinate their dependencies, progress, evidence, and
human-required decisions without losing the larger intent.

Value:
Larger work can survive separate agents, contexts, attempts, and validation
passes while humans retain ownership of strategy, priority, long-living
decisions, and acceptable risk.

Boundary:
Multi-Work Coordination begins when multiple work units must contribute to a
larger outcome. One work unit spanning multiple sessions, contexts, or attempts
is a more sophisticated Bounded Work realization. This domain is not general
portfolio management and does not make maximum autonomy an objective.

Prerequisites:
Requires Bounded Work because it composes and coordinates work units.

Selection guidance:
Select when larger outcomes repeatedly require separately progressing work
units, state or intent is lost between them, or coordination itself becomes
meaningful work. Keep it exploratory while one bounded work lifecycle remains
sufficient.

Validation:
Evidence should show that a larger outcome can be decomposed, progressed,
resteered, integrated, and evaluated across multiple work units without hidden
state or silent transfer of human-owned decisions.

Owned concept:
An **initiative** is one coherent, evaluable larger outcome that spans multiple
work units.

## Selection And Evolution

Brownfield selection normally begins from repeated or costly evidence.
Greenfield selection may begin from a credible anticipated operating need and
operator judgment. Both should name the expected outcome, cost, validation
approach, known limits, and revisit or removal signal.

Selection begins as a proposed Profile Change. A capability enters the current
Harness Profile only after its selected scope is realized and validation
provides evidence that the claimed outcome works. A failed or incomplete
validation remains in the proposal, installation record, or handoff; absence
of evidence cannot be recorded as a Known Limit to admit the capability into
the current profile.

Profile changes preserve dependency closure one approved change at a time. If
a proposed capability has an absent prerequisite, pause that proposal and
offer each missing prerequisite as a separate Profile Change. Install,
validate, update the current profile, and hand off the prerequisite before the
human decides whether to return to the dependent capability. Do not bundle an
uninstalled prerequisite into the dependent capability's approval.

Reject removal of a prerequisite while any current capability depends on it.
Remove or change each dependent capability through separately approved Profile
Changes before proposing removal of the prerequisite.

Installer, migration, and framework-maintenance procedures act on the
capability map but are not target-repo capability nodes. For example, an
entrypoint compatibility audit validates whether Bounded Work and Focused
Context are realized coherently; a recurring installed harness-health audit
may instead realize Maintainability Feedback.
