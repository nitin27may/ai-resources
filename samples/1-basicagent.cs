#:package Microsoft.Agents.AI.AzureAI@1.0.0-rc5
#:package Azure.AI.Projects.Agents@2.0.0-beta.1
#:package Azure.Identity@1.19.0

using Azure.AI.Projects;
using Azure.AI.Projects.Agents;
using Azure.Identity;
using Microsoft.Agents.AI;

string endpoint = Environment.GetEnvironmentVariable("AZURE_FOUNDRY_PROJECT_ENDPOINT")
    ?? throw new InvalidOperationException("AZURE_FOUNDRY_PROJECT_ENDPOINT is not set.");
string deploymentName = Environment.GetEnvironmentVariable("AZURE_FOUNDRY_PROJECT_DEPLOYMENT_NAME")
    ?? "gpt-4o-mini";

const string JokerInstructionsV1 = "You are good at telling jokes.";
const string JokerInstructionsV2 = "You are extremely hilarious at telling jokes.";
const string JokerName = "JokerAgent";

// A client for creating, retrieving and deleting server-side agents in Azure AI Foundry.
AIProjectClient aiProjectClient = new(new Uri(endpoint), new AzureCliCredential());

// Define the agent. A prompt agent is the simplest kind: a model plus instructions.
// Note this is a factory call, not a constructor -- AgentDefinition is the base type
// and each kind of agent has its own Create... method.
PromptAgentDefinition definition = AgentDefinition.CreatePromptAgentDefinition(model: deploymentName);
definition.Instructions = JokerInstructionsV1;

// Foundry manages agents by name, with a version history. Creating a version returns
// an AIAgent you can invoke straight away.
AIAgent jokerAgentV1 = await aiProjectClient.CreateAIAgentAsync(
    name: JokerName,
    creationOptions: new AgentVersionCreationOptions(definition));

// Publishing a second version is the same call with a different definition. The name
// is the stable identity; the version moves.
PromptAgentDefinition definitionV2 = AgentDefinition.CreatePromptAgentDefinition(model: deploymentName);
definitionV2.Instructions = JokerInstructionsV2;
AIAgent jokerAgentV2 = await aiProjectClient.CreateAIAgentAsync(
    name: JokerName,
    creationOptions: new AgentVersionCreationOptions(definitionV2));

// Fetching by name alone gives you whatever the latest version is.
AIAgent jokerAgentLatest = await aiProjectClient.GetAIAgentAsync(name: JokerName);

// The underlying Foundry version record is reachable through GetService.
AgentVersion? latestVersion = jokerAgentLatest.GetService<AgentVersion>();
Console.WriteLine($"Latest agent version id: {latestVersion?.Id}");

// Once you hold an AIAgent, it behaves like any other AIAgent regardless of where it lives.
Console.WriteLine(await jokerAgentLatest.RunAsync("Tell me a joke about a pirate."));

// Deleting by name removes every version created above.
// AgentsClient agents = new(new Uri(endpoint), new AzureCliCredential());
// await agents.DeleteAgentAsync(JokerName);
