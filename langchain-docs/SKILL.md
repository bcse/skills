---
name: langchain-docs
description: Use this skill for requests related to LangChain/LangGraph in order to fetch relevant documentation to provide accurate, up-to-date guidance.
---

# langchain-docs

## Overview

This skill explains how to access LangGraph Python documentation to help answer questions and guide implementation. It supports DeepWiki MCP for documentation discovery and direct web fetch for known pages or fallback.

## Instructions

Start with a known relevant documentation page. Fetch an index only when the page is unknown, and read additional pages only to resolve missing or conflicting information. Stop when the available evidence answers the request.

### Strategy 1: DeepWiki MCP (Preferred)

When documentation discovery is needed and the DeepWiki MCP server is available, prefer it for discovery. The relevant GitHub repositories are:

- `langchain-ai/langchain` — Core LangChain framework (chains, prompts, LLMs, retrievers, tools)
- `langchain-ai/langgraph` — LangGraph (stateful agents, graphs, persistence, streaming)
- `langchain-ai/langsmith-sdk` — LangSmith (tracing, evaluation, datasets)

#### Step 1: Identify the Relevant Repository

Map the user's question to one or more of the repositories above. When in doubt:
- Agent orchestration, state machines, cycles, human-in-the-loop → `langchain-ai/langgraph`
- Chains, prompts, chat models, retrievers, document loaders, tools → `langchain-ai/langchain`
- Tracing, evaluation, feedback → `langchain-ai/langsmith-sdk`

#### Step 2: Explore Documentation Structure

If the relevant page is unknown, use `read_wiki_structure` to identify it from the repository topic index.

#### Step 3: Read Relevant Documentation

Use `read_wiki_contents` to fetch relevant documentation only as needed to answer the user's question.

#### Step 4: Ask Targeted Questions (Optional)

For complex or cross-cutting questions, use `ask_question` against the relevant repository to get an AI-powered, context-grounded answer. This is especially useful when:
- The question spans multiple documentation pages
- You need a quick sanity check on an implementation approach
- The topic index doesn't clearly map to the user's question

#### Step 5: Provide Accurate Guidance

Synthesize the documentation into a clear, actionable response. Prefer code examples from the docs and cite the source repository when relevant.

### Strategy 2: Web Fetch

Fetch a known relevant documentation URL directly, or use web fetch when DeepWiki MCP is unavailable.

#### Step 1: Fetch the Documentation Index

If the relevant page is unknown, use the WebFetch tool to read the following URL:
https://docs.langchain.com/llms.txt

This provides a structured list of all available documentation with descriptions.

#### Step 2: Select Relevant Documentation

Identify documentation URLs from the index only for information still needed to answer the question. Prioritize:
- Specific how-to guides for implementation questions
- Core concept pages for understanding questions
- Tutorials for end-to-end examples
- Reference docs for API details

#### Step 3: Fetch Selected Documentation

Use the WebFetch tool to read the selected documentation URLs.

#### Step 4: Provide Accurate Guidance

After reading the documentation, complete the user's request.

## Notes

- When discovery is needed and both strategies are available, prefer DeepWiki MCP for its context and targeted Q&A.
- For questions that touch multiple repositories (e.g., "how do I trace a LangGraph agent in LangSmith"), query additional repositories only to resolve missing or conflicting information.
- Always ground answers in the fetched documentation rather than relying on training data, as LangChain/LangGraph APIs evolve rapidly.
