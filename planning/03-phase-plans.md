# ai-resources phase plans — 2026-09-02


> **Historical record.** All phases in this document are complete (see
> `STATUS.md`). Counts and module numbers quoted here are from the time of
> writing. Kept for the per-phase reasoning and the check-script rationale.

Detailed task lists for the phases in ai-resources-restructure-plan-2026-09-02.md. One phase = one branch = one PR. Nothing here changes an existing URL until Phase 9, which only adds URLs.

## Cross-cutting checks (every phase)

Run before opening the PR:

1. `mkdocs build --strict --clean` with zero warnings.
2. Sitemap guard: every `<loc>` in the live sitemap (baseline captured in Phase 1) exists in `site/sitemap.xml` or as a redirect stub in `site/`. Fails the build otherwise. Added to CI in Phase 1.
3. Internal link check (the script from the audit): zero broken `.md` links, zero broken `#anchors`.
4. Org-voice grep returns zero across docs/ from Phase 3 onward.
5. CI tag assertions (GA, Open Graph, JSON-LD) stay green.
6. For any phase that touches diagrams or layout: `mkdocs serve`, screenshots of the affected pages in dark and light mode attached to the PR.

Baseline numbers today, as printed by `planning/scripts/style-greps.sh` and `check-links.py` on 2026-09-02: 44 pages, 44 sitemap entries, 203 external URLs, 74 glossary terms, 0 header blocks, 115 double-hyphen dashes, 182 foreign palette hex occurrences across 11 files, 108 `\n` label breaks across 13 files, 18 org-voice lines, 24 bare "References" sections, 91 Title Case H2s, 40 pages without a level tag, 3 "eleven" claims, 49 Mermaid diagrams. Each phase's done-when says which of these must reach zero.

---

## Phase 1 — Hygiene and guards (about 2 hours)

Goal: fix the defects the audit found in config, and put the URL guard in place before anything structural happens.

Files: mkdocs.yml, requirements.txt, .github/workflows/deploy.yml, hooks/cache_control.py, docs/00-start-here/the-path.md, docs/index.md, docs/getting-started/index.md, docs/references/index.md, docs/concepts/foundation-and-models.md, tests/sitemap-baseline.txt (new)

Tasks:
1. `edit_uri: edit/main/docs/` replacing the Azure DevOps `?path=/docs/`. Verify one page's edit link resolves to a github.com/.../edit/main/docs/... URL.
2. Pin requirements: `mkdocs>=1.6,<2`, `mkdocs-material` pinned to the version CI resolves today, `mkdocs-glightbox`, `mkdocs-git-revision-date-localized-plugin`, `mkdocs-redirects`, `pymdown-extensions`. Remove mermaid2, minify, with-pdf, weasyprint, awesome-pages, macros, exclude-search, markdown.
3. Enable `redirects` plugin with an empty `redirect_maps`, so later merges are one line each.
4. Delete hooks/cache_control.py.
5. Capture the live sitemap into tests/sitemap-baseline.txt (44 URLs). Add a CI step after the build that asserts every baseline URL is present in site/sitemap.xml or has a redirect stub. Add a one-line script for running it locally.
6. "Eleven modules" to "Ten modules": the-path.md front matter and abstract, index.md description.
7. Glossary count: the glossary has 74 terms. Home says "70+", AI 101 says "60+". Both become the real number rounded down to the nearest ten with a plus.
8. Llama link: `https://llama.meta.com/` to `https://www.llama.com/` in references/index.md and foundation-and-models.md, after curl confirms 200.
9. Add `site/`, `labs/__pycache__/` sanity to .gitignore (dedupe the existing duplicate entries while there).

Done when: strict build passes, sitemap identical to live, CI green with the new guard, edit icon on a live page opens a GitHub edit URL after deploy.

---

## Phase 2 — Navigation skeleton and tags (about 4 hours)

