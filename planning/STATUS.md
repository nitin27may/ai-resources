# Restructure status

Update this file at the end of every working session. A new session reads this first, then planning/README.md.

**Last updated:** 2026-09-03. **The plan is complete and merged.** PRs #19
(restructure), #20 (C# port to Agent Framework 1.x) and #21 (samples repointed
to Azure OpenAI) are all merged and deployed.
**Branch:** `restructure/layered-hub`. One branch, one PR, one commit per phase.
**CI:** green on PR #19 — strict build, tag assertions, sitemap guard and link check all pass.

**What is left:** nothing on the plan. Remaining optional work is merging the
overlapping concept pages, which waits on Search Console data, and a computer-use
page once there is something durable to write.

| Phase | State | PR | Notes |
|---|---|---|---|
| 1 Hygiene and guards | done | b638a41 | edit_uri, pinned deps, CI URL guard, dead hook removed |
| 2 Nav skeleton and tags | done | daeabdc^ | six tabs, Choose your path, tags.md, layer+topic tags on 44 pages |
| 3 Home, AI 101, What's new | done | daeabdc | org voice gone, model table to capability tiers, 3 dated entries |
| 4 Header blocks and hand-offs | done | 3afbb9c | 44 header blocks, module 1 entry + module 9 exit, inbound floor of 2 |
| 5 Style sweep | done | 65a9930 | 297 headings, palette, dashes. Found and fixed: blank Mermaid sitewide, unreachable light theme, 2 pinned light diagrams, teal contrast |
| 6 Reference layer | done | 0d22cfc | Official sources rewritten with NVIDIA; 61 redirects fixed; 23 Go deeper sections; all 182 external links resolve |
| 7 Azure OpenAI and C# | done | b612286 | All 13 labs verified against a live Azure OpenAI deployment, env vars only. Setup and labs README carry a three-provider tab. All 6 C# samples compile on .NET 10 |
| 8 Repo docs and Docker | done | 45553ff | CLAUDE.md rewritten, copilot-instructions is a pointer, one Dockerfile (non-root, healthcheck), container verified healthy |
| 9a Structured output | done | 89524cb | Module 2 + lab. Measured on two providers: schema holds 6/6 where prompt-only and JSON mode drop to 0/6 |
| 9b Memory | done | 2ec9327 | Module 6 + lab. Poisoning reproduced identically on both providers |
| 9c Multi-agent | done | 2ec9327 | Module 12 + lab. Split cost 2.6x tokens AND lost information the single agent had |

States: not started, in progress, in review, merged, blocked.

## How to resume
1. `git status` and `git log --oneline -5` to see where the last session stopped.
2. Read the phase's task list in planning/03-phase-plans.md and tick items off in the notes column here as you go.
3. Before opening the PR, all five checks:

```bash
mkdocs build --strict --clean -d /tmp/site
planning/scripts/sitemap-guard.sh /tmp/site
python3 planning/scripts/check-links.py --min-inbound 2
planning/scripts/style-greps.sh
(cd /tmp/site && python3 -m http.server 8899 &)
python3 planning/scripts/check-diagrams.py     # every diagram renders
python3 planning/scripts/check-themes.py       # light + dark, contrast >= 3:1
```

The last two need playwright with chromium. They exist because a `--strict`
build passed for months while every diagram on the site rendered blank and the
light theme was unreachable. Building is not the same as rendering.

## The build path as it now stands

Thirteen modules, thirteen labs, all verified against both a local Ollama model
and Azure OpenAI on 2026-09-03:

0 Setup · 1 Tool calling · 2 Structured output · 3 The agent loop · 4 The
harness · 5 Context engineering · 6 Memory · 7 Retrieval · 8 Evaluation ·
9 Observability · 10 Safety · 11 Production · 12 Multi-agent

## Known debt, recorded not hidden

- ~~The six C# samples target a pre-1.0 Agent Framework preview.~~ **Done
  2026-09-03** (PR #20, #21). Ported to Agent Framework 1.x, then repointed from
  Foundry server-side agents to Azure OpenAI so they can actually be *run* rather
  than only compiled — they now use the same three environment variables as the
  Python labs, and all six were run end to end. `samples/readme.md` documents the
  pre-1.0 renames and the two type clashes.
- **Renumbering the build modules churns cross-references.** It happened twice
  in one session. Nav labels and prose carry the numbers; file paths do not, so
  no URL is at risk, but budget for a sitewide pass and check
  `planning/scripts/style-greps.sh` for the module-count guard.

## Deferred deliberately

- **Page merges** (folding concepts/retrieval-and-data into rag/, for example)
  wait for Search Console data, then need a `redirect_maps` entry each.
