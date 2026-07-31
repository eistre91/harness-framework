# Prompt Engineering: Intent and Priorities

If you own the agent's trajectory, the prompt is the first place you shape it: by communicating the outcome and what should guide decisions along the way.

Prompting can feel like an esoteric art: find the right words and structure, then iterate until the model behaves as intended.

Reasoning-capable models often need less of that choreography. Techniques designed to compensate for model limitations can waste time and context, or make results worse, when the selected model already handles the underlying reasoning well.

Effective prompt engineering can be boiled down to two concepts: intent and priorities. Intent answers, "What should the agent accomplish?" Priorities answer, "What should guide its decisions along the way?" Together, they provide a framework for shaping prompts even as models and techniques change.

The techniques in this lesson are applications of this framework, not rules to memorize. Use a technique when it helps communicate intent or direct the agent's priorities. If it does neither, it is probably just choreography.

## Intent

Your intent is the outcome you want and why it matters.

Models have gotten better over time at inferring intent from a prompt. Talking to early LLMs was like talking to a partner who never seemed to listen. You'd say one thing, they'd interpret it differently, and they'd do something else entirely.

But even the best models can only infer from what you communicate. When the distinction matters, close is not good enough.

The problem is that communicating intent is hard.

We humans struggle to communicate our intent even to one another. We carry assumptions we barely notice, make guesses about what other people know, and leave details out all the time. Even people who have known you for years and share a long history with you won't automatically understand what you mean.

On top of our existing communication struggles, LLMs and agents introduce two additional challenges.

First, LLMs draw on a broader body of learned knowledge than any individual human. But they do not know the particulars of your situation unless you provide them. When your prompt leaves a gap, a model will often resolve it using a plausible or common interpretation. That may be a good answer for the average case without being the right answer for your case.

Second, agents are designed to be task-completion machines. Faced with ambiguity, an agent will often resolve it and begin working rather than stop to ask a question. That bias toward action is useful, but it makes unstated assumptions dangerous.

How do we work with these constraints? By making the parts of our intent that matter explicit.

The central questions in defining your intent are:

- What outcome do I want?
- What plausible outcomes would still be wrong?
- Why do I want this outcome?

The purpose of the first is clear. Say what you want.

The second question distinguishes your situation from plausible defaults. It surfaces the assumptions that could lead the agent toward a reasonable but wrong interpretation.

People often don't consider the last question. The reason behind an outcome is usually specific to your situation. You should not expect the model to infer it reliably. Explaining why communicates design intent and gives the agent something to reason from when it encounters choices you did not anticipate.

Consider these two prompts.

> Move report generation to a background job.

> Move report generation to a background job because large reports are timing out web requests, and users need to be able to close the page and return later for the result.

The second prompt reveals a requirement implicit in the desired outcome: durability. The job and its result must outlive the original request. Without that why, an agent could plausibly choose an in-process background task that disappears when the process stops. The purpose behind the outcome exposes durability as a priority the agent can apply as implementation unfolds.

Finally, I want to stress that the goal in communicating intent is not to specify every decision in advance. Intent is communicated well enough when the agent can act, recognize success, avoid adjacent wrong outcomes, and make ordinary local decisions without losing sight of what matters.

### Bidirectional Prompting

When your intent is still unclear, you do not have to clarify it alone. You can use an agent to help surface ambiguities, assumptions and decisions that you have not yet considered.

*Bidirectional prompting* refers to this collaborative shaping and discovery of intent. In practice, this means prompting an agent to engage in a deliberately structured, interview-style discussion.

Bidirectional prompting is most useful when unanswered questions could materially change the outcome, plan or implementation. A small, well-bounded task doesn't need it. The goal is not to discuss every possible decision; it is to make the next valuable slice of work clear enough for both you and the agent to begin.

Bidirectional prompting can also help with broad, high-level design discussions, but those discussions require care and restraint. It is easy to design too large a slice upfront and later discover that much of that effort was unnecessary or wasted.

An example prompt for using this technique might look like the following. The exact wording matters less than achieving the desired behavior.

> Ask me one question at a time to surface ambiguities, clarify my intent and identify decisions that could materially affect the plan or implementation. Ground questions in the codebase and documentation when what already exists might answer or impact the decision. Once you believe the next valuable slice of work is clear, summarize your understanding and any remaining assumptions so that I can confirm or correct them and identify anything that still needs discussion.

Bidirectional prompting is not about achieving certainty and resolving every possible implementation decision in advance. Trying to micromanage that way is terrible for humans and it's terrible for agents. You want enough alignment to narrow the space of plausible outcomes so that the agent is unlikely to drift into an implementation that seems reasonable but misses your intent.

A downside to bidirectional prompting is that it's difficult and exhausting. The technique will rapidly consume your attention and a long interview will tire you out. If the conversation drags on, it is easy for your eyes to glaze over and for you to start giving empty answers or to cede ownership to the agent. At that point you are no longer building a shared understanding of your intent; you are letting the agent shape it for you.

### Examples and Templates

Sometimes the clearest way to communicate your intent is to show the agent the shape of what you want. That shape can be a complete example or a stub that leaves task-specific details open. Providing several examples in a prompt is commonly called few-shot prompting.

Complete examples communicate structure, content and level of detail. Stubs and templates communicate structure without anchoring the agent as strongly to one particular result, making them especially useful in reusable prompts and skills where the shape should remain consistent while the details change.

