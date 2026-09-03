---
description: Plain-language definitions of the AI terms you will meet across this site.
tags:
  - Reference
  - Reference
---

# AI glossary

!!! abstract "Reference · browse · no code"
    Every term used on this site, in plain English. Keep it open while you read anything else.

A comprehensive reference of AI terms and concepts explained in plain English. Use your browser's search (Ctrl+F / Cmd+F) or the site search to find specific terms.

---

## :material-cube-outline: Foundation & models {#foundation-models}

Large Language Model (LLM)
:   AI models trained on massive text datasets that can understand and generate human language. Examples include OpenAI's GPT-4o, Anthropic's Claude, Google's Gemini, and Meta's Llama. They power chatbots, code assistants, document summarization, and much more.

Small Language Model (SLM)
:   Compact, purpose-built language models optimized for specific tasks rather than general knowledge. They run faster, cost less, and can be deployed on-premises or at the edge. Examples include Microsoft's Phi series and Google's Gemma.

Foundation Model
:   A large AI model pre-trained on broad data that serves as a starting point for many downstream tasks. Instead of training from scratch, organizations fine-tune foundation models for their specific use cases, saving time and compute costs.

Vision Language Model (VLM)
:   Models that can process both images and text together, enabling tasks like describing photos, reading documents with images, or answering questions about visual content. GPT-4o, Gemini, and the Claude model family are examples that handle multimodal inputs.

Transformer
:   The neural network architecture behind modern LLMs. It uses a mechanism called "attention" to understand relationships between words in a sentence regardless of their position. Almost every major AI model today is built on transformers.

Token
:   The basic unit LLMs process — roughly three-quarters of a word in English. Tokens are used to measure both context limits and how much text is processed during input and output.

Context Window
:   The maximum amount of text an LLM can process in a single conversation. A 128K context window means the model can consider roughly 100,000 words at once. Larger windows allow processing longer conversations or larger documents in one pass.

Inference
:   The process of running a trained AI model to generate a response or prediction. When you send a prompt to ChatGPT and get an answer back, that is inference. Inference affects system responsiveness, compute usage, and application throughput.

---

Training cutoff
:   The date a model's training data ends. It knows nothing after it, and it is
    unreliable about the date itself, because that fact was also learned during
    training.

Temperature
:   A sampling setting controlling randomness. Low values give consistent,
    repetitive output; high values give varied, less predictable output.
    Temperature 0 is the closest you get to determinism, and is not a guarantee.

Top-p (nucleus sampling)
:   Restricts the model to the smallest set of candidate tokens whose combined
    probability reaches *p*. An alternative lever to temperature.

Max output tokens
:   The cap on what the model may generate in one response. A separate, much
    smaller limit than the context window, and the usual cause of an answer
    that stops mid-sentence.

Reasoning model
:   A model trained to work through a problem before answering, producing an
    internal chain of reasoning that is usually hidden. Better at maths, logic
    and planning; slower, and billed for the thinking you do not see.

Mixture of experts (MoE)
:   An architecture that routes each token to a subset of specialised
    sub-networks, so only a fraction of the model's total parameters are active
    per token. Why total parameter count no longer indicates cost or capability.

Prompt caching
:   Provider-side reuse of an unchanged prompt prefix, charged at a reduced rate
    and returned faster. Requires the stable parts of the prompt to come first
    and to stay byte-identical.

Distillation
:   Training a smaller model on a larger model's outputs so it performs well on
    one narrow task at a fraction of the cost. It inherits the teacher's
    mistakes.

Multimodal
:   Able to accept or produce more than text — typically images, sometimes audio
    or video.

Time to first token (TTFT)
:   The delay before the first character of a response appears. What users
    perceive as speed, as distinct from total generation time.

KV cache
:   Retained attention state for tokens already processed, so they are not
    recomputed on each new token. The reason long conversations consume server
    memory as well as tokens.

Prefill and decode
:   The two phases of inference. Prefill processes your prompt and parallelises
    well; decode generates the answer one token at a time and does not. Shorter
    outputs help latency more than shorter prompts.


## :material-database-search-outline: Retrieval & data {#retrieval-data}

