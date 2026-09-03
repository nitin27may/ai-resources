# ai-resources audit — 2026-09-02


> **Historical record.** This audit describes the site as it was on 2026-09-02,
> before the restructure. Every finding in it has been actioned. Kept because the
> reasoning explains why the current structure is the way it is. For the current
> state, read `STATUS.md`.

**Repo:** ~/workspace/ai-resources (nitin27may/ai-resources), HEAD b937fe5, main, clean tree
**Live:** https://nitinksingh.com/ai-resources/ (HTTP 200, last deploy 2026-09-02 01:06 UTC)
**Scale:** 44 pages, ~56,000 words, 10 Python labs, 6 C# samples
**Previous audit:** ai-resources-audit-2026-08-21.md (most of it has since been actioned, see section 1)

## Method

- `mkdocs build --strict --clean` in a throwaway venv (mkdocs 1.6.1, Material 9.x): 0 warnings, 44 pages, 1.2 s.
- Internal links: every `.md` link target resolved. Nav vs disk: no orphans, no missing entries.
- All 208 unique external URLs resolved with curl (status + final URL recorded).
- Live sitemap.xml and robots.txt fetched; sitemap has 44 URLs and is registered in the root robots.txt.
- Search Console: NOT verified. The gsc MCP hung 1800 s on two calls (token missing, known behaviour). Re-auth needed before indexing can be checked.

## 1. What the Aug 21 audit fixed (verified)

Done via PRs #4 to #17: site_url corrected, sitemap registered in root robots.txt, `--strict` in CI, GA block present and asserted in CI, OG/Twitter/JSON-LD tags, social card, Copilot Extensions page removed, MCP page rewritten to the 2026-07-28 spec, Tools & Frameworks rewritten around Microsoft Agent Framework, invented Claude Code memory section removed, Skills page fixed, 11-module agent path with 10 labs added, `reference/resources.md` vetted shelf added, `slides.md`/`Welcome.md` removed.

## 2. Still open from Aug 21 (unchanged)

| # | Item | Where |
|---|---|---|
| O1 | requirements.txt unpinned; 7 plugins installed but not enabled (mermaid2, minify, redirects, with-pdf, awesome-pages, macros, exclude-search) plus weasyprint | requirements.txt |
| O2 | hooks/cache_control.py is dead (no `hooks:` key in mkdocs.yml) | hooks/ |
| O3 | Dockerfile and Dev.Dockerfile byte-identical, root user, no healthcheck, pip list diverges from requirements.txt, `container_name: ea-notes-mkdocs`, obsolete `version:` key | Dockerfile, Dev.Dockerfile, docker-compose.yml |
| O4 | README documents a dev container that does not exist and `mkdocs config`, which is not a command | README.md |
| O5 | CLAUDE.md drift: lists minify/macros/awesome-pages/redirects as key plugins, cites mermaid-custom.css and mermaid-fullscreen.js (neither exists), documents the dev container, says concepts has "8 modules", does not mention 00-start-here/, 02-agents/, labs/ or reference/ at all | CLAUDE.md |
| O6 | .github/copilot-instructions.md still mandates a Blog nav entry, a purple/pink Mermaid palette, and contains emojis | .github/ |
| O7 | Org-internal framing on a public site: "Built for everyone in the organization", "What we use in our organization", "Co-op Students & New Joiners", "How AI Fits Into Our Organization", "View Our Stack", "what we invest in", "Reach out to the team" | index.md, getting-started/index.md, whats-new/index.md |
| O8 | What's New last entry March 2026. It also describes "Learning Paths, four structured routes", which no longer exists (the page is now a single path) | whats-new/index.md |
| O9 | Glossary size claimed as "70+ terms" on Home and "60+ AI terms" on Getting Started | index.md:64, getting-started/index.md:93 |
| O10 | C# samples pin a Nov 2025 MAF preview; samples/readme.md tells you to run `./app.cs`, which does not exist; samples are linked from nowhere on the site | samples/ |

## 3. New findings

### N1. `edit_uri` is an Azure DevOps format, so "Edit this page" is broken on GitHub
`mkdocs.yml`: `edit_uri: "?path=/docs/"`. With `repo_url` on github.com this produces `https://github.com/nitin27may/ai-resources?path=/docs/<file>`, which is not an edit URL. The `?path=` form is Azure DevOps' convention, a leftover from the internal EA repo. Fix: `edit_uri: edit/main/docs/`. Both `content.action.edit` and `content.action.view` are enabled, so every page shows two dead icons.

### N2. Tags plugin is enabled but produces nothing
`plugins: - tags` with no `tags_file`, and no page is designated as the tags index. Every page carries `tags:` front matter (Beginner, RAG, Reference...) that renders as chips linking nowhere useful. Either add `docs/tags.md` with the `tags` marker, or drop the plugin and the front matter.

