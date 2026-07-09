## The Mental Model for LLMs

The big idea is that LLMs are stateless nondeterministic functions.
    - Functions because they take some input and produce some output.
    - Stateless because they don't remember anything about your codebase or problem.
    - Nondeterministic because they might return different outputs for the same input.

The input to an LLM is the context window, everything in it up to now including your next prompt.

The output is its response, which might be just text in the CLI or files produces or code or anything else.

Getting the most values out of LLMs is all about controlling your inputs to give you the greatest chance of producing the desired output.

Note that you cannot guarantee you get the output you want. The process just needs to deliver the output that satisfies your constraints often enough
that it outperforms producing the output yourself.

Start thinking of yourself as an outcome shaper.

In the old world we were brick layers. In the new world we're iteratively shaping pottery.


## A Note on Prompt Engineering

Sophisticated prompt engineering is largely irrelevant now for frontier models. The current frontier reasoning models have largely displaced the need for this. It used to be that you had to walk a model through the exact magical formula and choose the exact right words to get it to do the thing you wanted. You could seemingly say the same thing but with synonyms and the output would be dramatically different.

What has changed is that models are a lot better now at aligning themselves with the communicated intent. But "communicated intent" is also where the new challenge lies.

The focus is thus "what is the best way for you to communicate your intent?" To be a good prompt engineer today is to effectively and clearly communicate your intent to ensure the agent is truly in alignment with what you want.

Humans are really not that great at communicating their intent. Miscommunication abounds even in teams in which everyone shares the same general ambient information. When the underlying domain is complicated, like software, and everyone has sharper mental models of different parts of the underlying system or different expectations of how things currently work or should work in the future, small mismatches compound into difficult and thorny communication issues.

This usually works itself out with humans as they will communicate "I don't understand this, or I don't agree" and you can work on clarifying things collaboratively until both parties feel like there is shared understanding. But LLMs are biased to action through training and by default they'd rather write thousands of lines of code than spend time on making sure you're perfectly aligned. They love to fill in gaps and predict tokens rather than stopping to ask whether it actually has enough information to fill the gap.

LLMs compound our insufficiences at this skill because they don't have the ambient context you have. They know a ton of stuff, have a ton of "latent knowledge" and don't know anything at all about the domain and context that you and your problem and your company exist in.

With LLMs you need to be aware of all of this background information and communicate enough of it that the LLM is sufficiently aligned. You can lean on their latent knowledge to help here and should, but if the LLM confidently produces an incorrect output, most of the time the failure was in what you failed to communicate.





### Notes

Foundational techniques are few-shot prompting (provide examples), chain of thought (how do you want the agent to reason through a problem) and meta prompting.

But there's increasingly an art of not constraining reasoning models too much.

Saying what you want is usually better than saying what you don't want. You can't always state things positively but you should try to.

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