Goal: the six-tab structure, the two new pages, and level tags on every page. No prose rewrites of existing pages.

Files: mkdocs.yml, docs/00-start-here/index.md (new), docs/tags.md (new), docs/concepts/index.md, docs/patterns/index.md, front matter of all 44 pages

Tasks:
1. Replace `nav:` with the six-tab structure from the restructure plan section 3. Understand in reading-path order. Build numbered 1 to 9. Go deeper with four sidebar groups. Reference with Glossary, Resources, Official sources, Browse by tag, What's new.
2. New docs/00-start-here/index.md, "Choose your path":
   - One paragraph: two ways through the site, pick by what you want at the end.
   - Reading path table (ten pages, times, one line each) and Build path table (Setup plus nine modules, times).
   - "If you only have an hour": AI 101, What an agent is, Safety and responsible AI.
   - "How pages are marked": the header block and the level tags, one example.
   - "Not sure": start with AI 101 regardless.
3. New docs/tags.md with the Material tags marker; `tags_file: tags.md` in the plugin config.
4. Tag every page with exactly one level tag (Understand, Build, Go deeper, Tools, Reference) and one to three topic tags (Agents, Retrieval, Safety, Evaluation, Prompting, Models, MCP, Claude Code, Copilot, Azure, Operations). Remove the old ad-hoc tags (Beginner, Intermediate, Advanced, News, Getting Started, Home, Concepts, Patterns, Tools). Full mapping is in the restructure plan disposition table.
5. concepts/index.md: reorder cards to reading-path order, add an Enterprise AI patterns card, add one line at the top: "This is the no-code layer. Each page links to its hands-on and in-depth versions."
6. patterns/index.md: keep the Enterprise patterns card, note that it lives under Understand.
7. Point every existing "not sure where to start" link (index.md, the-path.md) at 00-start-here/index.md.

Done when: 46 sitemap entries (44 plus the two new), six tabs render, the tag page lists every page under a level, no page missing a level tag (grep), strict build clean.

---

## Phase 3 — Home, AI 101, What's new (about 4 hours)

Goal: the three pages a first-time visitor sees describe the site that exists.

Files: docs/index.md, docs/getting-started/index.md, docs/whats-new/index.md

Tasks:
1. index.md rewrite:
   - Keep `hide: navigation, toc` and the H1 "AI Knowledge Hub".
   - Opening paragraph, public voice: what the site is, who it is for, that it is free and that the build path runs on your own machine.
   - Three door cards: "Understand AI, no code" to 00-start-here/index.md, "Build an agent" to the-path.md, "Look something up" to glossary.
   - "How this site is layered": four-row table, one sentence per layer.
   - Persona boxes, corrected: analysts and product managers; engineers; students and new joiners; leaders. Each names two pages.
   - Remove the site map diagram and the "What we use in our organization" card text.
   - Meta description: "A free path from AI basics to agents in production, for readers and builders. Ten hands-on modules, all local."
2. getting-started/index.md rewrite:
   - Keep the AI, ML, LLM explanations and the key terms; they are good.
   - "Popular LLMs" table becomes three capability tiers (frontier hosted, small and open-weight, on-device) with a dated link to each vendor's live model page. No model names.
   - Delete "How AI Fits Into Our Organization" and its four cards.
   - "Where to go next" becomes the reading path list, plus one line for developers pointing at the-path.md.
   - "References" becomes "Go deeper" with one line per link; drop the two links that redirect to retired paths.
3. whats-new/index.md:
   - New entry "September 2026: restructure" describing the layers and the two paths.
   - New entry "August 2026: the build path" listing the ten modules, labs, Resources shelf, MCP rewrite.
   - Fix the March entry: "Learning Paths, four structured routes" becomes a note that it was replaced by the single build path. Remove "Reach out to the team".
   - Keep the page in nav; it now has three dated entries.

Done when: org-voice grep returns zero for these three files, descriptions updated, CI tag assertions green, screenshots of Home in both modes attached.

