# Spec Map

Status: draft / active / stale

Audience: agents and maintainers changing product or project behavior.

Use when: deciding which project-area brief and deep reference docs to read
before changing code. This map compresses current-state orientation; it does
not replace the work brief, source code, tests, schemas, ADRs, or project docs.

## How To Use

1. Start from the current Agent Work Brief or equivalent work source.
2. Find the closest task intent below.
3. Read the primary project-area brief when it exists.
4. Read only the listed deep references whose trigger matches the behavior
   being changed.
5. If no route fits, inspect code and tests for the likely owner, then report
   the missing route as a project-doc cleanup issue.

Optional deep references are not a checklist. They are purpose labels for the
next source to open only after the area brief is not specific enough.

If the repo has a domain glossary such as `CONTEXT.md` or a `docs/project/`
glossary, use its canonical terms in task intents and area briefs. Do not
redefine glossary terms in this map; route to the glossary when term meaning is
the context an agent needs.

## Boundary

This map describes current system orientation: where important areas live,
what agents will find there, and which local mental models, invariants, and
gotchas matter before editing. It does not record planned work, roadmaps, or
desired future behavior.

The current Agent Work Brief or equivalent work source owns the requested
change. Use this map only to find the current-state context needed to execute
that work.

Code, tests, schemas, scripts, and runtime behavior are authoritative for what
the system currently does. If this map conflicts with those artifacts, trust
the executable artifact and update or report the stale route.

Area briefs compress where to look and what invariants to preserve. They should
not duplicate exact schemas, route labels, generated output, or implementation
details that code and tests already own.

## Task Intent Map

| Task intent | Primary route | Optional deep references by trigger |
| --- | --- | --- |
| `<behavior, product area, module, workflow, CLI, integration, or file format>` | `docs/project/areas/<area>.md` | trigger: `docs/project/<reference>.md`; decision: `docs/adr/<id>.md`; examples: `<path>` |
| `<task intent without a brief yet>` | No standalone area brief yet. Start with `<owning code/tests/docs>`, then record whether a new area brief is justified. | trigger: `<deep reference>` |

## Update This Map When

- A project-area brief is created, renamed, removed, or superseded.
- A task intent consistently sends agents to the wrong primary route.
- A deep reference stops being the first useful next source for its trigger.
- A new product area, module boundary, CLI, integration, file format, or user
  workflow becomes common enough that agents need routing help.
- An ADR, durable project decision, or code change alters the current-state
  orientation or route for an area.

## Maintenance Notes

- Keep this map short enough to scan before implementation work.
- Prefer task-intent language that appears in issues, briefs, code, tests, or
  user workflows.
- Do not route ordinary implementation agents to broad historical docs by
  default.
- Broken links or missing routes should be reported in the installation handoff, work
  handoff, or follow-up issue rather than silently ignored.
