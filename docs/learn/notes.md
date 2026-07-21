# Unincorporated Thoughts

Note, just because an LLM can produce an output doesn't always mean that it should. This is a topic for us to return to later, but sometimes in software engineering, we learn something in producing an output and that learning is itself required for the continued success of the project.

Later cover chained workflows that interweave agents, measurements and deterministic checks. One agent might generate or find candidates while another critiques, ranks or narrows them. Agent evaluation can be a useful filter, but it should not be mistaken for final judgment or independent evidence.

Later connect operator skill to system design: when successful steering repeatedly requires the same move, encode it in the surrounding harness through focused context, constraints, deterministic feedback, reviewable evidence or human checkpoints. Reliability belongs to the whole human-agent system, not continuous expert supervision.

Explore spec-driven development as an attempted response to unreliable agent outcomes: if every branch and decision is specified in advance, perhaps the agent will produce exactly what was intended. Later discuss where this helps, where it becomes premature design, and why exhaustive specification cannot replace judgment and feedback.

Return to how intent and priorities evolve over a trajectory. A possible course-level synthesis: human intent begins incomplete; prompting helps expose and shape it into an executable outcome; context supplies what is needed to act; constraints and boundaries limit drift; evidence tests the interpretation; feedback resteers the trajectory. Research, planning, implementation, and validation can expose ambiguity, missing context, challenged assumptions, or decisions that require the human to clarify intent and redirect the work.

Later expand intent shaping for complex asks beyond outcome, adjacent wrong outcomes, and purpose. Cover acceptance evidence ("What would prove I got it?"), protected boundaries ("What must not change?"), hidden assumptions, and delegation boundaries ("Which decisions can the agent make, and which should come back to me?"). Connect these to the idea that intent is sufficiently clear when the agent can act, recognize success, avoid adjacent wrong outcomes, and know when to ask.

Cover prompt structure as part of context engineering. When a prompt combines instructions, examples and source material, headings or delimiters can make the logical boundaries visible. Teach the durable principle—separating instructions from supplied material—rather than prescribing XML tags, Markdown headings or another syntax as required choreography.
