# AI Knowledge Hub

An open reference on how modern AI systems work, from the first explanation of
what a language model is through to running an agent in production. Written for
readers and builders alike. Built with
[MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and deployed to
GitHub Pages.

**Live site**: <https://nitinksingh.com/ai-resources/>

## Two routes through it

- **The reading path** — ten pages, four to five hours, no code. What these
  systems are, how they work, and where they fail.
- **The build path** — eleven modules and eleven labs. Everything runs against a model
  on your own machine: no account, no API key, no cost.

Both start at [Choose your path](https://nitinksingh.com/ai-resources/00-start-here/).

## How the content is layered

Most topics appear at more than one depth, and each page links to its
counterparts. **Understand** is the no-code layer. **Build** is the same idea as
something you run and break. **Go deeper** is design-level depth. **Reference**
is the glossary, a vetted reading list, and primary documentation by vendor.

## Running it locally

### Option 1: Docker Compose (no local Python needed)

```bash
git clone https://github.com/nitin27may/ai-resources.git
cd ai-resources
docker compose up          # DOCS_PORT=8080 docker compose up  to use another port
```

Site available at [http://localhost:8000](http://localhost:8000) with live reload.

To stop:
```bash
docker compose down
```

### Option 2: Direct Python

```bash
git clone https://github.com/nitin27may/ai-resources.git
cd ai-resources
pip install -r requirements.txt
mkdocs serve --dev-addr=0.0.0.0:8000 --livereload
```

## Adding a page

1. Create the Markdown file in `docs/` under the right section.
2. Add it to `nav:` in `mkdocs.yml`. Files are not auto-discovered, and a file
   missing from the nav fails the strict build.
3. Give it a header block and tags — see [CLAUDE.md](CLAUDE.md).
4. Run the checks below.

**Never move, rename or delete a file under `docs/` without adding a
`redirect_maps` entry in the same commit.** Every live URL is recorded in
`planning/sitemap-baseline.txt`, and CI fails if one stops being served.

## Build and checks

```bash
mkdocs build --strict --clean -d /tmp/site

planning/scripts/sitemap-guard.sh /tmp/site          # no live URL dropped
python3 planning/scripts/check-links.py --min-inbound 2
planning/scripts/style-greps.sh                      # every count should be 0

(cd /tmp/site && python3 -m http.server 8899 &)
python3 planning/scripts/check-diagrams.py           # every diagram renders
python3 planning/scripts/check-themes.py             # light + dark, contrast >= 3:1
```

The last two need `playwright` with chromium. They exist because a strict build
passed for months while every diagram on the site rendered blank and the light
theme was unreachable — a green build says nothing about what a reader sees.

`mkdocs config` is not a real command; `mkdocs build --strict` is the config
check.

## Deployment

Pushing to `main` triggers the GitHub Actions workflow (`.github/workflows/deploy.yml`), which builds and deploys to GitHub Pages automatically. PRs run a build-only check.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Port 8000 in use | `DOCS_PORT=8080 docker compose up`, or pass `--dev-addr` to `mkdocs serve` |
| Diagrams not rendering | The fence format must stay `fence_div_format` in `mkdocs.yml`. `fence_code_format` hands the block to Material's own integration, which renders nothing. See `planning/README.md` |
| Light mode snaps back to dark | Something is forcing the palette on load. `theme.palette` listing slate first is all that dark-by-default needs |
| Strict build fails on a new file | Add it to `nav:` in `mkdocs.yml` |
| `git-revision-date` warnings | The file is not committed yet, or the clone is shallow (`git fetch --unshallow`) |

## Contributing

1. Fork the repository
2. Create a branch: `git checkout -b docs/your-topic`
3. Follow the standards in [CLAUDE.md](CLAUDE.md)
4. Run the checks above; CI runs the same ones
5. Open a pull request against `main`
