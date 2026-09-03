# C# samples — Microsoft Agent Framework

Six single-file C# programs showing agent patterns against Azure AI Foundry.
Each one is a .NET file-based app: the `#:package` lines at the top declare its
own dependencies, so there is no project file and no solution.

**Verified as of 2026-09-02:** all six compile with .NET 10.

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

## About the package versions

The samples pin `Microsoft.Agents.AI*@1.0.0-preview.251114.1` — a November 2025
preview, from before Agent Framework reached 1.0 in April 2026.

That is deliberate for now, and it is a known piece of debt. The current packages
(`Microsoft.Agents.AI@1.20.0` and `Microsoft.Agents.AI.AzureAI@1.0.0-rc5`) changed
the Azure surface enough that all six samples fail to compile against them: the
`Azure.AI.Projects.OpenAI` namespace is gone, `AIProjectClient.CreateAIAgent` no
longer exists, and `AgentThread` moved. Porting them is a real piece of work
rather than a version bump, so they stay pinned to versions that build until that
work is done. Shipping samples that look current and do not compile would be
worse than pinning honestly.

`mcpuse.cs` pins `Microsoft.Extensions.AI@10.0.0` rather than the 9.4.3 preview
the others use, because `ModelContextProtocol@0.4.1-preview.1` requires it and
the mismatch made that one sample fail to restore. That sample did not build
before this change.

## Where these appear on the site

- [Frameworks and platforms](https://nitinksingh.com/ai-resources/tools-and-frameworks/)
- [Design patterns](https://nitinksingh.com/ai-resources/patterns/design-patterns/)

For the framework-free version of the same ideas — a working agent loop in about
thirty lines of Python, running against a model on your own machine — see
[the build path](https://nitinksingh.com/ai-resources/00-start-here/the-path/)
and the `labs/` directory.