Retrieval-Augmented Generation (RAG)
:   A pattern where the AI retrieves relevant documents from your data before generating a response, grounding its answers in your actual information rather than just its training data. This is the most common way to make LLMs work with enterprise data without fine-tuning the model itself.

Vector Database
:   A specialized database that stores data as mathematical vectors (embeddings), enabling similarity-based search instead of exact keyword matching. Examples include Azure AI Search, Pinecone, Weaviate, and Qdrant.

Embedding
:   A numerical representation of text, images, or other data as a list of numbers (a vector) that captures its meaning. Similar concepts end up close together in this vector space. Embeddings are what make semantic search and RAG possible.

Knowledge Graph
:   A structured representation of entities and their relationships, like a network connecting concepts together. When combined with AI (GraphRAG), it helps models reason about complex relationships in your data rather than just matching keywords.

GraphRAG
:   An advanced RAG approach that combines traditional document retrieval with knowledge graph traversal. Instead of just finding relevant text chunks, it follows relationships between entities to build richer context for the LLM's response.

Chunking
:   The process of splitting large documents into smaller, overlapping pieces before storing them in a vector database. How you chunk documents (by paragraph, page, semantic meaning) significantly impacts RAG quality. Poor chunking is the most common reason RAG systems underperform.

Parent-Child Chunking
:   A chunking strategy that stores two sizes of the same content: small child chunks (used for precise retrieval) and large parent chunks (swapped in at generation time to give the LLM more context). This balances retrieval precision with generation quality.

Late Chunking
:   An embedding technique where the full document is encoded first, then chunked after — preserving contextual information that would otherwise be lost when chunking before embedding. The Jina AI approach using ColBERT-style embeddings. Particularly effective for long documents where cross-paragraph context matters.

HNSW (Hierarchical Navigable Small Worlds)
:   The most widely used indexing algorithm for vector databases. Builds a layered graph structure that enables fast approximate nearest neighbor (ANN) search. Used by Qdrant, Weaviate, pgvector, and most modern vector databases. Trades a small amount of recall accuracy for dramatically faster query speeds.

Reranking
:   A two-stage retrieval technique where an initial fast retrieval (e.g., ANN vector search) returns a large candidate set, and a slower but more accurate cross-encoder model re-scores and re-orders the results. Significantly improves retrieval precision at the cost of latency. Common rerankers include Cohere Rerank and cross-encoder models from sentence-transformers.

HyDE (Hypothetical Document Embeddings)
:   A query expansion technique where the LLM generates a hypothetical answer to the user's question, and that hypothetical answer is embedded and used for retrieval instead of the original question. Often improves retrieval quality because the hypothetical answer is closer in embedding space to relevant documents than a short question is.

RAGAS (Retrieval Augmented Generation Assessment)
:   An open-source evaluation framework for RAG systems. Provides four key metrics: Faithfulness (does the answer match the retrieved context?), Answer Relevancy (does the answer address the question?), Context Precision (are retrieved chunks relevant?), and Context Recall (was all necessary information retrieved?). See [RAG Evaluation](../rag/rag-evaluation.md).

---

Hybrid search
:   Running semantic and keyword search together and merging the results.
    Usually the single highest-value improvement to a mediocre RAG system,
    because keyword search covers exactly what embeddings handle worst: codes,
    identifiers, names and acronyms.

Approximate nearest neighbour (ANN)
:   The class of algorithms vector databases use to find similar vectors
    quickly, trading exactness for speed. HNSW is one.

Cosine similarity
:   The usual measure of closeness between two embeddings, based on the angle
    between them rather than their magnitude. The score behind "how relevant is
    this chunk".

Similarity threshold
:   A minimum score below which a retrieval result is treated as no match.
    Necessary because retrieval always returns something: without a floor, an
    unanswerable question still yields chunks and a confident answer.


## :material-robot-outline: Agentic AI {#agentic-ai}

AI Agent
:   An AI system that can autonomously plan, reason, and take actions to accomplish goals, not just answer questions. An agent might research a topic, call APIs, create files, and iterate on results with minimal human input.

Tools (in the context of AI Agents)
:   External capabilities that an agent can invoke to interact with the real world — things like APIs, databases, search engines, file systems, or any custom function. Tools are what give agents the ability to do things beyond generating text.

