# Learning Course Maintenance

Audience: maintainers developing the learning course or intentionally reviewing
its conceptual relationship with the Agent Harness Framework.

Use when: shaping the course's scope or sequence, making a material conceptual
change to the course, or reconciling a possible tension between the course and
the framework. Do not use for ordinary framework maintenance or as part of the
published learning path.

## Course Purpose

`docs/learn/` is intended to grow into a complete course that develops the
mental models and judgment needed to understand why the Agent Harness Framework
works as it does. It teaches both the general ideas behind effective
human-agent systems and the reasoning that motivates the decision tests in
`docs/principles.md`.

The course must still stand on its own. Learners may want to improve their
agentic engineering practice without adopting or contributing to this
framework. The framework may appear as an implementation or example of the
course's ideas when that helps a lesson, but understanding the framework is not
a prerequisite for following the course.

## Relationship To Framework Sources

The course and framework have related but different responsibilities:

- `docs/learn/` owns the published teaching path and its pedagogical sequence.
- `docs/principles.md` owns the framework's normative decision tests.
- `docs/framework.md` owns the framework's conceptual shape and rationale.

The course develops ideas that the principles compress and the framework puts
into practice. It should not duplicate the framework documentation or teach the
framework asset by asset. Framework sources should not depend on course
material to be usable by maintainers.

## Context Routing

Keep the two ordinary paths independent:

- Course learners and ordinary course work should use the learning path and the
  material needed for the current lesson.
- Ordinary framework maintenance should use `docs/principles.md` and the
  task-specific framework sources routed by `AGENTS.md`.
- Intentional alignment work should begin here, identify the concept in
  question, and inspect only the corresponding lesson and framework sections.

Do not read the entire course during ordinary framework maintenance. Do not
load the framework documentation merely because a lesson teaches an idea that
also motivates the framework.

## Alignment And Drift

Alignment does not require identical coverage or wording. Pedagogical
sequencing, simplification, omission, and differences in abstraction may be
intentional and long-lived. A course lesson can prepare a learner for a
principle without naming it, and the framework can encode a decision test before
the course is ready to teach all of its motivation.

Treat a possible mismatch as a prompt for judgment, not an automatic sync
requirement. During an intentional alignment review, decide whether it is:

- an acceptable difference in audience, sequence, emphasis, or abstraction;
- a course claim that no longer reflects the underlying model;
- a framework principle or concept whose motivation has changed; or
- an unresolved contradiction that requires human judgment.

Reconciliation may update the course, the framework sources, or both. It may
also explain why a difference is intentional. If a material contradiction is
accepted temporarily, record it in `TODO.md` with the affected concepts,
reason for deferral, and a concrete signal for revisiting it.

Do not introduce an exhaustive course-to-framework mapping, an automated
semantic-alignment check, or a dedicated reconciliation skill unless repeated
maintenance work shows that the smaller path here is insufficient.
