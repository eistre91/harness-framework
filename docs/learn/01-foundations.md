This free [LLM Fundamentals](https://www.aihero.dev/llm-fundamentals) course from Matt Pocock covers essential concepts that you should know.

Key Takeaways for each lesson:

1. Messages, System Prompts and Reasoning Tokens
- System prompt instructions are weighed more strongly than user messages.
- The difference between the system prompt, user messages and assistant messages.

2. What Are Tokens?
- Tokens are how LLMs see the world.
- Tokens are not universal between models.
- What specific words or fragments get represented as a token can differ between models and is based on the underlying tokenizer.

3. What Is the Context Window?
- Context accrues over a session and previous inputs and model outputs are part of the context window on each subsequent call.
- The context window limit is the maximum amount of tokens a model supports in its context.
- Adding more content to a context window has consequences for both cost and performance.
  - More content in the context window means that future LLM calls have more input tokens.
  - May decrease performance due to limitations like the "lost in the middle" issue.

4. What Are Tools?
- An LLM doesn't directly execute tools. It outputs tool calls which an agent harness (e.g. Claude Code, Codex) executes and appends the results to the message history.

5. What Is an Agent?
- An LLM may be used as part of a workflow or as an agent.
- A workflow is a sequence of defined steps, wherein a step may itself be an LLM call.
- An agent is an LLM in a loop with access to tools. It decides when to stop.
  - NOTE: An agent **turn** refers to everything the agent does until it stops or cedes control back to the user after a prompt.
