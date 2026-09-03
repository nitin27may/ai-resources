---
title: Memory
description: Where information goes when it will not fit in the context window — and why a wrong write is worse than a wrong answer.
tags:
  - Build
  - Agents
---

# Memory

!!! abstract "Build · 1 h · hands-on"
    **Before this:** [5 Context engineering](context-engineering.md)  ·  **After this:** [7 Retrieval](retrieval.md)
    **Overview version:** [Agentic AI](../concepts/agentic-ai.md#agent-memory)

!!! abstract
    The model remembers nothing, so every memory feature is software you wrote.
    You will build a store, watch one bad write corrupt every later
    conversation, and then make the store safe to trust.

**Prerequisites:** [Context engineering](context-engineering.md) — you have
watched the window overflow.

**Verified as of 2026-09-02**, against a local Ollama model and Azure OpenAI.

## What you'll be able to do

Build a store an agent reads and writes; explain why long-term memory and
retrieval are the same machinery; recognise memory poisoning when it presents
as the model getting worse; and design writes you can later distrust.

## Why this comes after context engineering

The last module ended with things falling out of the window. This one is about
where they go instead.

That framing matters, because "add memory" is usually reached for as a feature
and is better understood as the second half of a constraint you have already
met. The window is finite. Anything that must survive it has to live somewhere
your code controls.

## The three kinds

| Kind | Lives in | Lost when | Example |
|---|---|---|---|
| **Short-term** | The message list you resend | The session ends, or the window overflows | What the user said three messages ago |
| **Long-term** | A store you own | Never, until you delete it | This customer prefers eco-friendly packaging |
| **Episodic** | A record of past runs | Never | This approach failed last time |

Short-term memory you already built, in module 1: it is the list you append to.
This module is about the other two, and they are the same mechanism — write
something down, decide later whether to put it back in the prompt.

## Build it

```bash
python3 labs/05b-memory/lab.py
```

Four stages: two sessions with no store, the same two with one, a single bad
write, and the fixes.

## Verify

**Stage 1** is the baseline. Tell the agent a preference, start a fresh
conversation, ask a question that depends on it, and watch it not know. The
model did not forget. It was never told.

**Stage 2** adds one line to a JSON file and replays it into the system prompt.
The agent now "remembers". Nothing about the model changed, and that is the
entire mechanism behind every personalised assistant you have used.

**Stage 3** is the one to sit with. A second fact is written — a delivery
address that was *inferred* rather than stated. The renderer prints every fact
identically, so nothing in the prompt marks it as weaker. Then:

```
user  > Where will my order be delivered?
agent < Your order will be delivered to 14 Bridge Street, Leeds.

user  > Can you confirm my details before I check out?
agent < Your delivery address is 14 Bridge Street, Leeds, and you have
        selected eco-friendly packaging.
```

Identical on both providers tested.

!!! danger "This is not a hallucination"
    The model is reporting its context accurately. Your store lied to it.

    That distinction decides where you look when it happens. The prompt is
    fine, the model is fine, and no amount of prompt engineering will fix it.
    The defect is a write that happened days earlier.

**Stage 4** applies three fixes and shows each working: provenance carried into
the prompt so unconfirmed facts are marked, forgetting so the bad write can be
removed, and narrow writes — the lab measures a transcript-style write at
roughly four times the size of a fact-style one, paid on every turn that
retrieves it.

## Why a bad write is worse than a bad answer

A wrong answer is seen once and discarded. A wrong memory is replayed into
every future run as established context, and the model has no mechanism for
doubting its own context.

The symptom is what makes it expensive to diagnose: the assistant appears to get
worse over time, for one user, intermittently. Teams reach for the model, the
prompt and the retrieval layer before they think to read the store.

**So writes deserve more suspicion than reads.** That is the inversion worth
carrying away, because every framework makes writing easy and none of them make
it careful.

## The four decisions, all yours

1. **What to write.** Facts and decisions, never transcripts. If you cannot say
   why a line will matter in a future conversation, do not store it.
2. **When to write.** Prefer explicit statements over inferences. If you must
   store an inference, record that it is one.
3. **When to read.** Retrieving everything on every turn wastes context and
   buries the current task. This is retrieval, with all of module 7's problems.
4. **When to forget.** Almost nobody builds this. It is why memory systems rot:
   preferences change, facts expire, and an append-only store never
   self-corrects.

## In a framework

LangGraph checkpointers, Agent Framework thread state and the various managed
memory services all provide the store and the plumbing. None of them decide what
is worth remembering, whether it was stated or inferred, or when it stops being
true. Those four decisions stay yours whichever you pick.

## In production

- **Scope memory to a subject and enforce it.** Memory keyed loosely by
  conversation rather than tightly by user is how one customer's preferences
  reach another. Same rule as
  [retrieval and permissions](../concepts/retrieval-and-data.md#retrieval-and-permissions).
- **Make it inspectable and deletable.** Users will ask what you remember and
  ask you to forget it. A deletion request must reach the memory store, not
  only the primary database.
- **Log what memory was in context.** Otherwise a bad answer cannot be traced to
  the write that caused it.
- **Cap it.** Memory grows without limit and is billed on every turn that
  retrieves it. Decide the budget before it decides itself.

## Go deeper

- [Agentic AI](../concepts/agentic-ai.md#agent-memory) — the same material
  without code.
- [Retrieval](retrieval.md) — the next module, and the machinery memory reuses.
- [Context engineering](context-engineering.md) — the constraint memory exists
  to work around.

## Next

[Retrieval](retrieval.md) — get information the model was never trained on into
its context, and find the case where it silently fails.
