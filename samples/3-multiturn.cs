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

AIAgent jokerAgent = await aiProjectClient.CreateAIAgentAsync(
    name: JokerName,
    creationOptions: new AgentVersionCreationOptions(definition));

// A session carries the conversation. Without one, each call is independent --
// the model itself holds nothing between requests.
// (This type was called AgentThread, and GetNewThread(), before Agent Framework 1.0.)
AgentSession session = await jokerAgent.CreateSessionAsync();
Console.WriteLine(await jokerAgent.RunAsync("Tell me a joke about a pirate.", session));
Console.WriteLine(await jokerAgent.RunAsync(
    "Now add some emojis to the joke and tell it in the voice of a pirate's parrot.", session));

// The same conversation, streamed. A fresh session, so the second exchange below
// has no knowledge of the one above.
session = await jokerAgent.CreateSessionAsync();
await foreach (AgentResponseUpdate update in
    jokerAgent.RunStreamingAsync("Tell me a joke about a pirate.", session))
{
    Console.Write(update);
}
Console.WriteLine();
await foreach (AgentResponseUpdate update in jokerAgent.RunStreamingAsync(
    "Now add some emojis to the joke and tell it in the voice of a pirate's parrot.", session))
{
    Console.Write(update);
}
Console.WriteLine();

AgentsClient agents = new(new AgentsClientSettings
{
    Endpoint = new Uri(endpoint),
    Options = new AgentsClientOptions(),
});
await agents.DeleteAgentAsync(JokerName);
#pragma warning restore SCME0002
