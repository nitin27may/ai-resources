---
description: Prompting techniques that still earn their keep, and the ones models made redundant.
tags:
  - Understand
  - Prompting
---

# Prompting

!!! abstract "Understand · 30 min · code optional"
    **Before this:** [How models work](foundation-and-models.md)  ·  **After this:** [Retrieval and data](retrieval-and-data.md)
    **Hands-on version:** [1 Tool calling](../02-agents/tool-calling.md)

How you ask changes what you get. **Prompt engineering** is designing the input
so the model produces something accurate and usable, and it remains the
lowest-effort, highest-impact lever on quality.

This page covers what still works, what models have made unnecessary, and the
one thing you should stop doing by hand entirely: asking politely for JSON.

---

## What is prompt engineering?

Prompt engineering is the art and science of crafting instructions (prompts) that get the best possible output from an AI model. It matters because:

- The same model can give vastly different answers depending on how you phrase the question.
- Good prompts reduce hallucinations, improve accuracy, and make interactions more efficient.
- Prompt engineering is the **lowest-effort, highest-impact** way to improve AI application quality.

!!! tip "Prompt engineering is iterative"
    Rarely will your first prompt be perfect. Treat prompts like code — write, test, evaluate, refine. Keep a library of prompts that work well for your use cases.

---

## System prompts

A **system prompt** (also called a system message) is a special instruction that sets the model's behavior, personality, and constraints for the entire conversation. It is typically invisible to the end user.

### What goes in a system prompt

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

!!! warning "System prompts are not security boundaries"
    Users can sometimes bypass system prompt instructions through prompt injection. Do not rely on system prompts alone for access control or sensitive data protection. Use proper application-level security.

---

## Zero-shot vs few-shot learning

### Zero-shot

In **zero-shot** prompting, you ask the model to perform a task without providing any examples. You rely entirely on the model's training to understand what you want.

**Example:**

```text
Classify the following customer feedback as Positive, Negative, or Neutral:

"The product arrived on time and works perfectly. Very happy with my purchase."
```

**Output:** Positive

Zero-shot works well for straightforward tasks where the model's training covers the domain.

### Few-shot

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

!!! tip "How many examples?"
    For most tasks, 2-5 examples are sufficient. More examples improve consistency but consume tokens. Include examples that cover edge cases and the range of expected outputs.

### When to use which

| Approach | Best For | Limitations |
|---|---|---|
| **Zero-shot** | Simple, well-defined tasks; when you want to save tokens | May not follow specific formats or handle edge cases |
| **Few-shot** | Tasks requiring a specific output format; nuanced classification; domain-specific patterns | Uses more tokens; examples must be representative |

---

## Chain of Thought (CoT) prompting

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

### How to trigger CoT

You can trigger chain of thought with simple additions to your prompt:

- "Let's think step by step."
- "Walk me through your reasoning."
- "Show your work."
- "Break this down into steps before answering."

### Reasoning models change this advice

