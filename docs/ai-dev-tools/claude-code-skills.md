---
title: Claude Code Skills & Agents
description: How to create custom slash command skills, use subagents for parallel work, configure hooks, and integrate MCP with Claude Code.
status: new
tags:
  - Tools
  - Claude Code
---

# Claude Code Skills & Agents

!!! abstract
    Beyond basic prompting, Claude Code supports skills (custom slash commands), subagents for parallel and isolated work, hooks that fire on tool events, and MCP server integration. This page covers each mechanism, when to use it, and how to configure it.

## Skills

A skill is a folder containing a `SKILL.md`. Claude either loads it because you
typed `/skill-name`, or **because its description matched what you asked for** —
that second half is the defining property, and it is what makes skills different
from a saved prompt.

!!! danger "The layout matters — a flat file registers nothing"
    A skill is a **directory**, and the directory name becomes the command:

    ```
    .claude/skills/commit/SKILL.md      <- registers /commit
    .claude/skills/commit.md            <- registers nothing
    ```

    Guidance showing flat `.md` files directly inside `.claude/skills/` is
    describing the older `.claude/commands/` layout. That layout still works —
    Anthropic merged custom commands into skills, and `.claude/commands/deploy.md`
    and `.claude/skills/deploy/SKILL.md` both create `/deploy` — but they are not
    interchangeable paths.

**Locations:**

| Scope | Path | Available in |
|---|---|---|
| Personal | `~/.claude/skills/<name>/SKILL.md` | all your projects |
| Project | `.claude/skills/<name>/SKILL.md` | this project, shared via git |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | wherever the plugin is enabled |

### Anatomy

```markdown
---
name: commit
description: Generate a conventional commit message for staged changes.
  Use when the user asks to commit, or mentions a commit message.
---

Review the staged git changes and generate a conventional commit message
following `type(scope): description`.

Use these types: feat, fix, docs, style, refactor, test, chore.

Keep the subject under 72 characters. If the change spans multiple concerns,
add a body explaining the reasoning — not what changed, but why.
```

**The `description` is load-bearing.** It is what Claude reads to decide whether
a skill is relevant. A vague description produces a skill that never fires on its
own; a precise one, naming the triggers, produces one that does.

Optional frontmatter worth knowing: `allowed-tools` scopes what the skill may
use, and `disable-model-invocation: true` makes it user-invocable only.

### Why a skill rather than CLAUDE.md

CLAUDE.md is loaded in full, every session, and costs context whether or not you
need it. A skill's body loads **only when used** — so long reference material
costs almost nothing until the moment it is relevant.

The rule: facts that apply always go in CLAUDE.md. Procedures that apply
sometimes go in a skill.

## Subagents

The Agent tool lets Claude Code spawn specialized subprocess agents. Each subagent runs in its own context, which keeps large search results or experimental work isolated from the main session's context window.

### Built-in Subagent Types

| Type | Purpose | When to Use |
|---|---|---|
| General purpose | Complex multi-step research and tasks | Default for anything not covered by a specialized type |
| Explore | Fast codebase exploration — file patterns, code search | When you need to find files or grep for patterns quickly |
| Plan | Software architecture planning | Before implementing a complex feature — get a plan first |

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

### Hook events

There are **31** hook events. These are the four you will reach for first:

| Hook | Fires when |
|---|---|
| `PreToolUse` | Before a tool runs — the place to gate or block |
| `PostToolUse` | After a tool succeeds — lint, test, format |
| `UserPromptSubmit` | When you submit a prompt, before Claude sees it |
| `Stop` | When Claude finishes responding — notifications, cleanup |

The rest cover session lifecycle (`SessionStart`, `SessionEnd`), subagents
(`SubagentStart`, `SubagentStop`), compaction (`PreCompact`, `PostCompact`),
permissions (`PermissionRequest`, `PermissionDenied`), failures
(`PostToolUseFailure`, `StopFailure`), and more. See the
[hooks reference](https://code.claude.com/docs/en/hooks) for the full set —
treat any list of three as a starting point, not an inventory.

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
      "args": ["-y", "@github/github-mcp-server"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "weather": {
      "command": "uv",
      "args": ["run", "--project", "path/to/project", "python", "server.py"],
      "env": {}
    }
  }
}
```

Once connected, the tools exposed by MCP servers appear alongside Claude Code's built-in tools in the same tool use loop. The agent selects them like any other tool.

For building custom MCP servers, configuring authentication, and the full list of official servers, see the [Model Context Protocol](mcp.md) page.

## References

- [Extend Claude with skills](https://code.claude.com/docs/en/skills)
- [Hooks reference](https://code.claude.com/docs/en/hooks) — all 31 events
- [Subagents](https://code.claude.com/docs/en/sub-agents)

## Next Steps

- [Model Context Protocol (MCP)](mcp.md) — build custom MCP servers and extend Claude Code with external tools
- [Claude Code](claude-code.md) — installation, CLAUDE.md configuration, and core capabilities
