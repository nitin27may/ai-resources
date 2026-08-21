"""Lab 05 — watch the context window silently eat your instructions.

Every previous lab appended to `messages` and never worried about size. This
one shows what happens when that list outgrows the model's context window:
nothing. No error, no warning, no field in the response. Just an answer that
has quietly forgotten something you told it.

The trick used here is a canary. The instruction says "end every reply with
ZEBRA-9". If the reply has no ZEBRA-9, the instruction is gone -- and you can
see exactly which shape of overflow removed it.

Run:  python3 labs/05-context-limits/lab.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from _shared import chat, banner, MODEL  # noqa: E402

CANARY = "ZEBRA-9"
RULE = f"Always end every reply with the exact token {CANARY} on its own line."
FILLER = "The quarterly inventory reconciliation notes routine stock movement. "


def probe(label, messages, expect):
    reply = chat(messages, max_tokens=128)
    alive = CANARY in (reply.get("content") or "")
    got = "survived" if alive else "LOST"
    flag = " " if got == expect else "  <-- differs from the reference run"
    print(f"  {label:<46} instruction {got}{flag}")
    return alive


banner(f"Context overflow is silent  ({MODEL})")
print("""
  A canary instruction is planted, then buried under increasing amounts of
  conversation. Nothing below raises an error. The only signal is whether the
  canary comes back.
""")

print("1. Baseline -- short conversation, everything fits\n")
probe("system prompt, 2 messages",
      [{"role": "system", "content": RULE},
       {"role": "user", "content": "Say hello."}], "survived")

print("\n2. One oversized message in the middle\n")
probe("system prompt + a ~10k-token message",
      [{"role": "system", "content": RULE},
       {"role": "user", "content": FILLER * 500},
       {"role": "assistant", "content": "Noted."},
       {"role": "user", "content": "Say hello."}], "survived")
print("     the huge message was dropped whole; the system prompt was spared")

print("\n3. The same, but the rule lives in an early USER message\n")
probe("rule as user turn 1, then a ~10k-token message",
      [{"role": "user", "content": f"Remember this rule: {RULE}"},
       {"role": "assistant", "content": "Understood."},
       {"role": "user", "content": FILLER * 500},
       {"role": "assistant", "content": "Noted."},
       {"role": "user", "content": "Say hello."}], "LOST")
print("     an instruction in the history is not protected the way a system")
print("     prompt is -- this is why agents put rules in the system message")

print("\n4. The agent case: many small turns that add up\n")
msgs = [{"role": "system", "content": RULE}]
for i in range(120):
    msgs.append({"role": "user", "content": f"Note {i}: " + "stock movement recorded. " * 12})
    msgs.append({"role": "assistant", "content": f"Logged {i}."})
msgs.append({"role": "user", "content": "Say hello."})
probe(f"system prompt + {len(msgs) - 1} accumulated messages", msgs, "LOST")
print("     nothing here is oversized on its own. 120 harmless turns of tool")
print("     results did it -- and this time the system prompt went too")

banner("Now fix it: keep the instruction, drop the middle")


def compact(messages, keep_recent=6):
    """The cheapest possible compaction: hold the system prompt, keep the most
    recent turns, and replace everything between with one summary line. Real
    implementations summarise with a model call; the shape is identical."""
    system = [m for m in messages if m["role"] == "system"]
    body = [m for m in messages if m["role"] != "system"]
    if len(body) <= keep_recent:
        return messages
    dropped = len(body) - keep_recent
    note = {"role": "user",
            "content": f"[{dropped} earlier messages summarised: routine stock "
                       f"movement notes, all logged, nothing outstanding.]"}
    return system + [note] + body[-keep_recent:]


small = compact(msgs)
print(f"\n  {len(msgs)} messages -> {len(small)} after compaction\n")
probe("same conversation, compacted", small, "survived")

banner("What you just learned")
print("""
  - Overflow is silent. No exception, no warning, no flag in the response.
    The only reliable signal is comparing usage.prompt_tokens against what you
    believe you sent -- if the server's number is far lower, you were truncated.

  - What gets dropped depends on the shape of the overflow, not just the size:
      one oversized message  -> that message goes, system prompt survives
      many accumulated turns -> the front of the list goes, system prompt too

  - Case 4 is the agent case. No single message was large. 120 turns of
    ordinary tool results were enough, and an agent loop generates those
    without anyone deciding to.

  - Compaction is not clever. Hold what must survive, keep what is recent,
    summarise the middle. Deciding *what must survive* is the actual work,
    and that is context engineering.
""")
