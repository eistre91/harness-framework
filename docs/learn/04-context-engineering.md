# Context Engineering: Steering a Trajectory

After you understand how to talk to LLMs, you next to figure out how to steer them over time. Prompt engineering is about the moment to moment interactions you're having with them.

Context engineering is about iteratively guiding an agent to your desired outcome.

It's about becoming aware





# Writing Notes


I'm not currently sure if context engineering == "trajectory engineering".

Prompt engineering is the beat to beat interactions.
Context engineering is about the accumulation of those beat to beat interactions to engineer direction towards an outcome. It feels like it's about steering and thus trajectory but I'm not sure that it is.


- Model performance degrades the more that's in a context window.
  - Lost in the middle issues, instruction budget, context rot.
  - This leads to worse reasoning, increased likelihood of hallucinations, less alignment (did it reach the outcome I wanted), missed requirements.
  - Models can improve but these are fundamental constraints of the current architecture for LLMs.
  - One of the primary skills in using agents effectively is context engineering.


Reflection

# What is context engineering?

So if a good prompt is now just make sure your agent understands everything it needs too, let's just feed it every document we have, let it read the whole codebase and then let's get to work. Unfortunately this doesn't work either.

The practice of deliberately designing what goes into an agent’s context window.

You are directing the attention of the agent.

Content Quality
Correctness
Completeness

Conversation Health
Size
Trajectory
Cohesion
Put another way, the worst things that can happen to your context window, in order, are:

Incorrect Information
Missing Information
Too much Noise



Context engineering

You should optimize your context window for:



The 4 verbs

research, plan, implement, validate

The agent did what I want and didn't do more than I wanted.

Handoffs vs compaction

Think in handoffs.

The ideal is that at any point you can create a new agent and it can quickly get up to speed. (Cattle vs pet)

Take advantage of latent knowledge.

The mental frame for writing software shifts. Draft and refine.


https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md
