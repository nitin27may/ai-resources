# Restructure status

Update this file at the end of every working session. A new session reads this first, then planning/README.md.

**Last updated:** 2026-09-02, phases 1-5 merged into the branch.
**Branch:** `restructure/layered-hub`. One branch, one PR, one commit per phase.

| Phase | State | PR | Notes |
|---|---|---|---|
| 1 Hygiene and guards | done | b638a41 | edit_uri, pinned deps, CI URL guard, dead hook removed |
| 2 Nav skeleton and tags | done | daeabdc^ | six tabs, Choose your path, tags.md, layer+topic tags on 44 pages |
| 3 Home, AI 101, What's new | done | daeabdc | org voice gone, model table to capability tiers, 3 dated entries |
| 4 Header blocks and hand-offs | done | 3afbb9c | 44 header blocks, module 1 entry + module 9 exit, inbound floor of 2 |
| 5 Style sweep | done | 65a9930 | 297 headings, palette, dashes. Found and fixed: blank Mermaid sitewide, unreachable light theme, 2 pinned light diagrams, teal contrast |
| 6 Reference layer | done | 0d22cfc | Official sources rewritten with NVIDIA; 61 redirects fixed; 23 Go deeper sections; all 182 external links resolve |
| 7 Azure OpenAI and C# | partly done | | C# half done: all 6 samples compile on .NET 10 (mcpuse.cs never did before), readme rewritten, samples linked from the site. **Still blocked:** the Azure OpenAI tab in Setup and labs needs an endpoint + key from Nitin in env vars |
| 8 Repo docs and Docker | done | 45553ff | CLAUDE.md rewritten, copilot-instructions is a pointer, one Dockerfile (non-root, healthcheck), container verified healthy |
| 9a Structured output | not started | | |
| 9b Memory | not started | | |
| 9c Multi-agent + agentic RAG | not started | | |

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

## Known debt, recorded not hidden

- **The six C# samples target a pre-1.0 Agent Framework preview.** They compile,
  but the current packages changed the Azure surface enough that all six fail
  against them (`Azure.AI.Projects.OpenAI` gone, `AIProjectClient.CreateAIAgent`
  gone, `AgentThread` moved). Porting is real work, not a version bump.
  `samples/readme.md` states this plainly.
- **The Azure OpenAI tab for Setup and the labs is not written.** It needs one
  live test against a real endpoint to confirm the auth header shape on the
  `/openai/v1` path. Needs an endpoint and key from Nitin, in env vars only.

## Deferred deliberately

- **'## References' -> 'Go deeper' with a reason per link** moved from phase 5
  into phase 6, where those same links are being resolved and updated anyway.
  23 pages still have a bare References heading.
- **Page merges** (folding concepts/retrieval-and-data into rag/, for example)
  wait for Search Console data, then need a `redirect_maps` entry each.
