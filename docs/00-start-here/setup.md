---
title: Setup
description: Get a model answering on your own machine, for free, in under an hour.
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

Whichever you use, the labs need only an OpenAI-compatible endpoint.

## Pointing the labs at a hosted provider

Every lab reads the same four environment variables and nothing else. No lab
code changes between these.

=== "Ollama (default, free)"

    ```bash
    export LAB_BASE_URL=http://127.0.0.1:11434/v1
    export LAB_API_KEY=ollama            # ignored, but the header must exist
    export LAB_MODEL=qwen2.5:14b
    export LAB_EMBED_MODEL=nomic-embed-text
    ```

=== "OpenAI"

    ```bash
    export LAB_BASE_URL=https://api.openai.com/v1
    export LAB_API_KEY=sk-...
    export LAB_MODEL=<a current model>
    export LAB_EMBED_MODEL=text-embedding-3-small
    ```

=== "Azure OpenAI"

    ```bash
    export LAB_BASE_URL="https://<your-resource>.openai.azure.com/openai/v1"
    export LAB_API_KEY="<your key>"
    export LAB_MODEL="<your chat deployment name>"
    export LAB_EMBED_MODEL="<your embedding deployment name>"
    ```

    Three things differ from the others, and each has cost someone an afternoon.

    **`LAB_MODEL` is your deployment name, not a model name.** If you deployed
    a model and called the deployment `chat-prod`, that is the value. Sending
    the model's own name gives you `DeploymentNotFound`.

    **Embeddings need a second deployment.** Ollama and OpenAI serve chat and
    embeddings from one endpoint, so one name covers both. On Azure they are
    separate deployments, so `LAB_EMBED_MODEL` must be set independently or
    [module 5](../02-agents/retrieval.md) fails with `DeploymentNotFound` while
    everything else works.

    **Use the `/openai/v1` path.** It speaks the standard OpenAI shape, so the
    key goes in an `Authorization: Bearer` header and no `api-version` query
    parameter is needed. The older
    `/openai/deployments/<name>/chat/completions?api-version=...` path also
    works and requires an `api-key` header instead; the labs assume the former.

!!! success "Verified on 2026-09-04"
    All thirteen labs were run end to end against Azure OpenAI with only these four
    variables set, and no change to any lab.

    One result does not carry across unchanged. The [retrieval
    module](../02-agents/retrieval.md) reports a dense margin of 0.014 measured
    on `nomic-embed-text`; on Azure with `text-embedding-3-small` the same query
    gives 0.007. Absolute cosine scores belong to the embedding model, not to
    the corpus, so compare the shape of the result rather than the digits.

!!! danger "Never put a key in the repository"
    Export these in your shell, or keep them in a `.env` file that is
    git-ignored. A key committed to a public repository is compromised within
    minutes, and rotating it is the only fix.

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
