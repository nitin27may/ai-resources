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
| [02-tool-dispatch](02-tool-dispatch/) | [Tool calling](../docs/02-agents/tool-calling.md) | The model requests; *you* execute. Arguments are an unvalidated string. |
| [03-agent-loop](03-agent-loop/) | [The agent loop](../docs/02-agents/the-agent-loop.md) | think → act → observe → repeat, in ~30 lines. |
| [04-loop-with-recovery](04-loop-with-recovery/) | [The harness](../docs/02-agents/the-harness.md) | Errors as context vs. limits in code; budgets that actually stop a run. |
| [05-context-limits](05-context-limits/) | [Context engineering](../docs/02-agents/context-engineering.md) | Overflow is silent. What gets dropped depends on the shape of the overflow. |
| [06-local-rag](06-local-rag/) | [Retrieval](../docs/02-agents/retrieval.md) | Retrieval always returns something. Toy corpora hide every real failure. |
| [07-eval-passk](07-eval-passk/) | [Evaluation](../docs/02-agents/evaluation.md) | pass@1 flatters; pass^k is what users experience. Judges need calibrating. |

## Swapping the model or the provider

Every lab reads three environment variables and nothing else:

```bash
# Local (default) — free
LAB_BASE_URL=http://127.0.0.1:11434/v1  LAB_API_KEY=ollama  LAB_MODEL=qwen2.5:14b

# A hosted OpenAI-compatible API — identical code, one line of config
LAB_BASE_URL=https://api.openai.com/v1  LAB_API_KEY=sk-...  LAB_MODEL=<a current model>
```

Run a lab both ways. The code does not change, which is the point — the
concepts here are not tied to any vendor.

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
