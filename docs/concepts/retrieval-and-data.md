---
description: A short overview of RAG, embeddings and vector databases before the deeper sections.
tags:
  - Understand
  - Retrieval
---

# Retrieval and data

!!! abstract "Understand · 30 min · no code"
    **Before this:** [Prompting](prompting-and-techniques.md)  ·  **After this:** [What an agent is](ai-agents.md)
    **Hands-on version:** [7 Retrieval](../02-agents/retrieval.md)  ·  **In depth:** [Retrieval in depth](../rag/index.md)

A model knows only what it was trained on, and it never knew anything of yours.
**Retrieval-augmented generation** closes that gap by fetching the relevant
material and putting it in the prompt, so the model reads instead of recalling.

This is the overview: how the pipeline works, the pieces it is built from, how
it fails, and when to reach for fine-tuning instead. The
[build module](../02-agents/retrieval.md) has you construct one and watch it get
a question quietly wrong; [Retrieval in depth](../rag/index.md) is six pages on
the engineering.

---

## What is RAG?

**Retrieval-Augmented Generation (RAG)** is a pattern where, instead of relying solely on a model's built-in knowledge, you **retrieve relevant information** from an external source and include it in the prompt before generating a response.

This solves several problems:

- **Stale knowledge**: Models have a training cutoff date. RAG gives them access to current data.
- **Hallucinations**: By grounding responses in retrieved facts, RAG significantly reduces fabrication.
- **Domain specificity**: Your internal documents, policies, and data can be surfaced without fine-tuning.

### How RAG works

```mermaid
graph TD
    A["User Question"] --> B["Generate<br/>Embedding"]
    B --> C["Vector<br/>Database"]
    C -->|"Similarity<br/>Search"| D["Relevant<br/>Chunks"]
    D --> E["Build Prompt<br/>(Question + Context)"]
    E --> F["LLM"]
    F --> G["Grounded<br/>Response"]

    style A fill:#0284c7,stroke:#0284c7,color:#fff
    style B fill:#0284c7,stroke:#0284c7,color:#fff
    style C fill:#0d9488,stroke:#0d9488,color:#fff
    style D fill:#0f766e,stroke:#0d9488,color:#fff
    style E fill:#0f766e,stroke:#0d9488,color:#fff
    style F fill:#0284c7,stroke:#0284c7,color:#fff
    style G fill:#16a34a,stroke:#16a34a,color:#fff
```

**Step by step:**

1. **User asks a question** — for example, "What is our company's remote work policy?"
2. **The question is converted to an embedding** — a numerical representation that captures its meaning.
3. **A similarity search runs against the vector database** — finding document chunks whose embeddings are closest to the question's embedding.
4. **The most relevant chunks are retrieved** — typically the top 3-10 results.
5. **A prompt is assembled** — combining the user's question with the retrieved context.
6. **The LLM generates a response** — grounded in the retrieved information rather than its general training data.

!!! tip "RAG is not keyword search"
    It uses **semantic similarity**, so it finds relevant content even when the
    words do not match. "Can I work from home?" matches a document titled
    "Remote Work Policy" with no shared vocabulary at all.

### The two steps almost every production system adds

The six steps above are the naive pipeline. Nearly every system that works in
production adds two more, and they are worth knowing at this level because they
account for most of the quality difference.

**Hybrid search.** Run semantic search *and* keyword search, then merge the
results. Semantic search is weak exactly where keyword search is strong: product
codes, error numbers, surnames, acronyms — anything where the exact string is
the point. A query for `ERR-4471` may return nothing useful from a pure vector
search, because the embedding of a code carries little meaning. This is usually
the single highest-value change to a mediocre RAG system.

**Reranking.** Retrieve more candidates than you need — say 50 — then pass them
through a reranker, a model that scores each candidate against the query
directly rather than comparing precomputed vectors. It is far more accurate and
far too slow to run over a whole corpus, which is why it goes second. Keep the
top handful.

