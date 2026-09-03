#:package Microsoft.Agents.AI.OpenAI@1.20.0
#:package Azure.AI.OpenAI@2.9.0-beta.1

// The simplest useful thing: an agent backed by an Azure OpenAI deployment.
//
// Note what an "agent" is here. It is a chat client plus instructions plus a
// name -- no server-side resource, nothing to provision, nothing to clean up.
// That is worth seeing before the versions with tools and sessions.

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

// GetChatClient takes the DEPLOYMENT name, not the model name. On Azure those
// are different things, and sending the model name is the most common first error.
AIAgent joker = azureClient
    .GetChatClient(deployment)
    .AsAIAgent(
        instructions: "You are good at telling jokes. Keep them to one line.",
        name: "JokerAgent");

Console.WriteLine(await joker.RunAsync("Tell me a joke about a pirate."));

// Each call is independent. Ask a follow-up without a session and the agent has
// no idea what it just said -- the model holds nothing between requests.
Console.WriteLine(await joker.RunAsync("Now make it shorter."));
