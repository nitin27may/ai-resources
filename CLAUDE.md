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
├── concepts/                   # Deep-dive AI topics (8 modules)
├── getting-started/            # Beginner entry point
├── patterns/                   # Design, enterprise, and code quality patterns
├── glossary/                   # 60+ AI terms
├── tools-and-frameworks/       # Framework reference
├── references/                 # Curated external links
└── whats-new/                  # Latest updates
```

`samples/` contains C# code examples illustrating agent patterns (basic agent, multi-turn, function tools, MCP usage, workflow).

### Theme and Plugins

- **Theme**: MkDocs Material with custom CSS in `overrides/assets/stylesheets/`
- **Key plugins**: `search`, `tags`, `git-revision-date-localized`, `glightbox`, `minify`, `macros`, `awesome-pages`, `redirects`
- **Diagrams**: Mermaid via `pymdownx.superfences` — no separate plugin needed
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
| Main flows | `#3b82f6` (blue) |
| Success paths | `#10b981` (green) |
| Processing/logic | `#8b5cf6` (purple) |
| Warnings/important | `#f97316` (orange) |
| Data/storage | `#14b8a6` (teal) |
| User interactions | `#ec4899` (pink) |

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
