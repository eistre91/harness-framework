
## A Note on Prompt Engineering

Sophisticated prompt engineering is largely irrelevant now for frontier models. The current frontier reasoning models have largely displaced the need for this. It used to be that you had to walk a model through the exact magical formula and choose the exact right words to get it to do the thing you wanted. You could seemingly say the same thing but with synonyms and the output would be dramatically different.

What has changed is that models are a lot better now at aligning themselves with the communicated intent. But "communicated intent" is also where the new challenge lies.

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