---

## Phase 4 — Header blocks, layer boxes, hand-offs (about 6 hours)

Goal: every page tells the reader where it sits and where to go next.

Files: all 44 pages, docs/02-agents/tool-calling.md, docs/02-agents/production.md, docs/00-start-here/the-path.md

Tasks:
1. Define the block once in CLAUDE.md (Phase 8 copies it) and apply it under every H1:
   ```
   !!! abstract "Understand · 30 min · no code"
       **Before this:** ...  **After this:** ...
       **Hands-on version:** ...   **In depth:** ...
   ```
   Before and After follow the reading path, build path, or nav order within a Go deeper group. Hands-on and In depth only where the overlap table names a counterpart.
2. Build pages: keep "What you'll be able to do" and "Next"; add the level line and an "Overview version" link back to the matching Understand page.
3. Layer boxes on the seven overlap pairs from the restructure plan section 4, including the agentic RAG chain: enterprise-patterns "Agentic RAG" to rag-fundamentals "Agentic RAG" to module 5.
4. Module 1 entry hand-off: a two-line note at the top of tool-calling.md pointing newcomers to How models work and What an agent is.
5. Module 9 exit: a "Where to go from here" section at the end of production.md listing Retrieval in depth, Architecture patterns, Frameworks and platforms, Developer tools, Resources, each with one line.
6. the-path.md "Who this is for": replace "and stop there" with a pointer to the reading path and Choose your path.
7. Inbound link floor: after this phase every page has at least two inbound links from other pages (six pages have one today).

Done when: a grep for the header admonition matches exactly 44 files, link check clean, inbound link script shows no page below two.

---

## Phase 5 — Style sweep (about 6 hours, half of it visual checking)

Goal: one voice, one palette, one heading style.

Files: 24 March-era pages, all Mermaid diagrams

