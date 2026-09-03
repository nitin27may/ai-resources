---
tags:
  - Reference
description: What changed on this site, newest first.
---

# What's new

!!! abstract "Reference · 5 min · no code"
    What changed on this site, newest first.

Changes to the AI Knowledge Hub, newest first.

---

## September 2026 — one ramp, two paths

The site had grown two halves that did not meet: a set of concept pages written
in March, and a hands-on agent path added in August. Nine top-level tabs held
them side by side, and nothing routed a reader from one to the other.

It is now organised as four layers, and most topics appear at more than one of
them on purpose.

- **[Choose your path](../00-start-here/index.md)** is the new entry point. Two
  routes: a ten-page reading path with no code, and the build path with ten labs.
- **Six tabs instead of nine**, ordered as a ramp: Start here, Understand,
  Build, Go deeper, Reference.
- **The reading path** puts retrieval before agents, because giving a model your
  data is a smaller step than letting it act, and safety after agents, because
  the failure that matters arrives through a tool result.
- **Every page is tagged** by layer and topic, and
  [Browse by tag](../tags.md) shows a single topic across every depth.
- **No URL changed.** Every page that was reachable before is reachable at the
  same address.

## August 2026 — the build path

Ten modules, each ending in code that runs against a model on your own machine.
No account, no API key, no cost.

- **[The build path](../00-start-here/the-path.md)** and
  [Setup](../00-start-here/setup.md), covering four hardware tiers.
- **Nine modules**: [tool calling](../02-agents/tool-calling.md),
  [the agent loop](../02-agents/the-agent-loop.md),
  [the harness](../02-agents/the-harness.md),
  [context engineering](../02-agents/context-engineering.md),
  [retrieval](../02-agents/retrieval.md),
  [evaluation](../02-agents/evaluation.md),
  [observability](../02-agents/observability.md),
  [safety](../02-agents/safety.md) and
  [production](../02-agents/production.md).
- **Ten labs** in the repository, standard library only, each one demonstrating
  the specific failure its module is about.
- **[Resources](../reference/resources.md)** — a ranked reading list with a
  reason to trust each item, and an explicit list of what to avoid and why.
- **Corrections.** The Model Context Protocol page was rewritten against the
  2026-07-28 revision. The Copilot CLI and Extensions page was removed: both
  products it documented were retired in late 2025. The frameworks page was
  rebuilt around Microsoft Agent Framework, which superseded Semantic Kernel and
  AutoGen in April 2026.

## March 2026 — launch

The site went live with the concept, pattern and reference sections: AI 101,
eight concept pages, [RAG and knowledge systems](../rag/index.md) in six parts,
[architecture patterns](../patterns/index.md),
[developer tools](../ai-dev-tools/index.md), the
[glossary](../glossary/index.md) and
[official sources](../references/index.md).

The original "Learning Paths" page offered four routes by role. It was replaced
in August by the single build path, and in September by the two paths on
[Choose your path](../00-start-here/index.md).

---

Corrections and additions are welcome: open an issue or a pull request on
[GitHub](https://github.com/nitin27may/ai-resources).
