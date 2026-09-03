# 04 — Page matrix

One row per page. This is the source of truth for Phase 2 (tags, nav labels) and Phase 4 (header block links). Paths are relative to docs/. '—' means the field is omitted from the header block. Before/After follow the reading path, the build path, or nav order within a Go deeper group.

Level tags (exactly one): Start here, Understand, Build, Go deeper, Tools, Reference.
Topic tags (one to three): Agents, Retrieval, Safety, Evaluation, Prompting, Models, Training, Patterns, Operations, MCP, Claude Code, Copilot, Azure, Reference, Home.

| File | Nav label | Level tag | Topic tags | Time | Code | Before | After | Hands-on version | In depth | Action |
|---|---|---|---|---|---|---|---|---|---|---|
| index.md | Home | Reference | Home | 5 min | no | — | 00-start-here/index.md | — | — | rewrite (Ph3) |
| 00-start-here/index.md | Choose your path | Start here | Home | 10 min | no | index.md | getting-started/index.md | 00-start-here/the-path.md | — | NEW (Ph2) |
| getting-started/index.md | AI 101 | Understand | Models | 30 min | no | 00-start-here/index.md | concepts/foundation-and-models.md | 00-start-here/the-path.md | glossary/index.md | rewrite (Ph3) |
| 00-start-here/the-path.md | The build path | Start here | Agents | 10 min | no | 00-start-here/index.md | 00-start-here/setup.md | — | — | frame |
| 00-start-here/setup.md | Setup | Build | Agents, Operations | 30 min | yes | 00-start-here/the-path.md | 02-agents/tool-calling.md | — | — | frame; Azure tab (Ph7) |
| concepts/index.md | Understand (index) | Understand | Models | 5 min | no | 00-start-here/index.md | concepts/foundation-and-models.md | — | — | frame (Ph2) |
| concepts/foundation-and-models.md | How models work | Understand | Models | 30 min | no | getting-started/index.md | concepts/prompting-and-techniques.md | 02-agents/context-engineering.md | tools-and-frameworks/index.md | frame; model table to tiers |
| concepts/prompting-and-techniques.md | Prompting | Understand | Prompting | 30 min | optional | concepts/foundation-and-models.md | concepts/retrieval-and-data.md | 02-agents/tool-calling.md | — | frame |
| concepts/retrieval-and-data.md | Retrieval and data | Understand | Retrieval | 30 min | no | concepts/prompting-and-techniques.md | concepts/ai-agents.md | 02-agents/retrieval.md | rag/index.md | frame; layer box |
| concepts/ai-agents.md | What an agent is | Understand | Agents | 40 min | no | concepts/retrieval-and-data.md | concepts/agentic-ai.md | 02-agents/the-agent-loop.md | patterns/design-patterns.md | rewrite-light; retitle; trim build-level sections |
| concepts/agentic-ai.md | Agentic AI | Understand | Agents, MCP | 40 min | no | concepts/ai-agents.md | patterns/enterprise-patterns.md | 02-agents/the-harness.md | ai-dev-tools/mcp.md | frame; layer boxes on tool-use, memory, observability, MCP sections |
| patterns/enterprise-patterns.md | Enterprise AI patterns | Understand | Patterns, Retrieval | 30 min | no | concepts/agentic-ai.md | concepts/safety-and-responsible-ai.md | 02-agents/retrieval.md (agentic RAG) | rag/rag-fundamentals.md#agentic-rag | frame; moves tab |
| concepts/safety-and-responsible-ai.md | Safety and responsible AI | Understand | Safety | 30 min | no | patterns/enterprise-patterns.md | concepts/fine-tuning-and-training.md | 02-agents/safety.md | reference/resources.md (OWASP) | frame; layer box |
| concepts/fine-tuning-and-training.md | Fine-tuning and training | Understand | Training, Models | 15 min skim | no | concepts/safety-and-responsible-ai.md | concepts/infrastructure-and-operations.md | — | rag/index.md (RAG vs fine-tune) | frame |
| concepts/infrastructure-and-operations.md | Infrastructure and operations | Understand | Operations | 15 min skim | no | concepts/fine-tuning-and-training.md | 00-start-here/the-path.md | 02-agents/production.md | patterns/code-quality-pipeline.md | frame |
| 02-agents/tool-calling.md | 1 Tool calling | Build | Agents | 45 min | yes | 00-start-here/setup.md | 02-agents/the-agent-loop.md | — | — | frame; entry hand-off to How models work + What an agent is; overview link concepts/ai-agents.md |
| 02-agents/the-agent-loop.md | 2 The agent loop | Build | Agents | 1 h | yes | 02-agents/tool-calling.md | 02-agents/the-harness.md | — | patterns/design-patterns.md | frame; overview link concepts/ai-agents.md |
| 02-agents/the-harness.md | 3 The harness | Build | Agents, Safety | 1 h | yes | 02-agents/the-agent-loop.md | 02-agents/context-engineering.md | — | patterns/design-principles.md | frame; overview link concepts/agentic-ai.md |
| 02-agents/context-engineering.md | 4 Context engineering | Build | Agents, Models | 1.5 h | yes | 02-agents/the-harness.md | 02-agents/retrieval.md | — | — | frame; overview link concepts/foundation-and-models.md |
| 02-agents/retrieval.md | 5 Retrieval | Build | Retrieval | 1.5 h | yes | 02-agents/context-engineering.md | 02-agents/evaluation.md | — | rag/index.md | frame; overview link concepts/retrieval-and-data.md |
| 02-agents/evaluation.md | 6 Evaluation | Build | Evaluation | 2 h | yes | 02-agents/retrieval.md | 02-agents/observability.md | — | rag/rag-evaluation.md | frame |
| 02-agents/observability.md | 7 Observability | Build | Evaluation, Operations | 1 h | yes | 02-agents/evaluation.md | 02-agents/safety.md | — | — | frame; overview link concepts/agentic-ai.md#observability |
| 02-agents/safety.md | 8 Safety | Build | Safety | 1.5 h | yes | 02-agents/observability.md | 02-agents/production.md | — | — | frame; overview link concepts/safety-and-responsible-ai.md |
| 02-agents/production.md | 9 Production | Build | Operations | 1 h | yes | 02-agents/safety.md | rag/index.md | — | patterns/index.md | frame; exit section 'Where to go from here' |
| rag/index.md | Retrieval in depth (index) | Go deeper | Retrieval | 10 min | no | 02-agents/retrieval.md | rag/rag-fundamentals.md | 02-agents/retrieval.md | — | frame |
| rag/rag-fundamentals.md | RAG fundamentals | Go deeper | Retrieval | 40 min | optional | rag/index.md | rag/embeddings.md | 02-agents/retrieval.md | — | frame; anchor #agentic-rag must exist |
| rag/embeddings.md | Embeddings | Go deeper | Retrieval, Models | 30 min | optional | rag/rag-fundamentals.md | rag/chunking-strategies.md | 02-agents/retrieval.md | — | frame |
| rag/chunking-strategies.md | Chunking strategies | Go deeper | Retrieval | 45 min | yes | rag/embeddings.md | rag/vector-databases.md | 02-agents/retrieval.md | — | frame |
| rag/vector-databases.md | Vector databases | Go deeper | Retrieval, Azure | 40 min | optional | rag/chunking-strategies.md | rag/graphrag.md | 02-agents/retrieval.md | — | frame |
| rag/graphrag.md | GraphRAG | Go deeper | Retrieval | 40 min | no | rag/vector-databases.md | rag/rag-evaluation.md | — | — | frame |
| rag/rag-evaluation.md | RAG evaluation | Go deeper | Retrieval, Evaluation | 40 min | optional | rag/graphrag.md | 02-agents/evaluation.md | 02-agents/evaluation.md | — | frame |
| patterns/index.md | Architecture patterns (index) | Go deeper | Patterns | 5 min | no | 02-agents/production.md | patterns/design-patterns.md | — | — | frame |
| patterns/design-patterns.md | Design patterns | Go deeper | Patterns, Agents | 45 min | optional | patterns/index.md | patterns/design-principles.md | 02-agents/the-agent-loop.md | — | frame; C# tabs (Ph7) |
| patterns/design-principles.md | Design principles | Go deeper | Patterns | 20 min | no | patterns/design-patterns.md | patterns/code-quality-pipeline.md | 02-agents/the-harness.md | — | keep |
| patterns/code-quality-pipeline.md | Code quality pipeline | Go deeper | Operations, Copilot | 40 min | yes | patterns/design-principles.md | tools-and-frameworks/index.md | — | — | keep |
| tools-and-frameworks/index.md | Frameworks and platforms | Go deeper | Patterns, Azure | 30 min | no | patterns/code-quality-pipeline.md | ai-dev-tools/index.md | — | — | frame; add OpenAI Agents SDK, Google ADK (Ph6) |
| ai-dev-tools/index.md | Developer tools (index) | Tools | Claude Code, Copilot, MCP | 10 min | no | tools-and-frameworks/index.md | ai-dev-tools/github-copilot.md | — | — | frame |
| ai-dev-tools/github-copilot.md | GitHub Copilot | Tools | Copilot | 30 min | no | ai-dev-tools/index.md | ai-dev-tools/claude-code.md | — | — | frame |
| ai-dev-tools/claude-code.md | Claude Code | Tools | Claude Code | 40 min | yes | ai-dev-tools/github-copilot.md | ai-dev-tools/claude-code-skills.md | — | — | frame; sentence-case headings |
| ai-dev-tools/claude-code-skills.md | Claude Code skills and agents | Tools | Claude Code | 40 min | yes | ai-dev-tools/claude-code.md | ai-dev-tools/mcp.md | — | — | frame |
| ai-dev-tools/mcp.md | Model Context Protocol | Tools | MCP | 45 min | yes | ai-dev-tools/claude-code-skills.md | reference/resources.md | — | concepts/agentic-ai.md#mcp (overview) | frame |
| glossary/index.md | Glossary | Reference | Reference | — | no | — | — | — | — | frame; add terms (Ph1/Ph9) |
| reference/resources.md | Resources | Reference | Reference | 20 min | no | — | references/index.md | — | — | keep; re-verify (Ph6) |
| references/index.md | Official sources | Reference | Reference | — | no | reference/resources.md | — | — | — | rewrite (Ph6) |
| tags.md | Browse by tag | Reference | Reference | — | no | — | — | — | — | NEW (Ph2) |
| whats-new/index.md | What's new | Reference | Reference | 5 min | no | — | — | — | — | rewrite (Ph3) |

Rows: 46 (44 existing + 2 new).

## Header block template (Phase 4)

```markdown
!!! abstract "<Level> · <Time> · <no code | code optional | code required>"
    **Before this:** [<label>](<before>)  ·  **After this:** [<label>](<after>)
    **Hands-on version:** [<label>](<hands-on>)  ·  **In depth:** [<label>](<in-depth>)
```

Rules: exactly one per page, directly under the H1, before any other admonition. Omit a line when its field is '—'. Build pages keep their existing 'What you'll be able to do' block after it and label the overview link **Overview version:**. The title string is what the Phase 4 done-check greps for: `^!!! abstract "(Start here|Understand|Build|Go deeper|Tools|Reference) ·`.
