"""Lab 07 — measuring an agent, and why one successful run proves nothing.

Lab 03's agent worked. You saw it work. This lab runs the same agent many times
and computes the two metrics that matter for anything non-deterministic:

    pass@k   at least one of k attempts succeeded   (optimistic)
    pass^k   ALL k attempts succeeded               (what a user experiences)

pass^k = p^k under independence, so it collapses fast. A 90%-reliable agent is
57% reliable across 8 turns. That gap is the whole subject of agent evaluation.

Run:  python3 labs/07-eval-passk/lab.py
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
EXPECTED = [{"sku": "ABC-1", "quantity": 22}]   # on_hand 3, reorder point 25


def run_once(temperature):
    """One full agent run. Returns (orders, final_text)."""
    orders = []

    def get_stock(sku):
        return STOCK.get(sku, {"error": f"unknown sku {sku}"})

    def create_restock_order(sku, quantity):
        if sku not in STOCK:
            return {"error": f"unknown sku {sku}"}
        if not isinstance(quantity, int) or quantity <= 0:
            return {"error": "quantity must be a positive integer"}
        orders.append({"sku": sku, "quantity": quantity})
        return {"order_id": f"RO-{len(orders)}", "sku": sku, "quantity": quantity}

    reg = {"get_stock": get_stock, "create_restock_order": create_restock_order}
    msgs = [
        {"role": "system", "content":
         "You are an inventory agent. Use the tools. Restock exactly up to the\n"
         "reorder point. Always answer in English."},
        {"role": "user", "content":
         "SKU ABC-1 is running low. Check it and restock to the reorder point."},
    ]
    for turn in range(6):
        reply = chat(msgs, tools=TOOLS, temperature=temperature)
        msgs.append(reply)
        calls = reply.get("tool_calls") or []
        if not calls:
            return orders, reply.get("content") or ""
        for call in calls:
            name = call["function"]["name"]
            try:
                args = json.loads(call["function"]["arguments"] or "{}")
                result = reg[name](**args) if name in reg else {"error": "no such tool"}
            except Exception as e:
                result = {"error": str(e)}
            msgs.append({"role": "tool", "tool_call_id": call.get("id", "c"),
                         "content": json.dumps(result)})
    return orders, "[turn limit]"


def outcome_correct(orders):
    """Outcome grading: check the world, not what the agent said about it."""
    return orders == EXPECTED


K = 8

banner(f"Running the same agent {K} times  ({MODEL})")
print("""
  Identical task, identical prompt. The only thing that changes is sampling.
""")

results = {}
for temp in (0.0, 0.7):
    print(f"  temperature={temp}")
    runs = []
    for i in range(K):
        orders, _ = run_once(temp)
        ok = outcome_correct(orders)
        runs.append(ok)
        qty = orders[0]["quantity"] if orders else None
        print(f"    run {i+1}: {'pass' if ok else 'FAIL'}   orders={len(orders)} qty={qty}")
    results[temp] = runs
    p = sum(runs) / K
    print(f"    pass@1 (mean) = {p:.2f}   pass@{K} = {1 if any(runs) else 0}   "
          f"pass^{K} = {1 if all(runs) else 0}\n")

banner("What those numbers mean")
p0 = sum(results[0.0]) / K
print(f"""
  pass@1  {p0:.2f}   the number people quote
  pass@{K}    {1 if any(results[0.0]) else 0}      at least one run worked -- almost always 1, almost always useless
  pass^{K}    {1 if all(results[0.0]) else 0}      every run worked -- what a user doing {K} things experiences

  Under independence pass^k = p^k. So even a genuinely good agent decays:

      p = 0.95  ->  pass^8 = {0.95**8:.2f}
      p = 0.90  ->  pass^8 = {0.90**8:.2f}
      p = 0.80  ->  pass^8 = {0.80**8:.2f}

  A "90% accurate" agent fails at least once in roughly 4 of every 10 eight-step
  sessions. Reporting pass@1 alone hides that completely.
""")

banner("Now the judge, and why it needs checking too")
print("""
  Outcome grading above compared the orders list to a known answer -- cheap,
  deterministic, unarguable. Most real tasks have no such check, so people reach
  for an LLM judge. Here is one grading the same runs.
""")

JUDGE = ("You are grading an inventory agent. The stock was 3 units and the reorder "
         "point was 25, so the ONLY correct action is a single restock order of "
         "exactly 22 units. Reply with exactly one word: PASS or FAIL.")

agree = 0

# Judge a fixed set of transcripts, including deliberately wrong ones, so the
# judge's error rate is measurable rather than assumed.
CASES = [
    ("[created restock order RO-1 for 22 units of ABC-1]", True),
    ("[created restock order RO-1 for 25 units of ABC-1]", False),
    ("[created restock order RO-1 for 22 units, then RO-2 for 22 units]", False),
    ("[checked stock: 3 on hand. No order was created.]", False),
    ("[created restock order RO-1 for 22 units of ABC-1, bringing stock to 25]", True),
]
print("  transcript                                              truth  judge")
for text, truth in CASES:
    verdict = chat([{"role": "system", "content": JUDGE},
                    {"role": "user", "content": text}], max_tokens=8).get("content", "")
    jp = "PASS" in verdict.upper()
    ok = jp == truth
    agree += ok
    print(f"  {text[:54]:<54}  {'PASS' if truth else 'FAIL'}   "
          f"{'PASS' if jp else 'FAIL'} {'' if ok else '  <-- WRONG'}")

print(f"\n  judge agreement with ground truth: {agree}/{len(CASES)}")

banner("What you just learned")
all_passed = all(results[0.0]) and all(results[0.7])
if all_passed:
    print("""
  - READ YOUR OWN RESULT FIRST. Every run passed -- and that is a warning about
    this suite, not reassurance about the agent. A task the model never fails
    cannot distinguish a good agent from a bad one and will not catch a
    regression. If your suite is green on the first run, make it harder.
""")
print(f"""
  - One successful run is not evidence. Report pass^k alongside pass@1, or you
    are describing a system nobody experiences.

  - Grade the outcome, not the narration. The agent's summary of what it did is
    generated text; the orders list is fact. Where you can check the world,
    check the world.

  - An LLM judge is an instrument, and instruments need calibration. This one
    scored {agree}/{len(CASES)} -- on cases with unambiguous, checkable answers,
    which is the easy half of the job. Judges degrade on the borderline cases you
    actually care about, where position and verbosity bias bite hardest. Measure
    yours on a labelled set, reporting true-positive and true-negative rates
    separately rather than accuracy, which flatters on imbalanced data.

  - Start with 20-50 tasks drawn from real failures. You do not need hundreds,
    and you do need them to be real.
""")
