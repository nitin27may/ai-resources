---
title: Claude Code Skills & Agents
description: How to create custom slash command skills, use subagents for parallel work, configure hooks, and integrate MCP with Claude Code.
tags:
  - Intermediate
  - Claude Code
status: new
---

# Claude Code Skills & Agents

!!! abstract
    Beyond basic prompting, Claude Code supports skills (custom slash commands), subagents for parallel and isolated work, hooks that fire on tool events, and MCP server integration. This page covers each mechanism, when to use it, and how to configure it.

## Skills (Slash Commands)

Skills are Markdown files that expand into full prompts when invoked with `/skill-name`. They let you encode repeatable tasks — code review, commit message generation, ADR writing — as first-class commands rather than prompts you retype from memory.

**Locations:**

- `.claude/skills/` — project-scoped skills, checked into source control and shared with the team
- `~/.claude/skills/` — user-scoped skills, available in every project

### Anatomy of a Skill File

A skill file is a Markdown file with optional YAML frontmatter. The frontmatter declares metadata; the body is the prompt that gets injected when the skill is invoked.

```markdown
---
name: commit
description: Generate a conventional commit message for staged changes
---

Review the staged git changes and generate a conventional commit message
following the format: `type(scope): description`.

Use these types: feat, fix, docs, style, refactor, test, chore.

Keep the subject line under 72 characters. If the changes span multiple
concerns or are complex, add a body paragraph explaining the reasoning
behind the change — not what changed, but why.
```

Invoke it with:

```
/commit
```

### More Example Skills

**`/review`** — structured code review checklist:

```markdown
---
name: review
description: Run a structured code review on the current changes
---

Review the staged or recently edited code against these criteria:

1. Correctness — does the logic match the intended behavior?
2. Error handling — are all error paths covered?
3. Security — SQL injection, input validation, secrets in code
4. Performance — N+1 queries, missing indexes, unnecessary allocations
5. Test coverage — are the new code paths tested?

Output findings grouped by severity: Critical, Major, Minor, Suggestion.
```

**`/document`** — generate docstrings for a file:

```markdown
---
name: document
description: Generate XML doc comments for all public members in the specified file
---

Read the file provided and generate complete XML documentation comments for
every public class, method, property, and constructor. Follow Microsoft XML
documentation conventions. Include <summary>, <param>, <returns>, and
<exception> tags where applicable. Write the summary as a complete sentence.
```

**`/adr`** — architecture decision record:

```markdown
---
name: adr
description: Draft an Architecture Decision Record for a technical decision
---

Draft an Architecture Decision Record (ADR) using this structure:

# ADR-NNN: [Title]

## Status
Proposed

## Context
[What is the situation that forces a decision?]

## Decision
[What is the decision made?]

## Consequences
[What are the positive and negative outcomes?]

Ask me for the title and context before drafting if not provided.
```

### Skills vs CLAUDE.md

| Mechanism | When It Applies | Best For |
|---|---|---|
| `CLAUDE.md` | Every session, automatically | Always-on context: conventions, build commands, project overview |
| Skills | Only when explicitly invoked | On-demand tasks you run occasionally |

Put recurring conventions and constraints in `CLAUDE.md`. Put structured task templates in skills.

## Subagents

The Agent tool lets Claude Code spawn specialized subprocess agents. Each subagent runs in its own context, which keeps large search results or experimental work isolated from the main session's context window.

### Built-in Subagent Types

| Type | Purpose | When to Use |
|---|---|---|
| General purpose | Complex multi-step research and tasks | Default for anything not covered by a specialized type |
| Explore | Fast codebase exploration — file patterns, code search | When you need to find files or grep for patterns quickly |
| Plan | Software architecture planning | Before implementing a complex feature — get a plan first |
| claude-code-guide | Questions about Claude Code itself | Meta-questions about tool behavior, configuration, capabilities |

### When to Use Subagents

