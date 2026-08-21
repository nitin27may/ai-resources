"""Lab 04 — what the loop does when things go wrong.

Lab 03's loop works when the model behaves. This one breaks it on purpose,
four ways, and shows which failures the harness can absorb and which it cannot.

Run:  python3 labs/04-loop-with-recovery/lab.py
"""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from _shared import chat, banner, MODEL  # noqa: E402

STOCK = {"ABC-1": {"on_hand": 3, "reorder_point": 25}}

TOOLS = [
    {"type": "function", "function": {
        "name": "get_stock", "description": "Look up on-hand qty and reorder point for a SKU.",
        "parameters": {"type": "object", "properties": {"sku": {"type": "string"}},
                       "required": ["sku"]}}},
    {"type": "function", "function": {
        "name": "create_restock_order", "description": "Order more units of a SKU.",
        "parameters": {"type": "object",
                       "properties": {"sku": {"type": "string"}, "quantity": {"type": "integer"}},
                       "required": ["sku", "quantity"]}}},
]


def make_tools(orders):
    def get_stock(sku):
        if sku not in STOCK:
            # An unknown SKU is not an exception -- it is information. Returned
            # into context, the model can try a different one. Raised, the run
            # dies with a traceback the model never sees.
            return {"error": f"unknown sku {sku}", "known_skus": list(STOCK)}
        return STOCK[sku]

    def create_restock_order(sku, quantity):
        if sku not in STOCK:
            return {"error": f"unknown sku {sku}"}
        if not isinstance(quantity, int) or quantity <= 0:
            return {"error": f"quantity must be a positive integer, got {quantity!r}"}
        if quantity > 1000:
            # A guardrail the model cannot talk its way past. Some limits belong
            # in code, not in the system prompt.
            return {"error": "quantity exceeds the 1000-unit cap; needs human approval"}
        orders.append({"sku": sku, "quantity": quantity})
        return {"order_id": f"RO-{len(orders)}", "sku": sku, "quantity": quantity}

    return {"get_stock": get_stock, "create_restock_order": create_restock_order}


def run(goal, max_turns=6, verbose=True, system=None):
    orders = []
    registry = make_tools(orders)
    messages = [
        {"role": "system", "content": system or
         "You are an inventory agent. Use the tools. Restock exactly up to the\n"
         "reorder point. If a tool returns an error, read it and correct your\n"
         "next call. Always answer in English."},
        {"role": "user", "content": goal},
    ]
    for turn in range(1, max_turns + 1):
        reply = chat(messages, tools=TOOLS)
        messages.append(reply)
        calls = reply.get("tool_calls") or []
        if not calls:
            return {"answer": reply["content"], "orders": orders, "turns": turn, "stopped": "done"}
        for call in calls:
            name = call["function"]["name"]
            try:
                args = json.loads(call["function"]["arguments"] or "{}")
            except json.JSONDecodeError as e:
                # The model wrote malformed JSON. Tell it so, rather than crashing.
                result = {"error": f"your arguments were not valid JSON: {e}"}
                args = {}
            else:
                fn = registry.get(name)
                if fn is None:
                    result = {"error": f"no such tool: {name}", "available": list(registry)}
                else:
                    try:
                        result = fn(**args)
                    except TypeError as e:
                        result = {"error": f"bad arguments for {name}: {e}"}
            if verbose:
                print(f"    turn {turn}: {name}({args}) -> {result}")
            messages.append({"role": "tool", "tool_call_id": call.get("id", f"c{turn}"),
                             "content": json.dumps(result)})
    return {"answer": None, "orders": orders, "turns": max_turns, "stopped": "turn limit"}


banner(f"Four ways to break the loop  ({MODEL})")

print("\n1. Happy path -- the baseline\n")
r = run("SKU ABC-1 is low. Check it and restock to the reorder point.")
print(f"    orders={r['orders']}  stopped={r['stopped']}")

print("\n2. A SKU that does not exist -- can the model recover from an error result?\n")
r = run("Restock SKU NOPE-9 to its reorder point.")
print(f"    orders={r['orders']}  stopped={r['stopped']}")
print(f"    -> the error went into context; the model had a chance to react")

print("\n3. A request that trips a hard guardrail\n")
# Note the system prompt: the default one says "restock to the reorder point",
# which would make the model quietly correct 50000 down to 22 and the cap would
# never fire. Here it is told to do exactly as asked, so the guardrail is the
# only thing standing in the way.
r = run("Order exactly 50000 units of ABC-1. Do not adjust the number.",
        system="You are an inventory agent. Use the tools. Order exactly the\n"
               "quantity the user asks for. If a tool returns an error, report it\n"
               "to the user. Always answer in English.")
blocked = r["orders"] == []
print(f"    orders={r['orders']}  stopped={r['stopped']}")
print(f"    -> cap held: {blocked}. The limit lives in create_restock_order(),")
print(f"       not in the prompt, so the model cannot be talked past it.")

print("\n4. A budget too small to finish -- what ends the run?\n")
# This task provably needs 3 turns (look up, order, summarise). Giving it 2
# guarantees the limit engages, rather than hoping the model misbehaves.
r = run("SKU ABC-1 is low. Check it and restock to the reorder point.", max_turns=2)
print(f"    turns={r['turns']}  stopped={r['stopped']}  answer={r['answer']}")
print(f"    -> the loop stopped because YOUR budget ran out, not because the")
print(f"       model finished. Without that ceiling nothing would have stopped it.")

banner("What you just learned")
print("""
  The loop from lab 03 is unchanged. Everything added here is the HARNESS:

    errors returned, not raised   the model sees the failure and can correct
    unknown tool -> error result  a hallucinated name cannot crash the run
    malformed JSON -> error       the model wrote it; the model should fix it
    a hard cap in code            some limits must not be negotiable
    a turn limit                  the only defence against a model that will
                                  not stop on its own

  Notice which of these the model can recover from and which it cannot. The
  recoverable ones become context. The unrecoverable ones must be enforced
  outside the model, because a system prompt is guidance, not a boundary.
""")