[Reasoning models](foundation-and-models.md#reasoning-models-and-paying-for-thinking)
do this internally, before answering, whether you ask or not. With them, several
long-standing habits become useless or actively harmful.

| Habit | With a standard model | With a reasoning model |
|---|---|---|
| "Let's think step by step" | Helps | Redundant. It is already doing this |
| Many few-shot examples | Helps consistency | Can hurt — vendors advise minimal examples |
| "Show your work" | Useful | You often cannot see it anyway; it is hidden |
| Detailed step-by-step instructions | Helps | Can constrain a better approach it would have found |
| Stating the goal and constraints clearly | Helps | Helps more. This is the whole job now |

The shift is real: with a reasoning model you describe **what** you want and what
counts as correct, and stop prescribing **how**. Check the vendor's guidance for
the specific model, because this is where their advice diverges most.

---

## Structured output: stop asking, start constraining

If your code has to parse the answer, do not ask for JSON in the prompt and hope.
This is the single largest reliability upgrade available in prompting, and it is
the part most guides still get wrong.

There are three levels, and they are not equivalent.

| Level | What it is | Failure mode |
|---|---|---|
| **Ask nicely** | "Respond in JSON with fields x and y" | Works most of the time. Fails with prose around the JSON, a trailing comma, a code fence, or a chatty preamble — and fails unpredictably, so it survives testing |
| **JSON mode** | A provider flag guaranteeing syntactically valid JSON | You get valid JSON. You do not get *your* JSON: fields can be missing, renamed or the wrong type |
| **Schema-constrained** | You supply a JSON Schema; the decoder is restricted so only conforming output can be produced | The shape is guaranteed by construction. The *values* can still be wrong |

The third is what you want, and every major provider now supports it, usually
called structured outputs or response format. It works by constraining
generation itself: at each step, tokens that would break the schema are not
available to be chosen. The model cannot emit malformed output because there is
no path to it.

!!! warning "A valid schema is not a correct answer"
    Constrained decoding guarantees the *shape*, never the *content*. A response
    can conform perfectly and still invent a customer ID, misread a total, or
    confidently fill a required field it had no basis for.

    Schema validation replaces parsing errors with silent wrong answers, which
    are harder to spot. You still need validation of the values — ranges,
    referential checks, enumerations — and you still need
    [evaluation](../02-agents/evaluation.md).

Three practical notes:

- **Describe your fields.** Schemas carry descriptions, and models read them.
  `{"type": "string", "description": "ISO 4217 currency code, e.g. GBP"}` gets
  you far better results than a bare string field.
- **Prefer enums to free text** wherever the set of answers is known. It removes
  a whole class of near-miss values like "Positive." or "positive sentiment".
- **Make refusal representable.** If the model cannot answer, it should have a
  legitimate way to say so within the schema — a nullable field, or a status
  enum with `insufficient_information`. Otherwise a strict schema forces it to
  invent something, and you have used a reliability feature to manufacture a
  hallucination.

The same mechanism underlies tool calling: a tool definition is a schema, and
the model's request to call it is schema-constrained output.
[Tool calling](../02-agents/tool-calling.md) builds one by hand, and
[Structured output](../02-agents/structured-output.md) measures all three levels
against each other — including the run where a required field the message never
mentioned was invented on every attempt, on two different providers.

---

## Where things go in the prompt

Position matters, for two independent reasons.

**Attention is uneven.** Models attend most reliably to the beginning and the
end of a long input and least reliably to the middle — the "lost in the middle"
effect. If an instruction must be followed, do not bury it in the centre of
forty pages of context. Putting the task after the documents, or repeating it at
the end, measurably helps.

**Caching depends on prefix stability.** Providers cache a prompt prefix and
charge less for reuse, but only while the prefix matches exactly. That gives a
clear ordering:

1. System prompt and rules — never change
2. Tool definitions — rarely change
3. Reference documents — change occasionally
4. Conversation history — grows
5. The current question — changes every turn

Most stable first, most volatile last. Insert one changing token near the front —
a timestamp, a session ID, a "today's date" line — and the cache misses on every
call. It is a common and expensive mistake.

---

## Grounding techniques

**Grounding** means anchoring the model's responses in specific, provided information rather than letting it rely on its general training data. This reduces hallucinations and improves accuracy.

### Common grounding techniques

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

## Best practices for effective prompts

### 1. Be specific

| Vague | Specific |
|---|---|
| "Tell me about Azure" | "Explain the key differences between Azure App Service and Azure Container Apps for deploying web applications" |
| "Write code" | "Write a Python function that takes a list of integers and returns the two numbers that sum to a target value" |

### 2. Provide structure

Tell the model exactly what format you want:

```text
Analyze the following log entry and respond with:
- Severity: (Critical / Warning / Info)
- Component: (which system component is affected)
- Summary: (one sentence describing the issue)
- Recommended Action: (what to do next)
```

### 3. Use delimiters

Separate different parts of your prompt clearly:

```text
### Instructions
Summarize the following article in 3 bullet points.

### Article
[article text here]

### Output Format
Return a JSON array of strings, each containing one bullet point.
```

### 4. Assign a role

Give the model a persona that matches your need:

```text
You are a senior database administrator with 15 years of experience
in PostgreSQL performance tuning. The user will describe a slow query
and you will provide optimization recommendations.
```

### 5. Specify what NOT to do

Models sometimes need explicit negative instructions:

```text
- Do NOT include code examples unless specifically asked.
- Do NOT apologize or use filler phrases like "Great question!"
- Do NOT make assumptions about the user's technical level.
```

!!! warning "Negative instructions are the weaker tool"
    "Do not mention pricing" puts pricing in the context and asks the model to
    avoid it, which works less reliably than describing what to do instead:
    "If asked about cost, direct the user to the pricing page."

    Use negatives for genuinely open-ended prohibitions where no positive
    framing exists, and prefer a positive rule whenever one does. Where a
    prohibition actually matters — money, deletion, data leaving the system —
    it belongs in code, not in the prompt. See
    [safety](safety-and-responsible-ai.md).

---

## Prompts are code, so treat them like code

The page said this at the top. Here is what it actually means, because "iterate
on your prompts" is where most teams stop and it is not enough.

**Version them.** A prompt is program logic. Keep it in source control, not in a
database row or a colleague's notebook, so a behaviour change has a diff and an
author.

**Never edit a live prompt to fix one complaint.** It is the equivalent of
patching production without a test. One user's problem becomes everyone's
regression, and nobody notices because there is nothing measuring the cases that
used to work.

**Keep the failures.** Every bad output is a test case. A collection of twenty
real failures is worth more than any amount of prompt-writing advice, including
this page, because it tells you whether a change helped.

**Change one thing at a time.** Prompts interact. Rewriting the role, adding
three examples and changing the output format together tells you nothing about
which one mattered.

That collection of failures is the beginning of an evaluation set, which is the
subject of [evaluation](../02-agents/evaluation.md) — and the reason a team with
mediocre prompts and good evals beats a team with the reverse.

---

## Common mistakes to avoid

!!! danger "Prompt anti-patterns"

    **Vague instructions**: "Make it better" gives the model no direction. Be specific about what "better" means.

    **Overloading a single prompt**: Asking the model to do five things at once reduces quality on each. Break complex tasks into sequential prompts.

    **Ignoring output format**: If you need JSON, say so. If you need bullet points, say so. Do not assume the model will guess your preferred format.

    **Not testing edge cases**: Your prompt may work for typical inputs but fail on edge cases. Test with unusual, empty, and adversarial inputs.

    **Using ambiguous language**: "Handle errors appropriately" means different things to different people. Specify exactly how errors should be handled.

    **Forgetting to iterate**: The first version of a prompt is a draft, not the final product. Evaluate outputs systematically and refine.

---

## Go deeper

Each vendor documents its own model's quirks. Read the one you are actually using; the general advice overlaps heavily.

- [Anthropic prompt engineering](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview) — the most detailed of the four, and the most transferable.
- [OpenAI prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering) — concise, with reasoning-model guidance that differs from the usual advice.
- [Azure OpenAI prompt engineering](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering) — the same ground with enterprise framing and content-filter behaviour.
- [Google prompting strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies) — Gemini-specific, notably on long context.
