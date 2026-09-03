#:package Microsoft.Agents.AI.OpenAI@1.20.0
#:package Azure.AI.OpenAI@2.9.0-beta.1

// Sessions. Sample 1 showed that each call is independent; a session is what
// carries the conversation between them.
//
// The type was called AgentThread, and the factory GetNewThread(), before Agent
// Framework 1.0.

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
    .AsAIAgent(instructions: "You are good at telling jokes.", name: "JokerAgent");

AgentSession session = await joker.CreateSessionAsync();
Console.WriteLine(await joker.RunAsync("Tell me a joke about a pirate.", session));
Console.WriteLine();
Console.WriteLine(await joker.RunAsync("Now tell the same joke as a parrot would.", session));

// A new session starts empty. The follow-up below has nothing to refer back to,
// which is the same behaviour sample 1 showed without any session at all.
Console.WriteLine();
Console.WriteLine("--- new session, streamed ---");
session = await joker.CreateSessionAsync();
await foreach (AgentResponseUpdate update in
    joker.RunStreamingAsync("Tell me a joke about a database.", session))
{
    Console.Write(update);
}
Console.WriteLine();
await foreach (AgentResponseUpdate update in
    joker.RunStreamingAsync("Explain why that was funny, in one sentence.", session))
{
    Console.Write(update);
}
Console.WriteLine();