Autonomous Agent
:   An AI agent that operates end-to-end with minimal or no human intervention once given a goal. It plans its own steps, executes actions, handles errors, and decides when the task is complete.

Semi-Autonomous Agent
:   An agent that can handle most of a workflow independently but pauses at predefined checkpoints or confidence thresholds to get human approval before continuing. This is the most common pattern in enterprise deployments.

Workflow (in the context of AI)
:   A defined sequence of steps — some handled by AI, some by humans, some by traditional code — that together accomplish a business process. Workflows can be rigid (predefined steps) or flexible (agent decides dynamically).

Agentic Workflow
:   A workflow where one or more AI agents drive the process, making decisions about what to do next rather than following a hardcoded sequence. The agent interprets the goal, picks the right tools, handles branching logic, and adapts when things go wrong.

Multi-Agent System (MAS)
:   An architecture where multiple specialized AI agents collaborate to handle complex workflows. For example, one agent reads a document, another validates data, and a third drafts the response. Each agent focuses on what it does best.

Model Context Protocol (MCP)
:   An open standard (created by Anthropic) that lets AI models connect to external tools and data sources through a standardized interface. Think of it as USB-C for AI — instead of building custom integrations for every tool, MCP provides one universal connector. MCP defines three primitives: Tools (callable functions), Resources (read-only data), and Prompts (reusable templates). See [MCP](../ai-dev-tools/mcp.md).

Agent-to-Agent Protocol (A2A)
:   A protocol (from Google) that enables AI agents built on different frameworks to discover, communicate, and collaborate with each other. It solves the problem of agents being siloed within their own ecosystems.

AG-UI (Agent-User Interaction Protocol)
:   An open protocol that standardizes how AI agents stream events and state changes back to frontend user interfaces. It bridges the gap between backend agent orchestration and real-time UI updates.

Copilot Extension
:   **Retired.** A GitHub App that extended Copilot Chat with external tools via `@`-mentions. The platform was deprecated in September 2025 and shut down on 10 November 2025, replaced by [MCP](../ai-dev-tools/mcp.md) servers. Listed here because the term is still widely used in older material.

Copilot Skillset / Copilot Agent Extension
:   **Retired**, with the platform above. The two build styles for a Copilot
    Extension: a Skillset exposed OpenAPI-described functions, while an Agent
    extension handled whole conversation turns over webhooks. Both were replaced
    by [MCP](../ai-dev-tools/mcp.md) servers. Defined here only because older
    tutorials still teach them.

Orchestration
:   The coordination layer that manages how agents, tools, and models work together in a workflow. Frameworks like LangGraph, AutoGen, and Semantic Kernel handle routing decisions, retry logic, state management, and handoffs between agents.

Human-in-the-Loop (HiTL)
:   A design pattern where AI handles routine processing but routes edge cases or high-confidence-required decisions to a human for review.

Tool Use / Function Calling
:   The ability of an LLM to invoke external functions or APIs during a conversation. Instead of just generating text, the model can call a database query, run a calculation, or trigger a workflow. This is what turns a chatbot into a useful agent.

ReAct (Reasoning + Acting)
:   The foundational agent loop pattern where the model reasons about what to do next, takes an action (like calling a tool), observes the result, then repeats. Most production AI agents follow this cycle.

Agent Memory (Short-term / Long-term)
:   How agents retain information within a session (short-term) and across sessions (long-term). Short-term memory is the conversation context. Long-term memory persists preferences and past interactions across separate conversations.

Reflection
:   A pattern where an agent evaluates its own output before returning it, essentially self-reviewing for correctness, completeness, or quality. The agent generates a response, critiques it, and revises if needed.

Supervisor / Router Pattern
:   An architecture where a central "supervisor" agent receives requests and dispatches them to the right specialized sub-agent based on intent or task type.

Handoff
:   The mechanism for one agent to transfer control, context, and conversation state to another agent mid-workflow. A clean handoff ensures the receiving agent has all the information it needs.

Observability / Tracing
:   The practice of logging and visualizing every step an agent takes — which tools it called, what it reasoned, what it returned, and how long each step took. Essential for debugging and auditing.

