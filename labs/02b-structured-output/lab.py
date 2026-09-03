"""Structured output: ask nicely, JSON mode, or constrain the decoder.

Module: docs/concepts/prompting-and-techniques.md (concept)
        docs/02-agents/tool-calling.md (mechanism)

You are going to measure the three ways of getting parseable output out of a
model, on the same task, and watch two of them fail in different ways.

Then you are going to see the failure that survives all three, which is the one
that matters: a schema guarantees the shape of an answer, never its truth.

    python3 labs/02b-structured-output/lab.py

Works against Ollama, OpenAI or Azure OpenAI. See labs/README.md.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _shared import chat, banner, MODEL, ProviderError  # noqa: E402

TRIALS = 6

# The thing we want back. Note `additionalProperties: false` and the explicit
# `required` list -- strict schema modes need both.
ORDER_SCHEMA = {
    "type": "object",
    "properties": {
        "sku": {"type": "string", "description": "Product code, e.g. ABC-123"},
        "qty": {"type": "integer", "description": "Number of units ordered"},
    },
    "required": ["sku", "qty"],
    "additionalProperties": False,
}

JSON_SCHEMA_FORMAT = {
    "type": "json_schema",
    "json_schema": {"name": "order", "strict": True, "schema": ORDER_SCHEMA},
}

ORDERS = [
    "Hi, can I get 3 units of ABC-123 shipped to the usual address?",
    "please send 12 x QRS-778, urgent",
    "We'd like to reorder the DEF-900s - make it 5 this time. Thanks!",
    "order: 2 of GHI-456",
    "Need 40 units ABC-123 by Friday if possible",
    "Could you put me down for seven JKL-222 units please",
]

# Two prompts, differing in one thing: whether the prompt names the fields.
#
# TOLD is what a careful person writes when nothing enforces the shape.
# UNTOLD is what you write when the *schema* is meant to carry the contract --
# which is the whole point of structured output. Comparing the two is how you
# see what each method actually knows.
TOLD = ("Extract the order from the message below. Respond with a JSON object "
        'with exactly two fields: "sku" (string) and "qty" (integer). '
        "No other text.\n\nMessage: {msg}")

UNTOLD = "Extract the order from this message.\n\nMessage: {msg}"

ASK = TOLD


def validates(text):
    """Does this parse as JSON and match the schema we asked for?"""
    try:
        obj = json.loads(text)
    except Exception:
        return False, "not JSON"
    if not isinstance(obj, dict):
        return False, "not an object"
    missing = [k for k in ("sku", "qty") if k not in obj]
    if missing:
        return False, f"missing {','.join(missing)} (got {list(obj)})"
    if not isinstance(obj.get("qty"), int):
        return False, f"qty is {type(obj['qty']).__name__}, not int"
    if not isinstance(obj.get("sku"), str):
        return False, f"sku is {type(obj['sku']).__name__}, not str"
    return True, obj


def run(label, response_format, prompt_tmpl=ASK):
    """Returns (conforming_count, notes). None means the provider refused."""
    ok, notes = 0, []
    for msg in ORDERS:
        try:
            r = chat([{"role": "user", "content": prompt_tmpl.format(msg=msg)}],
                     response_format=response_format, max_tokens=200)
            good, detail = validates(r["content"])
        except ProviderError as e:
            # Not a model failure -- the provider rejected the option itself.
            # Worth surfacing as a capability difference rather than a score.
            print(f"  {label:<34} refused by provider")
            print(f"       └─ {str(e)[:150]}")
            return None, [str(e)]
        ok += good
        if not good:
            notes.append(detail)
    print(f"  {label:<34} {ok}/{len(ORDERS)} conformed")
    for n in notes[:3]:
        print(f"       └─ {n}")
    return ok, notes


banner(f"Structured output, {len(ORDERS)} extractions per method, model={MODEL}")

print("\nRound 1 -- the prompt spells out the field names.")
print("This is the fair-weather case. Expect most of these to pass.\n")
told_plain = run("prompt only", None, TOLD)[0]
told_json = run("json_object", {"type": "json_object"}, TOLD)[0]
told_schema = run("json_schema", JSON_SCHEMA_FORMAT, TOLD)[0]

print("\nRound 2 -- identical task, but the prompt no longer names the fields.")
print("Only the schema knows the contract now. This is the honest test.\n")
untold_plain = run("prompt only", None, UNTOLD)[0]
untold_json = run("json_object", {"type": "json_object"}, UNTOLD)[0]
untold_schema = run("json_schema", JSON_SCHEMA_FORMAT, UNTOLD)[0]

n = len(ORDERS)
fmt = lambda v: " n/a" if v is None else f"{v}/{n}"
inline = lambda v: "refused" if v is None else f"{v}/{n}"
print(f"""
  method            prompt names fields   prompt does not
  ---------------   -------------------   ---------------
  prompt only             {fmt(told_plain)}                {fmt(untold_plain)}
  json_object             {fmt(told_json)}                {fmt(untold_json)}
  json_schema             {fmt(told_schema)}                {fmt(untold_schema)}