### N3. Material warns that MkDocs 2.0 will break plugins and theme overrides
Printed on every build. `mkdocs>=1.5.0` means CI resolves whatever is newest. Pin `mkdocs>=1.6,<2` now, before an upstream release breaks the deploy.

### N4. External links (208 checked)
- **Dead:** `https://llama.meta.com/` now lands on developer.meta.com with HTTP 400 (2 pages).
- **Bot-blocked, not rot:** openai.com/research, platform.openai.com/docs/overview (403).
- **Rate-limited during the sweep, unverified:** 4 deep links into nitin27may/e-commerce-agents (429 from GitHub after 67 rapid requests). Almost certainly fine; recheck singly.
- **Redirects that signal stale content, not just stale URLs:**
  - 9 learn.microsoft.com paths under `/ai-services/openai/`, `/ai-studio/`, `/ai-services/agents/` now redirect to `/azure/foundry/`. The References page still calls these "Azure OpenAI Service" and "Azure AI Studio".
  - OpenAI Assistants API link redirects to its migration page (Assistants is deprecated in favour of Responses/Agents SDK).
  - `docs.anthropic.com/en/docs/claude-code` redirects to code.claude.com (References page still uses the old host).
  - `python.langchain.com/docs/tutorials/rag/` now lands on the deepagents RAG page, a different product.
  - `cloud.google.com/vertex-ai/docs` redirects to "Gemini Enterprise Agent Platform" (product renamed).
  - Copilot "coding agent" docs renamed to "cloud agent".
  - The MS Learn "AI Fundamentals" path redirects to a different path (original retired).
  - MCP spec pinned link `specification/2025-11-25` in references/index.md is two revisions old and contradicts resources.md.

### N5. `references/index.md` contradicts `reference/resources.md`
Two folders, `reference/` and `references/`, one letter apart, both in the Reference tab. The older one lists AutoGen and Semantic Kernel as current official frameworks, links the retired "Copilot in the CLI", labels an MCP architecture page as "Building Copilot Extensions", and pins the old MCP spec. The newer one tells the reader to avoid AutoGen and any pre-July-2026 MCP tutorial. A reader who opens both will not know which to believe.

### N6. "Eleven modules" vs ten
the-path.md says "Eleven modules" in the title description, abstract and Home meta description. The table and the diagram list modules 0 to 9, which is ten. labs/ has ten labs. Pick one number.

### N7. Home page describes the old site
index.md is still the March 2026 landing page. It has no card for The Path, which is now the spine of the site. The Site Map diagram lists "Copilot CLI & Extensions" (deleted) and "Learning Paths" (renamed), and omits the entire agent path. The engineer persona box says "Follow the Developer Learning Path: Concepts, then RAG, then AI Developer Tools", which is no longer the path. The meta description promises "eleven modules, ten labs" that the body never mentions.

## 4. Structure and navigation assessment

### Two generations of content coexist, not one site
- **Gen 1 (March 2026):** getting-started, concepts (8), rag (6), patterns (4), ai-dev-tools (4), glossary, references, tools-and-frameworks, whats-new. Encyclopedic, org-internal voice, persona-driven (BA, PM, leader, co-op).
- **Gen 2 (Aug 2026):** 00-start-here (2), 02-agents (9), reference/resources, labs/. Hands-on, lab-driven, developer-only, "verified as of" dated.

