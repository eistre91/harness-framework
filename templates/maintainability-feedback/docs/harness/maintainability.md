# Maintainability Sensors

Audience: agents and maintainers selecting, operating, or reviewing the repo's
approved maintainability sensors.

Use when: a concrete recurring or high-cost signal, or an approved bounded
experiment, justifies observing accumulated drift across work or sessions.

This policy records only the sensors this repo selected. Framework sensor-family
definitions belong to the Level 4 manifest and installer, not here.

## Operating Boundary

Maintainability runs investigate, gather evidence, leave a durable record, and
help the operator shape bounded follow-up work. They do not repair findings,
perform broad cleanup, install or reconfigure tooling, change enforcement, or
create external tickets without separate explicit delegation.

Treat tool and review output as evidence for operator disposition, not automatic
proof that work is required. Classify a mechanism by purpose and effect: broader
health observation and later triage is Level 4; guiding, verifying, or blocking
a particular action is Level 3.

## Selected Sensors

Add one entry for each approved exact sensor. Remove unused prompts rather than
inventing values.

### <Sensor name>

- Family: <approved family ID from `manifests/maintainability-feedback.yml`>
- Why now and beneficiary: <current evidence, risk, or bounded experiment; who
  is better off and how>
- Intended debt categories: <one likely primary category and any possible
  secondary technical, harness, cognitive, or semantic categories>
- Repo and observation scope: <paths, work surfaces, sample, and time window>
- Mechanism and evidence sources: <approved existing commands, reports,
  inspections, human checks, or specialist skills>
- Trigger or cadence: <signal-triggered or periodic condition; do not prescribe
  a framework-wide schedule>
- Operator or decision owner: <role or person>
- Durable record destination: <canonical issue, ticket, Agent Work Brief, audit
  record, engineering-health system, or other approved persistent surface>
- Expected cost and noise: <runtime, cognitive cost, noise, and false-positive
  risk>
- Known limits: <blind spots, uncertainty, and interpretation limits>
- Supervised trial: <command or procedure, result, date, and operator review>
- Revisit or removal signal: <evidence that would change, pause, or remove this
  sensor>

Completeness applies only to the explicitly approved sensor scope. Do not imply
that every sensor family is installed or that Levels 2 or 3 are present.

## Run Records

Use the work surface that authorized the run by default. Choose another existing
surface only with operator approval. Do not create a second debt backlog when an
issue, ticket, work brief, audit record, review record, or engineering-health
system already owns the paper trail.

The durable record must survive chat and agent-context loss, remain available
after local workspace cleanup, and be recoverable from the canonical work source
or another approved persistent system. A gitignored local draft may support
same-workspace continuity but is not sufficient by itself.

Record:

- run scope and observation window,
- selected family and exact sensor,
- mechanisms and evidence sources,
- findings and evidence pointers, or a clean result or unresolved gap when no
  actionable finding is retained,
- one primary and optional secondary debt categories per finding,
- concrete impact and affected surface,
- known limits, uncertainty, and likely false positives,
- operator disposition for each retained finding, and
- links to approved follow-up work.

Allowed dispositions are investigate further; shape or create bounded repair
work; accept for now; defer with a revisit signal; or dismiss as noise or
unsupported. The repo's normal tracker or planning practice owns priority and
severity when a finding becomes work.

## Installed Workflows And Tools

- Coordinator: <installed `harness-maintainability` skill or equivalent>
- Specialist skills: <only specialists needed by selected sensors>
- Repo-owned tools and commands: <approved existing mechanisms>
- External issue-creation authority: <who may authorize it and where>

Do not add a tool, scheduler, hook, CI job, tracker adapter, or gate merely to
fill this section. Add mechanisms only when current evidence and operator
approval justify their cost.

## Deferred Sensors

List sensors considered but deliberately not selected, with the reason and a
signal for reconsideration. Do not copy the complete framework sensor menu.

- <Deferred exact sensor>: <reason and revisit signal>
