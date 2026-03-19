---
title: GitHub Copilot
description: What GitHub Copilot is, how to use it effectively in VS Code, and what its current limitations are.
tags:
  - Beginner
  - GitHub Copilot
status: new
---

# GitHub Copilot

!!! abstract
    GitHub Copilot is an AI coding assistant embedded in your IDE. This page covers how it works in VS Code — inline completion, Copilot Chat, slash commands, and PR integration — along with practical tips for getting better results and an honest account of where it will let you down.

---

## What Is GitHub Copilot?

GitHub Copilot is an AI coding assistant built by GitHub and Microsoft, powered by OpenAI models. It integrates directly into your development environment and surfaces suggestions at three levels: completing code as you type, answering questions in a chat pane, and reviewing pull requests on GitHub.com.

**Where it runs:**

- VS Code (primary experience)
- JetBrains IDEs (IntelliJ, PyCharm, WebStorm, etc.)
- Visual Studio
- GitHub.com (PR reviews, Copilot Workspace)
- Terminal (via `gh copilot` CLI — covered in [Copilot CLI & Extensions](copilot-cli-extensions.md))

**Three modes:**

- **Inline code completion** — ghost-text suggestions as you type, accepted with Tab
- **Copilot Chat** — conversational AI in a VS Code side pane, with awareness of your workspace
- **Copilot Workspace** — task-oriented, multi-step editing on GitHub.com (still maturing)

---

## Code Completion

Copilot's inline completion is the most-used feature. As you type, it predicts what comes next — a single line, a full function body, a test case — and displays it as grey ghost text.

**Controls:**

- `Tab` — accept the suggestion
- `Esc` — dismiss it
- `Alt+]` / `Alt+[` — cycle through alternative suggestions
- `Ctrl+Enter` — open a panel showing up to 10 alternatives

**Tips for better completions:**

Write descriptive function and variable names. Copilot uses everything visible in your editor as context. `processClaimSubmission()` gives it far more signal than `process()`.

Add a comment describing intent directly above the function. This is the highest-leverage thing you can do for completion quality:

```typescript
// Validates FNOL submission payload against business rules.
// Returns ValidationResult with field-level errors if invalid.
function validateFnolSubmission(payload: FnolPayload): ValidationResult {
```

Keep related files open in editor tabs. Copilot sees open files as additional context — if your interface is in one file and your implementation is in another, having both open improves suggestions significantly.

Write one test case manually, then let Copilot complete the rest. It pattern-matches your style quickly.

---

## Copilot Chat in VS Code

Copilot Chat is a full conversation interface embedded in VS Code. Unlike inline completion, it can answer questions, explain code, generate boilerplate, and suggest fixes — all without leaving the editor.

Open it from the sidebar icon or with `Ctrl+Alt+I`.

### Built-in Slash Commands

| Command | What It Does |
|---|---|
| `/explain` | Explains the selected code in plain language |
| `/fix` | Diagnoses a problem and suggests a fix |
| `/doc` | Generates a documentation comment for the selection |
| `/tests` | Generates unit tests for the selected function or class |
| `/optimize` | Suggests performance improvements |
| `/new` | Scaffolds a new file or project structure |

Slash commands work on selected code — highlight the function first, then run the command.

### Chat Participants

Prefix your message with `@` to scope the conversation:

- `@workspace` — Copilot indexes your entire workspace and can answer questions about any file
- `@vscode` — questions about VS Code settings, extensions, and configuration
- `@terminal` — explain or fix commands in the integrated terminal

Example: `@workspace Where is the claims processing logic for FNOL submissions?`

### Inline Chat

Press `Ctrl+I` on a selected block of code to open a floating chat prompt directly in the editor. Type your instruction, hit Enter, and Copilot generates a diff you can accept or discard. Faster than copy-pasting to the chat pane for small edits.

---

## Copilot for Pull Requests

