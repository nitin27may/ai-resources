# CLAUDE.md

Guidance for Claude Code (claude.ai/code) when working in this repository.

## Active restructure (2026-09)

A layered restructure is in progress. **Read `planning/STATUS.md` and
`planning/README.md` before changing anything under `docs/` or `mkdocs.yml`.**
The planning folder holds the audit, the target structure, per-phase task lists,
the per-page matrix, the URL fix list and the check scripts.

Hard rule until it completes: **no file under `docs/` moves, is renamed, or is
deleted without a `redirect_maps` entry in the same commit.** Every current URL
is listed in `planning/sitemap-baseline.txt` and CI fails if one stops being
served.

## Project overview

An **MkDocs Material** site — the "AI Knowledge Hub" — published at
<https://nitinksingh.com/ai-resources/> and deployed to GitHub Pages by GitHub
Actions on push to `main`.

It teaches modern AI from first principles through to running an agent in
production, for **both non-developers and developers**. Concepts are
vendor-agnostic; code samples use OpenAI-compatible APIs with Azure OpenAI as a
configuration change. It is not a certification guide.

## The four layers

Most topics appear more than once, at different depths. That is deliberate, and
it is the organising idea of the whole site.

| Layer | Who | Code | Where |
|---|---|---|---|
| **Understand** | Everyone, no prerequisites | None | `concepts/`, `getting-started/`, `patterns/enterprise-patterns.md` |
| **Build** | Developers | Every page ends in a lab | `00-start-here/`, `02-agents/`, `labs/` |
| **Go deeper** | Developers and architects | Some | `rag/`, `patterns/`, `tools-and-frameworks/` |
| **Tools** | Anyone using AI coding tools | Config and commands | `ai-dev-tools/` |
| **Reference** | Everyone | None | `glossary/`, `reference/`, `references/`, `whats-new/` |

Two routes run through those layers: a **reading path** (ten pages, no code) and
the **build path** (ten modules, ten labs). Both start at
`docs/00-start-here/index.md`. `planning/02-restructure-plan.md` section 2b has
the per-topic ladders — when you add a page, place it on one.

A page belongs to exactly one layer, declares it in its header block, and links
to its counterparts at other depths. Duplication across layers is fine.
Duplication within a layer is not.

## Commands

```bash
# Serve locally with live reload
docker compose up                      # http://localhost:8000 (DOCS_PORT to change)
mkdocs serve --dev-addr=0.0.0.0:8000   # or directly, if deps are installed

# Build (this is also the config check -- `mkdocs config` is not a command)
mkdocs build --strict --clean -d /tmp/site

# Install
pip install -r requirements.txt
```

### The five checks before any commit

```bash
mkdocs build --strict --clean -d /tmp/site
planning/scripts/sitemap-guard.sh /tmp/site        # no live URL dropped
python3 planning/scripts/check-links.py --min-inbound 2
planning/scripts/style-greps.sh                    # all counts 0
(cd /tmp/site && python3 -m http.server 8899 &)
python3 planning/scripts/check-diagrams.py         # every diagram renders
python3 planning/scripts/check-themes.py           # light + dark, contrast >= 3:1
```

The last two need playwright with chromium. **They exist because a `--strict`
build passed for months while every Mermaid diagram on the site rendered blank
and the light theme was unreachable.** Building is not rendering.

## Content structure

Everything published lives in `docs/`. The nav is explicit in `mkdocs.yml`:
adding a file does not add it to the nav, and a file not in the nav fails
`--strict`.

```
docs/
├── index.md              # landing page; hides nav and toc
├── 00-start-here/        # Choose your path, the build path, setup
├── getting-started/      # AI 101
├── concepts/             # the Understand layer
├── 02-agents/            # the nine build modules
├── rag/                  # retrieval in depth
├── patterns/             # architecture patterns
├── ai-dev-tools/         # Copilot, Claude Code, MCP
├── tools-and-frameworks/ # framework and platform landscape
├── glossary/             # 100+ terms
├── reference/            # Resources: the vetted, ranked shelf
├── references/           # Official sources: primary docs by vendor
├── whats-new/            # dated changelog
└── tags.md               # tag index
```

`labs/` holds the ten Python labs for the build path — standard library only,
talking to any OpenAI-compatible endpoint. `samples/` holds C# examples.
`planning/` is the restructure brief and is not published.

