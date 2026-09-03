---
description: The no-code layer — models, prompting, retrieval, agents, safety and operations, in the order they build on each other.
tags:
  - Understand
  - Models
---

# Understand

!!! abstract "Understand · 5 min · no code"
    **Before this:** [Choose your path](../00-start-here/index.md)  ·  **After this:** [How models work](foundation-and-models.md)
    The no-code layer. Every page here links to its hands-on and in-depth versions.

Nine pages, in order, each needing only the ones before it. Read straight through
and you will have an accurate picture of how these systems work, where they fail,
and what to ask of anyone proposing one. No code, at any point.

The order is the argument: prompting needs models, retrieval is "give the model
your data", an agent is "let the model act" and needs both, and safety comes
after agents because the failure that matters arrives through a tool result.

Start at [AI 101](../getting-started/index.md) if you have not read it — it is
page one of this route and sets up everything here.

<div class="grid cards" markdown>

-   :material-chip:{ .lg .middle } __2 · How models work__

    Tokens, context windows, inference settings, reasoning models, and why
    parameter counts stopped meaning anything.

    [:octicons-arrow-right-24: How models work](foundation-and-models.md)

-   :material-chat-processing-outline:{ .lg .middle } __3 · Prompting__

    System prompts, few-shot examples, chain of thought, and getting a model to
    do what you actually meant.

    [:octicons-arrow-right-24: Prompting](prompting-and-techniques.md)

-   :material-database-search-outline:{ .lg .middle } __4 · Retrieval and data__

    RAG, embeddings and vector search: how a model comes to know things it was
    never trained on.

    [:octicons-arrow-right-24: Retrieval and data](retrieval-and-data.md)

-   :material-robot-outline:{ .lg .middle } __5 · What an agent is__

    The components, the loop, multi-agent systems, and the more important
    question of when not to use one.

    [:octicons-arrow-right-24: What an agent is](ai-agents.md)

-   :material-connection:{ .lg .middle } __6 · Agentic AI__

    Tool use, memory, orchestration patterns, human-in-the-loop, and the
    protocols underneath: MCP, A2A, AG-UI.

    [:octicons-arrow-right-24: Agentic AI](agentic-ai.md)

-   :material-domain:{ .lg .middle } __7 · Enterprise AI patterns__

    The five shapes this work actually takes in an organisation: copilot,
    autonomous agent, document processing, conversational AI, agentic RAG.

    [:octicons-arrow-right-24: Enterprise AI patterns](../patterns/enterprise-patterns.md)

-   :material-shield-check-outline:{ .lg .middle } __8 · Safety and responsible AI__

    Hallucination, prompt injection, guardrails, red teaming — and why prompt
    wording is not a security control.

    [:octicons-arrow-right-24: Safety and responsible AI](safety-and-responsible-ai.md)

-   :material-tune-variant:{ .lg .middle } __9 · Fine-tuning and training__

    What fine-tuning changes and what it does not, LoRA, RLHF, and why the
    answer is usually retrieval instead.

    [:octicons-arrow-right-24: Fine-tuning and training](fine-tuning-and-training.md)

-   :material-server-outline:{ .lg .middle } __10 · Infrastructure and operations__

    MLOps, drift, quantisation, edge deployment and what actually drives cost.

    [:octicons-arrow-right-24: Infrastructure and operations](infrastructure-and-operations.md)

</div>

---

## After these

**If you write code**, take the [build path](../00-start-here/the-path.md): the
same ideas as eleven modules that each end in something you run and break,
a model on your own machine.

**If you want depth on retrieval**, [Retrieval in depth](../rag/index.md) is six
pages on chunking, embeddings, vector databases, GraphRAG and evaluation.

**If you are choosing what to read elsewhere**, [Resources](../reference/resources.md)
is a ranked list with a reason to trust each item, and an explicit list of what
to avoid.
