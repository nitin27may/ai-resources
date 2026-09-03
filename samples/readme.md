# C# samples — Microsoft Agent Framework

Six single-file C# programs showing agent patterns against Azure AI Foundry.
Each one is a .NET file-based app: the `#:package` lines at the top declare its
own dependencies, so there is no project file and no solution.

**Verified as of 2026-09-03:** all six compile with .NET 10, from a clean package cache.

| File | Shows |
|---|---|
| `1-basicagent.cs` | Create a server-side agent, version its instructions, run it |
| `2-agentasbackend.cs` | Drive an agent from a backend service rather than a chat UI |
| `3-multiturn.cs` | Threads, and how conversation state is held server-side |
| `4-functiontool.cs` | Give an agent a C# function as a tool |
| `mcpuse.cs` | Connect an agent to an MCP server |
| `workflow.cs` | Multi-step orchestration with the Workflows package |

## Running one

Needs the [.NET 10 SDK](https://dotnet.microsoft.com/download) or newer.

```bash
# Build only
dotnet build 1-basicagent.cs

# Build and run
dotnet run 1-basicagent.cs
```

Running (as opposed to building) needs an Azure AI Foundry project and an Azure
login, because the samples authenticate with `AzureCliCredential`:

```bash
az login
export AZURE_FOUNDRY_PROJECT_ENDPOINT="https://<your-project>.services.ai.azure.com/api/projects/<name>"
export AZURE_FOUNDRY_PROJECT_DEPLOYMENT_NAME="<your-deployment>"
```

Never put those values in the repository.

## Package versions

Ported to **Microsoft Agent Framework 1.x** on 2026-09-03. All six compile
against the current packages:

| Package | Version |
|---|---|
| `Microsoft.Agents.AI` | 1.20.0 |
| `Microsoft.Agents.AI.AzureAI` | 1.0.0-rc5 |
| `Microsoft.Agents.AI.Workflows` | 1.20.0 |
| `Microsoft.Agents.AI.AzureAI.Persistent` | 1.20.0-preview.260831.1 |
| `Azure.AI.Projects.Agents` | 2.0.0-beta.1 |
| `ModelContextProtocol` | 2.2.0 |

Two remain pre-release because no stable release exists yet: the Azure
integration is at `rc5`, and the persistent-agents integration is still preview.

### What changed from the pre-1.0 preview

Worth reading if you have code on the November 2025 preview, because none of
these produce a helpful error message.

| Was | Now |
|---|---|
| `new PromptAgentDefinition(model:)` | `AgentDefinition.CreatePromptAgentDefinition(model)` — a factory, not a constructor |
| `AgentVersionCreationOptions` in `Azure.AI.Projects.OpenAI` | moved to the new `Azure.AI.Projects.Agents` package |
| `aiProjectClient.Agents.CreateAgentVersion(...)` | `aiProjectClient.CreateAIAgentAsync(name, creationOptions)` |
| `aiProjectClient.GetAIAgent(...)` | `GetAIAgentAsync(...)`, or `AsAIAgent(...)` for the sync form |
| `AgentThread` / `agent.GetNewThread()` | `AgentSession` / `await agent.CreateSessionAsync()` |
| `AgentRunResponseUpdate` | `AgentResponseUpdate` |
| `AgentRunUpdateEvent` | `AgentResponseUpdateEvent` |
| `InProcessExecution.StreamAsync(...)` | `InProcessExecution.RunStreamingAsync(...)` |
| `aiProjectClient.Agents.DeleteAgentAsync(...)` | a separate `AgentsClient`, built from `AgentsClientSettings` |

Two things that will bite regardless of your code:

- **`AgentsClientSettings` is marked experimental** (`SCME0002`), which is an
  *error* rather than a warning by default. The samples opt in with an explicit
  `#pragma warning disable SCME0002` so the choice is visible rather than buried
  in a project file.
- **`AzureCliCredential` now exists in both `Azure.Core` and `Azure.Identity`.**
  Referencing both packages makes the type ambiguous across assemblies.
  `workflow.cs` omits the explicit `Azure.Identity` reference and takes the
  transitive one.

## Where these appear on the site

- [Frameworks and platforms](https://nitinksingh.com/ai-resources/tools-and-frameworks/)
- [Design patterns](https://nitinksingh.com/ai-resources/patterns/design-patterns/)

For the framework-free version of the same ideas — a working agent loop in about
thirty lines of Python, running against a model on your own machine — see
[the build path](https://nitinksingh.com/ai-resources/00-start-here/the-path/)
and the `labs/` directory.
