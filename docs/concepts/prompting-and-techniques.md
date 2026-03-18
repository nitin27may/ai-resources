---
tags:
  - Beginner
  - Concepts
---

# Prompting & Techniques

The quality of output you get from an AI model depends heavily on how you ask. **Prompt engineering** is the practice of designing inputs that guide AI models toward accurate, useful, and relevant responses. This page covers the core techniques, from basic principles to advanced strategies.

---

## What Is Prompt Engineering?

Prompt engineering is the art and science of crafting instructions (prompts) that get the best possible output from an AI model. It matters because:

- The same model can give vastly different answers depending on how you phrase the question.
- Good prompts reduce hallucinations, improve accuracy, and make interactions more efficient.
- Prompt engineering is the **lowest-effort, highest-impact** way to improve AI application quality.

!!! tip "Prompt Engineering Is Iterative"
    Rarely will your first prompt be perfect. Treat prompts like code -- write, test, evaluate, refine. Keep a library of prompts that work well for your use cases.

---

## System Prompts

A **system prompt** (also called a system message) is a special instruction that sets the model's behavior, personality, and constraints for the entire conversation. It is typically invisible to the end user.

### What Goes in a System Prompt

- **Role definition**: "You are a helpful customer service agent for Contoso Electronics."
- **Behavior rules**: "Always respond in formal English. Never discuss competitors."
- **Output format**: "Return your response as a JSON object with fields: answer, confidence, sources."
- **Constraints**: "Only answer questions about our product catalog. For anything else, say you cannot help."
- **Knowledge context**: Key facts the model should always know.

### Example

```text
You are a technical support assistant for Contoso Cloud Services.

Rules:
- Only answer questions about Contoso products and services.
- If you do not know the answer, say "I don't have that information" and suggest contacting support.
- Always include relevant documentation links in your response.
- Never share confidential internal information.
- Respond in a professional but friendly tone.
```

!!! warning "System Prompts Are Not Security Boundaries"
    Users can sometimes bypass system prompt instructions through prompt injection. Do not rely on system prompts alone for access control or sensitive data protection. Use proper application-level security.

---

## Zero-Shot vs Few-Shot Learning

### Zero-Shot

In **zero-shot** prompting, you ask the model to perform a task without providing any examples. You rely entirely on the model's training to understand what you want.

**Example:**

```text
Classify the following customer feedback as Positive, Negative, or Neutral:

"The product arrived on time and works perfectly. Very happy with my purchase."
```

**Output:** Positive

Zero-shot works well for straightforward tasks where the model's training covers the domain.

### Few-Shot

In **few-shot** prompting, you provide a few examples of the desired input-output pattern before asking the model to handle a new input. This "teaches" the model the pattern you expect.

**Example:**

```text
Classify customer feedback as Positive, Negative, or Neutral.

Feedback: "Terrible experience. The item was broken and support was unhelpful."
Classification: Negative

Feedback: "It's okay, nothing special but it does the job."
Classification: Neutral

Feedback: "Absolutely love it! Best purchase I've made this year."
Classification: Positive

Feedback: "The delivery was late but the product quality is excellent."
Classification:
```

**Output:** Positive

!!! tip "How Many Examples?"
    For most tasks, 2-5 examples are sufficient. More examples improve consistency but consume tokens. Include examples that cover edge cases and the range of expected outputs.

### When to Use Which

| Approach | Best For | Limitations |
|---|---|---|
| **Zero-shot** | Simple, well-defined tasks; when you want to save tokens | May not follow specific formats or handle edge cases |
| **Few-shot** | Tasks requiring a specific output format; nuanced classification; domain-specific patterns | Uses more tokens; examples must be representative |

---

## Chain of Thought (CoT) Prompting

**Chain of thought** prompting asks the model to show its reasoning step by step before arriving at an answer. This dramatically improves performance on tasks that require logic, math, or multi-step reasoning.

### Without CoT

```text
Question: A store has 15 apples. It sells 8 in the morning and receives
a shipment of 12 in the afternoon. A customer then buys 6. How many
apples does the store have?

Answer: 13
```

### With CoT

