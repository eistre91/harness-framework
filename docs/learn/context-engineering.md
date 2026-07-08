The big idea is that LLMs are stateless nondeterministic functions.
    - Functions because they take some input and produce some output.
    - Stateless because they don't remember anything about your codebase or problem.
    - Nondeterministic because they might return different outputs for the same input.

The input to an LLM is the context window, everything in it up to now including your next prompt.

The output is its response, which might be just text in the CLI or files produces or code or anything else.

Getting the most values out of LLMs is all about controlling your inputs to give you the greatest chance of producing the desired output.

Note that you cannot guarantee you get the output you want. The process just needs to deliver the output that satisfies your constraints often enough
that it outperforms producing the output yourself.

Sophisticated prompt engineering is largely irrelevant now for frontier models. 80/20 rule applies pretty well here.

Also you need to care about "just the right" prompt more when you've only got one shot at a thing.

The bulk of prompt engineering is all about getting the agent in alignment with what you want.

Foundational techniques are few-shot prompting (provide examples), chain of thought (how do you want the agent to reason throuhg a problem) and meta prompting.

But there's increasingly an art of not constraining reasoning models too much.

Reflection

# What is context engineering?

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

"roles" vs attention focusing

Playing house - tell an LLM what to do not what to be. (What does it MEAN to be an expert backend engineer? Scalable? Availability? etc.)

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

Just not a big fan of spec driven development in most of its forms

https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md