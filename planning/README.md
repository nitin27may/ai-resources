# planning/ — restructure hand-off pack

This folder is the complete brief for restructuring the AI Knowledge Hub. It is written so that a new session, with any agent or model, can pick up any phase without the conversation that produced it. MkDocs publishes only `docs/`, so nothing here appears on the site.

Read in this order:

| File | What it is |
|---|---|
| STATUS.md | Where things stand. Read first, update last. |
| README.md (this) | Decisions, facts a fresh model may not know, rules, glossary of the plan's own terms |
| 01-audit.md | What is wrong today and why (2026-09-02, supersedes the 2026-08-21 audit) |
| 02-restructure-plan.md | The target: layers, the two paths, topic ladders, nav YAML, conventions, style, dispositions |
| 03-phase-plans.md | Task lists per phase with files, steps, done-when, size, dependencies |
| 04-page-matrix.md | One row per page: level tag, topic tags, time, before/after, hands-on and in-depth links. Source of truth for Phases 2 and 4 |
| 05-url-fixes.md | Every dead or redirected external URL with its replacement; org-voice lines with replacement text; palette map |
| sitemap-baseline.txt | The 44 live URLs on 2026-09-02. The guard script fails any build that drops one |
| scripts/ | check-links.py, sitemap-guard.sh, style-greps.sh: the done-when checks, runnable |

## Decisions already made (do not reopen)

Recorded from Nitin on 2026-09-02.

1. **Audience includes non-developers.** The Understand layer and the reading path are first-class. Every concept must be readable with no code.
2. **Vendor-agnostic concepts.** Code samples use OpenAI-compatible HTTP or the OpenAI SDK, with Azure OpenAI as a config tab. Other providers appear in callouts, not the main flow.
3. **Not a certification guide.** Official vendor sources are curated as must-reads. No exam prep, no cert tables.
4. **Site name and URL stay.** "AI Knowledge Hub" at https://nitinksingh.com/ai-resources/.
5. **No URL changes.** The 44 live URLs are preserved. Restructure through nav, rewrites and new pages. Page merges are deferred until Search Console data exists, and then require a `redirect_maps` entry.
6. **Reading-path order is retrieval before agents.** Give the model your data is a smaller step than let the model act.
7. **Search Console verification is deferred** until Nitin re-authenticates the gsc MCP. Do not block on it.
8. **Stepping-stone rule.** Each page needs only the pages before it on its ladder (02-restructure-plan.md section 2b). When adding a page, place it on a ladder.

## Facts a model with an earlier cutoff may get wrong

These are true as of 2026-09-02 and are load-bearing for the content. Do not "correct" them backwards. Sources are in docs/reference/resources.md and docs/ai-dev-tools/mcp.md.

- **MCP spec revision 2026-07-28** is current and is a breaking redesign: stateless requests, no initialize handshake or sessions, stdio and Streamable HTTP only (standalone SSE removed), Elicitation as the client feature, Tasks / Skills over MCP / MCP Apps as extensions. The Python SDK renamed `FastMCP` to `MCPServer`. Anything teaching the 2025-11-25 model is stale.
- **Microsoft Agent Framework 1.0 shipped 2026-04-03** and merges Semantic Kernel and AutoGen. AutoGen is in maintenance mode (last release v0.7.5, Sep 2025). Semantic Kernel receives security patches to roughly April 2027 and is superseded for new work.
- **GitHub Copilot Extensions (GitHub App based) were shut down 2025-11-10** and replaced by MCP servers. The `gh copilot` CLI extension is retired, replaced by a standalone `copilot` CLI. Copilot "coding agent" docs are now titled "cloud agent".
- **Azure AI Foundry** is the umbrella; "Azure OpenAI Service" and "Azure AI Studio" URLs redirect there. Write "Azure OpenAI in Foundry Models" or just "Azure OpenAI".
- **A2A** was donated by Google to the Linux Foundation in June 2025; v1.0 April 2026. It is not "by Google".
- **OpenAI Assistants API is deprecated** in favour of the Responses API and Agents SDK. Swarm is superseded by the Agents SDK.
- **Claude Code**: skills are directories `.claude/skills/<name>/SKILL.md`, auto-loaded by description; `.claude/commands/*.md` still works and both create slash commands. There are 31 hook events. Auto memory lives at `~/.claude/projects/<project>/memory/` and is per project. Docs are at code.claude.com.
- **Model names rot.** Do not add model tables. Use capability tiers and dated links to vendor model pages. The "verified as of" stamp is the contract with the reader.
- **The labs default to `qwen2.5:14b` on Ollama** deliberately (no reasoning trace). Do not swap in a reasoning model.
- **This site's own numbers**: ten Build modules (0 to 9), ten labs, 74 glossary terms, 44 pages before this work.

