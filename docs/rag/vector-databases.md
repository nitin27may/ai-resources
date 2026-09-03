---
title: Vector Databases
description: Compare vector database options — Azure AI Search, Pinecone, Weaviate, Qdrant, Chroma, pgvector, and Milvus — and how to choose the right one.
status: new
tags:
  - Go deeper
  - Retrieval
  - Azure
---

# Vector databases

!!! abstract "Go deeper · 40 min · code optional"
    **Before this:** [Chunking strategies](chunking-strategies.md)  ·  **After this:** [GraphRAG](graphrag.md)
    **Hands-on version:** [7 Retrieval](../02-agents/retrieval.md)

**Verified as of 2026-09-02.**

!!! abstract
    Vector databases store and search high-dimensional embeddings using approximate nearest neighbor (ANN) algorithms. This page covers how they work, compares the major options, and gives you a practical decision framework for choosing between managed cloud services, self-hosted options, and lightweight alternatives.

---

## What makes a vector database different

Traditional databases search by exact match or range queries. Vector databases search by _similarity_ — finding the vectors closest to a query vector in high-dimensional space (typically 768–3072 dimensions for modern embedding models).

The core operation is **k-nearest neighbor (kNN) search**, and because exact kNN at scale is too slow, most systems use **approximate nearest neighbor (ANN)** algorithms that trade a small amount of recall for dramatically faster queries.

### ANN algorithms

**HNSW — Hierarchical Navigable Small Worlds**

The dominant algorithm in modern vector databases. Builds a multi-layer navigable graph where:

- Upper layers are sparse and enable fast long-distance traversal
- Lower layers are dense and enable fine-grained local search
- Queries start at the top and progressively narrow down

HNSW delivers millisecond latency at billion-vector scale with high recall. The tradeoff is memory: the graph structure is held in RAM. Build time is also non-trivial — adding 10M vectors can take minutes.

**IVF — Inverted File Index**

Partitions the vector space into Voronoi cells (clusters). At query time, only the nearest clusters are searched. More memory-efficient than HNSW but generally lower recall at the same speed. Useful when RAM is constrained.

**Flat (Exact)**

Brute-force exact search. 100% recall, no approximation error. Only practical up to ~100K vectors. Useful for small datasets or as a ground-truth baseline.

### Filtering + metadata

Raw ANN search gives you the nearest vectors — but in practice you almost always need to filter first ("only search documents from tenant X" or "only search articles from 2024"). How a database handles **pre-filtering vs post-filtering** significantly affects both accuracy and performance:

- **Pre-filtering**: filters the candidate set before ANN search — accurate but can be slow if the filter is selective
- **Post-filtering**: runs ANN then applies filters — fast but can return fewer than k results if many candidates are filtered out

Qdrant's payload filtering and Azure AI Search's hybrid filter support are both designed to handle this correctly.

!!! warning "Post-filtering is not access control"
    The distinction above is usually presented as a performance question. It is
    also a security one.

    If you retrieve first and filter afterwards, the restricted content was
    read, ranked and returned before your filter saw it. That is survivable
    inside a single trust boundary. It is not survivable when the filter is the
    thing enforcing which tenant or which user may see a document, because any
    bug, any bypassed code path, and the content is already in hand — and one
    step later it is in a prompt.

    Enforce identity and tenancy as a **pre-filter**, in the query the database
    executes. Treat post-filtering as an optimisation for non-security
    predicates only.

### Multi-tenancy and per-user access

Every serious retrieval system eventually needs "this user may see these
documents", and it is far cheaper to design in than to retrofit.

**Store the authorisation with the chunk.** At indexing time, write the groups,
roles or tenant identifier that may read it into the chunk's metadata. The unit
of access control has to be the chunk, because the chunk is the unit of
retrieval — a document-level check does not help once fragments are indexed
separately.

**Pass identity into every query.** The caller's groups become a filter on the
search itself. No filter should ever mean no results, rather than all results:
make the parameter required, so a forgotten filter fails loudly instead of
leaking quietly.

**Choose an isolation model deliberately.**

| Model | How | Suits |
|---|---|---|
| **Shared index, metadata filter** | One index, tenant ID on every chunk | Many small tenants; cheapest, and correctness rests entirely on the filter |
| **Index per tenant** | Separate index or collection each | Fewer, larger tenants; strong isolation, more to operate |
| **Cluster per tenant** | Separate deployment | Regulated or contractual isolation; most expensive |

Shared-with-filter is the common default and the one that fails hardest when it
fails, because a single missing predicate exposes everyone. If you use it, make
the filter impossible to omit in code, and test that with a case that would
otherwise leak.

