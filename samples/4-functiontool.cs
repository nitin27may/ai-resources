#:package Microsoft.Agents.AI.OpenAI@1.20.0
#:package Azure.AI.OpenAI@2.9.0-beta.1

// A function the model can ask you to run.
//
// Watch the split: the model emits a request naming this function and its
// arguments; the framework matches it, runs YOUR code, and feeds the result back.
// The model never executes anything.

using System.ComponentModel;
using System.ClientModel;
using Azure.AI.OpenAI;
using Microsoft.Agents.AI;
using Microsoft.Extensions.AI;
using OpenAI.Chat;

string endpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")
    ?? throw new InvalidOperationException("AZURE_OPENAI_ENDPOINT is not set.");
string apiKey = Environment.GetEnvironmentVariable("AZURE_OPENAI_KEY")
    ?? throw new InvalidOperationException("AZURE_OPENAI_KEY is not set.");
string deployment = Environment.GetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT")
    ?? throw new InvalidOperationException("AZURE_OPENAI_DEPLOYMENT is not set.");

// These [Description] attributes are not documentation. They become the JSON
// Schema the model reads to decide whether, and how, to call this.
[Description("Get the current weather for a given location.")]
static string GetWeather([Description("The city to get the weather for.")] string location)
{
    Console.WriteLine($"    [tool] GetWeather(\"{location}\") was actually invoked");
    return $"The weather in {location} is cloudy with a high of 15 C.";
}

AzureOpenAIClient azureClient = new(new Uri(endpoint), new ApiKeyCredential(apiKey));

AITool weather = AIFunctionFactory.Create(GetWeather);

AIAgent assistant = azureClient
    .GetChatClient(deployment)
    .AsAIAgent(
        instructions: "You are a helpful assistant that can look up the weather.",
        name: "WeatherAssistant",
        tools: [weather]);

AgentSession session = await assistant.CreateSessionAsync();
Console.WriteLine(await assistant.RunAsync("What is the weather like in Amsterdam?", session));

// Ask something the tool cannot answer. A well-behaved agent declines rather
// than inventing a call -- the tool is available, not obligatory.
Console.WriteLine();
Console.WriteLine(await assistant.RunAsync("And what is the capital of France?", session));