`includes/abbreviations.md` is auto-appended to every page via
`pymdownx.snippets`; add a term there to get tooltips everywhere.

## Documentation standards

### Header block

Every page except `index.md` and `tags.md` opens with exactly one of these,
directly under the H1:

```markdown
!!! abstract "Understand · 30 min · no code"
    **Before this:** [How models work](...)  ·  **After this:** [What an agent is](...)
    **Hands-on version:** [5 Retrieval](...)  ·  **In depth:** [Retrieval in depth](...)
```

Layer is one of Start here, Understand, Build, Go deeper, Tools, Reference. Code
is one of `no code`, `code optional`, `hands-on`. Omit any line you have nothing
for. Build pages label the third line **Overview version** instead.

### Tags

One layer tag and one to three topic tags per page. Topics: Agents, Retrieval,
Safety, Evaluation, Prompting, Models, Training, Patterns, Operations, MCP,
Claude Code, Copilot, Azure, Reference, Home.

### Voice

- Public. The site is not written for one organisation. No "our organization",
  no "co-op students", no "reach out to the team".
- Sentence case headings. Product names keep their capitals.
- Em dashes, never ` -- `.
- No emojis anywhere. Material icons only (`:material-robot:`).
- No AI-sounding phrasing: "delve", "leverage", "it's worth noting", "unlock".
- Date any page that names a product, model or spec: `**Verified as of YYYY-MM-DD.**`
- **No model-name tables.** They rot within a season. Describe capability tiers
  and link the vendor's live model page.
- End pages with **Go deeper**, and give every link a reason. A bare list of URLs
  is not a recommendation.

### Mermaid

Fences use `fence_div_format`, **not** the `fence_code_format` Material's docs
show. See `planning/README.md` — the code format hands the block to Material's
own integration, which silently renders nothing. Do not "fix" it back.

| Use | Color | White-text contrast |
|-----|-------|---------------------|
| Main flows / primary | `#0d9488` | 3.74:1 |
| Success paths | `#16a34a` | 3.30:1 |
| Processing / logic | `#0284c7` | 4.10:1 |
| Warnings / important | `#d97706` | 3.19:1 |
| Data / storage | `#0f766e` | 5.47:1 |
| Error / danger | `#dc2626` | 4.83:1 |

Always `color:#fff` on styled nodes. Use `<br/>` for line breaks, never `\n`.
Never pin a Mermaid `theme` in a diagram — it overrides the page's light/dark
scheme and makes the labels invisible in one of them. `#14b8a6` is a stroke
colour only: white text on it measures 2.49:1, under the 3:1 bar.

### Admonitions and cards

Types: `note`, `abstract`, `info`, `tip`, `success`, `question`, `warning`,
`failure`, `danger`, `bug`, `example`, `quote`.

```markdown
<div class="grid cards" markdown>

-   __Card title__

    One or two lines.

    [:octicons-arrow-right-24: Link](path/to/page.md)

</div>
```

## Theme and overrides

- Custom CSS in `overrides/assets/stylesheets/`, JS in `overrides/assets/javascripts/`.
- `overrides/main.html` adds Open Graph, Twitter and JSON-LD tags from the
  template rather than Material's `social` plugin, which needs cairo system
  libraries and would make CI fail for reasons unrelated to content. **CI asserts
  all three are present in the built output.**
- `overrides/assets/javascripts/mermaid-init.js` owns diagram rendering.
- Dark is the default because `theme.palette` lists slate first. Do not add a
  script to force it — the last one made light mode unreachable.
- Plugins actually enabled: `search`, `tags`, `redirects`,
  `git-revision-date-localized`, `glightbox`. `requirements.txt` lists only what
  is enabled; do not add a package without enabling it.

## Deployment

Push to `main` runs `.github/workflows/deploy.yml`: strict build, then assertions
for the analytics tag, Open Graph and JSON-LD, then the sitemap guard and link
check, then deploy to GitHub Pages. Pull requests run everything except deploy.

Never put secrets in the repo. The Google Analytics measurement ID in
`mkdocs.yml` is a public identifier served in every page, not a secret.

## Commit messages

`type: brief description` — `docs:`, `feat:`, `fix:`, `style:`, `refactor:`,
`chore:`. Explain why in the body, not just what.