**Plan for deletion and revocation.** Access changes and people leave. Re-index
or update metadata on permission changes, and remember that a deletion request
must reach the vector index and any long-term agent memory, not only the
primary database. Retrieval systems make copies; deletion has to follow them.

See [retrieval and permissions](../concepts/retrieval-and-data.md#retrieval-and-permissions)
for the same point at the overview level.

---

## Vector database comparison

| Database | Hosting | Scale | Hybrid Search | Filtering | Best For |
|---|---|---|---|---|---|
| **Azure AI Search** | Fully managed (Azure) | 100M+ vectors | BM25 + vector + semantic reranking | Pre/post filter with full OData expressions | Azure-integrated enterprise RAG |
| **Pinecone** | Managed cloud (serverless/pod) | Billions of vectors | Sparse + dense (hybrid) | Metadata filters | Standalone cloud-native RAG |
| **Weaviate** | Open-source + managed cloud | 100M+ vectors | BM25 + vector | GraphQL where clauses | Multi-modal search, GraphQL consumers |
| **Qdrant** | Open-source + managed cloud | 100M+ vectors | Sparse + dense | Rich payload filtering | High-performance self-hosted, Rust performance |
| **Chroma** | Local / self-hosted | <5M vectors | None (vector only) | Basic metadata | Local prototyping, notebooks |
| **pgvector** | Postgres extension (self-managed or managed) | Up to ~10M vectors | Postgres full-text + vector | Full SQL WHERE clauses | Teams already on Postgres, moderate scale |
| **Milvus** | Open-source + Zilliz Cloud | Billions of vectors | Sparse + dense | Scalar filtering | Enterprise self-hosted, cloud-native K8s |

---

## Indexing pipeline

When you ingest documents into a RAG system, each document goes through a pipeline before it's queryable:

```mermaid
flowchart LR
    A([Document]) --> B[Chunk]
    B --> C[Embed]
    C --> D[Upsert]
    D --> E[(Vector Index)]
    E --> F([Ready for Query])

    style A fill:#0284c7,color:#fff
    style B fill:#0d9488,color:#fff
    style C fill:#0d9488,color:#fff
    style D fill:#0d9488,color:#fff
    style E fill:#0f766e,color:#fff
    style F fill:#16a34a,color:#fff
```

**Chunk** — Split documents into overlapping segments (typically 256–512 tokens with 10–20% overlap). Chunk size affects both retrieval precision and context quality.

**Embed** — Pass each chunk through an embedding model (e.g., `text-embedding-3-large` or `text-embedding-3-small`). This produces a fixed-size float vector.

**Upsert** — Write the vector + metadata (source, chunk ID, text, timestamp, tenant ID) to the database.

**Index** — The database builds or updates its ANN index. Some databases do this continuously (HNSW append), others batch (IVF rebuild).

---

## Query pipeline

At query time the same flow runs in reverse:

```mermaid
flowchart LR
    A([User Question]) --> B[Embed Query]
    B --> C[ANN Search]
    C --> D[Top-K Results]
    D --> E{Rerank?}
    E -- Yes --> F[Reranker Model]
    E -- No --> G[LLM Context]
    F --> G

    style A fill:#0284c7,color:#fff
    style B fill:#0d9488,color:#fff
    style C fill:#0d9488,color:#fff
    style D fill:#0f766e,color:#fff
    style E fill:#d97706,color:#fff
    style F fill:#0284c7,color:#fff
    style G fill:#16a34a,color:#fff
```

**Reranking** (optional but high-impact) — A cross-encoder model scores each candidate chunk against the query. Significantly improves result quality at the cost of latency. Azure AI Search includes semantic reranking built-in. For standalone stacks, use Cohere Rerank or a local cross-encoder.

---

## Performance tradeoffs

| Algorithm | Query Speed | Recall | Memory Usage | Build Time |
|---|---|---|---|---|
| **HNSW** | Very fast (ms) | High (0.95–0.99) | High (graph in RAM) | Moderate |
| **IVF** | Fast | Medium (0.85–0.95, depends on nprobe) | Low–Medium | Fast |
| **Flat** | Slow (linear scan) | 100% (exact) | Low (just vectors) | Instant |

**recall@k** — the fraction of true nearest neighbors found in your top-k results. If recall@10 is 0.95, on average 9.5 of your 10 results are truly the closest vectors. Lower recall means relevant documents get dropped before the LLM ever sees them — a major failure mode in RAG. Always benchmark recall@k when tuning HNSW parameters (`ef_construction`, `M`).

---

## Azure AI Search deep dive

For Azure-based workloads, Azure AI Search is the default choice. It combines keyword search, vector search, and semantic reranking in a single managed service with enterprise security.

### Hybrid search

A single query can combine:

1. **BM25** — classic keyword ranking (good for precise terms, product codes, proper names)
2. **Vector search** — semantic similarity (good for paraphrased questions, synonyms)
3. **Semantic reranking** — a Microsoft-hosted cross-encoder re-scores the top results

The scores are combined using Reciprocal Rank Fusion (RRF) before reranking. This consistently outperforms pure vector search in production RAG benchmarks.

### Integrated vectorization

Azure AI Search can automatically embed documents on ingest via a **skillset** — you don't need to run a separate embedding pipeline. Point it at an Azure OpenAI embedding deployment and it handles chunking + embedding as part of the indexer run.

### Security

- RBAC on the search service (Reader, Contributor, Index Data Contributor roles)
- Private endpoint support — no public internet exposure
- Managed Identity for connecting to Azure OpenAI, Azure Blob, and Azure SQL data sources
- Customer-managed encryption keys (CMK)

### Index schema (simplified)

```json
{
  "name": "documents",
  "fields": [
    { "name": "id", "type": "Edm.String", "key": true },
    { "name": "content", "type": "Edm.String", "searchable": true },
    { "name": "content_vector", "type": "Collection(Edm.Single)",
      "dimensions": 1536, "vectorSearchProfile": "hnsw-profile" },
    { "name": "source", "type": "Edm.String", "filterable": true },
    { "name": "tenant_id", "type": "Edm.String", "filterable": true }
  ]
}
```

---

## Decision guide

=== "Managed Cloud"

    **Azure AI Search** — default if you're already on Azure. Handles hybrid search, semantic reranking, integrated vectorization, and enterprise security in one service. No separate infrastructure to manage.

    **Pinecone** — strong choice for teams not on Azure who want a dedicated, fully managed vector database. Serverless tier is cost-effective for variable workloads. Simple API, good SDKs. Doesn't include BM25 keyword search out of the box.

=== "Self-Hosted"

    **Qdrant** — best choice for teams who want high performance and rich filtering without a managed service. Written in Rust, memory-efficient, excellent payload filtering. Docker image is straightforward. Well-maintained with active development.

    **Weaviate** — good fit when you want GraphQL APIs or multi-modal search (text + images). More complex to operate than Qdrant. Its module system lets you plug in vectorizers at query time.

    **Milvus** — designed for cloud-native K8s deployments at billion-vector scale. More operational overhead than Qdrant but better horizontal scaling story. Use Zilliz Cloud (managed Milvus) if you want the scale without the ops burden.

=== "Already Have Postgres"

    **pgvector** — adds vector similarity search as a Postgres extension (`CREATE EXTENSION vector`). If your dataset is under ~5–10M vectors and your team is already running Postgres, pgvector is a legitimate production choice — not just a toy.

    When to graduate to a dedicated database:
    - Query latency exceeds acceptable thresholds (pgvector's HNSW is slower than native implementations)
    - You need hybrid search with BM25
    - You're running millions of updates per day (HNSW in pgvector doesn't handle deletes as cleanly)
    - Recall@k is materially lower than alternatives at your scale

=== "Prototyping"

    **Chroma** — zero-configuration, runs in-process or as a local server, stores data on disk. Ideal for notebooks, proof-of-concept work, and development. The API is simple and Python-first.

    Do not build production workloads on Chroma. It has no horizontal scaling, limited filtering, and no production support. Use it to validate your chunking strategy and prompt design, then migrate to a proper database before you ship.

---

!!! warning
    Don't over-engineer early. Start with pgvector (if you're on Postgres) or Chroma (for local dev). Only introduce a dedicated vector database when you have a concrete scale or performance problem. Premature infrastructure complexity is a real cost.

---

## Go deeper

- [Azure AI Search](https://learn.microsoft.com/en-us/azure/search/) — hybrid search and integrated vectorization; the default on Azure.
- [Pinecone](https://docs.pinecone.io/guides/get-started/overview) — managed, with the clearest documentation of the group.
- [Weaviate](https://docs.weaviate.io/weaviate) — open source with a hosted option, strong on hybrid search and filtering.
- [Qdrant](https://qdrant.tech/documentation/) — open source, Rust, notably good filtered-search performance.
- [pgvector](https://github.com/pgvector/pgvector) — vector search in Postgres. If you already run Postgres and are under roughly ten million vectors, start here and stop.

---
## Next steps

- [RAG Fundamentals](rag-fundamentals.md) — understand chunking, embedding, and retrieval before optimizing your vector store
- [GraphRAG](graphrag.md) — when standard vector search isn't enough for multi-hop or holistic queries
- [RAG Evaluation](rag-evaluation.md) — how to measure retrieval quality, recall@k, and end-to-end answer quality
