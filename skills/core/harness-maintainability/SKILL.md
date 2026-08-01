---
name: harness-maintainability
description: Coordinates bounded maintainability sensor runs that gather evidence, classify drift, record operator dispositions, and shape approved follow-up work without performing repairs. Use when recurring friction, code or architecture health, documentation drift, harness health, or human-agent comprehension needs investigation.
metadata:
  agent-harness-framework/claude-sync: agents-to-claude
---

# Harness Maintainability

Use when an operator authorizes a bounded maintainability run under the target
repo's selected maintainability policy.

## Purpose

Observe accumulated drift across work or sessions, leave a durable record, and
help the operator decide whether any finding should become bounded follow-up
work. Treat sensor output as evidence for judgment, not proof that repair is
needed.

This skill is a thin coordinator. It selects among already approved sensors and
guides their evidence into one reviewable result. Detailed sensor procedures
belong in repo-owned tools or specialist skills.

This skill does not install or reconfigure tools, broaden the approved audit,
change enforcement, mutate product code or documentation, implement repairs, or
create external tickets without separate explicit delegation.

## Required Inputs And Authority

Before starting, identify:

- the installed maintainability policy or equivalent source of selected sensor
  truth,
- the authorizing work surface and approved run scope,
- the exact selected sensor and its family,
- the observation window and repo surfaces in scope,
- approved mechanisms, evidence sources, and specialist skills,
- the operator or decision owner,
- the durable record destination, and
- any separate authority for external issue creation.

The record destination must survive chat and agent-context loss and local
workspace cleanup. Prefer the issue, ticket, Agent Work Brief, audit record, or
other durable surface that authorized the run. A local ignored draft can aid
continuity but does not independently satisfy this durability requirement.

If the policy, exact sensor, scope, read-only mechanism, or record destination
is missing or ambiguous, stop and obtain operator direction. Do not silently
substitute a broader family audit.

## Choose The Run Scope

When more than one approved sensor could run, recommend the smallest one that
addresses the strongest current signal, uncertainty, or risk. Consider the
named beneficiary, evidence quality, recurrence, likely consequence, runtime,
cognitive cost, noise, and known false-positive risk. Run only the exact sensor
the operator approves for this work unit.

Do not treat a request for a higher status label as evidence. A run needs a
concrete recurring or high-cost signal, or an operator-approved bounded
experiment into a named uncertainty or risk.

## Capability Boundary

Classify a mechanism by its purpose and effect:

- Maintainability Feedback observes broader health, trends, or accumulated
  drift and feeds later triage.
- Agent Action Boundaries guide, verify, or block a particular agent action or
  lifecycle transition.

The same detector may support both uses only when detection policy has one
source owner and each use declares its effect. A normal Maintainability
Feedback run is investigative and non-blocking; do not turn an observation
into a gate.

## Workflow

1. Read the selected maintainability policy and the authorizing work surface.
2. Restate the exact sensor, family, scope, observation window, mechanisms,
   evidence sources, expected cost and noise, limits, record destination, and
   findings-only authority.
3. If this is a supervised trial, present that proposal and wait for operator
   approval before running the mechanism.
4. Run only approved read-only commands, inspections, human checks, or
   specialist skills. Do not install tooling or inspect unrelated repo areas.
5. Link each significant observation to evidence. Record a clean result when
   the sensor inspected its claimed scope and found no retained finding.
6. Give each finding one primary debt category and optional secondary
   categories: technical, harness, cognitive, or semantic. Do not invent debt,
   severity, confidence, or priority scores.
7. For each finding, state concrete impact, affected surface, evidence quality,
   recurrence, known consequences, limits, uncertainty, and likely false
   positives.
8. Write the run result to the approved durable surface before claiming the run
   complete.
9. Present retained findings to the operator for disposition. Allowed
   dispositions are: investigate further; shape or create bounded repair work;
   accept for now; defer with a revisit signal; or dismiss as noise or
   unsupported.
10. For findings the operator approves for work shaping, help define a bounded
    outcome, scope, verification, and evidence links using the repo's normal
    planning practice. Do not perform the repair or create an external ticket
    unless that exact side effect was separately delegated.
11. Stop after investigation, recording, disposition, and approved work
    shaping.

## Durable Run Record

Follow the selected maintainability policy and the conventions of its approved
work surface. Write the durable record before claiming the run complete, and
obtain an operator disposition for every retained finding.

## Findings-First Output

Lead with retained findings, ordered by concrete impact. For each finding use:

```text
Finding: concise observation
Evidence: durable or source pointers
Classification: primary debt category; optional secondary categories
Impact and scope: affected surface and known consequence
Limits: uncertainty, blind spots, and likely false positives
Disposition: operator decision or pending decision
Follow-up: approved bounded work link, if any
```

Then report the exact sensor and scope, mechanisms used, clean areas or
unresolved gaps, runtime/noise/cognitive cost, durable record location, and
confirmation that no repair or undelegated external issue creation occurred.

This coordinator is an initial interface. Split or deepen it only after
repeated use reveals a stable sensor-specific seam that reduces context or
change cost.
