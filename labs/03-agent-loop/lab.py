"""Lab 03 — the agent loop, hand-built.

Goal: write the loop yourself, in about 30 lines, so that when you later read
`agent.run()` in any framework you recognise exactly what it is doing.

The task needs TWO tool calls, and the second one's arguments depend on what
the first one returned. That dependency is the whole reason a loop exists --
a single request/response cannot express it.

Run:  python3 labs/03-agent-loop/lab.py
"""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from _shared import chat, banner, MODEL  # noqa: E402

STOCK = {"ABC-1": {"on_hand": 3, "reorder_point": 25}}
ORDERS = []

TOOLS = [
    {"type": "function", "function": {
        "name": "get_stock",
        "description": "Look up on-hand quantity and reorder point for a SKU.",
        "parameters": {"type": "object",
                       "properties": {"sku": {"type": "string"}},
                       "required": ["sku"]}}},
    {"type": "function", "function": {
        "name": "create_restock_order",
        "description": "Order more units of a SKU.",
        "parameters": {"type": "object",
                       "properties": {"sku": {"type": "string"},
                                      "quantity": {"type": "integer"}},
                       "required": ["sku", "quantity"]}}},
]


def get_stock(sku):
    return STOCK.get(sku, {"error": f"unknown sku {sku}"})


def create_restock_order(sku, quantity):
    if sku not in STOCK:
        return {"error": f"unknown sku {sku}"}
    if quantity <= 0:
        # Errors are context, not exceptions. Hand them back so the model can
        # correct itself -- raising here would end the run with a traceback
        # the model never sees and cannot learn from.
        return {"error": "quantity must be positive"}
    ORDERS.append({"sku": sku, "quantity": quantity})
    return {"order_id": f"RO-{len(ORDERS)}", "sku": sku, "quantity": quantity}


REGISTRY = {"get_stock": get_stock, "create_restock_order": create_restock_order}

MAX_TURNS = 6          # without this, a confused model loops until you run out of money


def run_agent(goal):
    messages = [
        {"role": "system", "content":
         "You are an inventory agent. Use the tools. Restock exactly up to the\n"
         "reorder point. Always answer in English."},
        {"role": "user", "content": goal},
    ]

    for turn in range(1, MAX_TURNS + 1):
        reply = chat(messages, tools=TOOLS)          # 1. think
        messages.append(reply)

        calls = reply.get("tool_calls") or []
        if not calls:                                 # 4. no tool wanted -> done
            print(f"\n  turn {turn}: final answer")
            return reply["content"]

        for call in calls:                            # 2. act
            name = call["function"]["name"]
            args = json.loads(call["function"]["arguments"] or "{}")
            fn = REGISTRY.get(name)
            if fn is None:
                result = {"error": f"no such tool: {name}"}
            else:
                try:
                    result = fn(**args)
                except TypeError as e:
                    result = {"error": f"bad arguments: {e}"}
            print(f"  turn {turn}: {name}({args}) -> {result}")

            messages.append({                         # 3. observe
                "role": "tool",
                "tool_call_id": call.get("id", f"call_{turn}"),
                "content": json.dumps(result),
            })
        # loop back to 1, now with the result in context

    return "[stopped: hit the turn limit without finishing]"


banner(f"Running the loop against {MODEL}")
print("\n  on_hand=3, reorder_point=25  ->  a correct agent orders 22\n")

answer = run_agent("SKU ABC-1 is running low. Check it and restock to the reorder point.")

print(f"\n  {answer}\n")
print(f"  orders placed: {ORDERS}")
ok = ORDERS == [{"sku": "ABC-1", "quantity": 22}]
print(f"  VERDICT: {'PASS' if ok else 'FAIL — see below'}\n")

banner("What you just learned")
print("""
  The whole loop is four steps:  think -> act -> observe -> repeat,
  and it exits when the model returns content instead of a tool call.

  Everything a framework adds sits around those four steps:
    - MAX_TURNS            a budget, so a confused model cannot run forever
    - REGISTRY             name -> function; the model never touches your code
    - errors as results    returned into context, not raised out of the loop
    - the messages list    grows every turn -- this is what fills your context

  If the verdict said FAIL, that is worth sitting with. The loop is correct;
  the model got the arithmetic or the sequence wrong. That gap -- correct
  harness, unreliable model -- is what evaluation (module 11) exists to
  measure, and it does not go away by adding a framework.
""")
