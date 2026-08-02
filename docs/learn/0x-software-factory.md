A software factory is composed of repeatable workflows (loops in the current hyped language of today).

You identify an input that goes into the workflow and the output that you want it to generate.

Dex Horthy talks about "slow loops" which are occasionally run things which result in simple, easy to review outcomes and improvements.

https://newsletter.pragmaticengineer.com/p/context-engineering-with-dex-horthy

The main constraint on a software factory is that you still need to sit in the loop at the right level. Your attention and ability to keep up and figure out the next right step is the hard part.

The human must continue to learn the domain and problem and figure out what good looks like and be responsible for long term design and making decisions on trade offs.

The agent shapes the intent that comes from all of that via bounded and verifiable implementation.

Software is inherently an iterative process. We simply don't know enough and haven't accrued enough time with good software to specify waterfall style from the outset what a good UX will look like, what a good model looks like. The reality software is attempting to constrain and solve far is really complex and nearly impossible to predict in advance. You need to learn.




At a super high level some intent (the next feature you want) is split into individual work units. Those work units state the necessary conditions for a good work unit (what is it, what is it not, what's the goal or the why). That work unit along with supporting engineered context or state is given to an initial agent for implementation.

The small loop for implementation is initial agent produces an output (with quick short term steering like type checks and other deterministic gates), then that initial implementation may have further deterministic gates along with a fresh context adversarial reviewer agent (is the code good, what decisions is it making that are hard to reverse, how has the domain changed, does it adhere to our work unit). This can loop some amount of times with an agent that is there to resolve the reviewer's findings until it produces an output that we're ready to review ourselves (likely at an abstraction layer that we need for this bit of code).

If you use spec maps or compressed context that is fed to your agents (if the code isn't the only source of truth) then that needs to be kept updated. So another conveyor belt is keeping supporting documentation up to date.

Good modular code with clear interfaces, boundaries and seams means that we can isolate bad code but it's hard to isolate bad design that other modules will grow dependencies on.



At any point in any process, we can give conditions for which an agent or check should flag the need for human intervention.

Potentially summaries of each conveyor belt (defined input and output) can be used for the factory to learn. Though I still think good learning and memory takes a lot of care and human intervention and regular cleaning.

Every so often we do maintenance feedback checks for larger health signals (maybe using a tool like repowise which provides a code health score).


I think we also need processes by which you extract state of the product/software and try to teach the human about it, test them to see if they're still aware of the domain. Can they draw the domain? Can they accurately define what a term is and how it relates to other terms? Can they name what the modules are? Once we define and settle on the abstraction layer for a human, just as we need to verify the agent is doing what we expect, we need to verify the human hasn't accrued too much cognitive debt. We need a way of saying "we need to slow down and give the human time to catch up" because we put inherent value on the human being caught up. The "human-agent" system is as much about aiding the human as the agent.



A degradation in semantic coherence and understandability is hard to measure but code health metrics can provide warnings of this. Potentially an agent could to. (untested synthetic probes for this are dropping an agent without context support into a random part of the code and limiting its scoped to see how well it can understand things/are there natural boundaries that it can explore out to/the boundaries and seams should be "obvious") (ports/adapters model?)

Modern Software Engineering by David Farley
Separation of concerns
modularity
cohesion
coupling
information hiding and abstraction


Observability of the factory and what's going on