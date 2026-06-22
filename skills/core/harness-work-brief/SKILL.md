---
name: harness-work-brief
description: Converts external work from a tracker, issue, chat, or planning notes into an Agent Work Brief that agents can execute. Use when turning user intent or a work item into implementation-ready scope.
---

# Harness Work Brief

Use when turning an external work item into an Agent Work Brief. Use
`work-brief-template.md` from this skill directory as the default template.

## Goal

Create a self-contained implementation-ready brief that contains the information
the implementing agent needs to do the work.

The conversation context, codebase understanding, and any provided source work
items together inform the intended work brief.

The planning agent may build up more context than the implementer needs.
Distill that context into only the relevant outcome, constraints, decisions,
source-of-truth references, and acceptance evidence. Do not copy the full
discussion into the brief. Record accepted decisions that affect implementation
or review; omit rejected options unless a reviewer must know them to avoid a
specific mistake.

The planning goal is to identify the smallest valuable outcome that satisfies
the user's intent. Apply KISS and YAGNI before implementation starts: avoid
speculative abstractions, broad cleanup, new dependencies, or extra process
unless they are necessary to deliver the requested value or prevent a concrete
failure.

If `docs/project/intent.md` exists, consult it for strategic, exploratory,
product, or scope-sensitive planning. Do not route ordinary implementation
agents to that document unless the resulting brief needs it for the task.

## When To Use A Brief

Create a brief for ambiguous, multi-session, acceptance-heavy, or
boundary/interface-changing work.

Use `work-brief-template.md` as the starting template for Agent Work Brief
content. Fill only the sections that reduce risk for the current task. For tiny
work, source, goal, value target, context, verification, and done criteria may be
enough. Use the non-goals, ambiguity, boundary/interface, and acceptance
sections when scope or behavior could otherwise be misunderstood.

Small, contained edits can use the ticket, issue, or chat request directly when
it already names the source, goal, scope, context, verification, and done
criteria clearly. Do not create a brief just because the template exists.

## Tiers

Classify by implementation risk, not by estimated lines changed.

- Tiny: contained bug fix, docs tweak, prompt copy change, or test-only cleanup.
  No public contract changes, one obvious owner or area, clear verification, and
  little ambiguity after reading the source work item.
- Standard: adds or changes behavior inside an existing pattern or interface.
  Acceptance is clear enough to implement, verification is focused, and the work
  does not require sequencing, migration, or new boundary design.
- Complex: changes or depends on a boundary/interface, crosses multiple owners
  or areas, needs multiple dependent steps or sessions, requires explicit
  sequencing/backcompat/migration thinking, or has product/design ambiguity that
  materially affects implementation.

Boundary/interface examples include public APIs, CLIs, modules, jobs, file
formats, external API use, schedules, configuration or schema contracts, secret
declarations, runtime integrations, and other surfaces consumed by code or
people.

## Process

### Phase 1: Assess And Shape

Decide whether the source work item is already executable. Do not assume every
source work item needs reshaping.

1. Inspect the source work item and only the repo docs/code needed to understand
   the likely scope.
2. Infer obvious defaults from existing patterns.
3. Classify the likely tier: Tiny, Standard, or Complex.
4. Check whether the work has enough clarity on outcome, scope, owner or area,
   constraints, verification, and done criteria.
5. If the work is already scoped well, preserve that scope and move to drafting.
6. Ask focused human questions only when the answer materially affects scope,
   interface, product design, sequencing, verification, or acceptance evidence.
7. Decide whether the work is agent-runnable. If acceptance, ownership,
   interface, access, or product judgment is unclear, split runnable work from
   human decision work.

This phase should end in one of these states:

- Ready as-is: draft the brief from the existing work item.
- Ready after clarification: incorporate the decision and draft the brief.
- Needs splitting: propose slices before drafting implementation briefs.
- Blocked by human decision: record the decision needed before implementation.

Split work only when a single brief would require multiple unrelated outcomes,
unresolved product decisions, cross-boundary sequencing, or verification that
cannot be completed in one coherent implementation pass. Prefer vertical slices
that each produce user-visible or system-verifiable value. Each slice should
have a clear outcome, boundary or interface, test surface, and dependency
relationship.

Present proposed slices before finalizing them when the split changes scope,
dependency ordering, or human/agent ownership. Challenge any plan that adds
structure, generality, dependencies, or cleanup outside the requested value.
Keep it only when the trade-off is explicit.

### Phase 2: Draft The Brief

Convert the shaped scope into a handoff artifact.

1. Use `work-brief-template.md` as the starting template.
2. Fill only the sections that reduce implementation or review risk.
3. Record tier, goal, value target, non-goals, context, implementation guidance,
   verification, docs impact, and done criteria.
4. Record only accepted decisions and trade-offs that affect implementation or
   review. Do not preserve the planning transcript.
5. Add the boundary/interface section when the work changes or depends on a
   public API, CLI, module, job, file format, external API use, schedule,
   configuration/schema contract, secret declaration, runtime integration, or
   other consumed surface.
6. Add progress/divergence notes when work spans more than one session or the
   implementation differs from the original expectation.
7. Record lightweight design guardrails when they reduce implementation risk:
   owning module or boundary, public interface callers/tests should use, what
   complexity should stay hidden, test surface, dependency or blocker state, and
   any obvious gravity-well risk.
8. Write durable briefs around behavior, interfaces, acceptance evidence, and
   source-of-truth files. Avoid brittle line numbers in long-lived briefs.

### Phase 3: Validate The Brief

Check that another agent could execute the brief without guessing.

- The tier, owner or area, behavior boundary, and context to read are clear.
- The smallest valuable outcome is explicit.
- Non-goals are clear enough to prevent scope creep.
- Verification is concrete and proportionate to the tier.
- Human-owned decisions are resolved or explicitly marked blocked.
- Complex work is sliced into independently verifiable units when needed.
- The brief avoids speculative structure, broad cleanup, and new dependencies
  unless the trade-off is explicit.

## Work Source

Do not leave work brief durability implicit. Use the canonical location named in
the repo entrypoint or current request.

If the canonical source is external, such as Jira, GitHub Issues, or Linear, use
it when the current agent session has working read/write access through an MCP
server, API, CLI, or browser workflow. If that source is unavailable, use the
repo's gitignored local fallback only as temporary draft state.

Do not commit local fallback brief instances. Before handoff, copy durable
progress, evidence, blockers, and accepted plan changes back to the canonical
source when access is available. If the team wants versioned in-repo briefs,
they should choose an explicit durable path such as `docs/work/` as the
canonical location instead of treating local fallback drafts as source of truth.

Committed repo briefs can be useful shared work records, but they also become
documentation that can go stale. When the canonical location is a repo path,
include enough source, status, owner, and progress context for later agents to
tell whether the brief is current, completed, superseded, or ready to archive.

## Acceptance Evidence

Require acceptance evidence for externally visible behavior, boundary/interface
changes, runtime or integration behavior, CLI/script behavior, secrets
management behavior, scheduled work, deployment behavior, or generated output
changes.

For secrets management behavior, ask for evidence around declarations, aliases,
permissions, redaction, and runtime wiring without printing, revealing,
inspecting, or directly handling secret values.

## Collaboration

Use this while planning with the human. The final brief should keep only the
accepted decisions, trade-offs, and constraints the implementer or reviewer
needs.

For each meaningful choice, provide:

- recommended default,
- why it fits the repo,
- trade-off,
- when to revisit.

The human owns product intent, trade-offs, and the risk of delegated choices.
The planning agent owns making the intent executable.
