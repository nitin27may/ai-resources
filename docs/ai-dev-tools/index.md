---
title: AI Developer Tools
description: An overview of AI coding tools — from IDE assistants to agentic CLI tools and the MCP ecosystem — and how they fit together.
tags:
  - Beginner
  - GitHub Copilot
  - Claude Code
  - MCP
status: new
---

# AI Developer Tools

AI coding tools have moved from novelty to essential infrastructure. The question is no longer whether to use them, but which ones fit which tasks — and how to use them without accumulating bad habits.

The landscape breaks into three tiers, each with a different scope and mental model:

!!! info "Three-Tier Model"

    **Tier 1 — Code Completion** (:material-github: GitHub Copilot)

    Inline suggestions as you type. The AI sees your current file and nearby context, predicts your next line or block, and you accept or dismiss. Fast, low-friction, always on.

    **Tier 2 — Agentic Coding** (:material-robot: Claude Code)

    Reads your entire codebase, edits files, runs shell commands, and works autonomously toward a goal you describe. Operates over minutes, not milliseconds. Appropriate for tasks that span multiple files or require iterative refinement.

    **Tier 3 — Extensible Protocol** (:material-connection: MCP)

    The Model Context Protocol connects any tool — databases, APIs, file systems, services — to any AI host using a standard interface. Enables AI tools to pull in live context from your actual environment rather than relying solely on training data.

---

## What's in This Section

<div class="grid cards" markdown>

-   :material-github: __GitHub Copilot__

    ---

    What Copilot is, how to use it effectively in VS Code, built-in slash commands, and where it falls short.

    Beginner — Intermediate

    [:octicons-arrow-right-24: GitHub Copilot](github-copilot.md)

-   :material-github: __Copilot CLI & Extensions__

    ---

    Using Copilot in the terminal, and building Skillset or Agent extensions to connect Copilot to your own tools and services.

    Intermediate — Advanced

    [:octicons-arrow-right-24: Copilot CLI & Extensions](copilot-cli-extensions.md)

-   :material-robot: __Claude Code__

    ---

    Anthropic's agentic coding CLI — how it works, what it can do autonomously, and how to use it without losing track of what it changed.

    Beginner — Intermediate

    [:octicons-arrow-right-24: Claude Code](claude-code.md)

-   :material-robot: __Claude Code Skills & Agents__

    ---

    Building custom slash commands, reusable agent skills, and multi-agent workflows on top of Claude Code.

    Intermediate — Advanced

    [:octicons-arrow-right-24: Skills & Agents](claude-code-skills-agents.md)

-   :material-connection: __Model Context Protocol (MCP)__

    ---

    How MCP works, how to connect existing MCP servers to your AI tools, and how to build your own server to expose internal tools.

    Advanced

    [:octicons-arrow-right-24: MCP](mcp.md)

</div>

---

## Next Steps

- [GitHub Copilot](github-copilot.md) — start here if you're new to AI coding tools
- [Claude Code](claude-code.md) — start here if you want agentic, autonomous coding assistance
- [Model Context Protocol](mcp.md) — start here if you want to connect AI tools to your internal systems
