# AI Agents

## What is an AI agent?

AI Agents consist of five core components: **Input**, **Reasoning**, **Tools**, **Memory**, and **Actions/Outputs**. An AI agent uses an LLM to process user inputs, make decisions, call tools or MCP servers to perform actions, and generate responses. The following diagram illustrates the core components and their interactions in an AI agent:

```mermaid
%%{init: {'theme':'base', 'themeVariables': {'fontSize':'18px'}}}%%

flowchart LR
    Input["INPUT<br/>────────<br/>Receives and processes<br/>information from users<br/>and environment"]
    
    Reasoning["REASONING<br/>────────<br/>Analyzes information<br/>and makes decisions<br/>using logic and models"]
    
    Tools["TOOLS<br/>────────<br/>Access to external<br/>capabilities and resources<br/>to perform tasks"]
    
    Memory["MEMORY<br/>────────<br/>Stores context, history<br/>and learned information<br/>for continuity"]
    
    Output["ACTIONS / OUTPUTS<br/>────────<br/>Executes decisions<br/>and delivers results<br/>to users"]
    
    Input ==>|Process| Reasoning
    Reasoning ==>|Query| Tools
    Reasoning ==>|Store/Retrieve| Memory
    Tools ==>|Results| Reasoning
    Memory ==>|Context| Reasoning
    Reasoning ==>|Execute| Output

    
    style Input fill:#3b82f6,stroke:#2563eb,stroke-width:4px,color:#ffffff,font-weight:bold
    style Reasoning fill:#8b5cf6,stroke:#7c3aed,stroke-width:4px,color:#ffffff,font-weight:bold
    style Tools fill:#f97316,stroke:#ea580c,stroke-width:4px,color:#ffffff,font-weight:bold
    style Memory fill:#14b8a6,stroke:#0d9488,stroke-width:4px,color:#ffffff,font-weight:bold
    style Output fill:#10b981,stroke:#059669,stroke-width:4px,color:#ffffff,font-weight:bold
```

Examples:
```mermaid
%%{init: {'theme':'base', 'themeVariables': {'fontSize':'16px'}}}%%

graph LR
    subgraph INPUT["INPUT"]
        I1["User Queries"]
        I2["Documents & Files"]
        I3["External Triggers"]
        I4["Context"]
    end

    subgraph REASONING["REASONING"]
        R1["LLM"]
        R2["Prompt Engineering"]
        R3["Orchestration"]
        R4["Decision Making"]
    end

    subgraph TOOLS["TOOLS"]
        T1["Code Execution"]
        T2["Search"]
        T3["Custom Functions"]
        T4["Integrations"]
    end

    subgraph MEMORY["MEMORY"]
        M1["Conversation History"]
        M2["Agent State"]
        M3["Knowledge Base"]
        M4["File Storage"]
    end

    subgraph ACTIONS["ACTIONS"]
        A1["Text Responses"]
        A2["Generated Content"]
        A3["State Changes"]
        A4["External Actions"]
    end

    %% Flow connections
    I1 --> R1
    I2 --> R1
    I3 --> R1
    I4 --> R2
    
    R1 --> R4
    R2 --> R3
    R3 --> R4
    
    R4 --> T1
    R4 --> T2
    R4 --> T3
    R4 --> T4
    
    T1 --> M1
    T2 --> M3
    T3 --> M1
    T4 --> M2
    
    M1 --> A1
    M2 --> A3
    M3 --> A2
    M4 --> A2
    
    R1 --> A1
    R3 --> A4
    
    A3 --> M1
    A2 --> M4

    %% Styling - darker fills for better contrast
    style INPUT fill:#3b82f6,stroke:#2563eb,stroke-width:4px,color:#fff,font-weight:bold
    style REASONING fill:#7c3aed,stroke:#6d28d9,stroke-width:4px,color:#fff,font-weight:bold
    style TOOLS fill:#ea580c,stroke:#c2410c,stroke-width:4px,color:#fff,font-weight:bold
    style MEMORY fill:#0d9488,stroke:#0f766e,stroke-width:4px,color:#fff,font-weight:bold
    style ACTIONS fill:#059669,stroke:#047857,stroke-width:4px,color:#fff,font-weight:bold

    classDef inputStyle fill:#3b82f6,stroke:#2563eb,stroke-width:3px,color:#fff,font-size:14px
    classDef reasoningStyle fill:#7c3aed,stroke:#6d28d9,stroke-width:3px,color:#fff,font-size:14px
    classDef toolStyle fill:#ea580c,stroke:#c2410c,stroke-width:3px,color:#fff,font-size:14px
    classDef memoryStyle fill:#0d9488,stroke:#0f766e,stroke-width:3px,color:#fff,font-size:14px
    classDef actionStyle fill:#059669,stroke:#047857,stroke-width:3px,color:#fff,font-size:14px

    class I1,I2,I3,I4 inputStyle
    class R1,R2,R3,R4 reasoningStyle
    class T1,T2,T3,T4 toolStyle
    class M1,M2,M3,M4 memoryStyle
    class A1,A2,A3,A4 actionStyle
```


### When to use an AI agent?

AI agents are suitable for applications that require autonomous decision-making, ad hoc planning, trial-and-error exploration, and conversation-based user interactions. They are particularly useful for scenarios where the input task is unstructured and cannot be easily defined in advance.
Here are some common scenarios where AI agents excel:

