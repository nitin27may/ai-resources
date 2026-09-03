# ai-resources restructure plan — 2026-09-02

Companion to ai-resources-audit-2026-09-02.md. This is the content, navigation and style design. No URLs change in this plan.

## Decisions recorded (from Nitin, 2026-09-02)

- Audience includes non-developers. They are a first-class track, not a footnote.
- Not a certification guide. Official vendor sources are "must-read", not exam prep.
- Concepts are vendor-agnostic. Code samples primarily OpenAI and Azure OpenAI, written so the provider is a config change.
- Site name "AI Knowledge Hub" and the /ai-resources/ URL stay.
- Search Console verification deferred until re-auth.
- Every existing URL is preserved. Restructure happens through nav, rewrites and new pages only.

## 1. The ramp: four layers plus reference

The site currently has two disconnected halves (encyclopedic March pages, hands-on August path). The fix is to make the overlap deliberate: the same topic appears at up to three depths, each page says which depth it is, and each links up and down.

| Layer | Name in nav | Who | Code | Existing folder |
|---|---|---|---|---|
| 1 | **Understand** | Everyone. No prerequisites. | None required; any code is illustrative and skippable | concepts/, getting-started/, patterns/enterprise-patterns |
| 2 | **Build** | Developers. Can read Python and use a terminal. | Every page ends in a lab that runs | 00-start-here/, 02-agents/, labs/ |
| 3 | **Go deeper** | Developers and architects after Build (or straight in, if experienced) | Design-level, with samples | rag/, patterns/, tools-and-frameworks/ |
| 4 | **Tools** | Anyone using AI coding tools | Config and commands | ai-dev-tools/ |
| R | **Reference** | Everyone | None | glossary/, reference/, references/, whats-new/ |

Rule for authors: a page belongs to exactly one layer, declares it in the header, and links to its counterparts in the other layers. Duplication across layers is allowed; duplication within a layer is not.

## 2. Two paths through the site

### The reading path (no code, roughly 4 to 5 hours)
For analysts, product managers, leaders, students, and developers who want the map before the territory.

| # | Page | Existing file | Time |
|---|---|---|---|
| 1 | AI 101 | getting-started/index.md | 30 min |
| 2 | How models work | concepts/foundation-and-models.md | 30 min |
| 3 | Prompting | concepts/prompting-and-techniques.md | 30 min |
| 4 | Retrieval and data (RAG, embeddings, vector search, GraphRAG in outline) | concepts/retrieval-and-data.md | 30 min |
| 5 | What an agent is | concepts/ai-agents.md | 40 min |
| 6 | Agentic AI: protocols, memory, orchestration | concepts/agentic-ai.md | 40 min |
| 7 | Enterprise AI patterns (copilot, autonomous agent, IDP, conversational, agentic RAG) | patterns/enterprise-patterns.md | 30 min |
| 8 | Safety and responsible AI | concepts/safety-and-responsible-ai.md | 30 min |
| 9 | Fine-tuning vs RAG (skim) | concepts/fine-tuning-and-training.md | 15 min |
| 10 | Infrastructure and operations (skim) | concepts/infrastructure-and-operations.md | 15 min |

Why this order: each step needs only the ones before it. Prompting needs models. Retrieval is "give the model your data" and needs prompting. An agent is "let the model act" and needs tool calls, which build on prompting and retrieval. Agentic AI and enterprise patterns are agents at scale. Safety comes after agents because prompt injection through tool output is the failure that matters. Fine-tuning is last because the honest answer for most readers is "you probably want RAG", which they now understand.

Exit points: Glossary (always), Resources (what to read next), and for anyone who now wants to build, the Build path.

### The build path (code, 12 to 15 hours)
Unchanged: Setup, then modules 1 to 9 in 02-agents/. Two additions:
- **Entry hand-off:** module 1 (Tool calling) opens with "If you have not read *What an agent is* and *How models work*, do that first, 70 minutes". Setup already assumes nothing about ML but does assume a terminal.
- **Exit hand-off:** module 9 (Production) ends with "Where to go from here": Retrieval in depth, Architecture patterns (multi-agent), Frameworks and platforms, Tools. Today the path ends at Production with no onward route except the-path's "Going further" section, which nobody sees at the end.