## Do not revert: Mermaid fence format

`mkdocs.yml` uses `fence_div_format` for the mermaid custom fence, not the
`fence_code_format` that Material's own documentation shows. That is deliberate.

Material's built-in Mermaid integration claims `pre.mermaid`, swaps it for a
`div.mermaid`, loads `mermaid@11` (unpinned) from unpkg, and renders into it. On
this site that produced an **empty div on every page**: no SVG, no console error,
all 49 diagrams invisible in production, and it had been shipping that way. It
reproduces on a stock Material site with no overrides and no custom CSS, so it is
upstream, not a local misconfiguration.

`fence_div_format` emits `div.mermaid` directly, so Material's handler finds no
`pre.mermaid` to claim, and `overrides/assets/javascripts/mermaid-init.js` owns
rendering against a pinned mermaid version. Verified with a headless browser:
29 pages, 49 diagrams, all rendering in both colour schemes.

If someone "corrects" the fence back to `fence_code_format` to match the Material
docs, every diagram on the site goes blank again and nothing will fail in CI.
Re-check with `planning/scripts/check-diagrams.py` before touching it.

## Do not revert: the forced-dark script

`overrides/main.html` no longer forces the slate scheme on load. The script that
did read `localStorage["data-md-color-scheme"]`, a key **Material never writes**
(it stores the palette under `__palette`), so the condition was true on every
page load and dark was reasserted every time. A reader could click the light
toggle, watch the page turn light, follow any link, and be back in dark. Light
mode was unreachable for the whole site.

Dark-by-default does not need a script: `theme.palette` lists slate first, which
Material already treats as the default for a first-time visitor, and it then
persists whatever the reader picks. `planning/scripts/check-themes.py` asserts
the light scheme survives navigation.

## Rules that apply to every phase

- Never move, rename or delete a file under docs/ in Phases 1 to 8. If a later phase must, add the old path to `redirect_maps` in mkdocs.yml in the same commit.
- Run before every PR: `mkdocs build --strict --clean && planning/scripts/sitemap-guard.sh && python3 planning/scripts/check-links.py && planning/scripts/style-greps.sh`.
- No emojis anywhere. Material icons only. No AI-sounding phrasing ("delve", "leverage", "it's worth noting", "unlock").
- Sentence-case headings, em dashes, house Mermaid palette, `color:#fff` on styled nodes, `<br/>` for label line breaks. These are the target style; March-era pages are converted in Phase 5.
- Keep the `copyright` string and the `extra.analytics` block in mkdocs.yml byte-identical. CI asserts the GA tag, Open Graph and JSON-LD on every build.
- Public voice. The site is not written for one organisation. See 05-url-fixes.md for the exact lines.
- Commit messages: `type: description` (docs, feat, fix, style, refactor, chore). One phase per branch and PR.
- Do not put secrets in the repo. Azure OpenAI values for Phase 7 come from env vars.
- Update STATUS.md before ending a session.

## Vocabulary used across the plan

- **Layer**: Understand, Build, Go deeper, Tools, Reference. One per page, shown in the header block and as the level tag.
- **Reading path**: the ten-page no-code route (02-restructure-plan.md section 2).
- **Build path**: Setup plus modules 1 to 9 in docs/02-agents/, each with a lab in labs/.
- **Topic ladder**: the ordered pages for one topic across layers (section 2b). "Stepping stones" in Nitin's words.
- **Header block**: the single abstract admonition under every H1 (04-page-matrix.md has the template).
- **Layer box**: the lines inside the header block that point at the hands-on and in-depth counterparts.
- **Frame**: apply the header block, tags, voice and style fixes to a page without changing its substance. **Rewrite**: change the substance. **Keep**: touch nothing but the header block.
- **Sitemap guard**: the baseline check that no live URL is dropped.
