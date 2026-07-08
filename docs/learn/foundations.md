This free [LLM Fundamentals](https://www.aihero.dev/llm-fundamentals) course from Matt Pocock covers essential concepts that you should know.

Key Takeaways:
- The system prompt is very powerful.
- What's the difference between the system prompt, user messages and assistant messages?
- An LLM doesn't execute tools. It outputs tool calls which the agent harness like Claude Code or Codex executes and adds the results to the context window.
- Tokens are how LLMs see the world. (Why can't LLMs tell you how many r's are in strawberry?)
- Tokens are not universal between models. Different companies/models use different tokenizers.
- The context accrues and the entire context window is sent back with every message. (Caching is the only reason agentic tools are remotely affordable.)
- Model performance degrades the more that's in a context window.
  - Lost in the middle issues, instruction budget, context rot.
  - This leads to worse reasoning, increased likelihood of hallucinations, less alignment (did it reach the outcome I wanted), missed requirements.
  - Models can improve but these are fundamental constraints of the current architecture for LLMs.
  - One of the primary skills in using agents effectively is context engineering.
- Agent vs a workflow (what says stop?)
  - An agent **turn** refers to everything the agent does until it stops or cedes control back to the user after a prompt.
