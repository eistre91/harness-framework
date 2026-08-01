# Foundations

Matt Pocock's free [LLM Fundamentals](https://www.aihero.dev/llm-fundamentals)
course is the recommended preparation when these concepts are unfamiliar. This
page is a readiness check so this course can focus on human-agent systems and
harness engineering rather than repeat that material.

You are ready for the next lesson when you can explain messages and instruction roles, tokens and reasoning tokens, context windows, tools, workflows, and agents in your own words.

## Messages, System Prompts, and Reasoning Tokens

- System or developer instructions, user messages, and assistant messages have
  different roles and priorities.
- Higher-priority instructions constrain lower-priority messages.
- Reasoning models may generate reasoning tokens that are not part of the
  visible response.

## What Are Tokens?

- Tokens are how LLMs see the world.
- Tokens are not universal between models.
- What specific words or fragments get represented as a token can differ between models and is based on the underlying tokenizer.

## What Is the Context Window?

- Context accrues over a session and previous inputs and model outputs are part of the context window on each subsequent call.
- The context window limit is the maximum amount of tokens a model supports in its context.
- Adding more content to a context window has consequences for both cost and performance.
    - More content in the context window means that future LLM calls have more input tokens.
    - May decrease performance due to limitations like the "lost in the middle" issue.

## What Are Tools?

- An LLM doesn't directly execute tools. It outputs tool calls which an agent harness (e.g. Claude Code, Codex) executes and appends the results to the message history.

## What Is an Agent?

- An LLM may be used as part of a workflow or as an agent.
- A workflow is a sequence of defined steps, wherein a step may itself be an LLM call.
- An agent is an LLM in a loop with access to tools. It decides when to stop.
    - NOTE: An agent **turn** refers to everything the agent does until it stops or cedes control back to the user after a prompt.