Fix the count: it is ten modules (0 to 9), ten labs. "Eleven" appears in the-path.md front matter, abstract, and the Home meta description.

## 2b. Topic ladders: the stepping stones across layers

For each major topic, the exact order a reader climbs, from the first mention to the deepest page. This is what "proper order" means on this site, and it is what the header blocks encode. A reader can stop at any rung and still have a complete picture at that depth.

### Retrieval (RAG, agentic RAG, GraphRAG)
| Rung | Page | What the reader gets |
|---|---|---|
| 1 | AI 101, "RAG" in key terms | One sentence: give the model your documents before it answers |
| 2 | Understand: Retrieval and data | How RAG works end to end; what embeddings, vector search and chunking are; why GraphRAG exists; RAG vs fine-tuning decision |
| 3 | Understand: Enterprise AI patterns, "Agentic RAG" | What it looks like when an agent decides when and what to retrieve |
| 4 | Build: module 5 Retrieval | A local RAG that runs, and the case it silently gets wrong; hybrid search; retrieval as a tool |
| 5 | Go deeper: RAG fundamentals | Naive RAG, then Advanced, Modular, Agentic RAG as an evolution, with failure modes at each stage |
| 6 | Go deeper: Embeddings | Model choice, dimensions, input types, Matryoshka |
| 7 | Go deeper: Chunking strategies | Eight strategies including parent-child, late and agentic chunking |
| 8 | Go deeper: Vector databases | HNSW and IVF, hybrid search, Azure AI Search deep dive, pgvector |
| 9 | Go deeper: GraphRAG | Knowledge graph construction, local vs global search, when it beats vector RAG and at what cost |
| 10 | Go deeper: RAG evaluation | Faithfulness, relevancy, precision, recall; golden datasets |
| 11 | Build: module 6 Evaluation | pass^k and judge calibration, applied to the agent that wraps the retriever |

Gap on this ladder: nothing hands-on for agentic RAG or GraphRAG. Section 7 adds a lab for agentic RAG (the agent chooses between two retrievers and a no-retrieve option) as part of the multi-agent module, and GraphRAG stays read-only until a local, cheap indexing path is viable.

### Agents
| Rung | Page |
|---|---|
| 1 | AI 101, "AI agent" in key terms |
| 2 | Understand: What an agent is (components, when to use one, when not to, multi-agent in outline) |
| 3 | Understand: Agentic AI (tool use, ReAct, reflection, supervisor, handoff, memory, human-in-the-loop, MCP, A2A, AG-UI) |
| 4 | Understand: Enterprise AI patterns (copilot vs autonomous agent) |
| 5 | Build: 1 Tool calling, 2 The agent loop, 3 The harness |
| 6 | Build: 4 Context engineering, (new) Memory |
| 7 | Build: 7 Observability, 8 Safety, 9 Production |
| 8 | Build: (new) 10 Multi-agent |
| 9 | Go deeper: Design patterns (sequential, conditional, supervisor, hierarchical, parallel, plan-based, handoff, conversation-driven) |
| 10 | Go deeper: Design principles; Frameworks and platforms |
| 11 | Go deeper: MCP (build a server); Resources shelf (the Cognition vs Anthropic multi-agent pair) |

### Models and prompting
AI 101 → How models work → Prompting → Build: 1 Tool calling and (new) Structured output → Build: 4 Context engineering → Understand: Fine-tuning and training → Go deeper: Frameworks and platforms (model catalogues).

### Safety
AI 101 ("hallucination") → Understand: Safety and responsible AI (hallucination, injection, guardrails, RAI principles, red teaming, content safety) → Build: 3 The harness (limits in code vs errors as context) → Build: 8 Safety (injection measured, lethal trifecta, what actually holds) → Resources: OWASP agentic top 10, The Attacker Moves Second.

### Evaluation and observability
Understand: Agentic AI "Observability and tracing" → Go deeper: RAG evaluation → Build: 6 Evaluation → Build: 7 Observability → Resources: Evals FAQ, Adding Error Bars to Evals.

