#:package Microsoft.Agents.AI.AzureAI@1.0.0-rc5
#:package Azure.AI.Projects.Agents@2.0.0-beta.1
#:package Azure.Identity@1.19.0

using Azure.AI.Projects;
using Azure.AI.Projects.Agents;
using Azure.Identity;
using Microsoft.Agents.AI;

// AgentsClientSettings is still marked experimental in this preview. Opting in
// explicitly, rather than silently, so the choice is visible when it stabilises.
#pragma warning disable SCME0002

string endpoint = Environment.GetEnvironmentVariable("AZURE_FOUNDRY_PROJECT_ENDPOINT")
    ?? throw new InvalidOperationException("AZURE_FOUNDRY_PROJECT_ENDPOINT is not set.");
string deploymentName = Environment.GetEnvironmentVariable("AZURE_FOUNDRY_PROJECT_DEPLOYMENT_NAME")
    ?? "gpt-4o-mini";

const string JokerInstructions = "You are good at telling jokes.";
const string JokerName = "JokerAgent";

AIProjectClient aiProjectClient = new(new Uri(endpoint), new AzureCliCredential());

PromptAgentDefinition definition = AgentDefinition.CreatePromptAgentDefinition(model: deploymentName);
definition.Instructions = JokerInstructions;

// Create the server-side agent version and get an invocable AIAgent back.
AIAgent jokerAgent = await aiProjectClient.CreateAIAgentAsync(
    name: JokerName,
    creationOptions: new AgentVersionCreationOptions(definition));

// Streaming. This is what you want behind an API or a UI: tokens reach the user
// as they are produced rather than after the whole response is complete.
await foreach (AgentResponseUpdate update in jokerAgent.RunStreamingAsync("Tell me a joke about a pirate."))
{
    Console.Write(update);
}
Console.WriteLine();

// Cleanup. The agents client is constructed from settings rather than a bare URI.
AgentsClient agents = new(new AgentsClientSettings
{
    Endpoint = new Uri(endpoint),
    Options = new AgentsClientOptions(),
});
await agents.DeleteAgentAsync(JokerName);
#pragma warning restore SCME0002
