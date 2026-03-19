---
title: Copilot CLI & Extensions
description: How to use GitHub Copilot in the CLI, and how to build Copilot Extensions — both Skillsets and full Agent extensions.
tags:
  - Intermediate
  - GitHub Copilot
status: new
---

# Copilot CLI & Extensions

!!! abstract
    GitHub Copilot extends beyond the IDE. The CLI integration lets you get command suggestions and explanations without leaving the terminal. The Extensions platform lets you connect Copilot Chat to your own tools and services — either as a lightweight Skillset or a full Agent extension with conversation state.

---

## GitHub Copilot in the CLI

Copilot in the CLI is installed as a GitHub CLI extension. It gives you two core commands: suggest a shell command for a task, or explain what a command does.

### Installation

```bash
gh extension install github/gh-copilot
```

Requires the [GitHub CLI](https://cli.github.com/) (`gh`) and an active Copilot subscription. Authenticate with `gh auth login` if you haven't already.

### Core Commands

**Get a command suggestion:**

```bash
gh copilot suggest "list all pods in the claims namespace that are not running"
```

Copilot returns a suggested command and asks whether you want to explain it, revise the request, or copy it to the clipboard. Example output:

```
? What kind of command do you need?
  shell

Suggestion:
  kubectl get pods -n claims --field-selector=status.phase!=Running

? What would you like to do with this suggestion?
> Copy command to clipboard
  Explain command
  Revise command
  Cancel
```

**Explain an existing command:**

```bash
gh copilot explain "kubectl rollout restart deployment/api-gateway -n production"
```

Returns a plain-language explanation of what each part of the command does. Useful when you inherit a runbook full of commands you don't fully understand.

**Practical examples:**

```bash
# Forgot the exact docker inspect format string for IP addresses
gh copilot suggest "get the IP address of a running docker container named api"

# Understand what this git command actually does
gh copilot explain "git log --oneline --graph --decorate --all"

# Azure CLI operations
gh copilot suggest "rotate the primary key for storage account mystorageacct in resource group rg-claims"
```

!!! tip
    This is most useful for `kubectl`, `az`, `docker`, and `git` operations where you know what you want to do but can't remember the exact flags. Faster than a web search and stays in the terminal.

Copilot in the CLI can also be exposed as an MCP server, allowing other AI tools to call it programmatically. See the [Model Context Protocol](mcp.md) page for details.

---

## GitHub Copilot Extensions

Copilot Extensions let you connect Copilot Chat to external tools and services via `@`-mention. Type `@your-extension` in Copilot Chat and the extension handles the message — querying your internal APIs, databases, observability tools, or anything else.

There are two extension types with very different complexity profiles:

| | **Skillset** | **Agent** |
|---|---|---|
| **Complexity** | Low | High |
| **Conversation state** | No | Yes |
| **Streaming responses** | No | Yes (SSE) |
| **Setup** | JSON function definitions + HTTP endpoint | GitHub App + webhook handler + SSE |
| **Best for** | Exposing data or triggering actions | Multi-turn conversations, complex workflows |
| **When to choose** | You need Copilot to call a function and return a result | You need Copilot to carry context across turns or stream a response |

---

## Building a Skillset Extension

A Skillset extension is the simpler option. You define a set of functions in JSON — name, description, parameters — and expose an HTTP endpoint that Copilot calls when a user's message matches a function. No conversation management, no streaming.

### Steps

**1. Create a GitHub App**

In GitHub Settings → Developer Settings → GitHub Apps, create a new app. Under "Copilot", set the extension type to "Skillset" and provide your endpoint URL.

**2. Define your skills in JSON**

```json
{
  "skills": [
    {
      "name": "get_claim_status",
      "description": "Returns the current status and latest note for an insurance claim by claim number.",
      "parameters": {
        "type": "object",
        "properties": {
          "claim_number": {
            "type": "string",
            "description": "The claim number, e.g. CLM-2024-00123"
          }
        },
        "required": ["claim_number"]
      }
    }
  ]
}
```

Copilot uses the `description` fields to decide when to call each skill. Write them as if you're documenting for a smart colleague — specific, accurate, and unambiguous about what the function does and when it applies.

**3. Implement the HTTP endpoint**

Your endpoint receives a POST with the skill name and resolved parameters. Return a JSON response with the result. Copilot incorporates it into the chat response.

**4. Register the skills**

Upload the skill definitions in your GitHub App's Copilot configuration. GitHub validates them and makes them available when users `@mention` your extension.

!!! tip
    Skillsets are the right choice when you just need to expose data or trigger actions without conversation flow. If a user asks `@your-extension what's the status of claim CLM-123?` and you return the answer, a Skillset is enough. Choose an Agent extension only when you genuinely need multi-turn conversation.

---

## Building an Agent Extension

An Agent extension gives you full control over the conversation. Your server receives each turn, processes it however you want — calling other APIs, running LLMs, querying databases — and streams the response back using Server-Sent Events (SSE).

### Architecture

```
Copilot Chat → GitHub App webhook → Your server → [Process / call APIs / LLMs] → SSE stream → Copilot Chat
```

### Steps Overview

**1. Create a GitHub App with webhooks**

Set up a GitHub App as above, but set the extension type to "Agent". Provide a webhook URL and a secret for payload verification.

**2. Handle the `copilot_lsp_completion` event**

Your webhook receives a POST for each conversation turn. The payload includes the full conversation history as an array of messages.

**3. Parse the conversation messages**

```typescript
import { CopilotExtensionAgent } from "@github/copilot-extensions";

const agent = new CopilotExtensionAgent();

agent.on("message", async (request, response) => {
  const messages = request.messages; // Full conversation history
  const lastUserMessage = messages.at(-1)?.content;

  // Process the message, call your APIs, build context...
});
```

**4. Generate your response**

Your server can call any backend — internal REST APIs, Azure OpenAI, a database query, an Azure Service Bus operation. The agent has full access to whatever your server can reach.

**5. Stream back using Server-Sent Events**

```typescript
response.stream("Processing your request...");
// ... do work ...
response.stream(`Claim CLM-123 status: **Approved** as of 2024-03-15.`);
response.end();
```

!!! note
    Agent extensions require handling GitHub's Copilot API auth token, which is passed in the request headers and must be used to make calls back to the Copilot API on behalf of the user. Use the `@github/copilot-extensions` npm SDK rather than rolling this yourself — it handles token verification, message parsing, and SSE formatting.

**Install the SDK:**

```bash
npm install @github/copilot-extensions
```

---

## Published Extensions Worth Using

Beyond building your own, a growing set of published extensions connects Copilot to common developer tools:

| Extension | Publisher | What It Does |
|---|---|---|
| **Sentry** | Sentry | Look up recent errors, exceptions, and traces from Copilot Chat |
| **Datadog** | Datadog | Query logs, metrics, and monitors without leaving the IDE |
| **Mermaid Chart** | Mermaid Chart | Generate and render Mermaid diagrams via Copilot |
| **Docker** | Docker | Manage containers, query images, troubleshoot Dockerfiles |
| **Octopus Deploy** | Octopus Deploy | Trigger deployments and check release status from Copilot Chat |

Browse the full list at [github.com/marketplace](https://github.com/marketplace?type=apps&copilot_app=true) — filter by "Copilot" type.

---

## References

- [Building Copilot Extensions](https://docs.github.com/en/copilot/building-copilot-extensions)
- [Using Copilot in the CLI](https://docs.github.com/en/copilot/how-tos/use-copilot-for-common-tasks/use-copilot-in-the-cli)

---

## Next Steps

- [Claude Code](claude-code.md) — agentic coding that goes beyond what Copilot extensions can do
- [Model Context Protocol](mcp.md) — a standardized alternative to custom extensions for connecting AI tools to your systems
