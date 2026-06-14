# Maintainability Signals

Audience: agents and maintainers periodically checking whether the repo or
harness is accumulating drag.

Use when: review repeatedly finds similar issues, agents are confused by the
same areas, docs mislead people, verification failures recur, or objective
tools report structural hotspots.

Use this as a lightweight periodic sensor, not a gate on every change.

## Debt Types

Technical debt:
- code structure, duplication, missing tests, unsafe abstractions,
  overly complex implementation

Harness debt:
- instructions, hooks, scripts, skills, or workflows that no longer help

Cognitive debt:
- humans and agents no longer share a clear model of what the system does

Semantic debt:
- docs, tickets, decisions, or requirements no longer match reality

## Objective Signals

Useful sensors may include:

- repeated verification failures,
- large or fast-growing source files,
- large or unfocused test files,
- duplicated code or docs,
- dead code or unused dependencies,
- complexity or dependency drift,
- churn hotspots,
- stale references found by search,
- recurring review findings.

Use existing repo tools first. Tools such as repowise can help detect code
smells, dead code, duplication, or dependency issues, but treat their output as
signal for inspection, not automatic proof that a refactor is needed.

## When To Create Follow-Up Work

Create bounded follow-up work when a signal repeats, blocks delivery, misleads
agents, or increases review cost.

Do not create broad cleanup work without a concrete symptom and owner. Do not
add new maintainability tooling during initial harness installation unless the
team explicitly wants that tool.