**Auto-generated PR descriptions** — When creating a PR on GitHub.com, Copilot can generate a description from the diff. Click the Copilot icon in the description field. The output is a reasonable starting point but rarely publish-ready — review it before submitting.

**Code review suggestions** — On GitHub.com, request a Copilot review from the Reviewers panel the same way you'd request a human reviewer. Copilot adds inline comments on the diff. It's useful for catching obvious issues quickly, but it is not a substitute for human review on security-sensitive or business-logic-heavy code.

**How to request a review:**

1. Open the PR on GitHub.com
2. In the Reviewers panel on the right, click the gear icon
3. Select "Copilot" from the list

Copilot review is available on Team and Enterprise plans.

---

## Tips for Better Results

=== "Code Completion"

    **Write intent before code.** A one-line comment describing what the next function does dramatically improves the quality of the generated body.

    **Use consistent naming.** If your codebase uses `GetAsync` / `CreateAsync` / `DeleteAsync` patterns, Copilot will follow them — it learns from the files it can see.

    **Open context files.** Keep your interface, DTOs, or service contracts open in adjacent tabs. Copilot uses all open files, not just the current one.

    **Let it write boilerplate.** Copilot is fastest on predictable patterns: CRUD operations, DTO mappings, fluent configuration, test setup/teardown. Accept these without overthinking and focus your attention on the non-trivial logic it gets wrong.

=== "Chat"

    **Be specific about what you want.** "Refactor this" is a weak prompt. "Extract the database query into a separate repository method, keeping the existing interface" is actionable.

    **Provide context inline.** Start with a framing sentence: "In this ASP.NET Core minimal API handler, the response time is too high under load." Copilot doesn't know what your code _does_ unless you tell it.

    **Iterate.** The first answer is rarely final. Follow up: "That uses a blocking call — rewrite it with async/await." Treat it as a conversation, not a one-shot prompt.

    **Ask it to explain before it fixes.** For complex bugs, ask `/explain` first. Understanding what Copilot thinks is happening often reveals whether it has correctly diagnosed the issue before you let it change anything.

=== "PR Reviews"

    **Scope the review request.** If you want Copilot to focus on a specific concern, add a description to the PR that calls it out: "Please check this change for SQL injection risks in the raw query construction."

    **Don't treat it as the only review.** Copilot misses context-dependent issues — it doesn't know your team's security policies, your data model constraints, or business rules that live outside the diff.

    **Use it for consistency checks.** Copilot is good at catching inconsistent error handling, missing null checks, and code that deviates from the visible patterns in the codebase. These are tedious for humans and fast for Copilot.

---

## Limitations

!!! note "Hallucinations"
    Copilot produces confident, plausible-looking code that is sometimes wrong. This is most common with library APIs, framework-specific syntax, and edge cases in complex logic. Always verify that the generated code actually does what it claims — don't assume correctness because it compiles.

!!! note "Training Cutoff"
    Copilot's training data has a cutoff date. It may not know about breaking changes in a library released in the last 6–12 months, or recent deprecations. If you're working with a library that released a major version recently, treat Copilot's suggestions about that library with more skepticism than usual.

!!! note "No Runtime Context"
    Copilot cannot see your running application, your actual stack trace, or the state of your database. When debugging, it's working from the static code only. Paste the actual error message and stack trace into Chat explicitly — don't assume it knows what went wrong.

!!! note "Context Window Limits"
    For large codebases, Copilot can only see a subset of your files at a time. In `@workspace` mode it uses search to find relevant files, but it won't have the whole codebase in context simultaneously. If your question spans many files, you may need to paste the relevant sections explicitly or use a more agentic tool like Claude Code.

---

## References

- [GitHub Copilot documentation](https://docs.github.com/en/copilot)
- [Using Copilot in the CLI](https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-the-command-line)

---

## Next Steps

- [Copilot CLI & Extensions](copilot-cli-extensions.md) — using Copilot in the terminal and building custom extensions
- [Claude Code](claude-code.md) — when you need an AI that can read, edit, and run code autonomously across your whole project
