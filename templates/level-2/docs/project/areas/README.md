# Project Area Briefs

Audience: agents changing product or project behavior.

Use when: creating or reading short implementer briefs for one product area,
module family, user workflow, CLI, integration, file format, or other repeated
implementation concept.

Project area briefs are routing and compression docs. They name the relevant
behavior, modules, invariants, caveats, and verification sources for a task.
They do not replace code, tests, schemas, the Agent Work Brief, ADRs, or deeper
project references.

## Route Ownership

`../../../SPEC-MAP.md` owns the project-area inventory, task-intent routing,
and source-of-truth order. This README owns only the area-brief shape.

Briefs should point to executable checks and focused searches instead of
repeating exact schema columns, route labels, UI copy, parser internals, or
generated output.

## Size And Shape

Keep each brief roughly 80 to 150 lines. Split it or move detail back to a deep
reference when it stops being quick to scan. Organize by product concept first,
then list important module seams inside the concept.

`Read first` should name the brief sections, module seams, tests, or exact doc
sections needed before editing. Broad project docs belong under `Deep
references` with a trigger that explains when to open them.

## Brief Template

```md
# <Project Area Or Product Concept>

Audience: agents changing <specific behavior>.

Use when:
- <task trigger>
- <task trigger>

Read first:
- <smallest required brief sections, module seams, tests, or exact doc sections>

Deep references:
- <long specs, ADRs, examples, or UI overview sections with triggers>

Important modules:
- `<path>` - <ownership>
- `<path>` - <surface, if relevant>

Core invariants:
- <durable rule>
- <durable rule>

Do not:
- <common wrong turn>
- <deferred behavior that should not be implemented accidentally>

Implementation notes:
- <best practices, source-of-truth caveats, repair evidence, module seams>

Useful tests and searches:
- `<command or rg pattern>`
- `<test file or module family>`

Update docs when:
- <trigger for future doc maintenance>
```
