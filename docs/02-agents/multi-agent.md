---
title: Multi-agent
description: Two orchestrations of the same task, measured — and the failure that decides whether to split the work at all.
tags:
  - Build
  - Agents
  - Patterns
---

# Multi-agent

!!! abstract "Build · 1.5 h · hands-on"
    **Before this:** [11 Production](production.md)  ·  **After this:** [Retrieval in depth](../rag/index.md)
    **In depth:** [Design patterns](../patterns/design-patterns.md#when-multiple-agents-actually-help)

!!! abstract
    Run the same task as one agent and as a supervisor with three specialists,
    and measure both. Then watch two agents edit the same document. The second
    experiment is the one that decides the architecture.

**Prerequisites:** [Production](production.md) — you have a single agent you
trust.

**Verified as of 2026-09-02**, against a local Ollama model and Azure OpenAI.

## What you'll be able to do

Say what multiple agents actually buy, in tokens and wall time; recognise the
context loss that makes a split answer worse rather than merely dearer; and
apply the one rule that reconciles the published disagreement on this subject.

## Why this comes last

Everything before this module was one agent. That was not a simplification for
teaching — it is the right default, and most systems that reach for a second
agent have not exhausted the first.

Multi-agent architectures are attractive because they map onto how we think
about teams. That is not evidence.

## Build it

```bash
python3 labs/11-multi-agent/lab.py
```

One question over a three-document corpus, answered twice: once by a single
agent holding everything, once by a supervisor delegating to three specialists
running in parallel. Then a second experiment where two agents edit one
document.

## Verify

Measured on Azure OpenAI, `gpt-4.1`:

| | One agent | Supervisor + 3 |
|---|---|---|
| Model calls | 1 | 4 |
| Total tokens | 233 | 595 |
| Wall time | 1.4s | 2.3s |

The split cost **2.6x the tokens** and was **slower**, because on a corpus this
small the parallelism saves less than the extra round of calls costs. Each
sub-agent carries its own context, and the findings have to be passed back.

That is the boring result. Here is the one that matters.

!!! danger "The split answer was also worse"
    The single agent noted the 24-month warranty applies. The warranty
    specialist, seeing only the warranty document, judged the question NOT
    RELEVANT — correct about its own document, wrong about the question.

    That judgement is final. The supervisor cannot recover information a
    sub-agent decided not to return, because it never saw the source.

    The lab detects this and says so. It is intermittent, which is exactly what
    makes it dangerous: it will not show up in your demo.

This is the concrete form of the argument against multi-agent systems.
Sub-agents lose the context that made the connection visible, and no amount of
supervisor prompting recovers it, because the information never arrives.

## The write conflict

The second experiment gives two agents the same document and a different
requirement each, in parallel, neither aware of the other:

```
original          > refunds are issued within 5 working days.
finance officer   > refunds are issued within 14 working days to allow for reconciliation.
customer advocate > refunds are issued within 2 working days.
```

Both edits are individually correct and mutually exclusive. There is no merge.
Whichever write lands last wins, silently, and the published policy depends on
thread scheduling.

Nothing about the model caused this. Parallel writers to shared state is an
ordinary concurrency bug — and giving the writers judgement makes it worse,
because each produces a plausible result that hides the conflict rather than
raising it.

## The rule

Two companies shipping real agents published opposite conclusions one day apart
in June 2025: Cognition arguing against multi-agent systems, Anthropic
describing a multi-agent research system that worked. Both are right, and the
difference between the cases is what the sub-agents are doing.

> **Parallelise the reading. Keep one writer.**

| Splits well | Does not |
|---|---|
| Search, research, review | Editing shared state |
| Genuinely independent sub-tasks | Sub-tasks depending on each other's decisions |
| Findings compose by concatenation | Results needing reconciliation |
| Sources too large for one context | A corpus that already fits |

Cognition later revised their position to exactly this: multiple agents
contributing intelligence, with writes single-threaded.

## Before you split

In order, and most teams stop before the end:

1. One agent with more tools
2. One agent with better retrieval
3. Sub-agents for parallel, read-only work
4. Multiple writers, with real coordination

## In production

Everything from the earlier modules now applies N times over.

- **Budgets per agent and for the whole run.** A runaway sub-agent is a runaway
  bill, and the parent may not notice.
- **Correlated tracing from the start.** "Why did it do that?" across four
  agents is unanswerable without a shared run ID on every span. Retrofitting
  this after an incident means having no data about the incident.
- **Decide what a sub-agent failure means.** Does the parent retry, proceed with
  partial findings, or abort? Silently proceeding is the default and is rarely
  right.
- **Idempotency still applies**, and now the retry may come from a different
  agent than the original call.

## Go deeper

- [Design patterns](../patterns/design-patterns.md#when-multiple-agents-actually-help)
  — supervisor, hierarchical, handoff and parallel as patterns.
- [Don't build multi-agents](https://cognition.com/blog/dont-build-multi-agents)
  and [how we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
  — read them as a pair; the disagreement teaches more than either alone.
- [Multi-agents working](https://cognition.com/blog/multi-agents-working) —
  the revision, and the single-writer rule.

## Next

You have finished the path. [Retrieval in depth](../rag/index.md) goes further
on the retrieval layer, [Architecture patterns](../patterns/index.md) on
structure, and [Resources](../reference/resources.md) is the ranked reading list
for everything after.
