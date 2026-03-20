# AI Knowledge Hub

A centralized learning resource covering AI concepts, patterns, and tools — from fundamentals to enterprise architecture. Built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and deployed to GitHub Pages.

**Live site**: [https://nitin27may.github.io/ai-resources](https://nitin27may.github.io/ai-resources)

## Topics Covered

- AI fundamentals, foundation models, and prompting techniques
- RAG & Knowledge Systems (embeddings, chunking, vector databases, GraphRAG, evaluation)
- AI agents and agentic patterns
- AI developer tools (GitHub Copilot, Claude Code, MCP)
- Enterprise and design patterns for AI systems
- Responsible AI and safety

## Local Development

### Option 1: Docker Compose (recommended — no Python required)

```bash
git clone https://github.com/nitin27may/ai-resources.git
cd ai-resources
docker-compose up
```

Site available at [http://localhost:8000](http://localhost:8000) with live reload.

To stop:
```bash
docker-compose down
```

### Option 2: VS Code Dev Container

1. Clone the repo and open in VS Code:
   ```bash
   git clone https://github.com/nitin27may/ai-resources.git
   code ai-resources
   ```
2. When prompted, click **Reopen in Container** (or use Command Palette: `Dev Containers: Reopen in Container`)
3. The container builds automatically, installs dependencies, and starts the dev server on port 8000

The dev container includes Python 3.12, all MkDocs plugins, WeasyPrint for PDF export, and pre-configured VS Code extensions for Markdown and Mermaid.

### Option 3: Direct Python

```bash
git clone https://github.com/nitin27may/ai-resources.git
cd ai-resources
pip install -r requirements.txt
mkdocs serve --dev-addr=0.0.0.0:8000 --livereload
```

> PDF export (WeasyPrint) requires system libraries. Use Docker if you are not on Linux.

## Adding Documentation

1. Create a Markdown file in `docs/` under the appropriate section
2. Add it to the `nav:` section in `mkdocs.yml` — files are not auto-discovered
3. The dev server reloads automatically; no restart needed

## Build

```bash
mkdocs build
# Static output in ./site/
```

To validate config without building:
```bash
mkdocs config
```

## Deployment

Pushing to `main` triggers the GitHub Actions workflow (`.github/workflows/deploy.yml`), which builds and deploys to GitHub Pages automatically. PRs run a build-only check.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Port 8000 in use | Stop the other service, or change the port in `devcontainer.json` |
| Dev container won't start | Ensure Docker is running; try `Dev Containers: Rebuild Container` |
| Mermaid diagrams not rendering | Verify `pymdownx.superfences` is configured in `mkdocs.yml` |
| PDF export failing | Use Docker (WeasyPrint needs system libs not available on macOS/Windows) |
| `git-revision-date` errors | Ensure the repo has git history (`git fetch --unshallow` in shallow clones) |

## Contributing

1. Fork the repository
2. Create a branch: `git checkout -b docs/your-topic`
3. Make changes following the documentation standards in `CLAUDE.md`
4. Submit a pull request against `main`
