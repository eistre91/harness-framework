# TODO

This is a work record for deferred framework ideas, not active implementation
guidance. Use `docs/principles.md`, `docs/framework.md`,
`docs/implementation-guide.md`, `docs/maturity-model.md`, and the manifests as
the current source of truth.

## Deferred: PRD / Technical Design To Issue Pipeline

The current starter harness intentionally focuses on getting small loops right:

```text
work brief -> implementation -> verification -> review -> feedback
```

We have not yet designed a longer-horizon pipeline from product requirements
documents or technical design documents into individual issues and Agent Work
Briefs.

Why deferred:

- The starter harness should prove the small execution loop before adding
  larger planning machinery.
- PRD and technical design flows are likely higher on the maturity ladder,
  closer to orchestration and automation than Level 0.
- Premature process here could create harness debt before the team has evidence
  about how work decomposition actually fails.

Potential future shape:

- PRD or technical design document as the upstream intent artifact.
- Issue decomposition as human/team coordination.
- Agent Work Briefs as the executable unit for individual implementation loops.
- Review and feedback from those loops feeding back into the larger plan.

Signal to revisit:

- Work regularly spans multiple agent sessions or multiple issues.
- Humans repeatedly spend time decomposing PRDs or technical designs into
  agent-runnable work.
- Issues lack enough boundary, sequencing, or acceptance detail for agents to
  implement safely.

## Deferred: Harness Eval Suite

The framework should eventually include eval cases that test whether an agent
can apply the harness philosophy correctly, not just copy files.

Provenance:

- Walking Labs `learn-harness-engineering` includes a `harness-creator`
  skill with `evals/evals.json` covering starter harness creation, session
  continuity, harness assessment, verification workflow design, memory
  taxonomy, tool safety, context budgets, multi-agent coordination, lifecycle
  bootstrap, and scripted benchmark/report usage.
- Reference URL:
  `https://github.com/walkinglabs/learn-harness-engineering/tree/main/skills/harness-creator`
- The useful pattern is not the exact expected artifacts. Their evals assume
  `feature_list.json`, `progress.md`, `session-handoff.md`, and `init.sh`,
  while this framework centers repo fitting, Agent Work Briefs, and
  `scripts/repo-checks.sh`.

Why deferred:

- The starter framework needs real application trials before the evals can
  distinguish useful harness behavior from template compliance.
- Evals should reinforce the local philosophy: inspect first, propose a
  Harness Fit Proposal, install only justified assets, record deferrals, and
  avoid adding maturity for its own sake.

Potential future shape:

- A small `evals/` directory with scenario prompts, target repo fixtures or
  fixture descriptions, expected installed assets, and expectations.
- Cases for fitting Level 0 to a small repo, declining premature `SPEC-MAP.md`
  or `CONTEXT.md`, deriving `scripts/repo-checks.sh` from README/CI evidence,
  turning a vague issue into an Agent Work Brief, reviewing a change against a
  brief, and recommending higher-level controls only when signals justify them.
- A lightweight runner or checklist that reports whether the agent produced a
  coherent proposal, preserved tracker neutrality, separated mechanical and
  acceptance evidence, and documented intentional deferrals.

Signal to revisit:

- The framework has been applied to enough repos that repeated installation or
  review failures are visible.
- Humans want regression checks before changing templates, skills, manifests,
  or maturity guidance.
- The framework gains an installer or validator whose behavior needs
  representative scenario coverage.

## Deferred: Staged Level-By-Level Installation

The framework may need a more structured installation process where agents
install and validate one maturity layer at a time, even when inspection suggests
that multiple levels are eligible for the target repo.

Why deferred:

- The current guide still assumes a capable planning agent can inspect the repo,
  choose a target maturity, prepare one fit proposal, and install the approved
  shape.
- As the framework grows, handing the whole framework plus a target repo to an
  installing agent increases the chance that it misses required decisions,
  optional asset routing, entrypoint fit issues, project-intent handling, or
  validation steps.
- Level eligibility is not the same as installation readiness. A repo may show
  Level 2 or Level 3 signals while still needing a clean Level 0/1 foundation
  installed and verified first.

Potential future shape:

- Define an install pipeline such as inspect -> Level 0 proposal -> Level 0
  install -> validation -> Level 1 proposal -> Level 1 install -> validation
  -> selected higher-level pull-ins.
- Require a checkpoint after each level where the installing agent reports
  installed assets, deferrals, human decisions, communication audit findings,
  and whether the next level is still justified.
- Split the current implementation guide into phase-specific installer skills
  or checklists so agents do not need to hold the whole framework in one
  planning context.
- Treat selected higher-level assets as explicit pull-ins with local acceptance
  criteria instead of bundling them into one broad target-maturity install.

Signal to revisit:

- Installing agents miss optional assets, routing rules, or fit-proposal
  decisions when asked to install multiple maturity levels at once.
- Harness installs pass structurally but leave Level 0/1 behavior unclear.
- Humans have to repeatedly correct broad install proposals that conflate
  target maturity with immediate installation scope.

