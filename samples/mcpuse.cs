// Copyright (c) Microsoft. All rights reserved.
#:package ModelContextProtocol@2.2.0
#:package Microsoft.Agents.AI.AzureAI@1.0.0-rc5
#:package Azure.AI.Projects.Agents@2.0.0-beta.1
#:package Azure.Identity@1.19.0

// A Foundry agent using tools from an MCP server.
//
// Note who invokes what: the Foundry service calls the MCP tools, not the Agent
// Framework running here. Your process supplies the tool definitions and the
// service does the dispatch.

using Azure.AI.Projects;
using Azure.AI.Projects.Agents;
using Azure.Identity;
using Microsoft.Agents.AI;
using Microsoft.Extensions.AI;
using ModelContextProtocol.Client;

#pragma warning disable SCME0002

string endpoint = Environment.GetEnvironmentVariable("AZURE_FOUNDRY_PROJECT_ENDPOINT")
    ?? throw new InvalidOperationException("AZURE_FOUNDRY_PROJECT_ENDPOINT is not set.");
string deploymentName = Environment.GetEnvironmentVariable("AZURE_FOUNDRY_PROJECT_DEPLOYMENT_NAME")
    ?? "gpt-4o-mini";

Console.WriteLine("Starting MCP stdio transport for the GitHub server ...");

await using McpClient mcpClient = await McpClient.CreateAsync(new StdioClientTransport(new()
{
    Name = "MCPServer",
    Command = "npx",
    Arguments = ["-y", "@github/github-mcp-server"],
}));

IList<McpClientTool> mcpTools = await mcpClient.ListToolsAsync();

const string AgentName = "AgentWithMCP";
AIProjectClient aiProjectClient = new(new Uri(endpoint), new AzureCliCredential());

Console.WriteLine($"Creating the agent '{AgentName}' ...");

AIAgent agent = await aiProjectClient.CreateAIAgentAsync(
    name: AgentName,
    model: deploymentName,
    instructions: "You answer questions related to GitHub repositories only.",
    tools: [.. mcpTools.Cast<AITool>()]);

const string Prompt = "Summarize the last four commits to the microsoft/semantic-kernel repository.";
Console.WriteLine($"Invoking '{AgentName}' with: {Prompt}");
Console.WriteLine(await agent.RunAsync(Prompt));

AgentsClient agents = new(new AgentsClientSettings
{
    Endpoint = new Uri(endpoint),
    Options = new AgentsClientOptions(),
});
await agents.DeleteAgentAsync(AgentName);

#pragma warning restore SCME0002
