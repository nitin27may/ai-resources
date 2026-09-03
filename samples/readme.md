# C# samples — Microsoft Agent Framework on Azure OpenAI

Six single-file C# programs. Each declares its own dependencies with `#:package`
lines, so there is no project file and no solution — `dotnet run 1-basicagent.cs`
is the whole setup.

**Verified as of 2026-09-03:** all six *run*, not merely compile, against a live
Azure OpenAI deployment on .NET 10.

| File | Shows |
|---|---|
| `1-basicagent.cs` | The smallest agent: a chat client plus instructions. Also that each call is independent |
| `2-agentasbackend.cs` | Streaming, which is what you want behind an API or a UI |
| `3-multiturn.cs` | Sessions — what actually carries a conversation |
| `4-functiontool.cs` | A C# function as a tool, and an agent correctly *not* calling it |
| `mcpuse.cs` | Tools from an MCP server, and a sandbox boundary refusing an out-of-scope read |
| `workflow.cs` | Three agents in a fixed graph, where the model never chooses the path |

## Running them

Needs the [.NET 10 SDK](https://dotnet.microsoft.com/download) and an Azure
OpenAI deployment. The same three variables the Python labs use:

```bash
export AZURE_OPENAI_ENDPOINT="https://<your-resource>.openai.azure.com"
export AZURE_OPENAI_KEY="<your key>"
export AZURE_OPENAI_DEPLOYMENT="<your chat deployment name>"

dotnet run 1-basicagent.cs
```

`AZURE_OPENAI_DEPLOYMENT` is the **deployment** name you chose, not the model's
name. Sending the model name is the most common first error.

`mcpuse.cs` additionally needs `npx` on your PATH. It launches the reference
filesystem MCP server scoped to a temporary directory, so it needs no account
and no token.

Never put a key in the repository. Export it, or keep it in a git-ignored `.env`.

## Why Azure OpenAI rather than Foundry Agents

These previously targeted Azure AI Foundry's server-side agents, which meant
they needed a Foundry project and an `az login` — so they could be compiled but
almost never run. Pointing them at an Azure OpenAI deployment with a key means
they run with the same credentials as everything else on this site.

The trade is that server-side agent versioning, a Foundry feature, is no longer
demonstrated. That is a deployment concern rather than an agent concept, and it
is not what these samples are for.

## Package versions

| Package | Version |
|---|---|
| `Microsoft.Agents.AI.OpenAI` | 1.20.0 |
| `Microsoft.Agents.AI.Workflows` | 1.20.0 |
| `Azure.AI.OpenAI` | 2.9.0-beta.1 |
| `ModelContextProtocol` | 2.2.0 |

`Azure.AI.OpenAI` has no current stable release that carries the API these
samples use; 2.9.0-beta.1 is the newest published.

## If you have code on the pre-1.0 Agent Framework preview

None of these renames fail with a message that points at the fix, so they are
listed here.

| Was | Now |
|---|---|
| `AgentThread` / `agent.GetNewThread()` | `AgentSession` / `await agent.CreateSessionAsync()` |
| `AgentRunResponseUpdate` | `AgentResponseUpdate` |
| `AgentRunUpdateEvent` | `AgentResponseUpdateEvent` |
| `InProcessExecution.StreamAsync(...)` | `InProcessExecution.RunStreamingAsync(...)` |
| `new PromptAgentDefinition(model:)` | `AgentDefinition.CreatePromptAgentDefinition(model)` |
| `AgentVersionCreationOptions` in `Azure.AI.Projects.OpenAI` | moved to `Azure.AI.Projects.Agents` |
| `aiProjectClient.Agents.CreateAgentVersion(...)` | `aiProjectClient.CreateAIAgentAsync(name, creationOptions)` |
| `aiProjectClient.GetAIAgent(...)` | `GetAIAgentAsync(...)`, or `AsAIAgent(...)` for the sync form |

Two type clashes you will hit whatever you write:

- **`ChatMessage`** exists in both `Microsoft.Extensions.AI` and `OpenAI.Chat`.
  You need the `OpenAI.Chat` namespace for the `AsAIAgent` extension, so alias
  the message type rather than dropping the using. See `workflow.cs`.
- **`AzureCliCredential`** exists in both `Azure.Core` and `Azure.Identity`.
  Referencing both packages makes it ambiguous across assemblies.

## Where these appear on the site

- [Frameworks and platforms](https://nitinksingh.com/ai-resources/tools-and-frameworks/)
- [Design patterns](https://nitinksingh.com/ai-resources/patterns/design-patterns/)

For the framework-free version of the same ideas — an agent loop in about thirty
lines of Python, running against a model on your own machine — see
[the build path](https://nitinksingh.com/ai-resources/00-start-here/the-path/)
and the `labs/` directory.
