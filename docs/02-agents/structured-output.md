---
title: Structured output
description: Getting output your code can rely on — and why guaranteeing the shape converts loud failures into quiet ones.
tags:
  - Build
  - Prompting
  - Agents
---

# Structured output

!!! abstract "Build · 45 min · hands-on"
    **Before this:** [1 Tool calling](tool-calling.md)  ·  **After this:** [3 The agent loop](the-agent-loop.md)
    **Overview version:** [Prompting](../concepts/prompting-and-techniques.md#structured-output-stop-asking-start-constraining)

!!! abstract
    Three ways to get parseable output, measured on the same task. Two of them
    work until they do not. The third cannot produce a wrong shape — and that
    turns out to be the beginning of the problem rather than the end of it.

**Prerequisites:** [Tool calling](tool-calling.md) — you have dispatched a tool
call by hand.

**Verified as of 2026-09-02**, against a local Ollama model and Azure OpenAI.

## What you'll be able to do

Choose between prompting, JSON mode and schema-constrained decoding on
evidence; predict which failures each one leaves you with; and design a schema
that does not force the model to invent an answer.

## Why this comes second

You have just seen that a tool call is a `{name, arguments}` request your code
decides to honour. That request is schema-constrained output — the same
mechanism under a different name. Everything here applies to every tool you
will define for the rest of the path.

## The three levels

| Level | Mechanism | Guarantees |
|---|---|---|
| **Prompt only** | You describe the shape in words | Nothing. The model usually complies |
| **JSON mode** | `response_format={"type": "json_object"}` | Syntactically valid JSON |
| **Schema-constrained** | `response_format={"type": "json_schema", ...}` | Output conforms to your schema, by construction |

The third works by restricting generation itself: at each step, tokens that
would break the schema are removed from the candidate set. The model cannot emit
malformed output because there is no path through the grammar to it.

## Build it

```bash
python3 labs/02b-structured-output/lab.py
```

The lab extracts `{sku, qty}` from six messily-worded orders, at each of the
three levels, twice: once with the field names spelled out in the prompt, and
once without. That second round is the honest test, because the whole point of
a schema is that it — not the prose — carries the contract.

## Verify

The first round is unremarkable. On an easy task with a careful prompt, every
method looks fine. Measured on `qwen2.5:14b` locally and `gpt-4.1` on Azure:

| Method | Prompt names the fields | Prompt does not |
|---|---|---|
| Prompt only | 6/6 | **0/6** |
| JSON mode | 6/6 | **0/6** local, refused on Azure |
| Schema-constrained | 6/6 | **6/6** |

Two things to look at.

**JSON mode failed by succeeding.** Its output was valid JSON every time. It
just was not *your* JSON:

```json
{"item": "ABC-123", "quantity": 3, "shipping_address": "the usual address"}
{"product_code": "ABC-123", "quantity": 3, "action": "reorder"}
```

A parser accepts both. Your code does not. This is the failure mode to
remember: JSON mode moves you from "might not be JSON" to "is JSON, might not
be yours", which is harder to detect because it looks like success.

**Azure refused JSON mode outright**, with `'messages' must contain the word
'json' in some form`. A provider condition you would otherwise discover in
production. Schema-constrained mode has no such requirement on either provider.

## The failure a schema cannot fix

Now the part worth the walk. The lab sends one more message:

> Please send me some more of the ABC-123 when you get a chance.

There is no quantity in that sentence. The schema says `qty` is a required
integer, so there is no legal output that means "not stated". Six runs at
temperature 1, on both providers:

```
qty across 6 runs: [1, 1, 1, 1, 1, 1]
```

Every one conforms to the schema. Every one is invented. Constrained decoding
did not remove wrong answers — it removed the *noisy* ones. Before, a malformed
response threw an exception someone would notice. Now a fabricated quantity
flows silently into an order.

!!! danger "Guaranteeing the shape can manufacture a hallucination"
    A strict schema is a set of legal outputs. If none of them means "I cannot
    tell", you have not prevented invention — you have required it.

    This is the single most important thing on this page, and it is the
    opposite of how structured output is usually sold.

## The fix: make refusal representable

Not a better prompt. A better schema.

```python
{
  "sku":    {"type": ["string", "null"]},
  "qty":    {"type": ["integer", "null"]},
  "status": {"type": "string",
             "enum": ["complete", "missing_quantity", "missing_sku", "not_an_order"]}
}
```

Same message, same temperature, and now the honest answer is available:

```json
{"sku": "ABC-123", "qty": null, "status": "missing_quantity"}
```

Three rules that follow:

- **Every schema needs an escape hatch.** A nullable field, a status enum, or a
  discriminated union with a `refusal` branch. Ask of any schema: what does this
  model emit when it does not know?
- **Describe your fields.** Schemas carry descriptions and the model reads them.
  `{"type": "string", "description": "ISO 4217 currency code, e.g. GBP"}` beats
  a paragraph of system prompt, because it sits next to the field it governs.
- **Prefer enums to free text** wherever the answer set is known. It removes
  near-misses like `"Positive."` and `"positive sentiment"` structurally.

## In a framework

Every framework wraps this. Pydantic models in the OpenAI SDK and the Agents
SDK, Zod schemas in the TypeScript ecosystem, and typed tool parameters in
Microsoft Agent Framework all compile to the same JSON Schema and the same
`response_format`. Knowing what they compile *to* is why the failure above is
predictable rather than mysterious.

## In production

- **Validate values, not just shape.** The schema got you a well-formed object.
  Referential checks, ranges and enum membership are still yours: does that SKU
  exist, is that quantity plausible, is that date in the future?
- **Log the refusals.** A rising `missing_quantity` rate is a product signal —
  your intake form, not your model, is probably the problem.
- **Watch for schema drift.** The schema is a contract between your prompt and
  your code. Changing it without changing both sides fails the way any
  interface change fails.
- **Not every provider supports it.** Keep a fallback that parses and validates
  by hand, and treat conformance as something you measure rather than assume.

## Go deeper

- [Prompting](../concepts/prompting-and-techniques.md#structured-output-stop-asking-start-constraining)
  — the same three levels without the code, for readers who are not building.
- [Tool calling](tool-calling.md) — the same mechanism as a tool definition.
- [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
  — the reference for `json_schema`, including the subset of JSON Schema that is
  actually supported.
- [Evaluation](evaluation.md) — because "conforms to the schema" is not a
  quality measure, and you now need one that is.

## Next

[The agent loop](the-agent-loop.md) — put the tool call in a loop and let the
model decide when to stop.
