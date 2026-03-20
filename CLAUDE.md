# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **MkDocs Material** documentation site — the "AI Knowledge Hub" — a centralized learning resource covering AI concepts, patterns, and tools for multiple audiences. It is deployed to GitHub Pages via GitHub Actions.

## Commands

### Local Development

**Recommended: Docker Compose (no local Python required)**
```bash
docker-compose up
# Site available at http://localhost:8000 with live reload
```

**Or VS Code Dev Container**: Open in VS Code and select "Reopen in Container" — dependencies auto-install and port 8000 is forwarded.

**Direct Python (if dependencies installed)**
```bash
mkdocs serve --dev-addr=0.0.0.0:8000 --livereload
```

### Build

```bash
mkdocs build
# Output: ./site/ (static HTML)
```

### Validate Config

```bash
mkdocs config
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

PDF export (WeasyPrint) requires system libraries — use Docker if not on Linux.

## Architecture

### Content Structure

All documentation lives in `docs/`. The nav is defined in `mkdocs.yml` — adding a file does not automatically add it to the nav.

```
docs/
├── index.md                    # Landing page (hides nav/toc via frontmatter)
├── getting-started/            # Beginner entry point and learning paths
├── concepts/                   # Deep-dive AI topics (8 modules)
├── rag/                        # RAG & Knowledge Systems (fundamentals, embeddings, chunking, vector DBs, GraphRAG, evaluation)
├── ai-dev-tools/               # GitHub Copilot, Claude Code, MCP reference
├── patterns/                   # Design, enterprise, and code quality patterns
├── glossary/                   # AI terms
├── tools-and-frameworks/       # Framework reference
├── references/                 # Curated external links
└── whats-new/                  # Latest updates
```

`samples/` contains C# examples illustrating agent patterns: `1-basicagent.cs`, `2-agentasbackend.cs`, `3-multiturn.cs`, `4-functiontool.cs`, `mcpuse.cs`, `workflow.cs`.

`includes/abbreviations.md` defines site-wide abbreviation tooltips (e.g. RAG, MCP, LLM). Auto-appended to every page via `pymdownx.snippets`. Add new terms here to make them available everywhere.

### Theme and Overrides

- **Theme**: MkDocs Material; custom CSS in `overrides/assets/stylesheets/`, custom JS in `overrides/assets/javascripts/`
- **`overrides/main.html`**: Extends base template. Forces dark mode as default (slate scheme) unless user has explicitly chosen light. Loads `mermaid-fullscreen.js` for fullscreen diagram support.
- **Key plugins**: `search`, `tags`, `git-revision-date-localized`, `glightbox`, `minify`, `macros`, `awesome-pages`, `redirects`
- **Diagrams**: Mermaid via `pymdownx.superfences` — no separate plugin needed. `mermaid-custom.css` in overrides controls diagram styling.
- **PDF export**: WeasyPrint, enabled when `ENABLE_PDF_EXPORT=1` (set in Dockerfiles)

### Deployment

GitHub Actions (`.github/workflows/deploy.yml`) builds and deploys to GitHub Pages on push to `main`. PRs trigger a build-only check.

## Documentation Standards

### No Emojis

Never use Unicode emojis anywhere. Use MkDocs Material icons instead:
- `:material-robot:`, `:fontawesome-solid-brain:`, etc.
- Use bold text and headings for emphasis instead

### Mermaid Diagram Colors

Use these theme-compatible hex values (work in light and dark modes):

| Use | Color |
|-----|-------|
| Main flows / primary | `#0d9488` (teal) |
| Success paths | `#16a34a` (green) |
| Processing/logic | `#0284c7` (sky blue) |
| Warnings/important | `#d97706` (amber) |
| Data/storage | `#14b8a6` (teal-light) |
| Error/danger | `#dc2626` (red) |

Always set `color:#fff` on styled nodes.

### Admonitions

```markdown
!!! note
    ...
!!! warning
    ...
!!! tip
    ...
```

Types: `note`, `abstract`, `info`, `tip`, `success`, `question`, `warning`, `failure`, `danger`, `bug`, `example`, `quote`

### Grid Cards

```markdown
<div class="grid cards" markdown>

-   __Card Title__

    Description (1-2 lines).

    [View →](path/to/page.md)

</div>
```

No emojis in card titles. Use `__bold__` for titles.

### Landing Page Frontmatter

```yaml
---
hide:
  - navigation
  - toc
---
```

### Navigation

Keep top-level nav to 3-5 items max. New pages must be explicitly added to the `nav:` section in `mkdocs.yml`.

### Commit Messages

Format: `type: brief description`

Types: `docs:`, `feat:`, `fix:`, `style:`, `refactor:`, `chore:`