**Parallel independent research.** If a task requires exploring multiple separate parts of the codebase, running subagents in parallel is faster than sequential exploration in the main thread. For example: simultaneously searching the API controllers, the data access layer, and the test suite for usages of a type being renamed.

**Context window protection.** Large search results — full file listings, grep output across hundreds of files — can fill the main context window quickly. Running that search in a subagent returns only the summary, leaving the main context clean.

**Isolated experimentation.** Worktree-isolated subagents (see below) let the agent make changes on a copy of the repo without touching your working tree.

### Foreground vs Background

**Foreground (default):** The main agent waits for the subagent to complete before continuing. Use this when the subagent's result informs the next step — for example, when you need the search results before writing code.

**Background (`run_in_background: true`):** The main agent continues without waiting. Use this for genuinely independent long-running tasks — indexing, analysis, or tasks whose output doesn't affect the current work. You receive a notification when the background agent completes.

Don't default to background. If the result will influence the next action, run foreground — background saves time only when the two workstreams are truly independent.

### Worktree Isolation

Setting `isolation: "worktree"` causes Claude Code to create a temporary git worktree before running the subagent. The agent works on that copy of the repository, not your working tree.

This is safe for exploratory or experimental changes: if the subagent produces useful output, you can merge it back; if not, the worktree is discarded. Temporary worktrees are automatically cleaned up if the agent makes no changes.

Use worktree isolation when:

- Testing a proposed refactor before committing to it
- Running destructive operations (file reorganization, large-scale renaming) that you want to review before applying
- Giving an agent write access to the repo without risking your in-progress work

## Hooks

Hooks are shell commands configured in `settings.json` that Claude Code runs automatically in response to tool events. They let you enforce workflows without relying on the agent to remember to run them.

### Hook Types

| Hook | Fires When |
|---|---|
| `PreToolUse` | Before Claude executes a tool — can be used to gate or log |
| `PostToolUse` | After a tool completes — most common; use for lint, test, formatting |
| `Stop` | When Claude finishes responding — useful for notifications or cleanup |

### Configuration

Hooks live in `settings.json`, either globally at `~/.claude/settings.json` or project-scoped at `.claude/settings.json`.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npm run lint --quiet"
          }
        ]
      },
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npm test -- --passWithNoTests --silent"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code finished\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

The `matcher` field targets a specific tool name (`Edit`, `Bash`, `Read`, etc.). Omitting `matcher` applies the hook to all tool uses of that hook type.

### Common Hook Patterns

- **Auto-lint on edit:** run `eslint` or `dotnet format` after every file edit so the agent sees lint errors and self-corrects
- **Auto-test on change:** run the relevant test suite after edits so the agent catches regressions in the same session
- **Audit log:** write tool call metadata to a file for reviewing what the agent did in a session
- **Notification:** alert when a long-running task finishes

!!! warning
    Hooks run with your full user permissions. A `PostToolUse` hook that runs `bash` with project-supplied commands is as privileged as running that command yourself. If you're working with `.claude/settings.json` from a repository you don't fully trust, review the hooks before running any Claude Code sessions.

## MCP Integration

Claude Code is an MCP host — it can connect to MCP servers that expose tools, resources, and prompts. This is how you extend Claude Code with capabilities beyond the built-in file/shell/git tools: querying a database, calling an internal API, fetching from a knowledge base, or interfacing with external services.

MCP servers are configured in `.mcp.json` at the project root. Claude Code discovers this file automatically on startup and connects to each listed server.

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"],
      "env": {}
    }
  }
}
```

Once connected, the tools exposed by MCP servers appear alongside Claude Code's built-in tools in the same tool use loop. The agent selects them like any other tool.

For building custom MCP servers, configuring authentication, and the full list of official servers, see the [Model Context Protocol](mcp.md) page.

## References

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)

## Next Steps

- [Model Context Protocol (MCP)](mcp.md) — build custom MCP servers and extend Claude Code with external tools
- [Claude Code](claude-code.md) — installation, CLAUDE.md configuration, and core capabilities