### Production and operations
Understand: Infrastructure and operations (MLOps, drift, quantization, edge, cost) → Build: 9 Production (retries, idempotency, budgets) → Go deeper: Code quality pipeline; Frameworks and platforms.

### Protocols and tools
Understand: Agentic AI "Key protocols" → Tools: MCP → Tools: Claude Code, Skills, Copilot → Go deeper: Frameworks and platforms → Resources: A2A scepticism note.

Every rung is an existing page except the three marked (new): Structured output, Memory, Multi-agent.

## 3. Target navigation (URL-preserving)

Six tabs. Every file stays at its current path. Labels are sentence case to match the Build pages, which are the house voice going forward.

```yaml
nav:
  - Home: index.md
  - Start here:
      - Choose your path: 00-start-here/index.md          # NEW
      - AI 101: getting-started/index.md
      - The build path: 00-start-here/the-path.md
      - Setup: 00-start-here/setup.md
  - Understand:
      - concepts/index.md
      - How models work: concepts/foundation-and-models.md
      - Prompting: concepts/prompting-and-techniques.md
      - Retrieval and data: concepts/retrieval-and-data.md
      - What an agent is: concepts/ai-agents.md
      - Agentic AI: concepts/agentic-ai.md
      - Enterprise AI patterns: patterns/enterprise-patterns.md
      - Safety and responsible AI: concepts/safety-and-responsible-ai.md
      - Fine-tuning and training: concepts/fine-tuning-and-training.md
      - Infrastructure and operations: concepts/infrastructure-and-operations.md
  - Build:
      - 1 Tool calling: 02-agents/tool-calling.md
      - 2 The agent loop: 02-agents/the-agent-loop.md
      - 3 The harness: 02-agents/the-harness.md
      - 4 Context engineering: 02-agents/context-engineering.md
      - 5 Retrieval: 02-agents/retrieval.md
      - 6 Evaluation: 02-agents/evaluation.md
      - 7 Observability: 02-agents/observability.md
      - 8 Safety: 02-agents/safety.md
      - 9 Production: 02-agents/production.md
  - Go deeper:
      - Retrieval in depth:
          - rag/index.md
          - RAG fundamentals: rag/rag-fundamentals.md
          - Embeddings: rag/embeddings.md
          - Chunking strategies: rag/chunking-strategies.md
          - Vector databases: rag/vector-databases.md
          - GraphRAG: rag/graphrag.md
          - RAG evaluation: rag/rag-evaluation.md
      - Architecture patterns:
          - patterns/index.md
          - Design patterns: patterns/design-patterns.md
          - Design principles: patterns/design-principles.md
          - Code quality pipeline: patterns/code-quality-pipeline.md
      - Frameworks and platforms: tools-and-frameworks/index.md
      - Developer tools:
          - ai-dev-tools/index.md
          - GitHub Copilot: ai-dev-tools/github-copilot.md
          - Claude Code: ai-dev-tools/claude-code.md
          - Claude Code skills and agents: ai-dev-tools/claude-code-skills.md
          - Model Context Protocol: ai-dev-tools/mcp.md
  - Reference:
      - Glossary: glossary/index.md
      - Resources: reference/resources.md
      - Official sources: references/index.md
      - Browse by tag: tags.md                              # NEW
      - What's new: whats-new/index.md
```

Notes:
- Setup stays under Start here rather than Build so the Build tab is a clean 1 to 9. The-path links to it as module 0.
- Embeddings goes back into Retrieval in depth where its Next Steps links point.
- Enterprise patterns moves to Understand because it is the one patterns page a non-developer needs. patterns/index.md must stop listing it as a card, or keep the card with a note.
- Developer tools sits under Go deeper as a subsection. If the Tools pages turn out to be top search entry points once GSC is live, split it back out as a seventh tab. Zero URL cost either way.
- "Wider Context", "Foundations", "Your Tools", "The Agent Path" as tab names all go.

## 4. Routing conventions (applied to every page)

### Page header block
Directly under the H1, one admonition, same shape everywhere:

```markdown
!!! abstract "Understand · 30 min · no code"
    **Before this:** [How models work](...)
    **After this:** [Agentic AI](...)
    **Hands-on version:** [Module 1, Tool calling](...)   (only where a counterpart exists)
    **In depth:** [Retrieval in depth](...)                (only where a counterpart exists)
```

