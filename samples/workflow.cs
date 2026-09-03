#:package Microsoft.Agents.AI.OpenAI@1.20.0
#:package Microsoft.Agents.AI.Workflows@1.20.0
#:package Azure.AI.OpenAI@2.9.0-beta.1

// A workflow: three agents wired into a graph you define.
//
// Contrast this with an agent loop. Here the path is fixed -- English in,
// French, Spanish, back to English -- and the model never chooses what happens
// next. That is the trade: predictable cost and an obvious failure point, at the
// price of flexibility. Most production systems want this more often than they
// want an autonomous agent.

using System.ClientModel;
using Azure.AI.OpenAI;
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.Workflows;
using Microsoft.Extensions.AI;
using OpenAI.Chat;

// ChatMessage exists in both Microsoft.Extensions.AI and OpenAI.Chat. We need
// the OpenAI.Chat namespace for the AsAIAgent extension, so disambiguate the
// message type explicitly rather than dropping the using.
using ChatMessage = Microsoft.Extensions.AI.ChatMessage;

string endpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")
    ?? throw new InvalidOperationException("AZURE_OPENAI_ENDPOINT is not set.");
string apiKey = Environment.GetEnvironmentVariable("AZURE_OPENAI_KEY")
    ?? throw new InvalidOperationException("AZURE_OPENAI_KEY is not set.");
string deployment = Environment.GetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT")
    ?? throw new InvalidOperationException("AZURE_OPENAI_DEPLOYMENT is not set.");

AzureOpenAIClient azureClient = new(new Uri(endpoint), new ApiKeyCredential(apiKey));
ChatClient chatClient = azureClient.GetChatClient(deployment);

AIAgent Translator(string language) => chatClient.AsAIAgent(
    instructions: $"Translate the text you are given into {language}. "
                + "Reply with the translation only, nothing else.",
    name: $"{language}Translator");

AIAgent french = Translator("French");
AIAgent spanish = Translator("Spanish");
AIAgent english = Translator("English");

Workflow workflow = new WorkflowBuilder(french)
    .AddEdge(french, spanish)
    .AddEdge(spanish, english)
    .Build();

await using StreamingRun run = await InProcessExecution.RunStreamingAsync(
    workflow, new ChatMessage(ChatRole.User, "Hello world, I hope you are having a good day."));

// Agents wrapped as executors buffer their input and only run when they receive
// a turn token. Without this the workflow sits there doing nothing.
await run.TrySendMessageAsync(new TurnToken(emitEvents: true));

string? lastExecutor = null;
await foreach (WorkflowEvent evt in run.WatchStreamAsync())
{
    if (evt is AgentResponseUpdateEvent update)
    {
        if (update.ExecutorId != lastExecutor)
        {
            Console.WriteLine();
            Console.Write($"{update.ExecutorId}: ");
            lastExecutor = update.ExecutorId;
        }
        Console.Write(update.Data);
    }
}
Console.WriteLine();
Console.WriteLine();
Console.WriteLine("Compare the last line with the first. On a simple sentence the");
Console.WriteLine("round trip usually survives intact; lengthen it, or add nuance and");
Console.WriteLine("idiom, and each hop starts costing something. That is the real");
Console.WriteLine("lesson of a fixed pipeline: the failure is gradual, not loud, and");
Console.WriteLine("only the last executor's output is ever inspected.");