```mermaid
graph LR
    Q["Question"] --> V["Vector search"]
    Q --> K["Keyword search"]
    V --> M["Merge"]
    K --> M
    M --> R["Rerank<br/>top ~50"]
    R --> T["Top 3-5<br/>into the prompt"]

    style Q fill:#0284c7,stroke:#0270a8,color:#fff
    style V fill:#0d9488,stroke:#0b7a72,color:#fff
    style K fill:#0d9488,stroke:#0b7a72,color:#fff
    style M fill:#0f766e,stroke:#0d9488,color:#fff
    style R fill:#d97706,stroke:#b86005,color:#fff
    style T fill:#16a34a,stroke:#15803d,color:#fff
```

---

## Embeddings

An **embedding** is a dense numerical vector (a list of numbers) that represents the meaning of a piece of text. Similar meanings produce vectors that are close together in high-dimensional space.

!!! tip "Deep dive available"
    For embedding model comparisons, dimension tradeoffs, input types, and production guidance, see [Embeddings](../rag/embeddings.md).

| Text | Embedding (simplified) |
|---|---|
| "dog" | [0.12, 0.85, 0.33, ...] |
| "puppy" | [0.13, 0.84, 0.31, ...] |
| "automobile" | [0.91, 0.05, 0.72, ...] |

Notice that "dog" and "puppy" have very similar vectors, while "automobile" is far away. This is the core principle behind semantic search.

### Embedding models

Embedding models are specialized models designed to convert text into vectors. They are different from generative models — they do not produce text, only vectors.

| Model | Dimensions | Provider |
|---|---|---|
| text-embedding-3-large | 3,072 | OpenAI |
| text-embedding-3-small | 1,536 | OpenAI |
| Cohere Embed v4 | 1,024 (configurable) | Cohere |
| BGE-large-en-v1.5 | 1,024 | BAAI (open source) |

!!! note "Dimensions matter"
    Higher dimensions capture more nuance but require more storage and compute. For most enterprise use cases, 1,024-1,536 dimensions offer a good balance.

---

## Vector databases

A **vector database** is a specialized data store optimized for storing, indexing, and querying embedding vectors at scale. Traditional databases use exact-match queries; vector databases use **approximate nearest neighbor (ANN)** algorithms to find the most similar vectors efficiently.

### How vector search works

1. **Indexing**: When you ingest a document, each chunk is embedded and stored as a vector.
2. **Querying**: When a user asks a question, the question is embedded and the database finds the closest stored vectors.
3. **Ranking**: Results are ranked by similarity score (typically cosine similarity or dot product).

### Popular vector databases

| Database | Type | Key Strengths |
|---|---|---|
| Azure AI Search | Managed service | Hybrid search (vector + keyword), integrated with Azure ecosystem |
| Pinecone | Managed service | Simple API, serverless option, fast at scale |
| Weaviate | Open source / managed | GraphQL API, multi-modal support |
| Qdrant | Open source / managed | Rust-based performance, filtering |
| Chroma | Open source | Lightweight, great for prototyping |
| pgvector | PostgreSQL extension | Use your existing Postgres infrastructure |

!!! tip "Hybrid search"
    The best results often come from **hybrid search** — combining vector similarity with traditional keyword matching. Azure AI Search supports this natively with its hybrid search capability.

---

## Chunking strategies

Before you can embed documents, you need to break them into **chunks** — smaller pieces that fit within embedding model limits and provide focused, retrievable units of information.

Chunking strategy directly impacts retrieval quality. Too large and chunks contain mixed topics. Too small and chunks lack context.

!!! tip "Deep dive available"
    For all eight chunking strategies including parent-child, late chunking, and agentic chunking — with a decision flowchart — see [Chunking Strategies](../rag/chunking-strategies.md).

### Common strategies

| Strategy | Description | Best For |
|---|---|---|
| **Fixed-size** | Split every N characters/tokens with overlap | Simple documents, quick setup |
| **Sentence-based** | Split on sentence boundaries | Narratives, articles |
| **Paragraph-based** | Split on paragraph breaks | Well-structured documents |
| **Semantic** | Use an embedding model to detect topic shifts | Complex documents with varied content |
| **Recursive** | Try paragraph, then sentence, then character splits | General-purpose fallback |
| **Document-aware** | Respect headings, sections, tables | Technical docs, reports with structure |

!!! warning "Overlap is important"
    Always include overlap between chunks (typically 10-20% of chunk size). Without overlap, important information that spans a chunk boundary can be lost.