## Deferred: Skill Adaptation Guidance

Investigate whether installing agents need a short explicit policy for adapting
harness skill bodies.

Potential guidance:

- Preserve the core portable workflow semantics.
- Adapt repo-specific work sources, commands, context paths, risks, acceptance
  evidence, and storage policy.
- Keep platform-only behavior in adapters or mirrors rather than shared skill
  bodies.
- Record when an existing repo skill is merged, adapted, superseded, left alone,
  or deferred.

Signal to revisit:

- Installed skills repeatedly drift from framework intent.
- Agents overfit portable skills to one target repo.
- Installers are unsure how much repo-specific policy belongs in skills versus
  `AGENTS.md`, project docs, or platform adapters.

## Deferred: Primitive Phase Skills And Validation Schema

The framework now names `research -> plan -> implement -> validate` as
primitive agent work verbs, but only implementation, review, and work-brief
creation have concrete skill surfaces.

Why deferred:

- The primitive verbs are explanatory first and should not become mandatory
  ceremony for tiny work.
- Good research behavior is often repo-specific: shared utility locations,
  domain docs, RAG tools, dependency documentation, architecture records, and
  preferred source order vary by target repo.
- Validation result handling becomes more important in Level 5 orchestration,
  where agents may need to decide whether work can close, must iterate, or
  requires human approval.
- The formal session / attempt model is still deferred, so validation reports
  do not yet have a stable state model to attach to.

Potential future shape:

- Add a `harness-research` skill when repeated planning or implementation work
  suffers from missing context, duplicated investigation, or poor source
  selection.
- Define what research artifacts should contain: relevant code, docs, prior
  decisions, external references, repo conventions, risks, and open questions.
- Refine the formal attempt model so each execution pass can record actor,
  status, files touched, decisions, divergences, verification, acceptance
  evidence, blockers, and next action.
- Define a validation result schema, likely starting with `pass`,
  `pass with risks`, and `fail`, while deciding whether `blocked` and
  `needs human decision` are validation results, work-unit states, or both.
- Decide how human-required checkpoints are represented in briefs, validation
  reports, tracker comments, PRs, or orchestration stores.

Signal to revisit:

- Agents repeatedly implement before finding the relevant context.
- Research findings are useful but get lost between planning and implementation.
- Complex work needs independent verifier agents or structured validation
  reports.
- Humans need to explicitly approve residual risk before an agent can consider
  work done.
- Multiple attempts against the same work unit make current status or next
  action unclear.

## Deferred: Entrypoint Compatibility Audit

Installing agents should eventually push back more explicitly when an existing
repo setup conflicts with the harness philosophy instead of only adding the
selected harness assets.

Example signals:

- `AGENTS.md` is hundreds of lines long and no longer functions as a universal
  repo bootloader.
- Always-loaded instructions include product strategy, historical notes,
  one-off standards, or phase-specific workflow that belongs in skills, scripts,
  project docs, hooks, or review guidance.
- Multiple platform entrypoints duplicate or contradict shared behavior.
- Ordinary implementation agents are routed to harness-maintenance docs,
  project-intent docs, stale planning records, or broad doc trees by default.

Potential future shape:

- An installer checklist or skill that audits existing agent entrypoints before
  fitting the harness.
- Findings that recommend split, merge, defer, leave-alone, or human decision
  handling for conflicting instructions.
- A communication audit that reports what every agent truly needs to know
  versus what should be reached only by planning, implementation, review,
  diagnosis, or harness-maintenance phases.

Signal to revisit:

- Installed repos repeatedly keep oversized or contradictory `AGENTS.md` files.
- Agents read too much always-loaded context before ordinary implementation.
- Harness installs succeed structurally but preserve routing patterns that
  undermine focused context.

## Deferred: Structural Harness Validator

The framework may eventually include a validator that gives objective evidence
about whether a target repo has the expected harness surfaces installed and
coherent.

Provenance:

- Walking Labs `learn-harness-engineering` includes
  `skills/harness-creator/scripts/validate-harness.mjs`.
- That validator scores five subsystems: instructions, state, verification,
  scope, and lifecycle.
- The scoring is primarily structural: expected files exist, JSON parses,
  instructions mention startup/verification/state, verification scripts fail
  fast, and progress or handoff files mention blockers, evidence, and next
  steps.
- Reference URL:
  `https://github.com/walkinglabs/learn-harness-engineering/tree/main/skills/harness-creator/scripts`

Why deferred:

- This framework currently leans on acceptance and inferential evidence more
  than structural scoring.
- A presence check could accidentally reward installing more artifacts instead
  of fitting the smallest useful harness to the repo.
- The local maturity model is diagnostic and fit-based; higher maturity is not
  automatically better.

Potential future shape:

- Keep structural coverage separate from maturity fit.
- Check for the local core surfaces: repo entrypoint, chosen Agent Work Brief
  location, `scripts/repo-checks.sh`, harness owner docs, review guidance,
  documented deferrals, and acceptance evidence expectations.
- Report findings as advisory evidence, not as the definition of harness
  quality.
