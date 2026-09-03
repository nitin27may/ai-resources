---
title: GitHub Copilot
description: Copilot as it exists in 2026 — inline completion, chat, agent mode, the standalone CLI, and MCP as the extensibility story.
  - GitHub Copilot
tags:
  - Tools
  - Copilot
---

# GitHub Copilot

!!! abstract "Tools · 30 min · no code"
    **Before this:** [Developer tools](index.md)  ·  **After this:** [Claude Code](claude-code.md)

!!! abstract
    Copilot spans inline completion, a chat pane, an agent mode that edits across
    files, a standalone terminal CLI, and a coding agent that opens pull
    requests. This page covers what each is for, and is explicit about the two
    products that were retired — because a lot of published material still
    teaches them.

**Verified as of 2026-08-21.**

!!! warning "Two things this page used to cover no longer exist"
    **`gh copilot suggest` / `gh copilot explain`** — the GitHub CLI extension is
    **retired**. GitHub's own documentation says so plainly. It was replaced by a
    standalone GitHub Copilot CLI (the `copilot` command).

    **GitHub App-based Copilot Extensions** — the `@mention` extension platform
    was deprecated in September 2025 and **shut down on 10 November 2025**,
    replaced by MCP servers.

    If you find a tutorial building a Copilot Extension as a GitHub App with
    webhooks and SSE streaming, it is describing a platform that no longer runs.
    Extensibility is now MCP — see [Model Context Protocol](mcp.md).

## The surfaces

| Surface | What it does | When to reach for it |
|---|---|---|
| **Inline completion** | Completes the line or block you are typing | Constant, ambient. Boilerplate, obvious next lines |
| **Copilot Chat** | Conversational, workspace-aware, in a side pane | Explaining unfamiliar code, generating a scaffold |
| **Agent mode** | Multi-file edits, runs commands, iterates | A change that spans files |
| **Copilot CLI** | The `copilot` command in a terminal | Shell tasks, away from an editor |
| **Coding agent** | Runs on GitHub, opens exactly one PR per task | Well-specified work you can review async |
| **Code review** | Reviews a PR diff | A second pass before a human review |

Inline completion is the one people mean when they say "Copilot", and it is the
least interesting. Agent mode and the coding agent are where the behaviour is
genuinely different — they run a loop, which is the subject of
[the agent loop](../02-agents/the-agent-loop.md).

## Getting good results from completion

**Open the files that matter.** Completion draws on your open tabs. If you want
it to follow a pattern, have the file containing that pattern open.

**Write the signature and the docstring first.** A named function with a stated
contract produces far better completions than an empty body.

**Name things precisely.** `calculateTaxForInvoice` gets you a better completion
than `calc`. The name is most of the prompt.

**Reject fast.** Reading a wrong suggestion carefully costs more than dismissing
it and typing. The skill is in fast rejection, not careful evaluation.

## Where it will let you down

**It is fluent about APIs that do not exist.** Completion is pattern-matching
over plausible code. A method that *should* exist on a library will be suggested
with total confidence. Verify anything you have not used before.

**It reproduces your existing mistakes.** It learns your file's conventions,
including the bad ones. A codebase with a bad pattern gets more of it.

**It is weakest exactly where you need it most.** Novel logic, unusual
constraints, an unfamiliar domain — the cases where you would most value help are
the cases with the least pattern to draw on.

**Agent mode's confidence is uncalibrated.** It will report success on a change
that does not compile. Read the diff.

## Extensibility is MCP now

Since the Extensions shutdown, connecting Copilot to your own tools and data
means writing an **MCP server**. That is a net improvement: the same server works
in Claude Code, Cursor and anything else that speaks the protocol, instead of
being locked to one host.

MCP is GA in VS Code, JetBrains, Eclipse and Xcode. See
[Model Context Protocol](mcp.md) for how to build one.

## The honest picture on productivity

Copilot-style tooling is usually sold with a large speedup number. The best
available evidence is more equivocal, and worth knowing before you commit a team
to a metric.

METR — an independent evaluator, not a vendor — ran a randomised controlled trial
with 16 experienced open-source developers on 246 real issues in their own
repositories. Developers using AI tools took **19% longer**. They had predicted a
24% speedup beforehand, and afterwards *still believed they had been sped up by
20%*.

A larger 2026 follow-up (57 developers, 800+ tasks, agentic tools rather than
autocomplete) moved the point estimate toward neutral — −4% for new participants
— with confidence intervals crossing zero, and METR themselves call it *"only very
weak evidence"* because of severe selection effects.

The defensible reading in 2026: **there is no credible published evidence that
these tools make experienced developers measurably faster on real work in their
own codebases**, and the perception gap is roughly 40 points wide in the
flattering direction. That does not mean they are useless — it means *your* sense
of speedup is not evidence, and you should measure if the answer matters.

## References

- [Copilot documentation](https://docs.github.com/en/copilot)
- [Copilot coding agent](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent) — 59-minute session cap, one PR per task
- [Measuring the impact of early-2025 AI on experienced developers](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) — METR's RCT
- [Uplift update](https://metr.org/blog/2026-02-24-uplift-update/) — the larger 2026 follow-up

## Next

[Claude Code](claude-code.md) — the other agentic CLI, and a different set of
trade-offs.