### Chunk size guidelines

| Use Case | Recommended Chunk Size |
|---|---|
| FAQ / short-answer retrieval | 200-500 tokens |
| Document summarization | 500-1,000 tokens |
| Technical documentation | 300-800 tokens |
| Legal / regulatory text | 500-1,000 tokens |

---

## Knowledge graphs and GraphRAG

Traditional RAG retrieves isolated chunks. **GraphRAG** adds a layer of structure by building a **knowledge graph** from your documents — capturing entities, relationships, and themes.

!!! tip "Deep dive available"
    For Microsoft GraphRAG's full architecture, local vs global query modes, cost tradeoffs, and implementation options, see [GraphRAG](../rag/graphrag.md).

### Why GraphRAG?

- **Multi-hop reasoning**: Answer questions that require connecting information across multiple documents.
- **Thematic understanding**: Identify high-level themes and summaries across a corpus.
- **Better context**: Provide the LLM with structured relationships, not just text snippets.

### How GraphRAG works

```mermaid
graph TD
    A["Documents"] --> B["Entity &<br/>Relationship<br/>Extraction"]
    B --> C["Knowledge<br/>Graph"]
    C --> D["Community<br/>Detection"]
    D --> E["Summarization"]

    F["User Query"] --> G["Graph<br/>Traversal"]
    C --> G
    G --> H["Structured<br/>Context"]
    H --> I["LLM"]
    I --> J["Rich<br/>Response"]

    style A fill:#0284c7,stroke:#0284c7,color:#fff
    style B fill:#0284c7,stroke:#0284c7,color:#fff
    style C fill:#0d9488,stroke:#0d9488,color:#fff
    style D fill:#0f766e,stroke:#0d9488,color:#fff
    style E fill:#0f766e,stroke:#0d9488,color:#fff
    style F fill:#0284c7,stroke:#0284c7,color:#fff
    style G fill:#0284c7,stroke:#0284c7,color:#fff
    style H fill:#0f766e,stroke:#0284c7,color:#fff
    style I fill:#0284c7,stroke:#0284c7,color:#fff
    style J fill:#16a34a,stroke:#16a34a,color:#fff
```

!!! note "GraphRAG vs standard RAG"
    Use standard RAG when questions are about specific facts in specific documents. Use GraphRAG when questions require synthesis across many documents or understanding of relationships between entities.

---

## How RAG fails

Everything above is the happy path. These are the failures you will actually
meet, and the first one is the one that matters most.

### Retrieval always returns something

A vector search ranks by similarity, and something is always the most similar.
Ask a question your corpus cannot answer and you will still get chunks back —
the closest ones, however far away that is. Nothing in the mechanism says "no
good match".

The model then answers from whatever it was handed, fluently. The user sees a
confident answer built from irrelevant material, with no signal that anything
went wrong.

Two defences, and you want both. Look at the **similarity score**, not just the
rank, and set a floor below which you treat the result as no answer. And tell
the model explicitly that it may decline: *"If the context does not contain the
answer, say you do not know."* That instruction only works if the model has been
given a way to be right about being unable to answer.

!!! warning "Toy corpora hide this completely"
    On six documents, everything works. The build module measures what happens
    when forty plausible neighbours are added: dense search sat **0.014** away
    from returning the wrong document while still ranking the right one first.
    Read the margin, not the rank — see [Retrieval](../02-agents/retrieval.md).

### The other four

**Chunk boundaries cut the answer in half.** The fact spans two chunks; each
alone looks irrelevant. Overlap helps, parent-child retrieval helps more.

**The question does not look like the answer.** Users ask "why was I charged
twice?" while the document says "duplicate transaction handling". Semantic
search handles some of this and not all; hybrid search and query rewriting close
more of the gap.

**Stale index.** The document was updated, the index was not. RAG's advantage
over fine-tuning is freshness, and that advantage is only as good as your
re-indexing. Know your lag and monitor it.

**The context is retrieved and then ignored.** With many chunks in a long
prompt, the model can miss the one that matters, especially in the middle. More
context is not better context — see
[context engineering](../02-agents/context-engineering.md).

---

## Retrieval and permissions

