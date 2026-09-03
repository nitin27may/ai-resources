---
title: Resources
description: A short, ranked reading list with a reason to trust each item — and an explicit list of what to avoid.
  - Reference
tags:
  - Reference
  - Reference
---

# Resources

!!! abstract "Reference · 20 min · no code"
    **After this:** [Official sources](../references/index.md)

!!! abstract
    Curation, not accumulation. Every item below has a reason to trust it stated
    next to it, and every link was checked on the date shown. The **avoid** list
    at the bottom is as useful as the rest — most of it is material that ranks
    well and is quietly out of date.

**Verified as of 2026-08-21.**

## How to judge a source yourself

The field produces more confident writing than it does reliable writing. Three
filters that work:

**Check the date, then check what changed after it.** MCP had a breaking spec
revision in July 2026. Anything on MCP written before that teaches an API that no
longer exists, however good it was.

**No disclosed methodology and no named author with shown work → discard.** This
removes most "Top 10 agent frameworks" content in one step.

**Prefer sources that publish their own negative results.** A vendor blog that
says "we tried this and it did not work" is worth ten that only report wins.

## Essential

If you read only these, you are in good shape.

| Source | Why trust it |
|---|---|
| [Anthropic engineering blog](https://www.anthropic.com/engineering) | The highest-density teaching corpus in the field, and the rare vendor blog where the substance outweighs the marketing. Start with *Effective context engineering* (Sep 2025), *Writing tools for agents* (Sep 2025), *Effective harnesses for long-running agents* (Nov 2025), *Demystifying evals* (Jan 2026). |
| [MCP specification](https://modelcontextprotocol.io/specification) | The protocol itself. Check the revision date every time — `2026-07-28` is a breaking redesign. The [architecture page](https://modelcontextprotocol.io/docs/learn/architecture) is better than the spec for first contact. |
| [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Still the best vocabulary for agent patterns. **Read the banner** — Anthropic marks it superseded. Terminology, not current practice. |
| [Context Rot](https://www.trychroma.com/research/context-rot) | 18 models, six task families. The empirical basis for treating your context window as a ceiling rather than a budget. Vendor-published; pair with NoLiMa (ICML 2025) where it carries weight. |
| [LLM Evals FAQ](https://hamel.dev/blog/posts/evals-faq/) | Husain & Shankar, continuously maintained. The most current practitioner document on evaluation, with actual numbers. |
| [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | The only vendor-neutral security taxonomy for agents, each item backed by a documented incident. |
| [Simon Willison](https://simonwillison.net) | Highest-trust individual source in the field. No affiliate incentive, publishes corrections, dates everything. His [lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) tag is the public incident registry. |

## The pair worth reading together

Published **one day apart**, from two companies shipping real agents, arguing
opposite conclusions:

- [Don't Build Multi-Agents](https://cognition.com/blog/dont-build-multi-agents) — Cognition, Jun 2025
- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) — Anthropic, Jun 2025

Reading them as a pair teaches the actual decision criterion — context sharing
versus parallelisable read-heavy work — better than either alone. Cognition
[revised their position in 2026](https://cognition.com/blog/multi-agents-working):
what works is multiple agents contributing intelligence while **writes stay
single-threaded**.

## Read directly, not summarised

| Source | Note |
|---|---|
| [ReAct](https://arxiv.org/abs/2210.03629) | The origin of interleaved reasoning and acting. Short, current, not superseded. |
| [Agent Skills spec](https://agentskills.io/specification) | A genuinely cross-vendor format — one `SKILL.md` folder runs across Anthropic, OpenAI, Google, Microsoft and AWS tooling. |
| [A2A protocol](https://a2a-protocol.org) | Linux Foundation, v1.0 April 2026. Worth knowing; see the scepticism below before building on it. |
| [The Attacker Moves Second](https://arxiv.org/abs/2510.09023) | OpenAI, Anthropic and DeepMind jointly breaking 12 published injection defences at >90%. The three parties with most reason to claim otherwise. |
| [Adding Error Bars to Evals](https://arxiv.org/abs/2411.00640) | Miller. Standard errors, paired differences, power analysis. Short and directly implementable. |
| [AI Agents That Matter](https://arxiv.org/abs/2407.01502) | Princeton. Why accuracy-only benchmarking produced needlessly expensive agents. |

## Free courses that are actually current

| Course | Cost | Note |
|---|---|---|
| [Hugging Face AI Agents Course](https://huggingface.co/learn/agents-course) | Free, certificate | Deliberately multi-framework rather than vendor-captured. Actively maintained. Its Unit 2 certification Space has been unreliable — use the lesson content. |
| [DeepLearning.AI — Agentic AI](https://www.deeplearning.ai/courses/agentic-ai/) | Free to audit | The flagship structured course on multi-step tool-using systems. |
| [DeepLearning.AI — Evaluating AI Agents](https://www.deeplearning.ai/short-courses/evaluating-ai-agents/) | Free to audit | Evals are the bottleneck skill; this is the best structured treatment. |
| [Microsoft Agent Framework docs](https://learn.microsoft.com/en-us/agent-framework/) | Free | For the .NET half of the world. GA'd 1.0 April 2026; successor to Semantic Kernel and AutoGen. |

## Code worth reading

| Repo | Why |
|---|---|
| [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) | The agent loop in ~180 readable lines, with cost and step limits made explicit. Runs against Ollama. **The single best read before touching any framework.** |
| [claude-cookbooks](https://github.com/anthropics/claude-cookbooks) | `patterns/agents/` is the workflow taxonomy as runnable notebooks. CI-enforced against both code rot and link rot. |
| [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) | Framework-agnostic production principles. A 2025 document — the principles held up, the tooling references did not. |

## Tools that run locally, free

| Tool | Note |
|---|---|
| [Ollama](https://github.com/ollama/ollama) | The substrate for everything in this path. |
| [Phoenix](https://github.com/Arize-ai/phoenix) | `pip install arize-phoenix && phoenix serve` — tracing and evals, no account. **Elastic 2.0, not OSI open source.** |
| [promptfoo](https://github.com/promptfoo/promptfoo) | YAML evals in CI, local judges supported. Set the grader explicitly or it reaches for a hosted model. |
| [MCP Inspector](https://github.com/modelcontextprotocol/inspector) | Debug an MCP server without wiring up a host. |
| [pgvector](https://github.com/pgvector/pgvector) | The realistic production answer for vector search. |

## Avoid, and why

Not bad-faith — mostly good material that time moved past. It still ranks well.

| Item | Problem |
|---|---|
| **Any MCP tutorial predating mid-2026** | The `2026-07-28` revision removed the handshake and sessions, deprecated roots/sampling/logging, and dropped standalone SSE. The SDK renamed `FastMCP` to `MCPServer`. Most published MCP content teaches a dead API. |
| **`anthropics/courses`** | 22k stars, no commit since Nov 2025, examples target retired Claude 3 model IDs. Contains no MCP and no agents content. |
| **RAGAS as a dependency** | Last release Jan 2026, no commits since Feb, 563 open issues. The metric vocabulary is worth learning; the library is not worth depending on. |
| **AutoGen** | Maintenance mode; last release Sep 2025. Microsoft Agent Framework is the successor. Still recommended in current listicles. |
| **OpenAI Swarm** | Superseded by the Agents SDK, by its own README. |
| **`awesome-mcp-servers`** | 90k+ stars and 3,000+ unmerged pull requests. Nobody is curating it. Use the MCP Registry. |
| **`langchain-ai/rag-from-scratch`** | Heavily recommended, 14 months stale, pre-dates LangChain v1. |
| **"Top 10 agent frameworks for 2026" listicles** | Confirmed pattern of 2024 SEO refreshes still recommending AutoGen and Swarm. |
| **Medium / Towards Data Science as a brand** | The publication carries no trust signal. An individual piece by a named practitioner with a real repo can be fine; the masthead means nothing. |
| **LinkedIn AI content** | Over 40% of long-form posts flag as fully AI-generated. Default-distrust the channel. |
| **Any "we solved prompt injection" claim** | Contradicts OpenAI, Anthropic and Google DeepMind simultaneously. See [Safety](../02-agents/safety.md). |

## Worth knowing, worth scepticism

**A2A** is a well-designed spec solving a real problem — cross-organisational
agent delegation with identity and long-running tasks. After twelve months it has
150+ supporting organisations, hyperscaler platform support, and **no publicly
named production deployments**. Learn the Agent Card and task-lifecycle concepts;
do not treat it as something you need.

**GraphRAG** buys corpus-level sensemaking that no chunk retriever can do at any
`k`. It does **not** buy better factoid QA — two independent evaluations found
vanilla RAG matching or beating it on single-hop retrieval, with RAG-plus-reranking
winning decisively, at roughly 57x the indexing cost. Decide on query mix, not on
corpus size.