Build pages already have "What you'll be able to do" and "Next"; keep those, add the layer line and the "Overview version" back-link.

### Layer boxes on the overlap pairs
| Understand page | Build counterpart | Go deeper counterpart |
|---|---|---|
| concepts/retrieval-and-data | 02-agents/retrieval | rag/ (all) |
| concepts/safety-and-responsible-ai | 02-agents/safety | — |
| concepts/ai-agents | 02-agents/tool-calling, the-agent-loop, the-harness | patterns/design-patterns |
| concepts/agentic-ai (observability section) | 02-agents/observability | — |
| concepts/agentic-ai (MCP section) | — | ai-dev-tools/mcp |
| concepts/agentic-ai (memory, orchestration) | — | patterns/design-patterns |
| rag/rag-evaluation | 02-agents/evaluation | — |

Each Understand page says at the top: "This is the overview. To build it: X. For depth: Y." Each Build page says: "New to the idea? Read the overview first: X." Some of these links exist already (all nine Build pages link to concepts/, five concepts pages link down); they are inconsistent in placement and wording, so the standard block replaces them.

### Tags become the level system
The tags plugin is enabled but has no index page, so it does nothing. Give it a job:
- Level tags: `Understand`, `Build`, `Go deeper`, `Tools`, `Reference`. One per page.
- Topic tags: `Agents`, `Retrieval`, `Safety`, `Evaluation`, `Prompting`, `Models`, `MCP`, `Claude Code`, `Copilot`, `Azure`.
- Add `docs/tags.md` with the `<!-- material/tags -->` marker and set `tags_file: tags.md`.
- Replace today's ad-hoc tags (Beginner, News, Getting Started, Intermediate, Advanced) with the two sets above.

### Home page (index.md), rewritten
1. One-paragraph statement of what the site is and who it is for (public, no "our organization").
2. Three entry cards: **Understand AI (no code)** → 00-start-here/index.md reading path; **Build an agent** → the-path.md; **Look something up** → glossary.
3. "How this site is layered": a four-row table (Understand, Build, Go deeper, Reference) with one sentence each.
4. Persona boxes, kept but corrected: analysts and product managers; engineers; students and new joiners (not "co-op"); leaders. Each points at the reading path and one or two deeper pages.
5. Drop the 60-line site map diagram. The nav is the site map.
6. What's new link.

### New page: 00-start-here/index.md, "Choose your path"
- The two path tables from section 2 with time estimates.
- "How pages are marked": explains the header block and level tags.
- "If you only have an hour": AI 101, What an agent is, Safety.
- Becomes the target of every "not sure where to start" link.

## 5. Style unification

Two voices exist. The Build voice (August) is the better one: sentence case, dated, specific, admits what failed. Bring the March pages to it.

