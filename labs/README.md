# Labs

Small, framework-free programs you run yourself. Standard library only — no
`pip install`, no account, no API key, no cost.

Each lab exists to make one mechanism visible. They are deliberately not
production code: there is no retry logic, no streaming, no async. Those come
later, once you can see what they are wrapping.

## Setup

```bash
ollama pull qwen2.5:14b
ollama pull nomic-embed-text   # lab 06 only
OLLAMA_CONTEXT_LENGTH=64000 ollama serve
python3 labs/01-first-call/lab.py
```

That is the whole setup. See [Setup](../docs/00-start-here/setup.md) if you
have no GPU, 8 GB of RAM, or only a browser.

## The labs

| Lab | Module | What it makes visible |
|-----|--------|-----------------------|
| [01-first-call](01-first-call/) | The model | A conversation is a list you resend. The model is stateless. |
| [02b-structured-output](02b-structured-output/) | [Structured output](../docs/02-agents/structured-output.md) | A schema guarantees shape, never truth. Make refusal representable. |
| [02-tool-dispatch](02-tool-dispatch/) | [Tool calling](../docs/02-agents/tool-calling.md) | The model requests; *you* execute. Arguments are an unvalidated string. |
| [03-agent-loop](03-agent-loop/) | [The agent loop](../docs/02-agents/the-agent-loop.md) | think → act → observe → repeat, in ~30 lines. |
| [04-loop-with-recovery](04-loop-with-recovery/) | [The harness](../docs/02-agents/the-harness.md) | Errors as context vs. limits in code; budgets that actually stop a run. |
| [05-context-limits](05-context-limits/) | [Context engineering](../docs/02-agents/context-engineering.md) | Overflow is silent. What gets dropped depends on the shape of the overflow. |
| [05b-memory](05b-memory/) | [Memory](../docs/02-agents/memory.md) | The model remembers nothing. A bad write is replayed forever. |
| [06-local-rag](06-local-rag/) | [Retrieval](../docs/02-agents/retrieval.md) | Retrieval always returns something. Toy corpora hide every real failure. |
| [07-eval-passk](07-eval-passk/) | [Evaluation](../docs/02-agents/evaluation.md) | pass@1 flatters; pass^k is what users experience. Judges need calibrating. |
| [08-tracing](08-tracing/) | [Observability](../docs/02-agents/observability.md) | A trace is a span tree. Token cost is quadratic in turns. |
| [09-prompt-injection](09-prompt-injection/) | [Safety](../docs/02-agents/safety.md) | Tool output can instruct the agent. Prompt-level defences do not hold. |
| [10-production](10-production/) | [Production](../docs/02-agents/production.md) | A retry duplicates the order. Idempotency, not fewer retries. No model needed. |
| [11-multi-agent](11-multi-agent/) | [Multi-agent](../docs/02-agents/multi-agent.md) | Parallelise the reading, keep one writer. |

## Swapping the model or the provider

Every lab reads four environment variables and nothing else. The code does not
change between providers, which is the point — nothing here is tied to a vendor.

```bash
# Local (default) — free
LAB_BASE_URL=http://127.0.0.1:11434/v1
LAB_API_KEY=ollama
LAB_MODEL=qwen2.5:14b
LAB_EMBED_MODEL=nomic-embed-text

# OpenAI
LAB_BASE_URL=https://api.openai.com/v1
LAB_API_KEY=sk-...
LAB_MODEL=<a current model>
LAB_EMBED_MODEL=text-embedding-3-small

# Azure OpenAI
LAB_BASE_URL=https://<resource>.openai.azure.com/openai/v1
LAB_API_KEY=<key>
LAB_MODEL=<chat DEPLOYMENT name, not the model name>
LAB_EMBED_MODEL=<embedding DEPLOYMENT name>
```

**Azure notes.** `LAB_MODEL` is the deployment name you chose, not the model's
name — sending the latter returns `DeploymentNotFound`. Chat and embeddings are
separate deployments on Azure, unlike Ollama and OpenAI where one name serves
both, so `LAB_EMBED_MODEL` has to be set independently or lab 06 fails while
everything else works. The `/openai/v1` path speaks the standard OpenAI shape,
so the key goes in `Authorization: Bearer` with no `api-version` parameter.

**Verified 2026-09-04:** all thirteen labs run clean against Azure OpenAI with
only these variables set and no code change.

Lab 06 is the one lab whose printed numbers are provider-dependent, because
absolute cosine scores differ per embedding model. The margins quoted in the
[retrieval module](../docs/02-agents/retrieval.md) are the `nomic-embed-text`
run: dense 0.580 vs 0.566, a margin of 0.014. On Azure with
`text-embedding-3-small` the same query gives 0.413 vs 0.406 — a margin of
0.007, half as wide. The conclusion the lab draws is unchanged and slightly
stronger, and the lab prints whatever it actually measured rather than the
documented figure.

Keys belong in your shell or a git-ignored `.env`, never in the repository.

## Why the default model is not a reasoning model

`qwen2.5:14b` is the default because it returns no thinking trace. Reasoning
models interleave a long internal monologue and can spend their entire output
budget on it before producing an answer — measured on this hardware,
`qwen3.5:9b` emitted 3,957 characters of reasoning and **zero** characters of
content under a 1,024-token cap, while `qwen2.5:14b` answered the same prompt
in 10 seconds with no trace at all.

That behaviour is worth understanding, and it gets a module of its own
([context engineering](../docs/02-agents/context-engineering.md)). It is just
the wrong thing to meet while you are still learning what a tool call is.

## If a lab fails

That is often the lesson, not a bug. Lab 03 prints `PASS`/`FAIL` against a
known-correct answer. A `FAIL` means the harness ran correctly and the *model*
got it wrong — which is exactly the gap [evaluation](../docs/02-agents/evaluation.md)
exists to measure, and adding a framework does not close it.
