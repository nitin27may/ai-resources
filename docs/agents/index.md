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

    
    style Input fill:#667eea,stroke:#5568d3,stroke-width:4px,color:#ffffff,font-weight:bold
    style Reasoning fill:#764ba2,stroke:#5e3a82,stroke-width:4px,color:#ffffff,font-weight:bold
    style Tools fill:#f093fb,stroke:#d946ef,stroke-width:4px,color:#ffffff,font-weight:bold
    style Memory fill:#4facfe,stroke:#0ea5e9,stroke-width:4px,color:#ffffff,font-weight:bold
    style Output fill:#43e97b,stroke:#22c55e,stroke-width:4px,color:#ffffff,font-weight:bold
```

Examples:
```mermaid
graph TB
    subgraph INPUT["INPUT LAYER"]
        style INPUT fill:#FF6B6B,stroke:#C92A2A,stroke-width:3px,color:#fff
        I1["User Queries<br/>Natural language questions<br/>Chat messages"]
        I2["Documents & Files<br/>Images<br/>PDFs<br/>Spreadsheets"]
        I3["External Triggers<br/>Events<br/>Alerts<br/>API calls"]
        I4["Context<br/>Conversation history<br/>User preferences"]
    end

    subgraph REASONING["REASONING ENGINE"]
        style REASONING fill:#4ECDC4,stroke:#0B7285,stroke-width:3px,color:#fff
        R1["Large Language Model<br/>Understands intent<br/>Plans actions"]
        R2["Prompt Engineering<br/>Instructions<br/>Guidelines"]
        R3["Orchestration<br/>Coordinates workflow<br/>Manages multi-step tasks"]
        R4["Decision Making<br/>Selects tools<br/>Routes requests"]
    end

    subgraph TOOLS["TOOLS"]
        style TOOLS fill:#FFD93D,stroke:#F59F00,stroke-width:3px,color:#000
        T1["Code Execution<br/>Run Python code<br/>Data analysis"]
        T2["Search<br/>Document retrieval<br/>Web search"]
        T3["Custom Functions<br/>API calls<br/>Business logic"]
        T4["Integrations<br/>Email<br/>Databases<br/>Third-party services"]
    end

    subgraph MEMORY["MEMORY"]
        style MEMORY fill:#A78BFA,stroke:#7C3AED,stroke-width:3px,color:#fff
        M1["Conversation History<br/>Messages<br/>Thread continuity"]
        M2["Agent State<br/>Configuration<br/>Status tracking"]
        M3["Knowledge Base<br/>Documents<br/>Vector embeddings"]
        M4["File Storage<br/>Uploaded files<br/>Generated outputs"]
    end

    subgraph ACTIONS["ACTIONS/OUTPUTS"]
        style ACTIONS fill:#51CF66,stroke:#2F9E44,stroke-width:3px,color:#fff
        A1["Text Responses<br/>Answers<br/>Summaries<br/>Explanations"]
        A2["Generated Content<br/>Code<br/>Visualizations<br/>Reports"]
        A3["State Changes<br/>Save conversation<br/>Update context"]
        A4["External Actions<br/>Send notifications<br/>Trigger workflows<br/>Update systems"]
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

    %% Styling
    classDef inputStyle fill:#FF6B6B,stroke:#C92A2A,stroke-width:2px,color:#fff
    classDef reasoningStyle fill:#4ECDC4,stroke:#0B7285,stroke-width:2px,color:#fff
    classDef toolStyle fill:#FFD93D,stroke:#F59F00,stroke-width:2px,color:#000
    classDef memoryStyle fill:#A78BFA,stroke:#7C3AED,stroke-width:2px,color:#fff
    classDef actionStyle fill:#51CF66,stroke:#2F9E44,stroke-width:2px,color:#fff

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
    
    style Start fill:#667eea,stroke:#5568d3,stroke-width:3px,color:#ffffff,font-weight:bold
    style Func1 fill:#ff6b6b,stroke:#ee5a6f,stroke-width:4px,color:#ffffff,font-weight:bold
    style Agent1 fill:#f093fb,stroke:#d946ef,stroke-width:4px,color:#ffffff,font-weight:bold
    style Func2 fill:#feca57,stroke:#ff9f43,stroke-width:4px,color:#000000,font-weight:bold
    style Agent2 fill:#48dbfb,stroke:#0abde3,stroke-width:4px,color:#ffffff,font-weight:bold
    style End fill:#1dd1a1,stroke:#10ac84,stroke-width:3px,color:#ffffff,font-weight:bold
    
    linkStyle 0 stroke:#667eea,stroke-width:3px
    linkStyle 1 stroke:#ff6b6b,stroke-width:3px
    linkStyle 2 stroke:#f093fb,stroke-width:3px
    linkStyle 3 stroke:#feca57,stroke-width:3px
    linkStyle 4 stroke:#48dbfb,stroke-width:3px
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






