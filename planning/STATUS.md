# Restructure status

Update this file at the end of every working session. A new session reads this first, then planning/README.md.

**Last updated:** 2026-09-02 by the planning session (no implementation started).
**Current branch for implementation:** none yet. Each phase gets its own branch `restructure/phase-N`.

| Phase | State | PR | Notes |
|---|---|---|---|
| 1 Hygiene and guards | not started | | |
| 2 Nav skeleton and tags | not started | | |
| 3 Home, AI 101, What's new | not started | | |
| 4 Header blocks and hand-offs | not started | | |
| 5 Style sweep | not started | | Confirm with Nitin: sentence-case headings (yes/no) before starting |
| 6 Reference layer | not started | | |
| 7 Azure OpenAI and C# | not started | | Needs an Azure OpenAI endpoint + key in env vars from Nitin |
| 8 Repo docs and Docker | not started | | |
| 9a Structured output | not started | | |
| 9b Memory | not started | | |
| 9c Multi-agent + agentic RAG | not started | | |

States: not started, in progress, in review, merged, blocked.

## How to resume
1. `git status` and `git log --oneline -5` to see where the last session stopped.
2. Read the phase's task list in planning/03-phase-plans.md and tick items off in the notes column here as you go.
3. Before opening the PR: `mkdocs build --strict --clean && planning/scripts/sitemap-guard.sh && python3 planning/scripts/check-links.py && planning/scripts/style-greps.sh`.