Deterministic vs Non-deterministic Workflows
:   Whether an agent follows a fixed, predefined path (deterministic, like a DAG) or dynamically decides its next steps based on context (non-deterministic). Most production systems are a hybrid.

---

Agent loop
:   The core mechanism of an agent: call the model, which either requests an
    action or answers; perform the action; return the result; call again. It
    ends when the model stops requesting actions, and nothing else stops it.

Harness
:   Everything around the model in an agent: the loop, tool dispatch, error
    handling, permission checks and budgets. Most of what makes an agent work or
    fail lives here rather than in the model.

Context engineering
:   Deciding what occupies the context window on each turn, and what is dropped,
    summarised or moved outside it. Distinct from prompt engineering, which is
    about wording.

Context rot
:   Degradation in a model's use of information as the context grows, so
    advertised context length exceeds usable context length.

Memory poisoning
:   A wrong fact written to an agent's long-term memory and reinjected into
    later prompts as established context. Durable, invisible, and it presents as
    the model getting worse rather than the store being wrong.

Approval fatigue
:   The decay of human oversight under volume. Ask a person to approve enough
    actions and they stop reading them, which makes a confirmation step
    ceremonial.

Excessive agency
:   Granting an agent more capability or permission than its task requires, so a
    single failure or injection reaches further than it needed to.


## :material-pencil-outline: Prompting & techniques {#prompting-techniques}

Prompt Engineering
:   The practice of crafting effective instructions for AI models to get the desired output. In enterprise settings, this includes system prompts, few-shot examples, guardrails, and output formatting.

Chain of Thought (CoT)
:   A prompting technique where you ask the model to show its reasoning step by step before giving a final answer. This significantly improves accuracy on complex tasks.

Few-Shot Learning
:   Providing a few examples in your prompt to teach the model the pattern you want. Instead of lengthy instructions, you show 2-5 examples of input/output pairs.

Zero-Shot Learning
:   Asking the model to perform a task without providing any examples, relying solely on its pre-trained knowledge and your instructions.

System Prompt
:   The hidden instructions given to an LLM that define its behavior, personality, constraints, and capabilities for an entire conversation.

Grounding
:   Techniques that anchor AI responses to factual, verifiable information rather than the model's training data alone. RAG is one form of grounding.

---

Structured output
:   Constraining a model to produce output matching a supplied schema, enforced
    during generation so non-conforming text cannot be produced. Distinct from
    asking for JSON in the prompt, and from JSON mode, which guarantees valid
    JSON but not your fields.

JSON mode
:   A provider setting guaranteeing syntactically valid JSON. It does not
    guarantee your field names, types or presence — use a schema for that.

Lost in the middle
:   The tendency of models to use information at the start and end of a long
    input more reliably than information in the middle. Argues for putting
    instructions where they will be seen, and for retrieving less.


## :material-tune: Fine-tuning & training {#fine-tuning-training}

Fine-Tuning
:   Taking a pre-trained model and training it further on your specific data to improve performance on your tasks. Useful when prompting alone is not enough.

LoRA (Low-Rank Adaptation)
:   A technique that makes fine-tuning much cheaper and faster by only updating a small number of model parameters instead of all of them.

Transfer Learning
:   Using knowledge a model learned from one task to improve performance on a different but related task. Fine-tuning is a form of transfer learning.

Supervised Fine-Tuning (SFT)
:   Fine-tuning a model using labeled examples where each input has a known correct output.

RLHF (Reinforcement Learning from Human Feedback)
:   A training technique where human evaluators rank model outputs, and the model learns to prefer responses humans rate higher. This is how models like ChatGPT and Claude are aligned to be helpful and safe.

---

## :material-shield-check-outline: AI safety & governance {#ai-safety-governance}

Hallucination
:   When an AI model confidently generates information that is factually incorrect or entirely fabricated. RAG, grounding, and output validation are the primary defenses.

Prompt Injection
:   An attack where malicious input tricks an AI into ignoring its instructions or behaving unexpectedly.

Guardrails
:   Safety mechanisms built around AI systems to prevent harmful, off-topic, or policy-violating outputs. These include input/output filters, content safety APIs, and PII detection.

