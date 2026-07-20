# The Mental Model

## Tools for Outcomes

Don't think of LLMs or agents primarily as things you talk to. Think of them as tools that you use to achieve an outcome. Approach an LLM-powered tool as a photographer approaches their camera: the camera is powerful, but the photographer must learn how it works and how to shape the conditions around it to reliably produce a good shot. Engineers must develop the same kind of skill with agentic tools.

This is much more than a matter of adding agent skills, MCP servers, hooks, or other extensions. Those expand what an agentic tool can do, just as lenses and lighting expand what a photographer can capture. But those extensions do not replace the operator's judgment in using the tool well. Without an understanding of the underlying tool, adding more attachments mostly gives you a more complicated setup.

Chat is the interface through which most people first encountered LLMs, and it remains useful for many tasks. But chat also encourages a limited mental model: you say something, the model responds, and you decide what to ask next. For software engineering, an LLM can instead be placed inside a bounded process that is directed toward an outcome. That bounded process is what turns an LLM into part of an agent.

When using a tool as a chatbot, you ask, "What should I say to it next?"

When using it as a tool to achieve an outcome, instead ask, "How do I shape the conditions so this tool has the best chance of producing a result that satisfies my requirements?"

## Shape the Inputs

To understand how to shape those conditions, we first look at the LLM itself. One useful way to understand an LLM call is as a function. It accepts a sequence of input tokens, the model processes those tokens, and then it produces a sequence of output tokens as a response. That said, an LLM call is an unusual function because it is both stateless and nondeterministic.

LLM calls are stateless because the model does not remember previous calls. A chat application or agent harness creates continuity by supplying the relevant history again as input. Calls are nondeterministic because the same input can produce different outputs.

Thus the skill in using an LLM is learning how to shape its inputs so it is likely to produce the output you need. Note that the goal isn't to guarantee you get the exact output you want. With LLMs, you can't. The practical question is whether the model can satisfy the relevant constraints reliably enough that using it creates more value than doing the work without it.

## From Outputs to Outcomes

<figure class="model-shift">
  <div class="model-shift__panel" role="img" aria-label="A single LLM call transforms inputs into an output">
    <p class="model-shift__label">Single LLM call</p>
    <div class="model-shift__flow">
      <span class="model-shift__node">Inputs</span>
      <span class="model-shift__arrow" aria-hidden="true">→</span>
      <span class="model-shift__node">LLM</span>
      <span class="model-shift__arrow" aria-hidden="true">→</span>
      <span class="model-shift__node">Output</span>
    </div>
  </div>
  <div class="model-shift__panel model-shift__panel--agent" role="img" aria-label="A desired outcome guides an agent through a repeating cycle: act, observe, adjust, then use feedback to act again">
    <p class="model-shift__label">Agent trajectory</p>
    <div class="model-shift__agent-flow">
      <span class="model-shift__node">Desired outcome</span>
      <span class="model-shift__guide" aria-hidden="true">
        <span>guides</span>
        <span>↓</span>
      </span>
      <span class="model-shift__cycle">
        <span class="model-shift__cycle-flow">
          <span>Act</span>
          <span aria-hidden="true">→</span>
          <span>Observe</span>
          <span aria-hidden="true">→</span>
          <span>Adjust</span>
        </span>
        <span class="model-shift__return" aria-hidden="true">
          <span>feedback</span>
        </span>
      </span>
    </div>
  </div>
  <figcaption>One call produces an output. An agent uses feedback to steer repeated actions toward an acceptable outcome.</figcaption>
</figure>

A single LLM call ends when it produces an output. But software engineering work rarely ends there. The output must be integrated into a larger system, observed or tested, and then revised based on how it behaves in that system. Rather than manually shepherding an LLM through every step of this revision process, we can place it inside a harness that will carry information forward, give it tools, and let it work with some autonomy. That gives us an agent.

The skill in using agents evolves from shaping the output of a single call to steering a trajectory toward a desired outcome by shaping the feedback loop. The transition from LLMs to agents is a transition in focus: from outputs to outcomes. An agent searching for a solution to a problem navigates a complex space of possible paths. It takes actions, observes their results, and adjusts its path until it reaches an outcome. Your skill lies in shaping the conditions and feedback it receives so that it is more likely to arrive at an acceptable outcome.

## Apply Judgment to the Trajectory

This changes the engineer's relationship to the work. To use another metaphor, consider a bricklayer versus a potter. When writing code directly, you place many of the individual bricks yourself. When directing an agent, the work is often more like shaping clay: inspect what is taking form, apply pressure where it is needed, and repeat until the result meets your intent.

All of this is to stress that effective use of LLMs and agents is an intentional, focused activity. You define the outcome, shape the conditions, observe what the system produces, and deliberately use that feedback to steer what happens next.

The agent may perform implementation, but it does not remove the engineer from the process. Together, you and the agent form a human-agent system. The agent drives progress, but you own the trajectory: the intent, priorities, trade-offs and judgment applied to the result. This shifts where the engineer applies their experience and judgment: from producing every part directly to shaping the trajectory and judging the result.
