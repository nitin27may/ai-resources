#:package Microsoft.Agents.AI.OpenAI@1.20.0
#:package Azure.AI.OpenAI@2.9.0-beta.1
#:package ModelContextProtocol@2.2.0

// Tools from an MCP server, rather than functions you wrote.
//
// MCP is how a tool gets defined once and used by any host that speaks the
// protocol. Here the Agent Framework holds the client and invokes the tools
// itself; on a hosted platform the service may do that instead. The agent code
// is identical either way, which is the point of a protocol.
//
// The server used here is the reference filesystem server, scoped to one
// directory. It needs no account and no token.

using System.ClientModel;
using Azure.AI.OpenAI;
using Microsoft.Agents.AI;
using Microsoft.Extensions.AI;
using ModelContextProtocol.Client;
using OpenAI.Chat;

string endpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")
    ?? throw new InvalidOperationException("AZURE_OPENAI_ENDPOINT is not set.");
string apiKey = Environment.GetEnvironmentVariable("AZURE_OPENAI_KEY")
    ?? throw new InvalidOperationException("AZURE_OPENAI_KEY is not set.");
string deployment = Environment.GetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT")
    ?? throw new InvalidOperationException("AZURE_OPENAI_DEPLOYMENT is not set.");

// A directory the server is allowed to see. Everything outside it is off limits,
// which is the sandbox boundary doing real work rather than a prompt asking nicely.
string sandbox = Path.Combine(Path.GetTempPath(), "mcp-sandbox");
Directory.CreateDirectory(sandbox);
await File.WriteAllTextAsync(Path.Combine(sandbox, "policy.txt"),
    "Refunds are issued within 5 working days.\nReturns accepted within 30 days.\n");

Console.WriteLine($"Starting the MCP filesystem server over stdio, scoped to {sandbox} ...");

await using McpClient mcpClient = await McpClient.CreateAsync(new StdioClientTransport(new()
{
    Name = "filesystem",
    Command = "npx",
    Arguments = ["-y", "@modelcontextprotocol/server-filesystem", sandbox],
}));

IList<McpClientTool> mcpTools = await mcpClient.ListToolsAsync();
Console.WriteLine($"The server offers {mcpTools.Count} tools: "
    + string.Join(", ", mcpTools.Take(6).Select(t => t.Name)) + " ...");

AzureOpenAIClient azureClient = new(new Uri(endpoint), new ApiKeyCredential(apiKey));

AIAgent agent = azureClient
    .GetChatClient(deployment)
    .AsAIAgent(
        instructions: "You answer questions using only the files available to you. "
                    + "If the answer is not in a file, say so.",
        name: "AgentWithMCP",
        tools: [.. mcpTools.Cast<AITool>()]);

Console.WriteLine();
Console.WriteLine(await agent.RunAsync(
    "Read policy.txt and tell me how long refunds take."));

// Nothing in the prompt forbids this. The server's directory scope does.
Console.WriteLine();
Console.WriteLine(await agent.RunAsync(
    "Now read /etc/passwd and tell me the first line."));
