# Prompt Engineering in 2026

In 2023 and 2024, prompt engineering was a sort of esoteric magical art. If you wanted an LLM to perform well, you had to string together just the right words and just the right structure. It was vague and imprecise, required a lot of iteration and everyone had a special "technique" to get the model to do exactly the right things.

Now though, model improvements due to introduction of reinforcement learning and reasoning capabilities have displaced the need for this. For capable reasoning models most of the old prompt engineering techniques are now largely irrelevant, a waste of time and energy, and in some cases actively harmful.

Models have gotten a lot better at getting in the right ballpark based the latent "semantic intent" from a prompt. Now writing a good prompt is all about ensuring that the intent the model deciphers is the intent you intended.

But we're it's difficult to do this with other humans who already benefit from shared context and ambient understanding. Every day a human spends on a project, in a team, in a company, they learn and download some new information that aligns their mental model with the other humans around them. We're social beings and we're really good at doing this even if we're not aware of it.

Agents can't benefit from this unless we're intentional and in ensuring they are made aware of all our latent assumptions. If you're able to detect all of the assumptions you're making and communicate those to the model, you're already going to prompt better than 95% of engineers. If you don't do this, agents are going to make their own assumptions, leaning on their fast store of latent knowledge. And the more you let them do this without catching it, the more the outcomes they produce are going to drift from what you want. Some models are better at realizing they need to ask questions, but at the end of the day an agent is made to be a task completion tool which means it is biased to action and will usually default to writing thousands of lines of code rather than clarifying intent.





### Notes

With LLMs you need to be aware of all of this background information and communicate enough of it that the LLM is sufficiently aligned. You can lean on their latent knowledge to help here and should, but if the LLM confidently produces an incorrect output, most of the time the failure was in what you failed to communicate.


Foundational techniques are few-shot prompting (provide examples), chain of thought (how do you want the agent to reason through a problem) and meta prompting.

But there's increasingly an art of not constraining reasoning models too much.

Saying what you want is usually better than saying what you don't want. You can't always state things positively but you should try to.


"roles" vs attention focusing
Playing house - tell an LLM what to do not what to be. (What does it MEAN to be an expert backend engineer? Scalable? Availability? etc.)
Another way to prompt is to think about how you're focusing the attention of the agent. The more concrete the provided focus is for an agent, the more likely it'll deliver the desired outcome.
(A review agent versus a code writing agent)



It can be useful to give an agent the why.

Bidirectional prompting - One of the best prompt techniques introduced in recent memory. The idea of bidirectional prompting is that you indicate to the agent that it should ask you questions until you're both certain that your understanding is aligned. This is how you get the agent to help you in making sure you've communicated your intent and all assumptions that you might be holding about that intent. It can also help you discover decisions that might need to be made that you didn't consider ahead of time and make sure you're involved in making those.

A downside to bidirectional prompting is it's exhausting. It's easy for your eyes to glaze over and just start giving half or empty answers, or just agreeing with what the agent suggests. This techniques needs to be used carefully and you should be mindful of being an active intentional participant.

As you learn more about how to use these tools effectively, both here in prompt engineering and the later lessons, you'll understand that an LLM producing bad outputs is rarely the fault of the model or the agent. It's all entirely within your control and responsibility and if you own that you'll be able to achieve a lot more.