""")
if told_json is None:
    print("  json_object was refused outright. Azure OpenAI rejects it unless the")
    print("  word 'json' appears in the messages -- a provider quirk you would")
    print("  have to discover in production. json_schema has no such condition.\n")

# ---------------------------------------------------------------- the real trap
banner("The failure a schema cannot fix")

VAGUE = "Please send me some more of the ABC-123 when you get a chance."
print(f"\n  Message: {VAGUE!r}")
print("  There is no quantity in that sentence. The schema says qty is a")
print("  required integer, so the model has no legal way to say 'not stated'.\n")

invented = []
for _ in range(TRIALS):
    r = chat([{"role": "user", "content": ASK.format(msg=VAGUE)}],
             response_format=JSON_SCHEMA_FORMAT, max_tokens=200, temperature=1)
    try:
        invented.append(json.loads(r["content"]).get("qty"))
    except Exception:
        invented.append("unparseable")
print(f"  qty across {TRIALS} runs: {invented}")
print("  Every one of those conforms to the schema. Every one is invented.")

# The fix: make "I cannot tell" representable.
SAFE_SCHEMA = {
    "type": "object",
    "properties": {
        "sku": {"type": ["string", "null"]},
        "qty": {"type": ["integer", "null"]},
        "status": {"type": "string", "enum": ["complete", "missing_quantity",
                                              "missing_sku", "not_an_order"]},
    },
    "required": ["sku", "qty", "status"],
    "additionalProperties": False,
}
SAFE_FORMAT = {"type": "json_schema",
               "json_schema": {"name": "order_or_refusal", "strict": True,
                               "schema": SAFE_SCHEMA}}
SAFE_ASK = ("Extract the order from the message. If a field is not stated, set it "
            "to null and set status accordingly. Do not guess.\n\nMessage: {msg}")

print("\n  Now with null allowed and a status enum, so 'not stated' is sayable:\n")
for _ in range(3):
    r = chat([{"role": "user", "content": SAFE_ASK.format(msg=VAGUE)}],
             response_format=SAFE_FORMAT, max_tokens=200, temperature=1)
    print(f"    {r['content'].strip()}")

banner("What you just learned")
print(f"""
  - On an easy task with a careful prompt, all three methods can look fine.
    That is exactly why this is dangerous: prompt-only passes the demo.

  - Take the field names out of the prompt and the difference appears. Only
    json_schema still knows what you wanted ({inline(untold_schema)}); the other two are
    guessing ({inline(untold_plain)} and {inline(untold_json)}). JSON mode guarantees valid JSON,
    never *your* JSON -- where it failed it renamed your fields while staying
    perfectly parseable. A parser accepts that; your code does not.

  - Schema-constrained decoding cannot emit a wrong shape, because tokens that
    would break the schema are never available to be chosen. It is a
    construction guarantee, not a request.

  - Then the part that matters. With a required integer and no quantity in the
    text, the model invented one on every run, and every invention was
    schema-valid. Constraining the decoder did not remove wrong answers. It
    converted noisy parse errors into silent wrong ones.

  - The fix is not a better prompt. It is making refusal representable -- a
    nullable field, a status enum. If the only legal outputs are answers, you
    have arranged for an answer.

  - Descriptions inside the schema do real work. `"ISO 4217 currency code"` on
    a field beats a paragraph of system prompt, because the model reads the
    schema.

  - A tool definition is this same mechanism with another name: the model's
    request to call a tool is schema-constrained output. See module 1.
""")