You do not always need an example. When the required shape is easy to describe, state it directly: who the result is for, what information it must contain and what form it should take. Specify only what serves the outcome; incidental formatting can constrain the agent just as strongly as incidental details in an example.

Examples make abstract intent concrete, but be warned: every included detail may attract the agent's attention. Highlight the aspects you want it to follow, or remove incidental details entirely.

### Prompt Positively

Lead with what you want. Positive requirements such as "I want X" give the agent a target to pursue. Negative requirements such as "I don't want Y" primarily rule out part of the space of possible outcomes.

Start by telling the agent what it should accomplish. Then add negative requirements that rule out plausible but unacceptable interpretations.

Consider this requirement:

> Don't spread validation logic throughout the service.

A stronger version provides a target as well as a boundary:

> Validate requests at the API boundary and return the existing validation error type. Do not introduce validation inside the domain model.

The goal is not to avoid negative requirements. Use them to protect important boundaries, but do not use a list of exclusions as a substitute for describing the outcome you want. Leading with the positive also forces you to understand your own intent instead of describing it only by exclusion.

## Priorities

Intent tells the agent what outcome to pursue. Priorities tell it what matters along the way.

A good prompt makes those priorities explicit and frames the agent's attention.

When a human is working, they may come across decisions or ambiguities they didn't anticipate. In that case, they may stop and re-evaluate their current task. On the other hand, agents tend to hold the current task tightly. That persistence helps them make progress, but it can also keep them pursuing a local objective after new evidence should cause the plan to change.

That persistence makes agents relentless, hyperfocused task-completion machines. That focus is a liability when aimed at an assumption instead of an open question, and a strength when the task and its priorities are well framed.

Let's say we're looking for performance issues in a codebase. Consider providing an agent with the following prompt.

> Find the performance issues in the service.

This is a bit like "leading the witness." You have told the agent that performance issues exist; its task is now to produce them. That framing makes it more likely to report issues without first deciding whether any are material.

Contrast that with the following.

> Assess whether this service has material performance risks. Ground each finding in a concrete code path and either measurements or explicit workload assumptions. If the evidence does not support a material issue, say so.

The first prompt implicitly makes producing findings the priority. The second makes materiality the priority and gives the agent a standard for deciding whether anything is worth reporting.

Communicating priorities gives an agent a lens: what to notice, what matters most and how to decide.

### Role Prompting

Role prompting is an indirect way of communicating priorities. Telling an agent to "act as a senior backend engineer" is a compact way to suggest the perspective you want it to take.

That shorthand can be useful, but it's also ambiguous. "Senior backend engineer" bundles together many possible priorities, practices, and assumptions. That still leaves the agent with a lot of latitude to decide which of those matter, and its plausible interpretation may not match yours.

When those possible interpretations could change the result, unpack the role and be specific. Instead of:

> Review this API as a senior backend engineer.

Tell the agent what you want that engineer to care about:

> Review whether clients can use this API correctly without understanding its internal implementation. Focus on naming, request and response consistency, error behavior and compatibility with existing clients. Ground each concern in a concrete example.

The role itself is not the important part. The important part is the lens you wanted the role to provide. If a role could reasonably imply different or broader priorities than what you need from that agent, make the priorities explicit.

### Meta Prompting

Sometimes you know the outcome but don't know how to express the priorities that should guide the agent. For example, what if you don't have significant experience as a backend engineer? You may not know what concerns are hidden inside that role.

In that case, ask an agent to help you write a prompt for a future agent. This is *meta prompting*. The first agent can combine its general domain knowledge with investigation of your codebase to surface relevant vocabulary, assumptions and questions for an initial prompt.

Bidirectional prompting is especially useful here. Let the agent ask questions that help you explore what a backend engineer might care about and determine which of those concerns matter for your task.

> Help me prepare a prompt for an agent that will review this API. I do not have backend engineering experience, so ask me one question at a time to identify which backend concerns matter for this service. Ground your questions in the codebase and documentation when possible. Once the task is clear enough, draft the prompt and identify any assumptions I should verify.

Treat the resulting prompt as a starting point. The agent can surface candidate priorities, but you still decide which serve your outcome. Update them as you learn which backend concerns matter in your situation.

### Guiding Reasoning

Explicit step-by-step reasoning prompts can help some model and task combinations, but they are not a reliable default. For reasoning models, prescribing a detailed reasoning path can constrain the model to a worse approach than it would find on its own.

This doesn't mean leaving reasoning entirely unframed. If there are sources the agent must inspect, alternatives it should consider or checks it should perform before concluding, say so. Tell the agent what should inform its decision and what should validate its conclusion.

> Investigate the latency spike. Check the application logs, traces, deployment history and saturation metrics. Compare plausible explanations against those signals before concluding. Report the evidence supporting your conclusion and any uncertainty that remains.

This prompt directs the agent toward relevant evidence and makes the result reviewable, but it does not decide the order of investigation or require the agent to narrate its private reasoning.

When you need to understand a result, ask for the evidence that supports it, the assumptions behind it and the checks that were performed. Ask yourself: Am I prescribing these steps because the work must include them, or because I am trying to micromanage how the model thinks?

The durable skill is not memorizing prompting techniques. It is making the outcome and priorities clear enough for the agent to act, then asking for evidence that lets you judge the result. A prompt begins that work, but it is only one part of the context shaping the agent.
