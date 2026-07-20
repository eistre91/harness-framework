# Prompt Engineering: Intent and Priorities

In 2023 and 2024, prompt engineering often felt like an esoteric magical art. If you wanted an LLM to perform well, you had to find the right words and the right structure. The process was vague, imprecise, and iterative, and everyone seemed to have a special technique for making the model do exactly the right thing.

Capable reasoning models need much less of that choreography. Many techniques designed around the limitations of earlier models are no longer necessary. Many of them simply waste time and context, and some can even make results worse.

Effective prompt engineering can be boiled down to two concepts: intent and priorities. Intent answers, "What should the agent accomplish?" Priorities answer, "What should guide its decisions along the way?" Together, they provide a framework for shaping prompts even as models and techniques change.

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

The second prompt reveals that durability is part of the desired outcome: the job and its result must outlive the original request. Without that why, an agent could plausibly choose an in-process background task that disappears when the process stops. The why becomes a decision rule the agent can apply as implementation unfolds.

Finally, I want to stress that the goal in communicating intent is not to specify every decision in advance. Intent is communicated well enough when the agent can act, recognize success, avoid adjacent wrong outcomes, and make ordinary local decisions without losing sight of what matters.

### Bidirectional Prompting

When your intent is still unclear, you do not have to clarify it alone. You can use an agent to help surface ambiguities, assumptions and decisions that you have not yet considered.

*Bidirectional prompting* refers to this collaborative shaping and discovery of intent. In practice, this means prompting an agent to engage in a deliberately structured, interview-style discussion.

Bidirectional prompting is most useful when unanswered questions could materially change the outcome, plan or implementation. A small, well-bounded task doesn't need it. The goal is not to discuss every possible decision; it is to make the next valuable slice of work clear enough for both you and the agent to begin.

Bidirectional prompting can also help with broad, high-level design discussions, but those discussions require care and restraint. It is easy to design too large a slice upfront and later discover that much of that effort was unnecessary or wasted.

An example prompt for using this technique might look like the following. The exact wording matters less than achieving the desired behavior.

> Ask me one question at a time to surface ambiguities, clarify my intent and identify decisions that could materially affect the plan or implementation. Ground questions in the codebase and documentation when what already exists might answer or impact the decision. Once you believe the next valuable slice of work is clear, summarize your understanding and any remaining assumptions so that I can confirm or correct them and identify anything that still needs discussion.

Bidirectional prompting is not about achieving certainty and resolving every possible implementation decision in advance. Trying to micromanage that way is terrible for humans and it's terrible for agents. You want enough alignment to narrow the space of plausible outcomes so that the agent is unlikely to drift into an implementation that seems reasonable but misses your intent.

A downside to bidirectional prompting is that it's difficult and exhausting. The technique will rapidly consume your attention and a long interview will tire you out. If the conversation drags on, it is easy for your eyes to glaze over and for you to start giving empty answers or to cede ownership to the agent. At that point you are no longer shaping shared intent; you are letting the agent shape yours.

### Examples and Templates

Sometimes the clearest way to communicate your intent is to show the agent the shape of what you want. That shape can be a complete example or a stub that leaves task-specific details open. Providing several examples in a prompt is commonly called few-shot prompting.

Complete examples communicate structure, content and level of detail. Stubs and templates communicate structure without anchoring the agent as strongly to one particular result, making them especially useful in reusable prompts and skills where the shape should remain consistent while the details change.

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

Treat the resulting prompt as a starting point. As you learn which backend concerns matter in your situation, update its priorities in later collaborative sessions.

### Guiding Reasoning

Chain-of-thought prompting is an older technique that asks a model to reason through a problem step by step before answering. It can still help some models and tasks, but it is not a good default for models trained to reason internally. Prescribing a detailed reasoning path can constrain the model to a worse approach than it would find on its own.

