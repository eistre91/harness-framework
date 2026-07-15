# Prompt Engineering in 2026

In 2023 and 2024, prompt engineering was a sort of esoteric magical art. If you wanted an LLM to perform well, you had to string together the right words and the right structure. It was vague and imprecise, required a lot of iteration and everyone had a special technique to get the model to do exactly the right things.

This is now much less necessary. Model improvements resulting from reinforcement learning and reasoning capabilities have displaced the need for this. For capable reasoning models most of the old prompt engineering techniques are now largely irrelevant, a waste of time and energy, and in some cases actively harmful.

Current prompt engineering practice boils down to two things: intent and attention. The former answers, "What should the agent accomplish?" and the latter answers "What should the agent consider while doing it?"

## Intent

Talking to early LLMs was like talking to a partner that never felt like they were listening. You'd say one thing and then they'd take it in the wrong way and do something else entirely.

Models have gotten a lot better at understanding intent than those early days, but they aren't perfect. And they never will be.

This isn't the fault of the models. It turns out communicating our intent is hard. We struggle with it daily with other humans. With other humans who have the benefit of memory and getting to know you, being on the same team as you and part of the same company as you. Every day you spend enmeshed in the same social context as another human, you learn and download new information that helps you understand each other. And it's still hard.

LLMs don't get to benefit from any of that without us preparing entire harnesses to support them! Partly LLMs come at the problem in a different way but having far broader knowledge and exposure than any human can. Every interaction with them will leverage that broad base of knowledge. But this also means they'll fill in gaps all too happily because something "sounds right" rather than is right. Since LLMs are biased to action through training, they'd much rather write thousands of lines of code that are close rather than exactly what you need. But as a software engineer you're not in the business of close.

Why are we so bad at communicating our intent? It's because we're bad at realizing how many latent assumptions we're holding. We're intuitive creatures that get by on 100s of snap decisions every hour made without our awareness in the subconscious. You have to uncover those to use LLMs effectively.

The central questions in defining your intent are:

- What outcome do I want?
- What outcomes do I NOT want?
- Why do I want this outcome?

Well communicated intent means that the agent can act, recognize success and avoid adjacent wrong outcomes.

Luckily there's a prompt technique that can help extract all that juicy intent from your brain.

## Bidirectional Prompting

Bidirectional prompting is one of the best prompt techniques introduced in recent memory and I expect it to stick around for a long time. It is the collaborative shaping and discovery of intent with an agent.

The idea of bidirectional prompting is that you indicate to the agent it should ask you questions until the next valuable slice of work is clear and that both you and the human are sufficiently confident that your understanding is aligned and you share a design concept.

Note that I did not say certain. Attempting to achieve certain alignment is a way to madness. It doesn't work with other humans and it certainly won't work with agents.




  This is how you get the agent to help you in making sure you've communicated your intent and all assumptions that you might be holding about that intent. It can also help you discover decisions that might need to be made that you didn't consider ahead of time and make sure you're involved in making those.


A downside to bidirectional prompting is it's difficult and exhausting. It's easy for your eyes to glaze over and just start giving half or empty answers, or just agreeing with what the agent suggests. This techniques needs to be used carefully and you should be mindful of being an active intentional participant.



## Attention


  Role prompting is a crude form of attention direction. “Act like a senior backend engineer” invokes a vague
  bundle of associations. It is usually better to unpack the role:

  > Focus on service boundaries, failure modes, operational behavior, compatibility, and maintainability.

  A role can be useful shorthand, but it should not substitute for naming what matters.

"roles" vs attention focusing
Playing house - tell an LLM what to do not what to be. (What does it MEAN to be an expert backend engineer? Scalable? Availability? etc.)
Another way to prompt is to think about how you're focusing the attention of the agent. The more concrete the provided focus is for an agent, the more likely it'll deliver the desired outcome.
(A review agent versus a code writing agent)


### Notes

Some models are better at realizing they need to ask questions, but at the end of the day an agent is made to be a task completion tool which means it is biased to action and will usually default to writing thousands of lines of code rather than clarifying intent.

I think there's two primary ways that I look at prompt engineering now and I'm not sure how to unify or communicate both in this lesson. But one is communicating intent (and all the details that come along with that like figuring out your actual intent with all the latent assumptions and information you have). The other is focusing the agent's attention in the right places. Role based prompting gets at this but it also falls short because if its like of specificity. What does it mean to "act like a senior backend engineer"? What are the thing you actually want the "senior backend engineer" to focus on that matters for the problem or domain you're in?

  They can be unified as two questions:

  - Intent: What should the agent accomplish?
  - Attention: What should the agent notice, consider, or prioritize while doing it?

  The framework encodes intent through outcomes, non-goals, constraints, acceptance evidence, and human-owned
  decisions. It encodes attention through focused context, task-intent routing, explicit boundaries, and
  separate planning, implementation, and review lenses.


> Modern prompt engineering is communicating the intended outcome and directing the model’s attention toward
> the considerations that matter.

The practice of "spec-driven development" was developed out of these struggles. The thought was if only you had considered every possible branch of the design tree and made every possible decision, then surely the LLM would do exactly what you wanted. (Not really a big fan of current forms of SDD and we'll circle back to this later.) Is this worth having here or too much of a deter this early on?

Models have gotten a lot better at getting in the right ballpark based the latent "semantic intent" from a prompt. Now writing a good prompt is all about ensuring that the intent the model deciphers is the intent you intended.


The framework explicitly says that human intent is the initial input but must not be assumed complete. Research,
planning, implementation, or validation can reveal ambiguity, missing context, or decisions requiring another injection
of human intent.


With LLMs you need to be aware of all of this background information and communicate enough of it that the LLM is sufficiently aligned. You can lean on their latent knowledge to help here and should, but if the LLM confidently produces an incorrect output, most of the time the failure was in what you failed to communicate.


Foundational techniques are few-shot prompting (provide examples), chain of thought (how do you want the agent to reason through a problem) and meta prompting.

But there's increasingly an art of not constraining reasoning models too much.

Saying what you want is usually better than saying what you don't want. You can't always state things positively but you should try to.



As you learn more about how to use these tools effectively, both here in prompt engineering and the later lessons, you'll understand that an LLM producing bad outputs is rarely the fault of the model or the agent. It's all entirely within your control and responsibility and if you own that you'll be able to achieve a lot more.

  > Human intent begins incomplete. Prompting helps expose and shape it into an executable outcome; context supplies what
  > is needed to act; constraints and boundaries limit drift; evidence tests the interpretation; feedback resteers the
  > trajectory.



It can be useful to give an agent the why.



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