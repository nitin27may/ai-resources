---
tags:
  - Reference
description: Primary documentation by vendor — the pages to read instead of a summary, including this site's.
---

# Official sources

!!! abstract "Reference · browse · no code"
    **Before this:** [Resources](../reference/resources.md)
    Primary documentation by vendor. For a ranked, opinionated shortlist with a
    reason to trust each item, read [Resources](../reference/resources.md) first.

Every link on this page is a vendor's own documentation. When a detail matters —
a parameter, a limit, a price, which model exists this week — go here rather than
to any summary, including this site's.

**Verified as of 2026-09-02.** Every URL was resolved on that date. This page
carries no courses-and-certifications section on purpose: the goal is to point
you at the source of truth, not at a syllabus.

## Anthropic

| Resource | What it is for |
|---|---|
| [Claude documentation](https://docs.claude.com/) | The API, models, pricing and limits. The starting point for anything Claude |
| [Engineering blog](https://www.anthropic.com/engineering) | The highest-density teaching corpus in the field. Context engineering, tool design, harnesses, evals |
| [Claude Code docs](https://docs.claude.com/en/docs/claude-code/overview) | The agentic CLI: skills, subagents, hooks, memory, MCP |
| [Prompt engineering guide](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview) | Claude-specific prompting, but most of it generalises |
| [Claude cookbooks](https://github.com/anthropics/claude-cookbooks) | Runnable notebooks. `patterns/agents/` is the workflow taxonomy as code |

## Microsoft

| Resource | What it is for |
|---|---|
| [Azure AI Foundry](https://learn.microsoft.com/en-us/azure/foundry/) | The umbrella platform. "Azure AI Studio" and most "Azure OpenAI Service" URLs now redirect here |
| [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/) | The current .NET and Python agent SDK. GA 1.0 in April 2026; successor to Semantic Kernel and AutoGen |
| [Foundry Agent Service](https://learn.microsoft.com/en-us/azure/foundry/agents/overview) | Hosted agents on Azure, with tools and threads managed for you |
| [Model catalogue](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure) | What is actually deployable today, with context limits |
| [Azure AI Search](https://learn.microsoft.com/en-us/azure/search/) | Hybrid vector and keyword retrieval; the usual RAG layer on Azure |
| [Azure AI Content Safety](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/) | Content filtering, prompt shields, groundedness detection |
| [Generative AI for Beginners](https://github.com/microsoft/generative-ai-for-beginners) | A free, self-paced course. Genuinely maintained |
| [AI Agents for Beginners](https://github.com/microsoft/ai-agents-for-beginners) | The agent-focused companion to the above |

!!! warning "Semantic Kernel and AutoGen"
    Both are superseded by Microsoft Agent Framework and are not listed above.
    Semantic Kernel still receives security fixes into 2027 and existing code
    keeps working, but new agent work should start on Agent Framework. AutoGen
    has been in maintenance mode since late 2025. Listicles still recommend both.

## OpenAI

| Resource | What it is for |
|---|---|
| [API documentation](https://developers.openai.com/api/docs) | The reference. Note the host: `platform.openai.com` links now redirect here |
| [Models](https://developers.openai.com/api/docs/models) | The live catalogue. Prefer it to any model table, including ours |
| [Agents SDK](https://openai.github.io/openai-agents-python/) | The supported agent framework. It replaced Swarm, which was an experiment |
| [Function calling](https://developers.openai.com/api/docs/guides/function-calling) | Tool schemas and the request/response shape the whole industry copied |
| [Embeddings](https://developers.openai.com/api/docs/guides/embeddings) | The `text-embedding-3` models, dimensions and the Matryoshka reduction |

## Google

| Resource | What it is for |
|---|---|
| [Gemini API docs](https://ai.google.dev/gemini-api/docs) | The API, models and limits |
| [Agent Development Kit](https://google.github.io/adk-docs/) | Google's open-source agent framework, with its own evaluation tooling |
| [Gemini Enterprise Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform) | The managed platform. The old Vertex AI agent URLs land here |
| [AI Studio](https://aistudio.google.com/welcome) | Prototyping against Gemini without writing a client |
| [Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) | Still the clearest free introduction to learning from data |

## NVIDIA

The layer below the frameworks: what the models actually run on, and the parts
you need when you self-host rather than call an API.

| Resource | What it is for |
|---|---|
| [NIM](https://docs.nvidia.com/nim/) | Prebuilt inference microservices. The realistic route to self-hosting a model with an OpenAI-compatible endpoint |
| [NeMo Guardrails](https://docs.nvidia.com/nemo/guardrails/latest/index.html) | Programmable rails for dialogue, topic and safety control. One of the few guardrail systems with a real specification language |
| [NeMo Guardrails source](https://github.com/NVIDIA/NeMo-Guardrails) | Read the rails and the examples; the concepts transfer even if you never deploy it |
| [Technical blog, generative AI](https://developer.nvidia.com/blog/category/generative-ai/) | Inference optimisation, quantisation and serving, from the people who build the hardware |

## Protocols and standards

| Resource | What it is for |
|---|---|
| [Model Context Protocol](https://modelcontextprotocol.io/) | The protocol itself. Check the revision date every time; `2026-07-28` was a breaking redesign |
| [MCP specification](https://modelcontextprotocol.io/specification) | The normative document. The [architecture page](https://modelcontextprotocol.io/docs/learn/architecture) is better for first contact |
| [MCP Inspector](https://github.com/modelcontextprotocol/inspector) | Debug a server without wiring up a host |
| [A2A protocol](https://a2a-protocol.org) | Agent-to-agent delegation. Linux Foundation, not Google, since June 2025 |
| [Agent Skills specification](https://agentskills.io/specification) | One `SKILL.md` format that runs across several vendors' tooling |
| [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | The vendor-neutral security taxonomy, each item backed by a real incident |

## Frameworks and retrieval

| Resource | What it is for |
|---|---|
| [LangChain](https://docs.langchain.com/oss/python/langchain/overview) | Composable building blocks. Note the host: `python.langchain.com` now redirects |
| [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview) | Stateful, graph-based orchestration with cycles and checkpoints |
| [LlamaIndex](https://developers.llamaindex.ai/python/framework/) | Retrieval-first framework with strong ingestion and indexing |
| [CrewAI](https://docs.crewai.com/) | Role-based multi-agent orchestration |
| [Microsoft GraphRAG](https://microsoft.github.io/graphrag/) | Graph-based retrieval. Read the indexing cost section before adopting |
| [pgvector](https://github.com/pgvector/pgvector) | Vector search inside Postgres; the realistic production default |
| [Cohere Embed](https://docs.cohere.com/docs/cohere-embed) | Embedding models with explicit input types |
| [MTEB leaderboard](https://huggingface.co/spaces/mteb/leaderboard) | Benchmark comparison for embedding models. A filter, never a verdict |

## Tooling and community

| Resource | What it is for |
|---|---|
| [GitHub Copilot docs](https://docs.github.com/en/copilot) | Every Copilot surface, including the cloud agent |
| [GitHub MCP server](https://github.com/github/github-mcp-server) | GitHub's own server. It replaced the archived reference implementation |
| [Hugging Face](https://huggingface.co/) | Models, datasets and the [agents course](https://huggingface.co/learn/agents-course) |
| [Meta Llama](https://www.llama.com/) | Open-weight models and licences |
| [Ollama](https://ollama.com/) | Run models locally. The substrate for every lab on this site |