This doesn't mean leaving reasoning entirely unframed. If there are sources the agent must inspect, alternatives it should consider or checks it should perform before concluding, say so. Tell the agent what should inform its decision and what should validate its conclusion.

> Investigate the latency spike. Check the application logs, traces, deployment history and saturation metrics. Compare plausible explanations against those signals before concluding. Report the evidence supporting your conclusion and any uncertainty that remains.

This prompt directs the agent toward relevant evidence and makes the result reviewable, but it does not decide the order of investigation or require the agent to narrate its private reasoning.

When you need to understand a result, ask for the evidence that supports it, the assumptions behind it and the checks that were performed. Ask yourself: Am I prescribing these steps because the work must include them, or because I am trying to micromanage how the model thinks?

# Writing Notes

What lies below are my thoughts of what I might want to include in this article, or thoughts that maybe need to be stored to be incorporated later.

The practice of "spec-driven development" was developed out of these struggles. The thought was if only you had considered every possible branch of the design tree and made every possible decision, then surely the LLM would do exactly what you wanted. (Not really a big fan of current forms of SDD and we'll circle back to this later.) Is this worth having here or too much of a deter this early on?


The framework explicitly says that human intent is the initial input but must not be assumed complete. Research,
planning, implementation, or validation can reveal ambiguity, missing context, or decisions requiring another injection
of human intent.


With LLMs you need to be aware of all of this background information and communicate enough of it that the LLM is sufficiently aligned. You can lean on their latent knowledge to help here and should, but if the LLM confidently produces an incorrect output, most of the time the failure was in what you failed to communicate.


meta prompting (agents prompting agents) but maybe that belongs later as well if what we're doing right now is "how do I use one agent effectively"


As you learn more about how to use these tools effectively, both here in prompt engineering and the later lessons, you'll understand that an LLM producing bad outputs is rarely the fault of the model or the agent. It's all entirely within your control and responsibility and if you own that you'll be able to achieve a lot more.

  > Human intent begins incomplete. Prompting helps expose and shape it into an executable outcome; context supplies what
  > is needed to act; constraints and boundaries limit drift; evidence tests the interpretation; feedback resteers the
  > trajectory.

• The central questions are:

  - What outcome do I want?
  - Why do I want it—what problem am I solving?
  - What would prove I got it?
  - What plausible outcome would still be wrong?
  - What must not change?
  - What am I assuming that may not be obvious?
  - Which decisions can the agent make, and which should come back to me?

  Intent is communicated well enough when the agent can act, recognize success, avoid adjacent wrong outcomes,
  and know when to ask.

It might be later thing to expand on the other central questions of intent. I think for now, what do I want, what do I not want, and why do I want it is the meat. Things like "how do I recognize I have it?" or "What does it look like" are more like acceptance criteria questions and I think a practice in defining things effectively for a complex ask.


Should I spend a beat somewhere on "technique" vs "engineering"? It's like back in math class when you'd have a method, vs understanding the method. A technique is there to achieve an outcome, but on its own without understanding, it doesn't advance you anything. I'm trying to teach both here.


Bidirectional prompting is the iterative human-agent collaborative shaping and discovery of shared intent.
I haven't introduced the "human-agent" system concept yet. Should I introduce that framing earlier or is it okay to do later?
I do think it's my unique sauce and perspective.


Might want to split Prompt Engineering into two or more pages. Not sure. Will see how long it looks when done. But there might be an introductory quick read, high level. Then one on intent and then one on attention. What page length is easy for people to consume but still gives them enough to take away something valuable.



(We'll touch on this later, but you can use one agent to find things and then another to pare down. I still think judgement LLMs won't make the right call but they are useful filters.) (This note might move to a later chapter. Not sure it fits here or distracts from the section/lesson. Right now I think we're scoped on "how do I interact with one agent process well" vs "how do you layer agents into effective workflows and collaborative structures".)


Calling the section Priorities vs Perspective. Perspective might be better. Perspective implies priorities.