- **Customer Support:** AI agents can handle multi-modal queries (text, voice, images) from customers, use tools to look up information, and provide natural language responses.
- **Education and Tutoring:** AI agents can leverage external knowledge bases to provide personalized tutoring and answer student questions.
- **Code Generation and Debugging:** For software developers, AI agents can assist with implementation, code reviews, and debugging by using various programming tools and environments.
- **Research Assistance:** For researchers and analysts, AI agents can search the web, summarize documents, and piece together information from multiple sources.

The key is that AI agents are designed to operate in a dynamic and underspecified setting, where the exact sequence of steps to fulfill a user request is not known in advance and might require exploration and close collaboration with users.
### When not to use an AI agent?

AI agents are not well-suited for tasks that are highly structured and require strict adherence to predefined rules. If your application anticipates a specific kind of input and has a well-defined sequence of operations to perform, using AI agents might introduce unnecessary uncertainty, latency, and cost.

**If you can write a function to handle the task, do that instead of using an AI agent. You can use AI to help you write that function.**

A single AI agent might struggle with complex tasks that involve multiple steps and decision points. Such tasks might require a large number of tools (for example, over 20), which a single agent cannot feasibly manage.

In these cases, consider using workflows instead.

## Workflows
### What is a Workflow?

A workflow can express a predefined sequence of operations that can include AI agents as components while maintaining consistency and reliability. Workflows are designed to handle complex and long-running processes that might involve multiple agents, human interactions, and integrations with external systems.
The execution sequence of a workflow can be explicitly defined, allowing for more control over the execution path. The following diagram illustrates an example of a workflow that connects two AI agents and a function:

```mermaid
%%{init: {'theme':'base', 'themeVariables': {'fontSize':'16px'}}}%%

graph LR
    Start([User Input])
    Func1["FUNCTION<br/>────────<br/>Data Fetching<br/>• REST API calls<br/>• Database queries<br/>• External data sources"]
    Agent1["AI AGENT 1<br/>────────<br/>Research Agent<br/>• Analyzes request<br/>• Searches knowledge base<br/>• Gathers information"]
    Func2["FUNCTION<br/>────────<br/>Data Processing<br/>• Validates data<br/>• Transforms format<br/>• Applies business rules"]
    Agent2["AI AGENT 2<br/>────────<br/>Response Agent<br/>• Synthesizes findings<br/>• Generates response<br/>• Formats output"]
    End([User Output])
    
    Start -->|"1. Initial Request"| Func1
    Func1 -->|"2. Fetched Data"| Agent1
    Agent1 -->|"3. Analyzed Data"| Func2
    Func2 -->|"4. Processed Data"| Agent2
    Agent2 -->|"5. Final Response"| End
    
    style Start fill:#3b82f6,stroke:#2563eb,stroke-width:3px,color:#ffffff,font-weight:bold
    style Func1 fill:#f97316,stroke:#ea580c,stroke-width:4px,color:#ffffff,font-weight:bold
    style Agent1 fill:#8b5cf6,stroke:#7c3aed,stroke-width:4px,color:#ffffff,font-weight:bold
    style Func2 fill:#14b8a6,stroke:#0d9488,stroke-width:4px,color:#ffffff,font-weight:bold
    style Agent2 fill:#ec4899,stroke:#db2777,stroke-width:4px,color:#ffffff,font-weight:bold
    style End fill:#10b981,stroke:#059669,stroke-width:3px,color:#ffffff,font-weight:bold
    
    linkStyle 0 stroke:#3b82f6,stroke-width:3px
    linkStyle 1 stroke:#f97316,stroke-width:3px
    linkStyle 2 stroke:#8b5cf6,stroke-width:3px
    linkStyle 3 stroke:#14b8a6,stroke-width:3px
    linkStyle 4 stroke:#ec4899,stroke-width:3px
```

Workflows can also express dynamic sequences using conditional routing, model-based decision making, and concurrent execution. This is how multi-agent orchestration patterns are implemented. The orchestration patterns provide mechanisms to coordinate multiple agents to work on complex tasks that require multiple steps and decision points, addressing the limitations of single agents.

### What problems do Workflows solve?

Workflows provide a structured way to manage complex processes that involve multiple steps, decision points, and interactions with various systems or agents. The types of tasks workflows are designed to handle often require more than one AI agent.

Here are some of the key benefits of Agent Framework workflows:

- **Modularity:** Workflows can be broken down into smaller, reusable components, making it easier to manage and update individual parts of the process.
- **Agent Integration:** Workflows can incorporate multiple AI agents alongside non-agentic components, allowing for sophisticated orchestration of tasks.
- **Type Safety:** Strong typing ensures messages flow correctly between components, with comprehensive validation that prevents runtime errors.
- **Flexible Flow:** Graph-based architecture allows for intuitive modeling of complex workflows with executors and edges. Conditional routing, parallel processing, and dynamic execution paths are all supported.
- **External Integration:** Built-in request/response patterns enable seamless integration with external APIs and support human-in-the-loop scenarios.
- **Checkpointing:** Save workflow states via checkpoints, enabling recovery and resumption of long-running processes on the server side.
- **Multi-Agent Orchestration:** Built-in patterns for coordinating multiple AI agents, including sequential, concurrent, hand-off, and Magentic.
- **Composability:** Workflows can be nested or combined to create more complex processes, allowing for scalability and adaptability.