```text
Question: A store has 15 apples. It sells 8 in the morning and receives
a shipment of 12 in the afternoon. A customer then buys 6. How many
apples does the store have?

Let's work through this step by step:
1. Start: 15 apples
2. Sell 8 in the morning: 15 - 8 = 7 apples
3. Receive shipment of 12: 7 + 12 = 19 apples
4. Customer buys 6: 19 - 6 = 13 apples

Answer: 13
```

Both arrive at the same answer in this simple case, but for complex problems, CoT significantly reduces errors because:

- It forces the model to break the problem into manageable steps.
- Each step can be verified independently.
- Errors are easier to spot and diagnose.

### How to Trigger CoT

You can trigger chain of thought with simple additions to your prompt:

- "Let's think step by step."
- "Walk me through your reasoning."
- "Show your work."
- "Break this down into steps before answering."

!!! note "Some Models Have Built-In CoT"
    Models like OpenAI's o1/o3 and DeepSeek R1 automatically use chain of thought reasoning internally. For these models, you do not need to explicitly request step-by-step reasoning -- they do it by default.

---

## Grounding Techniques

**Grounding** means anchoring the model's responses in specific, provided information rather than letting it rely on its general training data. This reduces hallucinations and improves accuracy.

### Common Grounding Techniques

Contextual grounding
:   Include relevant documents, data, or facts directly in the prompt. The model answers based on this provided context.
    ```text
    Based on the following document, answer the user's question.
    Document: [inserted text]
    Question: What is the return policy?
    ```

Citation-based grounding
:   Ask the model to cite specific sources from the provided context.
    ```text
    Answer using only the provided documents. Include [Source: document name]
    after each claim.
    ```

Constraint-based grounding
:   Explicitly tell the model what it should and should not do.
    ```text
    Only use information from the provided context.
    If the answer is not in the context, say "I don't have enough information."
    Do not make up facts.
    ```

---

## Best Practices for Effective Prompts

### 1. Be Specific

| Vague | Specific |
|---|---|
| "Tell me about Azure" | "Explain the key differences between Azure App Service and Azure Container Apps for deploying web applications" |
| "Write code" | "Write a Python function that takes a list of integers and returns the two numbers that sum to a target value" |

### 2. Provide Structure

Tell the model exactly what format you want:

```text
Analyze the following log entry and respond with:
- Severity: (Critical / Warning / Info)
- Component: (which system component is affected)
- Summary: (one sentence describing the issue)
- Recommended Action: (what to do next)
```

### 3. Use Delimiters

Separate different parts of your prompt clearly:

```text
### Instructions
Summarize the following article in 3 bullet points.

### Article
[article text here]

### Output Format
Return a JSON array of strings, each containing one bullet point.
```

### 4. Assign a Role

Give the model a persona that matches your need:

```text
You are a senior database administrator with 15 years of experience
in PostgreSQL performance tuning. The user will describe a slow query
and you will provide optimization recommendations.
```

### 5. Specify What NOT to Do

Models sometimes need explicit negative instructions:

```text
- Do NOT include code examples unless specifically asked.
- Do NOT apologize or use filler phrases like "Great question!"
- Do NOT make assumptions about the user's technical level.
```

---

## Common Mistakes to Avoid

!!! danger "Prompt Anti-Patterns"

    **Vague instructions**: "Make it better" gives the model no direction. Be specific about what "better" means.

    **Overloading a single prompt**: Asking the model to do five things at once reduces quality on each. Break complex tasks into sequential prompts.

    **Ignoring output format**: If you need JSON, say so. If you need bullet points, say so. Do not assume the model will guess your preferred format.

    **Not testing edge cases**: Your prompt may work for typical inputs but fail on edge cases. Test with unusual, empty, and adversarial inputs.

    **Using ambiguous language**: "Handle errors appropriately" means different things to different people. Specify exactly how errors should be handled.

    **Forgetting to iterate**: The first version of a prompt is a draft, not the final product. Evaluate outputs systematically and refine.

---

## References

- [Microsoft Prompt Engineering Guide](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/prompt-engineering)
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
- [Google Prompting Guide](https://ai.google.dev/gemini-api/docs/prompting-strategies)