- Include explicit fit risks such as premature `SPEC-MAP.md`, duplicated
  platform policy, stale placeholder repo checks commands, or a second source
  of truth for work state.

Signal to revisit:

- Humans want a quick smoke test after applying the framework to a repo.
- Repeated installations miss the same required Level 0 surfaces.
- A future installer needs a post-install repo checks command.

## Deferred: Persistent Work State Model

The framework agrees with the principle that long-running agent work needs
durable state outside chat, but it does not currently prescribe a repo-local
state file.

Provenance:

- Walking Labs `harness-creator` scaffolds `feature_list.json`, `progress.md`,
  and `session-handoff.md`.
- The useful principle is explicit persistent state: active work, status,
  dependencies, evidence, blockers, and next steps survive individual agent
  sessions.
- The exact Walking Labs artifact shape may not generalize to large projects
  with multiple team members, issue decomposition, and collaboration across
  trackers.

Why deferred:

- The likely long-horizon shape for this framework is PRDs or technical design
  documents decomposed into issues, then into Agent Work Briefs.
- A single repo-local `feature_list.json` risks becoming a second source of
  truth and does not scale cleanly for many parallel contributors.
- The correct backing store may be an external tracker, a command-center style
  store, repo files, or a combination.

Potential future shape:

- Define the durable work-state contract independently of storage: source,
  owner, status, dependencies, active brief, evidence, blockers, next action,
  and review state.
- Preserve tracker neutrality so Jira, GitHub Issues, Linear, repo files, or a
  dedicated store can satisfy the contract.
- Make Agent Work Briefs the executable unit while allowing larger PRDs,
  designs, or epics to remain the upstream planning artifacts.
- Define how state flows from PRD/design to issue to brief to implementation
  evidence and review feedback.

Signal to revisit:

- Work regularly spans multiple issues, sessions, or agents.
- Humans repeatedly reconstruct current state from chat, commits, or scattered
  comments.
- The PRD/design-to-issue pipeline is designed enough to decide where durable
  state should live.

## Deferred: Multi-Agent Coordination Details

Level 5 now names multi-agent coordination rules, but the framework has not
yet specified the detailed operating model.

Provenance:

- Walking Labs `harness-creator` includes a multi-agent coordination pattern
  covering coordinator, fork, and swarm modes.
- Its useful invariants are: the coordinator synthesizes instead of delegating
  understanding, worker prompts are self-contained, ownership boundaries are
  explicit, forked children do not recursively fork, and integration/review
  gates happen before claiming completion.
- Reference URL:
  `https://github.com/walkinglabs/learn-harness-engineering/blob/main/skills/harness-creator/references/multi-agent-pattern.md`

Why deferred:

- The starter framework should prove single-agent work brief loops first.
- Multi-agent machinery can create coordination overhead before work volume
  justifies it.
- The local framework needs to decide how multi-agent work maps to PRDs,
  issues, Agent Work Briefs, review independence, and durable state.

Potential future shape:

- Add a Level 5 guide for coordinator-led work: research, synthesis,
  implementation slices, integration, independent review, and closeout.
- Require explicit ownership boundaries by file, module, interface, or issue.
- Require self-contained worker prompts that include the relevant synthesized
  context rather than vague references to prior findings.
- Define integration gates: canonical verification, acceptance evidence,
  review findings, and state updates before work is considered complete.
- Treat reviewer agents as independent contexts when practical.

Signal to revisit:

- Humans are routinely decomposing large work into many agent tasks.
- Agents duplicate each other's research or step on overlapping files.
- Work cannot be completed reliably in one agent context or one brief.

## Deferred: Formal Session / Attempt Model

The framework currently treats the Agent Work Brief as the executable unit of
work and allows temporary local drafts, but it does not define a formal model
for repeated sessions or attempts against the same brief.

Provenance:

- Walking Labs `harness-creator` uses `progress.md` and
  `session-handoff.md` to make agent sessions resumable.
- The useful principle is that an agent work episode should leave behind
  enough status, evidence, blockers, decisions, and next action for a later
  agent or human to resume without relying on chat history.

Why deferred:

- The local framework does not yet define the larger durable work store.
- Session or attempt records may belong in Jira, a remote store, a PR, repo
  files, or a future command-center style system.
- Adding local session files too early could create drift from the chosen
  source of truth.

Potential future shape:

- Define "session" as one agent or human work episode against a brief, issue,
  or implementation slice.
- Define "attempt" as a resumable execution record with actor, time, objective,
  files touched, decisions, divergences, verification, acceptance evidence,
  blockers, and next action.
- Decide how attempts relate to Agent Work Brief status, PR history, review
  findings, and long-horizon PRD/issue state.
- Keep temporary local handoff files optional unless the target repo chooses
  repo-local work artifacts as the durable store.

Signal to revisit:

- Multiple agents or humans make several attempts against the same brief.
- Reviewers cannot tell why the implementation diverged from the original
  plan.
- Work pauses frequently enough that current status and next action are lost
  between sessions.