Gen 2 is the better material and matches the "agentic bible" goal. Gen 1 is where the beginner entry point lives. They are joined by a nav rewrite (PR #11) that deliberately moved nothing, so the join shows.

### Nav: 9 top-level tabs against a house rule of 3 to 5
Home, Start Here, Foundations, The Agent Path, Retrieval in Depth, Wider Context, Patterns, Your Tools, Reference. Problems:
- **"Wider Context"** is a holding pen for five leftover concepts pages. The label tells a reader nothing.
- **"Foundations"** pulls `rag/embeddings.md` out of the RAG folder into a different tab, so its Next Steps links jump tabs.
- **Folder numbering is half-done:** `00-start-here`, `02-agents`, nothing at 01, and concepts spread across three tabs.
- **Reference** has two near-duplicate pages (N5) plus a stale What's New.

### Overlap map (same topic, three places)
| Topic | Gen 1 concept page | Gen 1 deep section | Gen 2 path module |
|---|---|---|---|
| Retrieval | concepts/retrieval-and-data (1,672 words: RAG, embeddings, vector DBs, chunking, GraphRAG) | rag/* (6 pages) | 02-agents/retrieval |
| Safety / injection | concepts/safety-and-responsible-ai | — | 02-agents/safety |
| Agents, loop, tools | concepts/ai-agents + concepts/agentic-ai (tool use, memory, HITL, observability, protocols) | patterns/design-patterns | 02-agents/tool-calling, the-agent-loop, the-harness |
| Observability | concepts/agentic-ai "Observability and Tracing" | — | 02-agents/observability |
| Evaluation | — | rag/rag-evaluation | 02-agents/evaluation |
| MCP | concepts/agentic-ai "Key Protocols" | ai-dev-tools/mcp | — |

None of it is wrong, but a reader arriving from search lands on whichever copy ranks, and the copies disagree in depth, date and voice.

### The beginner-to-expert continuum is broken in the middle
- Beginner entry is getting-started/index.md (AI 101). Its "Where to Go Next" routes into Gen 1 concepts, never into The Path.
- The Path's "Who this is for" says it is for working developers, and tells everyone else to read AI 101, the glossary and Safety "and stop there".
- Result: a beginner is never handed to the path, and the path never looks back at the beginner material. That is the opposite of the stated goal.

### Coverage gaps against the "agentic bible" goal (files mentioning the term)
| Topic | Files | Note |
|---|---|---|
| NVIDIA (NIM, NeMo Guardrails, NeMo Agent Toolkit, DLI) | 0 | You named NVIDIA as a must-have source |
| OpenAI Agents SDK / Responses API | 0 to 1 | Only Swarm is mentioned, as "avoid" |
| Google ADK / Gemini CLI | 0 | |
| Structured output / JSON schema | 0 | A core agent building block, absent |
| Computer use / browser agents | 0 | |
| Prompt caching | 1 | Cost is covered but caching is one mention |
| Multi-agent orchestration, hands-on | 0 labs | Covered conceptually in patterns; the path stops at a single agent in production |
| Memory (short/long-term) | concepts only | No module, no lab |
| A2A, AG-UI | concept-level | Fine for now, matches resources.md scepticism |
| Reasoning models, thinking budgets | 2 | |
| Certifications and official courses | 1 | No AI-102, no Anthropic Academy, no NVIDIA DLI, no Google/AWS paths |
| vLLM / self-hosted serving | 0 | |
| Copilot Studio / Foundry Agent Service | ~1 | |

## 5. URL safety rules for any restructure

The 44 live URLs come from file paths, not nav labels. This means:
- **Zero risk:** renaming tabs, regrouping, reordering, changing section titles, adding new pages, rewriting page bodies. Do all of this freely.
- **Needs a redirect:** moving or renaming a file, or merging two pages. `mkdocs-redirects` is already in requirements.txt; enable it and add `redirect_maps` for every moved path. It emits meta-refresh stubs that GitHub Pages serves fine, and it keeps them out of the sitemap.
- **Never:** delete a page that is in the live sitemap without a redirect target.
- After any move: rebuild, diff the new sitemap.xml against the live one, and confirm every removed URL has a redirect stub in `site/`.

Recommendation: keep all 44 paths as they are for this pass. The structural problems above are fixable with nav changes, page rewrites and new pages, which touch no URLs. Merges (for example folding concepts/retrieval-and-data into rag/) are a later, redirect-backed step.

## 6. Proposed target structure (URL-preserving)

Five tabs, all existing files stay where they are:

1. **Start Here** — index (rewritten), AI 101 (re-framed for the public), The Path, Setup, Glossary
2. **Learn** (Foundations) — how models work, prompting, embeddings, fine-tuning, infrastructure, safety & RAI
3. **Build** (The Agent Path) — the 10 modules; then a new "Beyond the path" group: multi-agent patterns (patterns/design-patterns), enterprise patterns, agentic AI protocols (concepts/agentic-ai), retrieval in depth (rag/*)
4. **Tools** — Claude Code, Skills, Copilot, MCP, frameworks & platforms (tools-and-frameworks)
5. **Reference** — Resources (vetted shelf, becomes the single reference page), Official docs by vendor (references/index rewritten to match, adding NVIDIA/Google/OpenAI current links and certifications), What's New (updated or dropped from nav)

Page-level moves that need decisions (see questions): concepts/ai-agents and concepts/retrieval-and-data are the two Gen 1 pages that most fully duplicate Gen 2; they either become short "overview, then go to X" pages or get merged with redirects.

## 7. Work order

**Under an hour, no content:** N1 edit_uri; N3 pin mkdocs<2; O1 prune requirements; O2 delete hook; N6 pick ten or eleven; O9 one glossary number; fix llama.meta.com link.

**Half a day, hygiene:** O3 to O6 (Docker, README, CLAUDE.md, copilot-instructions); N2 tags decision; enable mkdocs-redirects (empty map for now).

**One to two days, structure:** new Home page around The Path; five-tab nav; re-frame the six org-internal passages; rewrite references/index.md so it agrees with resources.md; update What's New; add the "beginner to path" hand-off in AI 101 and the "path to depth" hand-off at the end of Production.

**Ongoing, content:** vendor must-read shelf (Anthropic, Microsoft, NVIDIA, OpenAI, Google, plus certifications); structured output, memory and multi-agent modules with labs; refresh the Azure naming.

## Not verified
- Search Console indexing status of the 44 URLs (MCP token). Re-auth and rerun.
- The 4 e-commerce-agents deep links (GitHub 429 during the sweep).
- C# samples were not compiled (no .NET SDK here).
