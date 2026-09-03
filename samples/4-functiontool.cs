#:package Microsoft.Agents.AI.AzureAI@1.0.0-rc5
#:package Azure.AI.Projects.Agents@2.0.0-beta.1
#:package Azure.Identity@1.19.0

using System.ComponentModel;
using Azure.AI.Projects;
using Azure.Identity;
using Microsoft.Agents.AI;
using Microsoft.Extensions.AI;

string endpoint = Environment.GetEnvironmentVariable("AZURE_FOUNDRY_PROJECT_ENDPOINT")
    ?? throw new InvalidOperationException("AZURE_FOUNDRY_PROJECT_ENDPOINT is not set.");
string deploymentName = Environment.GetEnvironmentVariable("AZURE_FOUNDRY_PROJECT_DEPLOYMENT_NAME")
    ?? "gpt-4o-mini";

// The [Description] attributes are not decoration. They become the JSON Schema the
// model reads to decide whether and how to call this function.
[Description("Get the weather for a given location.")]
static string GetWeather([Description("The location to get the weather for.")] string location)
    => $"The weather in {location} is cloudy with a high of 15°C.";

const string AssistantInstructions = "You are a helpful assistant that can get weather information.";
const string AssistantName = "WeatherAssistant";

AIProjectClient aiProjectClient = new(new Uri(endpoint), new AzureCliCredential());

AITool tool = AIFunctionFactory.Create(GetWeather);

AIAgent newAgent = await aiProjectClient.CreateAIAgentAsync(
    name: AssistantName,
    model: deploymentName,
    instructions: AssistantInstructions,
    tools: [tool]);

// Retrieving an existing agent by name.
//
// The server stores only the tool's *schema*, never the code behind it. So the
// invocable tools must be supplied again on retrieval, or the framework can see
// that a call was requested but has nothing to run and you must dispatch it
// yourself. This is the same request/response split every agent runtime has.
AIAgent existingAgent = await aiProjectClient.GetAIAgentAsync(name: AssistantName, tools: [tool]);

AgentSession session = await existingAgent.CreateSessionAsync();
Console.WriteLine(await existingAgent.RunAsync("What is the weather like in Amsterdam?", session));

// The same exchange, streamed.
session = await existingAgent.CreateSessionAsync();
await foreach (AgentResponseUpdate update in
    existingAgent.RunStreamingAsync("What is the weather like in Amsterdam?", session))
{
    Console.Write(update);
}
Console.WriteLine();

// Cleanup, if you want it -- see 2-agentasbackend.cs for the AgentsClient shape.
