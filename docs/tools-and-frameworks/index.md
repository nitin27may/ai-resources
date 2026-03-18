---
tags:
  - Intermediate
  - Tools
---

# Tools & Frameworks

The AI ecosystem moves fast. This page provides a curated overview of the tools and frameworks most relevant to building enterprise AI solutions -- organized into orchestration frameworks, AI platforms, and developer tools.

Each entry includes a brief description, who it is for, and a link to official documentation.

---

<div class="grid cards" markdown>

-   :material-robot-outline:{ .lg .middle } __Orchestration Frameworks__

    SDKs and libraries for building AI agents, chains, and multi-agent systems.

    [:octicons-arrow-right-24: Jump to section](#orchestration-frameworks)

-   :material-cloud-outline:{ .lg .middle } __AI Platforms__

    Cloud services for hosting models, managing data, and building end-to-end AI solutions.

    [:octicons-arrow-right-24: Jump to section](#ai-platforms)

-   :material-wrench-outline:{ .lg .middle } __Developer Tools__

    Tools that help developers build, test, and deploy AI-powered applications.

    [:octicons-arrow-right-24: Jump to section](#developer-tools)

</div>

---

## Orchestration Frameworks

Orchestration frameworks provide the building blocks for connecting large language models to tools, data, and each other. They handle prompt management, memory, tool calling, and multi-step workflows so you can focus on the application logic.

### Semantic Kernel

:material-microsoft:{ .middle } **Microsoft** | .NET, Python

Semantic Kernel is Microsoft's open-source SDK for integrating LLMs into applications. It provides a lightweight, extensible architecture with support for prompt management, plugins (tool calling), memory, and planning. Semantic Kernel is the foundation for Microsoft Copilot and is well-suited for teams building on the .NET or Python stack.

**Who it is for:** Developers building LLM-powered features in .NET or Python applications, especially those already in the Microsoft ecosystem.

**Key capabilities:**

- Prompt templating and management
- Plugin architecture for tool calling
- Built-in memory and vector store connectors
- Agent framework for single and multi-agent scenarios
- Process framework for long-running business workflows

[:octicons-link-external-16: Semantic Kernel Documentation](https://learn.microsoft.com/en-us/semantic-kernel/)

---

### LangChain / LangGraph

:material-language-python:{ .middle } **LangChain AI** | Python, JavaScript/TypeScript

**LangChain** is a popular open-source framework for building applications with LLMs. It provides composable building blocks -- chains, tools, retrievers, memory -- that snap together to create complex LLM workflows.

**LangGraph** extends LangChain with a stateful, graph-based orchestration layer. Where LangChain chains are linear, LangGraph models workflows as directed graphs with cycles, conditional branching, and persistent state -- making it ideal for building agents and multi-step reasoning systems.

**Who it is for:** Python and JavaScript developers building LLM applications, especially those who need flexibility and a large ecosystem of integrations.

**Key capabilities:**

- Composable chains, tools, and retrievers (LangChain)
- Stateful graph-based orchestration with cycles and branching (LangGraph)
- Extensive integrations with vector stores, APIs, and data sources
- Built-in support for RAG, agents, and conversational memory
- LangSmith for observability, tracing, and evaluation

[:octicons-link-external-16: LangChain Documentation](https://python.langchain.com/docs/) | [:octicons-link-external-16: LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

---

### AutoGen

:material-microsoft:{ .middle } **Microsoft** | Python

AutoGen is Microsoft's open-source framework for building multi-agent conversational systems. Agents in AutoGen communicate through structured conversations, enabling flexible collaboration patterns -- from simple two-agent dialogs to complex group chats with specialized roles.

**Who it is for:** Researchers and developers exploring multi-agent architectures, especially those who want agents that collaborate through conversation rather than rigid orchestration.

**Key capabilities:**

- Multi-agent conversation framework
- Flexible agent roles and collaboration patterns
- Human-in-the-loop support
- Code execution and tool use within conversations
- Extensible agent and conversation designs

[:octicons-link-external-16: AutoGen Documentation](https://microsoft.github.io/autogen/)

---

### CrewAI

:material-account-group-outline:{ .middle } **CrewAI** | Python

CrewAI is a role-based multi-agent framework that models teams of AI agents working together toward a goal. Each agent has a defined role, backstory, and set of tools. A "crew" orchestrates the agents, assigning tasks and managing collaboration.

**Who it is for:** Developers who want to build multi-agent systems using an intuitive role-and-task mental model, with minimal boilerplate.

**Key capabilities:**

- Role-based agent definitions with goals and backstories
- Task assignment and delegation between agents
- Sequential and hierarchical crew execution
- Integration with LangChain tools and LLM providers
- Simple, readable agent definitions

[:octicons-link-external-16: CrewAI Documentation](https://docs.crewai.com/)

---

## AI Platforms

AI platforms provide the cloud infrastructure for hosting models, managing data, and building production-grade AI solutions. These are the services your AI applications run on.

### Azure AI Foundry

:material-microsoft-azure:{ .middle } **Microsoft** | Cloud Platform

Formerly known as Azure AI Studio, Azure AI Foundry is Microsoft's unified platform for building, evaluating, and deploying AI solutions on Azure. It brings together model catalog access, prompt engineering tools, evaluation frameworks, and deployment pipelines in a single interface.

**Who it is for:** Teams building AI solutions on Azure who need a centralized platform for the full AI development lifecycle.

**Key capabilities:**

- Access to OpenAI, Meta, Mistral, and other models via the model catalog
- Prompt playground for experimentation
- Built-in evaluation and red-teaming tools
- Deployment to managed endpoints
- Integration with Azure AI Search, Content Safety, and other Azure services

[:octicons-link-external-16: Azure AI Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-studio/)

---

### Azure OpenAI Service

:material-microsoft-azure:{ .middle } **Microsoft** | Cloud Service

Azure OpenAI Service provides access to OpenAI's models (GPT-4o, GPT-4, o1, o3, DALL-E, Whisper) hosted on Azure infrastructure. It adds enterprise features -- virtual network support, managed identity, content filtering, and regional data residency -- that are critical for production deployments.

**Who it is for:** Organizations that want to use OpenAI models with enterprise-grade security, compliance, and support.

**Key capabilities:**

- GPT-4o, GPT-4, o-series reasoning models, embeddings, image generation, speech
- Enterprise security (VNet, private endpoints, managed identity)
- Built-in content filtering and abuse monitoring
- Regional deployment options for data residency
- Managed and provisioned deployment options

[:octicons-link-external-16: Azure OpenAI Service Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)

---

### Azure AI Search

:material-magnify:{ .middle } **Microsoft** | Cloud Service

Azure AI Search (formerly Azure Cognitive Search) is a fully managed search service that supports both traditional keyword search and modern vector search. It is the most common retrieval layer for RAG solutions built on Azure, enabling AI applications to find and surface relevant information from large document collections.

**Who it is for:** Teams building RAG solutions, enterprise search, or any application that needs to retrieve relevant information from large datasets.

**Key capabilities:**

- Hybrid search combining vector similarity and keyword matching
- Integrated vectorization with Azure OpenAI embeddings
- Semantic ranking for improved relevance
- Built-in skillsets for document cracking, OCR, and enrichment
- Index management and query APIs

[:octicons-link-external-16: Azure AI Search Documentation](https://learn.microsoft.com/en-us/azure/search/)

---

## Developer Tools

Developer tools help you build, test, and ship AI-powered applications more effectively. These tools integrate into your existing development workflow.

### GitHub Copilot

:octicons-copilot-16:{ .middle } **GitHub** | IDE Extension

GitHub Copilot is an AI pair programmer that provides code suggestions, completions, and chat-based assistance directly in your IDE. It supports VS Code, Visual Studio, JetBrains IDEs, and more. Copilot helps developers write code faster, understand unfamiliar codebases, and automate repetitive tasks.

**Who it is for:** Any developer who wants AI-assisted coding in their editor.

**Key capabilities:**

- Inline code completions and suggestions
- Chat interface for questions, explanations, and refactoring
- Multi-file context awareness
- Support for virtually all programming languages
- Workspace and terminal integration

[:octicons-link-external-16: GitHub Copilot Documentation](https://docs.github.com/en/copilot)

---

### Azure AI Document Intelligence

:material-file-document-outline:{ .middle } **Microsoft** | Cloud Service

Azure AI Document Intelligence (formerly Form Recognizer) extracts text, key-value pairs, tables, and structure from documents using pre-built and custom models. It powers intelligent document processing (IDP) pipelines, turning unstructured documents into structured data.

**Who it is for:** Teams building document processing pipelines -- invoices, receipts, contracts, forms, and any document that needs automated data extraction.

**Key capabilities:**

- Pre-built models for invoices, receipts, IDs, and more
- Custom models for domain-specific documents
- Layout analysis for tables, figures, and structure
- Batch processing for high-volume scenarios
- REST API and SDKs for .NET, Python, Java, and JavaScript

[:octicons-link-external-16: Azure AI Document Intelligence Documentation](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/)

---

### Prompt Flow

:material-transit-connection-variant:{ .middle } **Microsoft** | Development Tool

Prompt Flow is a visual development tool for building, evaluating, and deploying LLM-based workflows. It provides a graph-based interface where you connect prompts, tools, and logic into executable flows -- then evaluate them systematically before deploying to production.

**Who it is for:** AI developers who want a structured, visual approach to building and testing LLM applications, with built-in evaluation and CI/CD integration.

**Key capabilities:**

- Visual flow editor for LLM workflows
- Built-in evaluation framework with metrics
- Local development and cloud deployment
- Integration with Azure AI Foundry
- CI/CD pipeline support for automated testing and deployment

[:octicons-link-external-16: Prompt Flow Documentation](https://microsoft.github.io/promptflow/)

---

## Comparison at a Glance

| Tool | Category | Primary Use | Language / Platform |
|------|----------|-------------|---------------------|
| Semantic Kernel | Orchestration | LLM integration, plugins, agents | .NET, Python |
| LangChain | Orchestration | LLM application building blocks | Python, JS |
| LangGraph | Orchestration | Stateful agent orchestration | Python, JS |
| AutoGen | Orchestration | Multi-agent conversations | Python |
| CrewAI | Orchestration | Role-based multi-agent systems | Python |
| Azure AI Foundry | Platform | Full AI development lifecycle | Azure |
| Azure OpenAI Service | Platform | Enterprise OpenAI model hosting | Azure |
| Azure AI Search | Platform | Vector + keyword search for RAG | Azure |
| GitHub Copilot | Developer Tool | AI-assisted coding | IDE Extension |
| Document Intelligence | Developer Tool | Document data extraction | Azure |
| Prompt Flow | Developer Tool | Visual LLM workflow builder | Azure, Local |

---

## References

- [Semantic Kernel Docs](https://learn.microsoft.com/en-us/semantic-kernel/)
- [LangChain Docs](https://python.langchain.com/docs/)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [AutoGen Docs](https://microsoft.github.io/autogen/)
- [Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-studio/)
- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Azure AI Search](https://learn.microsoft.com/en-us/azure/search/)
- [GitHub Copilot](https://docs.github.com/en/copilot)
- [CrewAI Docs](https://docs.crewai.com/)
