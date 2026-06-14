---
name: documentation-quality-audit
description: "Audits docs for semantic debt: stale, misleading, duplicated, over-routed, too historical, or no longer useful to agents and humans. Use when checking whether documentation still helps current work or is misleading agents."
maturity: level-4
install_when: Docs route agents, docs are drifting, agents are misled by prose, or maintainability reviews repeatedly find documentation debt.
repo_specific_adaptation: Active doc paths, historical/provenance paths, source-of-truth code areas, doc routing maps, and approval rules for removal.
---

# Documentation Quality Audit

Use when auditing whether documentation still helps current work.

## Core Question

Does this document save meaningful inference for a specific audience, or has it
become semantic debt?

## Classify Docs

- active routed docs,
- historical/provenance docs,
- ADRs and decision logs,
- work records such as PRDs and issues,
- production/project docs,
- agent or harness docs.

## Check

- stale claims,
- duplicated code truth,
- obsolete plans,
- broad reading lists,
- docs routed to the wrong audience,
- chronological history where a current rule would be better,
- missing source-of-truth pointers.

## Recommendations

For each doc, recommend one:

- keep,
- simplify,
- move,
- merge,
- remove.

Do not remove, move, or merge docs without human approval unless the operator
has explicitly delegated that batch.
