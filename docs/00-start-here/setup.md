---
title: Setup
description: Get a model answering on your own machine, for free, in under an hour.
  - Getting Started
tags:
  - Build
  - Agents
  - Operations
---

# Setup

!!! abstract "Build · 30 min · hands-on"
    **Before this:** [The build path](the-path.md)  ·  **After this:** [1 Tool calling](../02-agents/tool-calling.md)

!!! abstract
    One goal: a model answering on hardware you control, at zero cost. Everything
    after this assumes you have it. If you get stuck here, nothing later works —
    so this page covers four hardware tiers and says plainly what to do when your
    machine cannot run a model at all.

**Verified as of 2026-08-21.**

## Why local first

Cost should not decide who gets to learn this. Free hosted tiers exist, but they
move: GitHub Models was the standard free recommendation across most AI curricula
until it was **retired at the end of July 2026**, breaking every tutorial that
pointed at it. A model on your own disk does not get retired.

Local also teaches you things a hosted API hides — context limits, tool-calling
reliability, what a reasoning trace costs you. Those are real engineering
constraints, and meeting them early is an advantage.

## Pick your tier

| Your machine | Model to pull | Notes |
|---|---|---|
| **16 GB VRAM GPU** | `qwen2.5:14b` | The labs' default. ~10s per call. |
| **16 GB RAM, no GPU** | `qwen2.5:14b` or a 9B | Works, noticeably slower. Be patient on first load. |
| **8 GB RAM, no GPU** | a 3-4B class model | Verify tool calling before trusting it — see below. |
| **Browser only** | *see [No local machine](#no-local-machine)* | Free notebook compute. |

## Install

```bash
# 1. Install Ollama — https://ollama.com/download
# 2. Pull a model
ollama pull qwen2.5:14b

# 3. Start the server with a raised context window (see the warning below)
OLLAMA_CONTEXT_LENGTH=64000 ollama serve
```

Confirm it works:

```bash
curl http://127.0.0.1:11434/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"qwen2.5:14b","messages":[{"role":"user","content":"say hi"}]}'
```

!!! warning "Raise the context window before you do anything else"
    Ollama defaults to a **4,096-token** context on machines with under 24 GiB of
    VRAM. An agent loop accumulating tool results passes that within a few turns,
    and Ollama then **silently discards the oldest messages — starting with your
    system prompt** — with no error and nothing in the response to tell you.

    The symptom is a confident, well-formed, wrong answer, and it is routinely
    misdiagnosed as "the model is not smart enough". Ollama's own documentation
    recommends at least 64,000 tokens for agent workloads.

## Check your model can actually call tools

Every agent module depends on this, and the failure is quiet: a model with weak
tool support stops calling tools and starts inventing answers instead of
erroring. Run [lab 02](https://github.com/nitin27may/ai-resources/tree/main/labs/02-tool-dispatch) — it exits non-zero and
tells you if the model answered from imagination instead of requesting the tool.

Measured on this hardware, 2026-08-21, on a two-tool multi-step task:

| Model | Tool calling | Reasoning trace | Latency |
|---|---|---|---|
| `qwen2.5:14b` | pass | none | ~10 s |
| `gemma4:12b` | pass | ~1,000 chars | ~39 s |
| `qwen3.5:9b` | pass | ~4,000 chars | ~65 s |

One scenario is not a benchmark — treat this as evidence that the 9B-and-up
class is viable, not as a ranking.

**The labs default to `qwen2.5:14b` because it emits no reasoning trace.**
Reasoning models interleave a long internal monologue and can spend their whole
output budget on it before answering — under a 1,024-token cap, `qwen3.5:9b`
produced 3,957 characters of reasoning and zero characters of answer. That
behaviour matters and gets [its own module](../02-agents/context-engineering.md);
it is simply the wrong thing to meet while learning what a tool call is.

## No local machine

If you cannot run a model locally, in rough order of how stable they have proven:

- **GitHub Codespaces** — 120 free core-hours/month, a full Linux box, `ollama`
  installs normally. The most concretely guaranteed of these options.
- **Google Colab / Kaggle** — free notebook GPUs. Colab deliberately publishes no
  quota or GPU type, so do not depend on getting a specific one.
- **A hosted free tier** — several exist. They change often, so this page does not
  pin one; check the provider's current limits before building on it.

Whichever you use, the labs need only an OpenAI-compatible endpoint:

```bash
export LAB_BASE_URL=...   # e.g. https://api.example.com/v1
export LAB_API_KEY=...
export LAB_MODEL=...
```

## Verify

```bash
python3 labs/01-first-call/lab.py
```

You should see the model answer, then fail to answer a follow-up without
conversation history, then answer it correctly with history. That is the whole
point of the lab, and it means your setup is good.

## Next

[Tool calling](../02-agents/tool-calling.md) — the first thing that turns a chat
model into something that can act.
