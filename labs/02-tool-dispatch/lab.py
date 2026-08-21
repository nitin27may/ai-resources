"""Lab 02 — tool calling, dispatched by hand.

Goal: see that "the model called a function" is a fiction. The model emits a
structured *request*. Nothing happens until your code decides to run it.

Run:  python3 labs/02-tool-dispatch/lab.py
"""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from _shared import chat, banner, MODEL  # noqa: E402

# ---------------------------------------------------------------- the tool
# A tool is two things that must agree: a JSON Schema the model reads, and a
# function you run. Nothing enforces that they match. If they drift, the model
# sends arguments your function does not accept, and you get a runtime error
# the model never sees.
STOCK = {"ABC-1": {"on_hand": 3, "reorder_point": 25}}

TOOLS = [{
    "type": "function",
    "function": {
        "name": "get_stock",
        "description": "Look up on-hand quantity and reorder point for a SKU.",
        "parameters": {
            "type": "object",
            "properties": {"sku": {"type": "string", "description": "e.g. ABC-1"}},
            "required": ["sku"],
        },
    },
}]


def get_stock(sku):
    """The actual implementation. The model cannot call this. Only you can."""
    return STOCK.get(sku, {"error": f"unknown sku {sku}"})


banner(f"Asking {MODEL} something it cannot answer without a tool")

messages = [{"role": "user", "content": "How many units of ABC-1 do we have in stock?"}]
reply = chat(messages, tools=TOOLS)

if not reply.get("tool_calls"):
    print(f"\nThe model answered directly instead of calling a tool:\n  {reply['content']}\n")
    print("That is the quiet failure mode. A model with weak tool support will")
    print("invent a number rather than admit it needs to look one up.\n")
    raise SystemExit(1)

# ------------------------------------------------------- what came back
call = reply["tool_calls"][0]
print("\nThe model did NOT run anything. It returned a request:\n")
print(json.dumps(call, indent=2))

name = call["function"]["name"]
args = json.loads(call["function"]["arguments"] or "{}")
print(f"\n  name      : {name}")
print(f"  arguments : {args}   <- a string the model wrote; parse and validate it")

# -------------------------------------------------------- you dispatch it
banner("Now YOU run it and hand the result back")

result = get_stock(**args)          # the dispatch step -- this is the whole trick
print(f"\n  {name}({args}) -> {result}")

messages.append(reply)
messages.append({
    "role": "tool",
    "tool_call_id": call.get("id", "call_0"),
    "content": json.dumps(result),   # results go back as a string, always
})

final = chat(messages, tools=TOOLS)
print(f"\nWith the result in context, the model answers:\n  {final['content']}\n")

banner("What you just learned")
print("""
  - "Function calling" is a request/response protocol, not execution. The
    model emits {name, arguments}; your code decides whether to run it.
  - Arguments arrive as a JSON *string*. Parse it. Validate it. The model is
    not bound by your schema -- it is only guided by it.
  - The result goes back as a role:"tool" message, and the model then gets a
    turn it did not have before.
  - That last part is the seed of the agent loop: one tool result can create
    the need for another call. Lab 03 turns this into a loop.
""")