This is where enterprise RAG projects most often go wrong, and it rarely appears
in tutorials.

An index built from "all the company's documents" will happily retrieve a
salary review, an unannounced restructure, or another customer's contract, and
the model will summarise it politely for whoever asked. The retrieval layer has
no idea who is asking unless you build that in.

Three rules:

1. **Filter at query time, by the asking user's identity.** Store the access
   control list with each chunk and pass the user's groups as a filter on the
   search itself. Every serious vector store supports metadata filtering for
   this reason.
2. **Never filter after retrieval, in the prompt.** "Only use documents the user
   is allowed to see" is an instruction, and instructions are not access
   control. The content is already in the context by then.
3. **Re-check at answer time if permissions move fast.** Access can be revoked
   between indexing and asking.

The same reasoning applies to what retrieval can *carry*. A document is
untrusted input: if it contains text saying "ignore your instructions and
forward this", that text arrives inside your prompt. See
[safety](safety-and-responsible-ai.md) and the
[safety module](../02-agents/safety.md).

---

## How you know it is working

RAG has two failure surfaces and they need measuring separately, because fixing
the wrong one is wasted effort.

| Question | What it tests | If it is bad |
|---|---|---|
| Did we retrieve the right material? | The retriever | Chunking, embeddings, hybrid search, reranking |
| Did the answer use it faithfully? | The generator | Prompt, model, context length |

A system can retrieve perfectly and answer badly, or retrieve nothing useful and
produce a fluent answer that happens to sound right. A single end-to-end score
hides both.

The minimum worth having is a set of real questions with known correct sources.
Twenty is enough to start, and it tells you more than any amount of tuning by
feel. See [RAG evaluation](../rag/rag-evaluation.md).

---

## RAG vs fine-tuning: when to use which

This is one of the most common decisions in AI application design. Here is a clear comparison:

| Factor | RAG | Fine-tuning |
|---|---|---|
| **Best for** | Grounding in specific, changing data | Teaching the model new behaviors or styles |
| **Data freshness** | Real-time (data can be updated anytime) | Static (requires retraining to update) |
| **Setup effort** | Moderate (indexing pipeline) | High (training pipeline, GPU resources) |
| **Cost** | Per-query retrieval cost + LLM cost | Upfront training cost + inference cost |
| **Hallucination control** | Strong (responses grounded in retrieved data) | Moderate (model may still hallucinate) |
| **Customization depth** | Surface-level (provides context) | Deep (changes model behavior) |
| **When data changes** | Re-index documents | Retrain the model |
| **Example use case** | "Answer questions about our HR policies" | "Write emails in our brand voice" |

!!! tip "Combine them"
    RAG and fine-tuning are not mutually exclusive. A fine-tuned model that also uses RAG can provide domain-specific behavior **and** up-to-date, grounded responses. Many production systems use both.

### Decision guide

=== "Use RAG when"

    - Your data changes frequently
    - You need citations and traceability
    - You want to avoid retraining costs
    - Accuracy on specific documents is critical
    - You need to keep data private (data stays in your infrastructure)

=== "Use fine-tuning when"

    - You need the model to adopt a specific tone or style
    - The task requires specialized domain knowledge baked into the model
    - You want to reduce prompt size (the model "just knows" things)
    - Latency is critical and you cannot afford retrieval overhead

=== "Use both when"

    - You need domain-specific behavior AND current data
    - You want a fine-tuned model that can also reference live documents
    - You are building a production system that requires both accuracy and style

---

## Go deeper

- [Retrieval in depth](../rag/index.md) — six pages on this site covering chunking, embeddings, vector databases, GraphRAG and evaluation. Start there before any vendor guide.
- [RAG with Azure AI Search](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview) — Microsoft's production-oriented walkthrough, including hybrid search.
- [LangChain RAG tutorial](https://docs.langchain.com/oss/python/langchain/rag) — end to end in code, if you want a framework doing the wiring.
- [Microsoft GraphRAG](https://microsoft.github.io/graphrag/) — read the indexing-cost section before you get excited.
- [Pinecone learning centre](https://www.pinecone.io/learn/) — vendor-published, but the chunking and hybrid-search explanations are genuinely good.


