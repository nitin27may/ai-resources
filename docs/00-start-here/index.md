---
title: Choose your path
tags:
  - Start here
  - Home
description: Two routes through this site — one to understand AI without writing code, one to build an agent. Pick by what you want at the end.
---

# Choose your path

!!! abstract "Start here · 10 min · no code"
    **After this:** [AI 101](../getting-started/index.md)
    Two routes through the site. Pick either; you can switch at any point.

There are two ways through this site, and they are both complete. Pick by what
you want to have at the end: an accurate picture of how these systems work, or
an agent running on your own machine.

You can switch between them at any point. Every page says which layer it belongs
to and links to the same idea one level up or down.

## The reading path — understand AI, no code

Ten pages, four to five hours, nothing to install. For analysts, product
managers, leaders, students, and for developers who want the map before the
territory.

Each step needs only the ones before it. Prompting needs models. Retrieval is
"give the model your data". An agent is "let the model act", which needs both.
All ten pages live under [Understand](../concepts/index.md), and you can read
them there in any order once you have the first two.

| # | Read | Time |
|---|---|---|
| 1 | [AI 101](../getting-started/index.md) — what AI, ML and an LLM actually are, and the three things a model cannot do | 40 min |
| 2 | [How models work](../concepts/foundation-and-models.md) — tokens, context windows, inference | 30 min |
| 3 | [Prompting](../concepts/prompting-and-techniques.md) — system prompts, few-shot, chain of thought | 30 min |
| 4 | [Retrieval and data](../concepts/retrieval-and-data.md) — RAG, embeddings, vector search, GraphRAG | 30 min |
| 5 | [What an agent is](../concepts/ai-agents.md) — components, and when not to use one | 40 min |
| 6 | [Agentic AI](../concepts/agentic-ai.md) — protocols, memory, orchestration, human-in-the-loop | 40 min |
| 7 | [Enterprise AI patterns](../patterns/enterprise-patterns.md) — copilot, autonomous agent, agentic RAG | 30 min |
| 8 | [Safety and responsible AI](../concepts/safety-and-responsible-ai.md) — hallucination, injection, guardrails | 30 min |
| 9 | [Fine-tuning and training](../concepts/fine-tuning-and-training.md) — skim; the answer is usually RAG | 15 min |
| 10 | [Infrastructure and operations](../concepts/infrastructure-and-operations.md) — skim; MLOps, drift, cost | 15 min |

Safety comes after agents on purpose. The failure that matters most is an
instruction arriving through a tool result, which only makes sense once you know
what a tool result is.

## The build path — build an agent, ten labs

Roughly 12 to 15 hours. Everything runs against a model on your own machine: no
account, no API key, no cost. It assumes you can read Python and use a terminal,
and it assumes nothing about machine learning.

[The build path](the-path.md) has the full module list. In short: set up a local
model, then tool calling, the agent loop, the harness, context engineering,
retrieval, evaluation, observability, safety, production.

If you have not read pages 1, 2 and 5 of the reading path, do those first. That
is about 100 minutes and the modules assume them.

## If you only have an hour

[AI 101](../getting-started/index.md), then
[What an agent is](../concepts/ai-agents.md), then
[Safety and responsible AI](../concepts/safety-and-responsible-ai.md).

That is enough to follow any conversation on this subject and to tell a real
claim from a marketed one.

## How pages are marked

Every page opens with a block like this one:

!!! abstract "Understand · 30 min · no code"
    **Before this:** How models work  ·  **After this:** What an agent is
    **Hands-on version:** Module 5, Retrieval  ·  **In depth:** Retrieval in depth

It tells you the layer, how long the page takes, whether you need to write code,
and where the same idea lives at other depths. The four layers:

| Layer | What it is | Code |
|---|---|---|
| **Understand** | The concept, in plain language | None |
| **Build** | The same idea as something you run and break | Every page |
| **Go deeper** | Design-level depth for builders and architects | Some |
| **Reference** | Glossary, vetted reading, official sources | None |

You can also [browse by tag](../tags.md) to see everything on one topic across
all four layers.

## Not sure

Start with [AI 101](../getting-started/index.md). It takes half an hour and it
is the right first page whichever route you end up taking.

If you have been here before, [What's new](../whats-new/index.md) lists what
changed and when.