Tasks:
1. Sentence-case headings on the 24 Title Case pages. Product names and acronyms keep their capitals. Heading changes change anchor IDs: update the 6 in-page and cross-page `#anchor` links found in the audit, then re-run the link check.
2. Dashes: 115 occurrences of ` -- ` become em dashes. Code blocks excluded.
3. Mermaid palette: sed map on the 11 files. Navy and cyan (#057398, #00A0DF, #004987) to sky #0284c7; maroon and purple (#632C4F, #853175, #9e57a2) to teal #0d9488 or amber #d97706 depending on role; green #259638 to #16a34a; light blue #38bdf8 to teal-light #14b8a6. Every styled node gets `color:#fff`.
4. Mermaid line breaks: `\n` to `<br/>` in the 13 files.
5. Org voice: the 18 lines from the audit grep, replaced with public phrasing.
5. "References" to "Go deeper" on 24 pages: keep the links, add one line per link on why it is worth the click, remove any that redirect to retired content (list in Phase 6).
6. Visual pass: serve locally, open every page with a diagram (49 diagrams), dark mode and light mode, fix any contrast or overflow, attach a contact sheet to the PR.

Done when: greps for ` -- `, the seven foreign hex values, `\n` inside mermaid fences, and the org phrases all return zero; anchors resolve; screenshots attached.

---

## Phase 6 — Reference layer (about 5 hours)

Goal: the two reference pages agree with each other and with the vendors' current sites; NVIDIA, OpenAI and Google are represented.

Files: docs/references/index.md, docs/tools-and-frameworks/index.md, docs/reference/resources.md, plus the ~15 pages carrying redirected URLs

Tasks:
1. references/index.md rewrite as "Official sources" (URL stays references/). One table per vendor, each row: link, one line on what it is for. Current URLs only, each curl-verified on the day, page stamped "Verified as of".
   - Anthropic: platform docs, engineering blog, Claude Code docs, cookbooks, MCP site and spec (current revision, unpinned link plus the dated one).
   - Microsoft: Azure AI Foundry, Agent Framework, Azure AI Search, Content Safety, Document Intelligence, generative-ai-for-beginners, ai-agents-for-beginners, Responsible AI.
   - OpenAI: developer docs, models page, Agents SDK, Responses API, function calling, embeddings, cookbook.
   - Google: Gemini API docs, ADK, AI Studio, Gemini Enterprise Agent Platform, ML crash course.
   - NVIDIA: NIM, NeMo Guardrails, NeMo Agent Toolkit, developer blog.
   - Meta: llama.com. GitHub: Copilot docs, github-mcp-server. Linux Foundation: A2A.
   - Removed: AutoGen and Semantic Kernel as current, Copilot in the CLI, "Building Copilot Extensions", Azure AI Studio naming, OpenAI Assistants.
   - No certification section.
2. tools-and-frameworks/index.md: add OpenAI Agents SDK and Google ADK entries and rows in the comparison table; add a short "how to choose" paragraph (language, cloud, whether you need a graph); stamp the page.
3. reference/resources.md: re-run every link, bump the verified date, add NeMo Guardrails to the local tools table if it runs locally without an account.
4. Fix the redirected URLs across docs to their final targets: the nine learn.microsoft.com Foundry paths, docs.anthropic.com to code.claude.com and platform.claude.com, platform.openai.com to developers.openai.com, python.langchain.com to docs.langchain.com, docs.llamaindex.ai to developers.llamaindex.ai, the Vertex AI and Copilot agent renames, the MS Learn path.
5. Re-run the 208-URL sweep; target zero 404 and 400, and note the two known 403 bot-blocks.

Done when: link sweep clean, the two reference pages make no contradictory claims (AutoGen, SK, MCP revision), NVIDIA present.

---

## Phase 7 — Azure OpenAI and C# (about 4 hours plus a test that needs your Azure resource)

Goal: the build path runs on Azure OpenAI with a config change, and the C# samples reach the site.

Files: docs/00-start-here/setup.md, labs/README.md, labs/_shared.py (comment only), samples/*.cs, samples/readme.md, docs/tools-and-frameworks/index.md, docs/patterns/design-patterns.md

Tasks:
1. Test the Azure OpenAI v1 endpoint with the labs' raw HTTP client: base URL `https://<resource>.openai.azure.com/openai/v1`, model = deployment name, auth as `api-key` header and as Entra bearer. This needs a resource of yours; values go in env vars, never in the repo.
2. setup.md and labs/README.md: a third tab, "Azure OpenAI", next to Ollama and OpenAI, with the three env vars and a note on which header worked.
3. samples/: repin to Microsoft Agent Framework 1.0 and current Microsoft.Extensions.AI and ModelContextProtocol packages; fix the stray `2` in 1-basicagent.cs; rewrite samples/readme.md with the actual file names and `dotnet run` instructions. Compile each with the local .NET 10 SDK.
4. Link the samples from the site: tools-and-frameworks Agent Framework section (a "six runnable samples" list) and design-patterns.md (tabbed Python and C# for the workflow and handoff patterns).

Done when: all six samples build, the Azure tab has been run end to end on lab 01 and 03, links resolve.

---

## Phase 8 — Repo documentation and Docker (about 3 hours)

Goal: the files that steer future sessions describe the site that now exists.

Files: CLAUDE.md, .github/copilot-instructions.md, README.md, Dockerfile, Dev.Dockerfile, docker-compose.yml

Tasks:
1. CLAUDE.md rewrite: the four layers and the two paths, the folder map including 00-start-here, 02-agents, labs, reference, the header block template, the tag sets, the style rules from Phase 5, the commands that exist (`mkdocs build --strict`, `mkdocs serve`, the sitemap guard script), the URL rule (never move a file without a redirect_maps entry). Remove the dev container, `mkdocs config`, the plugin list that is not enabled, mermaid-custom.css and mermaid-fullscreen.js.
2. copilot-instructions.md becomes five lines pointing at CLAUDE.md.
3. README: remove the dev container option, replace `mkdocs config` with `mkdocs build --strict`, refresh the topics list to the layers, keep the troubleshooting table minus the devcontainer row.
4. Docker: one Dockerfile installing from requirements.txt, non-root user, HEALTHCHECK on :8000, no PDF layers. Delete Dev.Dockerfile. docker-compose.yml: drop `version`, rename the container, point at the one Dockerfile. Verify `docker compose up` serves the site.

Done when: a fresh session reading CLAUDE.md can find every convention used in Phases 2 to 5; docker compose serves on 8000.

---

## Phase 9 onward — Content additions (one PR each, about a day each)

Each new module follows the Build page shape (What you'll be able to do, concept, Build it, Verify, In a framework, In a real system, In production, Go deeper, Next), ships with a lab in labs/, gets a nav entry, a header block, a place on its topic ladder, a glossary entry for any new term, and a What's new line. New URLs only.

9a. **Structured output** (Build, after 1 Tool calling). Schema-constrained output, validation, retry on invalid, the difference between JSON mode and schema enforcement, what to do when the provider does not support it. Lab: extract an order from free text into a schema, count validation failures with and without enforcement.

   **Where it sits, now decided.** The concept is introduced in
   [Prompting](../docs/concepts/prompting-and-techniques.md) under "Structured
   output: stop asking, start constraining", which gives the three levels (ask
   nicely, JSON mode, schema-constrained) and the warning that a valid schema is
   not a correct answer. That page already links forward to `02-agents/tool-calling.md`
   for the mechanism.

   So the Build module goes **between 1 Tool calling and 2 The agent loop**, as
   module 1b or a renumbered 2, because a tool definition *is* a schema and the
   model's request to call it *is* schema-constrained output — the lab reuses
   the dispatcher built in module 1 rather than introducing new machinery. Its
   lab directory is `labs/02b-structured-output/` if the existing numbers are
   kept, or a full renumber of `labs/` if not. Renumbering labs changes no site
   URL (lab directories are not published pages) but does change the module
   numbers in nav labels and in `the-path.md`, which is free.

   Ladder placement: Models and prompting ladder, between Prompting and
   4 Context engineering.

9b. **Memory** (Build, after 4 Context engineering). Short-term as the message list, long-term as a store the agent reads and writes, retrieval-backed memory, the failure where stale memory poisons a run. Lab: a file-backed memory, then a poisoned entry, then the fix.

9c. **Multi-agent, including agentic RAG** (Build, after 9 Production). Supervisor and handoff on the same task; the agentic RAG lab where the agent picks between two retrievers and no retrieval; the Cognition vs Anthropic trade-off measured on context sharing versus parallel reads. Lab: both orchestrations, same task, compare tokens and pass^k.

9d. **Prompt caching and cost** as a section in 7 Observability, not a page.

9e. **Computer use and browser agents** as a Go deeper page when there is something durable to write.

---

## Order and dependencies

1 → 2 → 3 → 4 are sequential; each depends on the previous. 5 and 6 can run in parallel after 4. 7 and 8 can run any time after 1. 9 needs 4 (the header block) and 8 (CLAUDE.md conventions) so new pages are born consistent.

| Phase | Depends on | Size |
|---|---|---|
| 1 Hygiene and guards | — | 2 h |
| 2 Nav skeleton and tags | 1 | 4 h |
| 3 Home, AI 101, What's new | 2 | 4 h |
| 4 Header blocks and hand-offs | 3 | 6 h |
| 5 Style sweep | 4 | 6 h |
| 6 Reference layer | 4 | 5 h |
| 7 Azure OpenAI and C# | 1, plus your Azure resource | 4 h |
| 8 Repo docs and Docker | 1 | 3 h |
| 9a to 9c Content modules | 4, 8 | 1 day each |
