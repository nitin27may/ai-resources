---
description: Principles that hold across AI system design, independent of framework or vendor.
tags:
  - Go deeper
  - Patterns
---

# Design principles

!!! abstract "Go deeper · 20 min · no code"
    **Before this:** [Design patterns](design-patterns.md)  ·  **After this:** [Code quality pipeline](code-quality-pipeline.md)
    **Hands-on version:** [3 The harness](../02-agents/the-harness.md)

These are the architectural decisions that decide whether an agent system is
debuggable and operable, independent of framework or vendor. They divide into
two groups.

The first five are ordinary good engineering, and they matter more here than
usual because agent workloads are slow, long-running and cancellable. The
second five have no equivalent in conventional software, because conventional
software does not have a component that can decide to do something you did not
anticipate.

---

## Ordinary principles that matter more here

### 1. Async-first architecture

!!! success "Why async?"
    Agent tasks involve multiple slow operations: LLM API calls (500ms-5s), tool executions (variable), and I/O operations. Without async, your agent sits idle during each call, making multi-agent systems painfully slow.

**Performance impact**

- **Synchronous approach**: A simple 3-agent workflow could take 30 seconds
- **Async approach**: The same workflow takes only 10 seconds with proper concurrency

**Implementation**

We embrace `async/await` throughout because retrofitting async into synchronous code is much harder than the reverse.

---

### 2. Event-based streaming

!!! info "Real-time progress updates"
    Agent tasks can take 30+ seconds to complete multiple steps. Without streaming, users stare at blank screens wondering if anything is happening.

**Benefits**

- **Real-time progress updates**: Users see what's happening as it occurs
- **Responsive user interfaces**: Better user experience with live feedback
- **Enhanced observability**: Supplies the data you need to debug multi-step agent behavior
- **Debugging support**: When an agent gets stuck in a tool call loop, streaming events show you exactly where the problem occurs

---

### 3. Component serialization

!!! abstract "Configuration as code"
    When every component (agents, tools, memory) can serialize itself to JSON, you gain powerful capabilities for configuration management.

**Use cases**

- Save agent configurations for reuse
- Share configurations between team members
- Build visual editors for non-technical users
- Version control complete agent setups
- Build configuration UIs
- Restore agent configuration and state from saved sessions

**Implementation**

All components implement serialization to JSON format, enabling programmatic and visual configuration tools.

---

### 4. Graceful cancellation

!!! warning "User control is critical"
    Users will start long-running agent tasks and then need to cancel them - whether due to incorrect prompts, infinite loops, or to provide feedback.

**Requirements**

- Support for cancellation at any point in execution
- Clean resource cleanup when tasks are cancelled
- Proper state management during cancellation
- User feedback on cancellation status

---

### 5. Abstract base classes with core behaviors

!!! tip "Flexibility and extensibility"
    When you want to support multiple LLM providers, different tool types, or various memory backends, abstract interfaces prevent vendor lock-in and enable testing with mock implementations.

**Benefits**

- **Provider flexibility**: Support multiple LLM providers without code changes
- **Tool extensibility**: Start with simple functions, later add REST API tools, database tools, or emerging standards like MCP tools
- **Testing support**: Use mock implementations for unit testing
- **Future-proofing**: Easily adopt new technologies without architectural changes

**Example**

The `BaseTool` interface lets you start with simple functions and later add REST API tools, database tools, or emerging standards like MCP tools without changing your agent code.

---

## Principles specific to agent systems

### 6. Errors are context; limits are code

The distinction that determines whether an agent is useful or dangerous.

A **recoverable error** is information. A wrong product code, a malformed date,
an empty result — return it to the model as a tool result and let it try again.
Raising an exception here gives you an agent that dies on trivia.

A **limit** is a boundary. A refund above a threshold, a delete on production, a
50,000-unit order. Enforce it in code and refuse. Putting it in the prompt gives
you an agent that can be argued out of it, because a prompt is a suggestion and
a conditional is not.

Confusing the two in either direction produces a characteristic failure:
brittleness one way, and an agent that can be talked into anything the other.

### 7. Budgets, enforced in code

An agent loop has no natural end. The model stops requesting actions, or it does
not. Four budgets, all checked by your code and none by the model:

| Budget | Stops | Without it |
|---|---|---|
| **Steps** | Runaway loops | An agent retrying the same failing call indefinitely |
| **Tokens or cost** | Expensive runs | A single request that costs more than the feature earns |
| **Wall clock** | Hung tasks | Held connections and a user watching a spinner |
| **Per-tool calls** | Repetition | Forty searches when three would do |

Exceeding a budget should end the run with a clear reason, not silently truncate.
Silent truncation is how you get an agent that reports success on a task it
abandoned.

### 8. Idempotency on anything with an effect

A timeout does not tell you whether the work happened. The dangerous failure is
not the call that failed; it is the call that succeeded while the acknowledgement
was lost — because the obvious response, retrying, charges the customer twice.

Give every side-effecting operation an idempotency key derived from the intent
rather than from the attempt, so a retry is recognised as the same request. Then
retrying is safe, and retrying is unavoidable.

### 9. State outside the process

Runs are long, and long things get interrupted: a deploy, a crash, a
rate limit, a human who needs to approve something before the next step.

If the run's state lives only in a variable in a running process, none of that is
survivable and every interruption starts over. Keep the conversation, the
progress and the pending decisions in a store, so a run can be paused, resumed,
inspected while stuck, and continued on a different machine. This is what
"checkpointing" means in the frameworks, and it is why it exists.

### 10. Observability is a prerequisite, not a phase

Ordinary software tells you it failed. An agent produces a confident, plausible,
wrong result and carries on. You cannot answer "why did it do that?" from logs
that record only inputs and outputs.

Every model call, tool invocation, argument and result belongs in a trace,
correlated by run. Instrument it as you build; adding tracing after the first
production incident means having no data about the incident. See
[observability](../02-agents/observability.md).

!!! tip "Push non-determinism to the edges"
    The principle underneath most of the above. Every step where the model
    decides is a step you cannot fully test, cannot exactly reproduce, and must
    evaluate statistically.

    So use the model where judgement is genuinely required, and ordinary code
    everywhere else. A system with three model calls in a deterministic pipeline
    is far easier to operate than one where the model chooses every step — and
    in most cases it does the same job. See
    [deterministic and non-deterministic, mixed](../concepts/agentic-ai.md#deterministic-and-non-deterministic-mixed).

---

## Go deeper

- [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/) — async-first, streaming and serialization as implemented in a production SDK.
- [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview) — checkpointing and resumable state, which is where serialization stops being theoretical.
- [Foundry Agent Service](https://learn.microsoft.com/en-us/azure/foundry/agents/overview) — the managed take on the same lifecycle concerns.
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) — a deliberately small surface area; a useful contrast to the larger frameworks.
- [The harness](../02-agents/the-harness.md) — these principles as something you build and then break on purpose.
