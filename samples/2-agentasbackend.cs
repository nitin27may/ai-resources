#:package Microsoft.Agents.AI.OpenAI@1.20.0
#:package Azure.AI.OpenAI@2.9.0-beta.1

// Streaming. This is the shape you want behind an API or a UI: tokens reach the
// user as they are produced, rather than after the whole response is finished.
// It does not reduce total time -- it removes the blank screen.

using System.ClientModel;
using Azure.AI.OpenAI;
using Microsoft.Agents.AI;
using OpenAI.Chat;

string endpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")
    ?? throw new InvalidOperationException("AZURE_OPENAI_ENDPOINT is not set.");
string apiKey = Environment.GetEnvironmentVariable("AZURE_OPENAI_KEY")
    ?? throw new InvalidOperationException("AZURE_OPENAI_KEY is not set.");
string deployment = Environment.GetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT")
    ?? throw new InvalidOperationException("AZURE_OPENAI_DEPLOYMENT is not set.");

AzureOpenAIClient azureClient = new(new Uri(endpoint), new ApiKeyCredential(apiKey));

AIAgent joker = azureClient
    .GetChatClient(deployment)
    .AsAIAgent(
        instructions: "You are good at telling jokes.",
        name: "JokerAgent");

await foreach (AgentResponseUpdate update in
    joker.RunStreamingAsync("Tell me a joke about a pirate, in about three sentences."))
{
    Console.Write(update);
}
Console.WriteLine();
