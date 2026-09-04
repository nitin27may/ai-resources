"""Lab 08 — trace an agent run, and find where the tokens actually go.

Evaluation tells you THAT a run failed. Tracing tells you WHERE, and what it
cost. This lab builds a minimal tracer -- about 30 lines -- around the agent
from lab 03, then reports the thing most people have never measured: how many
tokens a short agent run really costs, versus how much unique text was in it.

Run:  python3 labs/08-tracing/lab.py
"""
import json, sys, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from _shared import chat, banner, MODEL, last_usage  # noqa: E402

# ------------------------------------------------------------- the tracer
SPANS = []


class span:
    """A span is a named, timed, nested interval with attributes. That is the
    whole data model behind every tracing tool -- OpenTelemetry included."""

    def __init__(self, name, kind, **attrs):
        self.rec = {"name": name, "kind": kind, "depth": len([s for s in SPANS if s.get("open")]),
                    "attrs": attrs, "open": True}

    def __enter__(self):
        self.rec["t0"] = time.time()
        SPANS.append(self.rec)
        return self.rec

    def __exit__(self, *exc):
        self.rec["ms"] = int((time.time() - self.rec["t0"]) * 1000)
        self.rec["open"] = False
        return False


# ---------------------------------------------------------------- the agent
STOCK = {"ABC-1": {"on_hand": 3, "reorder_point": 25}}
TOOLS = [
    {"type": "function", "function": {
        "name": "get_stock", "description": "On-hand qty and reorder point for a SKU.",
        "parameters": {"type": "object", "properties": {"sku": {"type": "string"}},
                       "required": ["sku"]}}},
    {"type": "function", "function": {
        "name": "create_restock_order", "description": "Order more units of a SKU.",
        "parameters": {"type": "object",
                       "properties": {"sku": {"type": "string"}, "quantity": {"type": "integer"}},
                       "required": ["sku", "quantity"]}}},
]
ORDERS = []


def get_stock(sku):
    return STOCK.get(sku, {"error": "unknown sku"})


def create_restock_order(sku, quantity):
    ORDERS.append({"sku": sku, "quantity": quantity})
    return {"order_id": f"RO-{len(ORDERS)}", "sku": sku, "quantity": quantity}


REG = {"get_stock": get_stock, "create_restock_order": create_restock_order}


def run_traced(goal):
    msgs = [
        {"role": "system", "content":
         "You are an inventory agent. Use the tools. Restock exactly up to the\n"
         "reorder point. Always answer in English."},
        {"role": "user", "content": goal},
    ]
    with span("invoke_agent", "agent", model=MODEL) as root:
        for turn in range(1, 7):
            with span(f"chat turn {turn}", "llm") as c:
                reply = chat(msgs, tools=TOOLS)
                c["attrs"].update(last_usage())
            msgs.append(reply)
            calls = reply.get("tool_calls") or []
            if not calls:
                root["attrs"]["turns"] = turn
                return reply.get("content") or ""
            for call in calls:
                name = call["function"]["name"]
                args = json.loads(call["function"]["arguments"] or "{}")
                with span(f"execute_tool {name}", "tool", **args) as t:
                    result = REG[name](**args) if name in REG else {"error": "no tool"}
                    t["attrs"]["result"] = json.dumps(result)[:44]
                msgs.append({"role": "tool", "tool_call_id": call.get("id", "c"),
                             "content": json.dumps(result)})
    return "[turn limit]"


banner(f"Tracing one agent run  ({MODEL})")
answer = run_traced("SKU ABC-1 is running low. Check it and restock to the reorder point.")

# ------------------------------------------------------------- the waterfall
banner("The trace")
print()
for s in SPANS:
    pad = "  " + "    " * s["depth"]
    a = s["attrs"]
    if s["kind"] == "llm":
        extra = f"in={a.get('prompt_tokens','?'):<5} out={a.get('completion_tokens','?')}"
    elif s["kind"] == "tool":
        extra = f"-> {a.get('result','')}"
    else:
        extra = f"turns={a.get('turns','?')}"
    label = (pad + s["name"])[:44]
    print(f"{label:<46}{s['ms']:>6}ms   {extra}")

# --------------------------------------------------------------- the numbers
llm = [s for s in SPANS if s["kind"] == "llm"]
tools = [s for s in SPANS if s["kind"] == "tool"]
total_in = sum(s["attrs"].get("prompt_tokens", 0) for s in llm)
total_out = sum(s["attrs"].get("completion_tokens", 0) for s in llm)
first_in = llm[0]["attrs"].get("prompt_tokens", 0) if llm else 0
wall = SPANS[0]["ms"]
llm_ms = sum(s["ms"] for s in llm)

banner("Where the time and tokens went")
print(f"""
  wall clock          {wall:>7} ms
  in the model        {llm_ms:>7} ms   ({100*llm_ms//max(wall,1)}% of the run)
  in your tools       {sum(s['ms'] for s in tools):>7} ms

  LLM calls           {len(llm):>7}
  prompt tokens       {total_in:>7}   billed on every call
  completion tokens   {total_out:>7}
""")

banner("The number nobody measures")
print(f"""
  The first call sent {first_in} prompt tokens. The run sent {total_in} in total,
  across {len(llm)} calls -- roughly {total_in/max(first_in,1):.1f}x the first call, for a task
  whose actual new content was a handful of tool results.

  That is not waste, it is the mechanism: the conversation is stateless, so
  every turn resends everything before it. Cost grows with the SQUARE of the
  turn count, not linearly -- c*n^2/2 for context growing c per turn.

  Prompt caching changes the price of those resent tokens (typically to about a
  tenth). It does not change the exponent. Teams routinely believe caching
  fixed the scaling problem; it capped the coefficient.
""")

banner("What you just learned")
print("""
  - A trace is a tree of named, timed, nested spans with attributes. That is
    the entire data model. OpenTelemetry's GenAI conventions name the spans
    you saw here: invoke_agent at the root, chat per model call, execute_tool
    per dispatch.

  - Instrument at the boundary you own. Tokens and duration come from the
    provider response; the tree structure comes from your harness. Nothing
    here required the model's cooperation.

  - Token cost is quadratic in turns. If you only look at the last call you
    will badly underestimate a long session.

  - Cost is NOT standardised. OpenTelemetry defines token and duration
    metrics; there is no currency metric, so every platform derives spend from
    its own price table. Portable telemetry does not mean portable cost.

  For the real thing locally: pip install arize-phoenix && phoenix serve
  gives you this waterfall in a UI, over OTLP, with no account and no cloud.
""")
