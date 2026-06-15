---
name: documentation-quality-audit
description: "Audits docs for semantic debt: stale, misleading, duplicated, over-routed, too historical, or no longer useful to agents and humans. Use when checking whether documentation still helps current work or is misleading agents."
maturity: level-4
install_when: Docs route agents, docs are drifting, agents are misled by prose, or maintainability reviews repeatedly find documentation debt.
repo_specific_adaptation: Active doc paths, historical/provenance paths, source-of-truth code areas, doc routing maps, and approval rules for removal.
---

# Documentation Quality Audit

Use when auditing whether documentation still helps current work.

## Goal

Protect future agents and humans from bad context. Keep docs only when they
provide useful task-specific orientation, durable vocabulary, decision
rationale, source-of-truth routing, or actively maintained operator guidance.

Code, tests, schemas, scripts, generated artifacts, and ADRs are often closer
to source of truth than prose. Treat docs as maintained routing and compression
interfaces, not as harmless storage.

Documentation quality work is broader than deletion. The job is to control
semantic debt: documentation that still looks authoritative while it no longer
compresses current reality, routes agents to stale context, preserves obsolete
plans, duplicates code or tests, or hides binding decisions inside historical
narrative.

## Core Question

Does this document save meaningful inference for a specific audience, or has it
become semantic debt?

## Core Principles

- Name the audience precisely: agents changing a feature, operators running a
  workflow, maintainers deciding a trade-off, or humans onboarding to a domain.
- Treat documentation audits as interactive reviews with the operator, not
  one-shot cleanup. Surface judgment calls before editing.
- Prefer progressive disclosure over broad reading lists.
- Remove planned, historical, or stale docs from active routing paths.
- Avoid current-status dashboards in general-purpose docs. Work trackers,
  issues, PRDs, or briefs should describe current work.
- Keep source-of-truth distance short. A doc that duplicates code without
  compressing it should usually be removed, moved, or shortened.
- Preserve ADRs and decision logs for durable decisions, but do not make agents
  read them by default unless the task needs that decision context.
- Convert event history into current guidance. Active docs should state the
  resulting rule, invariant, boundary, or task route.
- Omit generic engineering advice and framework facts that a reasonable agent
  can infer or find in official docs. Keep project-specific, high-blast-radius,
  recently changed, counterintuitive, or trade-off-heavy guidance.

## Classify Docs

- active routed docs,
- historical/provenance docs,
- ADRs and decision logs,
- work records such as PRDs and issues,
- production/project docs,
- agent or harness docs.

Active routed docs should answer:

```text
What is true now, what must I preserve, and where do I go next?
```

Historical docs can remain useful for provenance, audits, or explaining why a
rule exists, but they should not be required reading for normal implementation
work.

PRDs, issues, work briefs, and verification reports are work records. They
should not remain the stable home for current rules after the work is absorbed
into production docs, project docs, agent docs, or code.

## What Must Be Explicit

Document these in active routed docs because agents cannot reliably infer them
from general training data:

- project-specific invariants, lifecycle boundaries, and domain language,
- non-obvious ownership or source-of-truth routing,
- decisions with valid alternatives, especially product or architecture
  trade-offs,
- recently changed behavior likely to conflict with older docs or habits,
- high-cost mistakes such as destructive commands, migrations, auth, external
  side effects, branch policy, provider receipts, or data retention,
- local exceptions to common practice,
- capability, runtime, or environment requirements needed before work starts.

## What To Leave Out

Remove, compress, or move these out of active routed docs:

- generic engineering advice unless the project has a specific command,
  contract, or exception,
- framework or library facts better covered by official docs,
- chronological issue, PRD, report, or chat history when only the current rule
  matters,
- implementation details already clear in code, tests, schemas, scripts, or
  generated artifacts,
- completed-work inventories and status notes that will drift outside work
  tracking,
- long reading lists that do not tell the agent which source to read first for
  a concrete task.

## Routing Map Drift

When a repository has multiple documentation maps or indexes, check that they
still have distinct jobs. For example:

- glossary or context docs own vocabulary and mental model,
- domain or decision maps route durable product decisions, ADRs, and
  provenance,
- implementation maps route agents who are actively changing code to relevant
  area briefs, modules, source files, gotchas, and guardrails,
- area briefs compress implementation invariants and source-truth pointers for
  one product concept without duplicating broad history.

Flag drift when one map becomes a live roadmap, status board, duplicated
implementation checklist, or broad reading list.

## Compression Standard

When historical evidence led to a current rule, write the rule first and move
the chronology out of the active path.

Bad active guidance:

```text
PRD 123 fixed issue 456 after verification found missing metadata.
```

Good active guidance:

```text
Current rule: follow-up work items must name their parent work item, branch or
target surface when relevant, role, acceptance criteria, and blocker state.
```

If provenance still matters, add one short pointer to the ADR, decision log,
historical note, PRD, issue, or work brief rather than embedding chronology.

## Check

- stale claims,
- duplicated code truth,
- obsolete plans,
- broad reading lists,
- docs routed to the wrong audience,
- chronological history where a current rule would be better,
- missing source-of-truth pointers.

## Workflow

1. Inventory one docs area at a time.
2. For each doc, identify its audience, task trigger, source of truth, and
   whether it is active, planned, historical, provenance, or operator-only.
3. For questionable docs, compare claims against code, tests, package scripts,
   UI behavior, generated artifacts, and current project docs.
4. Classify each doc as keep, simplify, move, merge, or remove.
5. Ask whether the doc earns maintenance:
   - Does it save meaningful code reading?
   - Does it orient a specific task audience?
   - Is it less likely to drift than the source it describes?
   - Would just-in-time documentation be better?
   - Does a future agent need this before acting, or is it only provenance?
   - Can chronological history be compressed into a current rule or decision?
6. Present review results before editing docs unless the user has already
   delegated the exact cleanup batch.
7. Ask which recommendations to apply when the next action is judgment-heavy.
   Treat remove, move, and merge recommendations as requiring operator approval
   unless that approval was already explicit.
8. Apply approved changes in small batches.
9. Update navigation and enforcement, such as `AGENTS.md`, README files, doc
   indexes, context maps, project docs, and tests that enforce doc routing.
10. Verify deleted or moved references with `rg`, and run relevant doc tests or
    mechanical checks when docs affect tests, scripts, imports, or generated
    surfaces.

## Output Format

For each doc, recommend one:

- keep,
- simplify,
- move,
- merge,
- remove.

For each reviewed doc, report:

- Document: path and purpose.
- Audience: current implied audience and better specific audience.
- Risk: stale, misleading, over-routed, duplicated, low-value, or missing.
- Source truth: code, tests, scripts, UI, generated artifacts, ADRs, or docs
  checked.
- Recommendation: keep, simplify, move, merge, or remove.
- Routing changes: links, indexes, maps, references, and tests to update.

Do not remove, move, or merge docs without human approval unless the operator
has explicitly delegated that batch.

## Change Guidance

Prefer deletion and routing cleanup over rewriting large docs. If a doc remains,
make its audience and trigger explicit near the top, and keep it short enough
that an agent can quickly tell whether it applies to the task.
