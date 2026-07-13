# Prompt Engineering in 2026

In 2023 and 2024, prompt engineering was a sort of esoteric magical art. If you wanted an LLM to perform well, you had to string together just the right words and just the right structure. It was vague and imprecise, required a lot of iteration and everyone had a special "technique" to get the model to do exactly the right things.

Now though, advances in the models due to introduction of reinforcement learning and reasoning capabilities have displaced the need for this. When using recent, frontier reasoning models most of the old prompt engineering techniques are now largely irrelevant, a waste of time and energy, and in some cases are actively harmful.

Specifically what has happened is that models have gotten a lot better at understanding the communicated intent in a prompt. Everything that remains for being a good prompt engineer is about being good at communicating your intent.




This is a harder problem than you might think. 

The focus is thus "what is the best way for you to communicate your intent?" To be a good prompt engineer today is to effectively and clearly communicate your intent to ensure the agent is truly in alignment with what you want.

Humans are really not that great at communicating their intent. Miscommunication abounds even in teams in which everyone shares the same general ambient information. When the underlying domain is complicated, like software, and everyone has sharper mental models of different parts of the underlying system or different expectations of how things currently work or should work in the future, small mismatches compound into difficult and thorny communication issues.

This usually works itself out with humans as they will communicate "I don't understand this, or I don't agree" and you can work on clarifying things collaboratively until both parties feel like there is shared understanding. But LLMs are biased to action through training and by default they'd rather write thousands of lines of code than spend time on making sure you're perfectly aligned. They love to fill in gaps and predict tokens rather than stopping to ask whether it actually has enough information to fill the gap.

LLMs compound our insufficiences at this skill because they don't have the ambient context you have. They know a ton of stuff, have a ton of "latent knowledge" and don't know anything at all about the domain and context that you and your problem and your company exist in.

With LLMs you need to be aware of all of this background information and communicate enough of it that the LLM is sufficiently aligned. You can lean on their latent knowledge to help here and should, but if the LLM confidently produces an incorrect output, most of the time the failure was in what you failed to communicate.


Foundational techniques are few-shot prompting (provide examples), chain of thought (how do you want the agent to reason through a problem) and meta prompting.

But there's increasingly an art of not constraining reasoning models too much.

Saying what you want is usually better than saying what you don't want. You can't always state things positively but you should try to.


"roles" vs attention focusing
Playing house - tell an LLM what to do not what to be. (What does it MEAN to be an expert backend engineer? Scalable? Availability? etc.)


It can be useful to give an agent the why. "