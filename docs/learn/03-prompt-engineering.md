# Prompt Engineering: Intent and Attention

In 2023 and 2024, prompt engineering often felt like an esoteric magical art. If you wanted an LLM to perform well, you had to find the right words and the right structure. The process was vague, imprecise, and iterative, and everyone seemed to have a special technique for making the model do exactly the right thing.

Capable reasoning models need much less of that choreography. Many techniques designed around the limitations of earlier models are no longer necessary. Many of them simply waste time and context, and some can even make results worse.

Effective prompt engineering can be boiled down to two concepts: intent and attention. Intent answers, "What should the agent accomplish?" Attention answers, "What should the agent consider while doing it?" Together, they provide a framework for shaping prompts even as models and techniques change.

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

Luckily there's a prompt technique which will help you clarify, understand and communicate your intent with an agent.

Bidirectional prompting is one of the best prompt techniques introduced in recent memory and I expect it to stick around for a long time. It is the collaborative shaping and discovery of intent with an agent.

The idea of bidirectional prompting is that you indicate to the agent it should ask you questions until the next valuable slice of work is clear and that both you and the human are sufficiently confident that your understanding is aligned and you share a design concept.

Note that I did not say certain. Attempting to achieve certain alignment is a way to madness. It doesn't work with other humans and it certainly won't work with agents. But what you can do is get yourself and the agent aligned enough that the chance of big surprises in its plan and implementation are minimal.

There are various examples out there of how to approach this but I encourage you to consider and refine your own over time.

"Ask me questions until you're confident we're on the same page. Only ask me one question at a time and wait for my response before asking another one. The goal is to narrow ambiguities, clarify my intent, and surface important decisions that will materially affect our plan or implementation.

A downside to bidirectional prompting is it's difficult and exhausting. It's easy for your eyes to glaze over and just start giving half or empty answers, or just agreeing with what the agent suggests. If you're not an active and engaged participant in the process, your own understanding will drift.

### Few Shot Prompting

Few shot prompting is where you provide examples of what you want the outcome to look like. Most obviously useful when you want an LLM to adhere to some document template, but it can be also be useful when planning code tasks. For example, describe what you want the data flow to look like. That lets you provide a high level example without resorting to writing the implementation yourself.

Examples communicate your intent with concretes.

### Prompt Positively

You generally want to spend more time and effort on specifying what you do want rather than what you don't want. Where possible "I want X" is always preferred to "I don't want Y".

One, it's better communication. Eliminating possiblities from a complex space barely trims down the space of acceptable answers.

Two, the agent will, whether you like it or not, always give some weight to every token in its context window. Agents really hate to leave any information behind. It's like telling a human to "not think about an elephant".

The preferred shape of intent is always going to be stating positively the thing you want, then spending some limited time on eliminating adjacent possible answers. (INSERT SIMPLE EXAMPLE)

The goal is not to avoid negative requirements. It's often impossible. But focus your own attention and energy on the positive requirements. It also force you to understand your own intent better.

(really can't decide if this belongs in intent or attention)

## Attention

The other primary consideration when prompting is attention. You need to tell an agent not only what to do, but what it should be focused on while it does that thing.

Agents seem to be uniquely bad at zooming out. When a human might be working on implementing some spec, they may come across decisions they didn't anticipate or start to feel like something isn't going well. They'll stop and re-evaluate whether the original plan needs to be revised. Agents don't tend to have this behavior in the right sort of way and its why agents left to their own devices on a codebase end up causing it to become incomprehensible spaghetti.

Agents will get blind to anything that wasn't specified, they don't stop to think. They get hyperfocused on a task. You can try to fight this with prompting and there is limited success to be had. But another approach is to see this limitation as a strength.

Agents are relentless task completion machines. Which means if you give them precise leading words about what matters, they will find things that satsify that task.

This is a double edged sword. Ask them to find performance issues, and more likely than not they'll suggest some even in the most finely tuned codebase that ever existed. They want to come up with an answer and abhor saying "there's nothing to do here". But careful prompting and keeping yourself engaged means you can turn this to your advantage.

(We'll touch on this later, but you can use one agent to find things and then another to pare down. I still think judgement LLMs won't make the right call but they are useful filters.) (This note might move to a later chapter. Not sure it fits here or distracts from the section/lesson. Right now I think we're scoped on "how do I interact with one agent process well" vs "how do you layer agents into effective workflows and collaborative structures".)

### Role Prompting

Role prompting is perhaps one of the most well known prompt techniques. And it's precisely an example of focusing the attention of the agent. Telling the agent to "act as a senior backend engineer" primes the agent to focus on things that might be relevant to a backend engineer and to use "backend engineer" language.

That said, role prompting is often a prompt crutch that people lean on and promotes bad practices. A good prompt is specific. "Act as a senior backend engineer" is far from specific. Tell the agent what it means to be a senior backend engineer for your company or problem.

"Focus on whether this service is scalable, maintainable, and highly available. We want the API to be clear and intuitive." etc. etc. (maybe expand on this a bit)

This is partly about communicating your intent as well. What does it MEAN to you to act like a senior backend engineer? Why do you want a senior backend engineer lens on this?

Spending a bit of time on getting straight on that will dramatically improve the output and ensure its tailored to what you need.

### Meta Prompting

Don't know what it means to be a backend engineer? That's fine. Talk to an LLM about that. Then have it help you write a prompt. Bidirectional prompting used to help you generate a prompt for a future agent is incredibly powerful.

### Chain of Thought

How do you want the agent to reason through the problem?

This is hard to get right. Reasoning models are pretty good at figuring out what they should do now. So this technique has become more about making sure that the agent doesn't overlook important sources of information and gathers relevant evidence first before coming to a conclusion.

"Make sure to check these logs, look at them for anomalous signals like X, Y, Z." (EXPAND EXAMPLE PROBABLY)

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