| Item | March pages do | Build pages do | Rule |
|---|---|---|---|
| Heading case | Title Case ("Design Patterns for AI Agent Systems") | Sentence case ("The agent loop") | Sentence case everywhere; H1 included |
| Dashes | ` -- ` double hyphen (74 occurrences) | em dash (211) | Em dash in prose. Never ` -- ` |
| Bottom section | "References" (link list) | "Go deeper" (annotated) | "Go deeper", each link with one line on why |
| Dating | none | "Verified as of YYYY-MM-DD" | Every page that names a product, model or spec carries the stamp; conceptual pages do not |
| Mermaid palette | navy/cyan/maroon/purple (#057398, #632C4F, #853175, #9e57a2, #004987, #259638, #00A0DF) in 11 files | CLAUDE.md palette (teal, green, sky, amber, red) | CLAUDE.md palette only, `color:#fff` on every styled node. Replace with a sed sweep, then eyeball each diagram in dark mode |
| Mermaid line breaks | `\n` in labels | `<br/>` | `<br/>` |
| Voice | "our organization", "we use", "reach out to the team" | public | Public. "Your team", "an organisation", "open a pull request" |
| Model names | in tables ("GPT-4o / GPT-4.1") | capability tiers, dated links | No model tables. Name the class (frontier, small, open-weight) and link the vendor's live model page |
| Glossary size | "70+" and "60+" | — | Count it once, state it once, or say "the glossary" |

Not changed: no emojis (already respected), admonition types, grid cards.

### Code sample dialect
- **Concepts pages:** no code required. Where a snippet clarifies (prompting, tool schemas), it is a short JSON or pseudo-Python block marked optional.
- **Build pages and labs:** stay as they are. They use raw OpenAI-compatible HTTP from the standard library, which is the most vendor-neutral form possible. Add an **Azure OpenAI** tab to Setup and labs/README next to the Ollama and OpenAI ones: base URL `https://<resource>.openai.azure.com/openai/v1`, key or Entra token, model = deployment name. Verify the auth header shape before publishing; the v1 endpoint accepts `api-key` and Entra bearer tokens, and whether it accepts a raw key as Bearer needs a test.
- **Go deeper pages:** where SDK code is shown, use `pymdownx.tabbed` (already enabled, with `content.tabs.link` so a choice sticks across pages): tabs **Python (openai SDK)** and **C# (Azure OpenAI / MAF)** where a .NET equivalent is meaningful. The six C# samples in samples/ become the source for those tabs once repinned to MAF 1.0, and get linked from the site for the first time.
- Provider-specific behaviour (Anthropic thinking blocks, Google thought signatures, Azure content filters) goes in a callout, not the main flow.

## 6. Page-by-page disposition

Legend: **keep** (no content change), **frame** (add header block, fix voice/style, no structural change), **rewrite** (substantial), **new**.

| Page | Layer | Action | Notes |
|---|---|---|---|
| index.md | — | rewrite | Section 4 |
| 00-start-here/index.md | Start | new | Choose your path |
| 00-start-here/the-path.md | Start | frame | Ten not eleven; "Who this is for" gains the reading-path pointer instead of "stop there"; link to Choose your path |
| 00-start-here/setup.md | Start | frame | Azure OpenAI tab |
| getting-started/index.md | Understand | rewrite | Remove "Our Organization" section and tabs; "Where to go next" becomes the reading path; model table becomes capability tiers |
| concepts/index.md | Understand | frame | Cards in reading-path order; add Enterprise patterns card |
| concepts/foundation-and-models.md | Understand | frame | Model table to tiers with dated links; palette |
| concepts/prompting-and-techniques.md | Understand | frame | Nine code blocks: keep, mark optional; palette |
| concepts/ai-agents.md | Understand | rewrite (light) | Retitle "What an agent is"; its "Detailed Component Architecture" and "Workflows" sections are Build/Deeper material, trim to overview and link to the modules and design patterns |
| concepts/agentic-ai.md | Understand | frame | Layer boxes on the tool-use, memory, observability, MCP sections pointing down |
| concepts/retrieval-and-data.md | Understand | frame | Layer box to 02-agents/retrieval and rag/; stays as the reader-level overview |
| concepts/fine-tuning-and-training.md | Understand | frame | palette |
| concepts/safety-and-responsible-ai.md | Understand | frame | Layer box to 02-agents/safety; add OWASP agentic top 10 link |
| concepts/infrastructure-and-operations.md | Understand | frame | palette |
| patterns/enterprise-patterns.md | Understand | frame | Moves tab; palette; its Agentic RAG section gets the layer box down to rag/rag-fundamentals "Agentic RAG" and module 5 |
| 02-agents/* (9 pages) | Build | frame | Header block with "Overview version" back-link; module 1 entry hand-off; module 9 exit hand-off |
| rag/index.md | Deeper | frame | |
| rag/* (6 pages) | Deeper | keep or frame | Best section on the site; sentence-case headings, dates on the tool tables |
| patterns/index.md | Deeper | frame | Drop or annotate the Enterprise patterns card |
| patterns/design-patterns.md | Deeper | frame | palette; link from concepts/agentic-ai orchestration section |
| patterns/design-principles.md | Deeper | keep | |
| patterns/code-quality-pipeline.md | Deeper | keep | |
| tools-and-frameworks/index.md | Deeper | frame | Add OpenAI Agents SDK and Google ADK entries so it is not a Microsoft-only landscape; dated |
| ai-dev-tools/* (5 pages) | Tools | frame | Sentence case on claude-code.md headings |
| glossary/index.md | Reference | frame | Count terms; add: structured output, idempotency, pass^k, harness, context rot, lethal trifecta, elicitation, Streamable HTTP; confirm the RAG family is complete as a set (naive, advanced, modular, agentic RAG, GraphRAG, hybrid search, reranking, HyDE, late chunking, parent-child chunking) |
| reference/resources.md | Reference | keep | The model for the other reference page |
| references/index.md | Reference | rewrite | Becomes "Official sources": one table per vendor (Anthropic, Microsoft, OpenAI, Google, NVIDIA, Meta, GitHub, Linux Foundation for MCP/A2A), current URLs only, each with one line on what it is for. Remove AutoGen and SK as "current", remove retired Copilot CLI, fix the MCP spec pin, Llama link, Azure naming. No certification section |
| whats-new/index.md | Reference | rewrite | Entries for Aug 2026 (the path, labs, resources) and Sep 2026 (restructure); fix "four routes" |
| tags.md | Reference | new | |

## 7. Content additions (after the restructure, each one page plus a lab where marked)

Ordered by how big a gap they leave today.

1. **Structured output** (Build, between 1 Tool calling and 2 The agent loop, or as 1b). Zero coverage today of the mechanism every agent depends on. Lab: schema-constrained output, validate, retry on failure.
2. **Memory** (Build, after 4 Context engineering). Concepts/agentic-ai covers it in prose; no lab. Lab: short-term via the message list, long-term via a file store, and the failure where memory poisons context.
3. **Multi-agent** (Build, after 9 Production, as 10). The path stops at one agent. Lab: supervisor and handoff on the same task, with the Cognition vs Anthropic trade-off measured (context sharing vs parallel reads).
4. **Official sources** rewrite with NVIDIA (NIM, NeMo Guardrails, NeMo Agent Toolkit), OpenAI (Agents SDK, Responses API), Google (ADK, Gemini API), alongside Anthropic and Microsoft.
5. **Prompt caching and cost** as a section in 7 Observability or 9 Production rather than a page.
6. **Computer use and browser agents** as a Go deeper page once there is something durable to say.

Inserting new modules into the numbered sequence does not change any URL; module numbers live in nav labels and page text only.

## 8. Implementation sequence (PR-sized, each independently shippable)

Each PR ends with: `mkdocs build --strict`, diff `site/sitemap.xml` against the live sitemap (must be a superset, never missing an entry), and the CI tag assertions.

| PR | Scope | URL risk |
|---|---|---|
| 1 | Hygiene from the audit: edit_uri, pin mkdocs<2, prune requirements, delete hook, fix Llama link, one glossary number, ten-not-eleven, enable mkdocs-redirects with an empty map | none |
| 2 | Nav rewrite to section 3; new Choose your path page; new tags page; level and topic tags on every page | none |
| 3 | Home page rewrite; AI 101 rewrite; What's new update | none |
| 4 | Header blocks and layer boxes on all 44 pages; module 1 entry and module 9 exit hand-offs | none |
| 5 | Style sweep: sentence case, dashes, palette, `<br/>`, org voice; visual check of every diagram in dark mode | none |
| 6 | Official sources rewrite; Frameworks page additions; Resources shelf re-verified with new date | none |
| 7 | Azure OpenAI tab in Setup and labs; C# samples repinned to MAF 1.0 and linked | none |
| 8 | CLAUDE.md rewritten to describe the layered structure and the conventions above; delete or stub copilot-instructions.md; README fixes; Docker consolidation | none |
| 9+ | Content additions from section 7, one PR each | new URLs only |

Page merges (for example folding concepts/retrieval-and-data into rag/index) are deliberately not in this plan. Revisit after GSC shows which copy of each overlapping topic actually earns traffic; then merge toward the winner with a redirect.

## Open items
- Azure OpenAI v1 endpoint auth header shape: test before writing the Setup tab.
- Whether Developer tools warrants its own tab: decide after GSC data.
- Term count for the glossary: count during PR 1.