Responsible AI (RAI)
:   A framework of principles and practices ensuring AI systems are fair, transparent, accountable, and safe.

Explainable AI (XAI)
:   AI systems designed to make their decision-making process understandable to humans.

Red Teaming
:   The practice of deliberately trying to break or exploit an AI system to find vulnerabilities before bad actors do.

Content Safety
:   Automated filtering and moderation of AI inputs and outputs to block harmful or policy-violating content.

---

Lethal trifecta
:   The three conditions that together make prompt injection dangerous: access
    to private data, exposure to untrusted content, and a way to communicate
    externally. Removing any one eliminates the attack class, which makes it a
    design constraint rather than a filtering problem.

Indirect prompt injection
:   Injection delivered through content the system processes rather than through
    the user's message — a retrieved document, a web page, an email, a pull
    request. Harder to detect because the attacker never talks to your system.

Jailbreak
:   Input designed to make a model bypass its own safety training. Related to,
    but distinct from, prompt injection, which targets the application's
    instructions rather than the model's guardrails.

Data residency
:   The requirement that data be processed and stored in a particular
    jurisdiction. A common reason to use a regional deployment of a model rather
    than a vendor's default endpoint.


## :material-server-outline: Infrastructure & operations {#infrastructure-operations}

MLOps
:   The practice of deploying, monitoring, and maintaining ML models in production. Includes model versioning, A/B testing, drift detection, and retraining pipelines.

Model Drift
:   When a deployed model's performance degrades over time because the real-world data has shifted from what it was trained on.

Quantization
:   Reducing the precision of a model's numerical weights (e.g., from 32-bit to 4-bit) to make it smaller and faster with minimal quality loss.

Edge AI
:   Running AI models directly on local devices or on-premises servers rather than in the cloud.

---

Evaluation set
:   A fixed collection of inputs with known-good outcomes, used to tell whether
    a change helped. Usually built from real failures. The single most valuable
    artefact a team building on models can own.

pass@k and pass^k
:   pass@k is the chance of at least one success in k attempts, which flatters.
    pass^k is the chance of succeeding k times in a row, which is what a user
    experiences across repeated use. The second is the number that matters.

LLM-as-judge
:   Using a model to grade another model's output against criteria. Cheap and
    scalable, and it needs calibrating against human judgements before its
    scores mean anything.

Idempotency
:   The property that repeating an operation has the same effect as performing
    it once. Essential when retrying, because a timeout does not tell you
    whether the work already happened.

Rate limit
:   A provider cap on requests or tokens per interval. The token limit usually
    binds first, and exceeding it is a common launch-day failure.


## :material-domain: Enterprise AI patterns {#enterprise-ai-patterns}

Copilot Pattern
:   An AI assistant embedded within an existing application that helps users with their current workflow. Microsoft 365 Copilot is the canonical example. The AI augments human work rather than replacing it.

Autonomous Agent Pattern
:   An AI system that operates independently, making decisions and taking actions with minimal human oversight. Best suited for well-defined, low-risk processes.

Intelligent Document Processing (IDP)
:   Using AI to automatically extract, classify, and process information from unstructured documents. Combines OCR, NLP, and classification models.

Conversational AI
:   AI systems that interact with users through natural language dialogue, including chatbots, voice assistants, and virtual agents.

Agentic RAG
:   An evolution of basic RAG where an AI agent decides what to retrieve, when to retrieve it, and how to combine information from multiple sources.

---

## :material-tools: Frameworks & tools {#frameworks-tools}

Semantic Kernel
:   **Superseded.** Microsoft's SDK for integrating LLMs into applications,
    providing prompt management, memory, planning and tool integration. Merged
    into [Microsoft Agent Framework](../tools-and-frameworks/index.md) at its
    1.0 release in April 2026. Existing code keeps working and security fixes
    continue, but new work should start on Agent Framework.

LangChain / LangGraph
:   Popular open-source frameworks for building LLM-powered applications. LangChain provides building blocks, while LangGraph adds stateful graph-based orchestration.

Microsoft Agent Framework (MAF)
:   Microsoft's framework for building production-grade AI agents that integrate with Azure services.

Prompt Shields
:   Microsoft's security layer that detects and blocks prompt injection attacks and jailbreak attempts in real time.
