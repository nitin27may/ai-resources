"""Lab 10 — the production concerns, shown by breaking them.

Everything so far assumed tools succeed, runs finish, and nobody is paying.
Production removes all three assumptions. This lab demonstrates the failure
each one causes, then the fix -- mostly without calling a model, because these
are engineering problems and they reproduce deterministically.

Run:  python3 labs/10-production/lab.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from _shared import banner  # noqa: E402

banner("1. A tool that fails intermittently")

ORDERS = []
attempt = {"n": 0}


def create_order_flaky(sku, qty):
    """Fails on the first call, succeeds on the second. Exactly what a network
    blip, a lock timeout, or a rate limit looks like from your side."""
    attempt["n"] += 1
    ORDERS.append({"sku": sku, "qty": qty})     # the write lands...
    if attempt["n"] == 1:
        raise TimeoutError("upstream timed out after 30s")   # ...then the ack is lost
    return {"order_id": f"RO-{len(ORDERS)}"}


print("""
  The dangerous case is not 'the call failed'. It is 'the call succeeded and
  the acknowledgement was lost'. From the caller, those are identical.
""")

print("  naive retry:")
try:
    create_order_flaky("ABC-1", 22)
except TimeoutError as e:
    print(f"    attempt 1 -> TimeoutError: {e}")
    print("    retrying...")
    r = create_order_flaky("ABC-1", 22)
    print(f"    attempt 2 -> {r}")

print(f"\n    orders actually created: {len(ORDERS)}")
for o in ORDERS:
    print(f"      {o}")
print(f"    *** the customer was charged twice ***\n" if len(ORDERS) > 1 else "")

banner("2. The fix: idempotency, not fewer retries")

ORDERS2 = {}
attempt2 = {"n": 0}


def create_order_idempotent(sku, qty, idempotency_key):
    """The key is chosen by the CALLER and is stable across retries. The server
    stores the result against it, so a repeat returns the original rather than
    doing the work twice."""
    attempt2["n"] += 1
    if idempotency_key in ORDERS2:
        return {**ORDERS2[idempotency_key], "replayed": True}
    result = {"order_id": f"RO-{len(ORDERS2)+1}", "sku": sku, "qty": qty}
    ORDERS2[idempotency_key] = result
    if attempt2["n"] == 1:
        raise TimeoutError("upstream timed out after 30s")
    return result


key = "restock:ABC-1:2026-08-21:22"
print(f"\n  idempotency key: {key}\n")
try:
    create_order_idempotent("ABC-1", 22, key)
except TimeoutError as e:
    print(f"    attempt 1 -> TimeoutError: {e}")
    print("    retrying with the SAME key...")
    r = create_order_idempotent("ABC-1", 22, key)
    print(f"    attempt 2 -> {r}")
print(f"\n    orders actually created: {len(ORDERS2)}   <- retry was safe\n")

banner("3. Retry policy: what to retry, and what never to")

CASES = [
    ("timeout / connection reset", True, "transient, the operation may not have run"),
    ("429 rate limited", True, "transient, back off and respect Retry-After"),
    ("500 / 503 from upstream", True, "transient"),
    ("400 malformed request", False, "deterministic — retrying sends the same bad request"),
    ("401 / 403 auth failure", False, "deterministic — fix the credential, do not hammer"),
    ("422 business rule violation", False, "the answer will not change"),
    ("model produced a bad tool call", False, "return it as context; the MODEL retries, not you"),
]
print()
print(f"  {'condition':<34} {'retry?':<8} why")
for cond, retry, why in CASES:
    print(f"  {cond:<34} {'yes' if retry else 'NO':<8} {why}")
print("""
  Exponential backoff with jitter, and a cap. Without jitter, everything that
  failed together retries together and you rebuild the thundering herd you were
  recovering from.""")

banner("4. Budgets, and the number that surprises people")

print("""
  From lab 08, measured: a two-turn agent run sent 224 prompt tokens on the
  first call and 563 across the run. Context is resent every turn, so cost
  grows with the SQUARE of turn count.

  Published multipliers, relative to a plain chat interaction:""")
print("""
    a single agent            ~4x tokens
    a small agent team        ~7x
    a full multi-agent system ~15x

  And the same vendor's later guidance revised the multi-agent figure DOWN to
  3-10x while narrowing when it is justified at all: context protection,
  genuine parallelism, or real specialisation. Outside those, coordination cost
  usually exceeds the benefit.

  Enforce four ceilings in code, not in the prompt:""")
for b, what in [("turns", "a confused model that will not stop"),
                ("tokens", "context silently truncating (module 6)"),
                ("money", "per-run and per-tenant spend"),
                ("wall clock", "a hung tool call")]:
    print(f"    {b:<12} {what}")

banner("5. What production adds that a demo never needs")

for item, why in [
    ("Idempotency keys", "retries are inevitable; duplicates must not be"),
    ("Circuit breakers", "stop calling a dependency that is already down"),
    ("Rate limiting", "per-tenant, or one user's loop starves everyone"),
    ("Graceful degradation", "answer without the tool rather than fail the request"),
    ("Structured logs + traces", "you cannot debug a non-deterministic system from a stack trace"),
    ("Cost attribution", "per tenant and per feature, or you cannot price it"),
    ("Replay fixtures", "deterministic CI that costs nothing per run"),
    ("A kill switch", "disable an agent without a deploy"),
]:
    print(f"  {item:<26} {why}")

banner("What you just learned")
print("""
  - The dangerous failure is not the call that failed. It is the call that
    succeeded while the acknowledgement was lost. Idempotency is what makes
    that survivable, and the key must be chosen by the caller.

  - Retry only what is transient. A 400 will still be a 400. A bad tool call
    from the model is not your retry -- return it as context and let the model
    correct itself, as in module 5.

  - Cost is quadratic in turns and multiplied again by agent count. Budget in
    code, at four ceilings, because none of them are things a prompt can hold.

  - Everything here is ordinary distributed-systems engineering. The agent part
    is not what makes it hard; the non-determinism only means your tests need
    fixtures and your logs need traces.
""")
