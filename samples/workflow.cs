// Copyright (c) Microsoft. All rights reserved.
#:package Microsoft.Agents.AI.AzureAI.Persistent@1.20.0-preview.260831.1
#:package Microsoft.Agents.AI.Workflows@1.20.0
#:package Microsoft.Agents.AI@1.20.0

// Three Foundry agents chained into a workflow: English in, French, Spanish,
// then back to English. The point is the shape -- a workflow is a graph you
// define, not a path the model chooses. Compare with the agent loop, where the
// model decides each step.

using Azure.AI.Agents.Persistent;
// No explicit Azure.Identity reference here. Azure.Core now also carries
// Azure.Identity.AzureCliCredential, and referencing both packages makes the
// type ambiguous across assemblies. The transitive reference is enough.
using Azure.Identity;
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.Workflows;
using Microsoft.Extensions.AI;

public static class Program
{
    private static async Task Main()
    {
        string endpoint = Environment.GetEnvironmentVariable("AZURE_FOUNDRY_PROJECT_ENDPOINT")
            ?? throw new InvalidOperationException("AZURE_FOUNDRY_PROJECT_ENDPOINT is not set.");
        string deploymentName = Environment.GetEnvironmentVariable("AZURE_FOUNDRY_PROJECT_DEPLOYMENT_NAME")
            ?? "gpt-4o-mini";

        PersistentAgentsClient persistentAgentsClient = new(endpoint, new AzureCliCredential());

        AIAgent frenchAgent = await GetTranslationAgentAsync("French", persistentAgentsClient, deploymentName);
        AIAgent spanishAgent = await GetTranslationAgentAsync("Spanish", persistentAgentsClient, deploymentName);
        AIAgent englishAgent = await GetTranslationAgentAsync("English", persistentAgentsClient, deploymentName);

        Workflow workflow = new WorkflowBuilder(frenchAgent)
            .AddEdge(frenchAgent, spanishAgent)
            .AddEdge(spanishAgent, englishAgent)
            .Build();

        // StreamAsync became RunStreamingAsync in Agent Framework 1.x.
        await using StreamingRun run = await InProcessExecution.RunStreamingAsync(
            workflow, new ChatMessage(ChatRole.User, "Hello World!"));

        // Agents wrapped as executors buffer their input and only run when they
        // receive a turn token. Without this the workflow sits idle.
        await run.TrySendMessageAsync(new TurnToken(emitEvents: true));

        await foreach (WorkflowEvent evt in run.WatchStreamAsync())
        {
            if (evt is AgentResponseUpdateEvent update)
            {
                Console.WriteLine($"{update.ExecutorId}: {update.Data}");
            }
        }

        // Cleanup, if you want it:
        // await persistentAgentsClient.Administration.DeleteAgentAsync(agentId);
    }

    private static async Task<ChatClientAgent> GetTranslationAgentAsync(
        string targetLanguage,
        PersistentAgentsClient persistentAgentsClient,
        string model)
    {
        var agentMetadata = await persistentAgentsClient.Administration.CreateAgentAsync(
            model: model,
            name: $"{targetLanguage} Translator",
            instructions: $"You are a translation assistant that translates the provided text to {targetLanguage}.");

        return await persistentAgentsClient.GetAIAgentAsync(agentMetadata.Value.Id);
    }
}
