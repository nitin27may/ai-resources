"""Memory: the model remembers nothing, so memory is software you wrote.

Module: docs/02-agents/memory.md

Context engineering showed you what happens when the window fills: things fall
out. This lab is about where they go instead, and about the failure that makes
memory dangerous rather than merely useful.

    python3 labs/05b-memory/lab.py

Works against Ollama, OpenAI or Azure OpenAI. See labs/README.md.
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _shared import chat, banner, MODEL  # noqa: E402

STORE = Path(__file__).with_name("memory.json")

SYSTEM = ("You are a support assistant for an online shop. Answer in one short "
          "sentence. Use the facts in MEMORY as established truth about this "
          "customer.")


# --------------------------------------------------------------- the store
def load():
    if STORE.exists():
        return json.loads(STORE.read_text())
    return []


def save(mem):
    STORE.write_text(json.dumps(mem, indent=2))


def remember(mem, fact, source, confidence="stated"):
    """Every write records where it came from. That is the whole trick."""
    mem.append({"fact": fact, "source": source, "confidence": confidence,
                "written_at": time.strftime("%Y-%m-%d %H:%M:%S")})
    save(mem)
    return mem


def render(mem):
    if not mem:
        return "MEMORY: (empty)"
    return "MEMORY:\n" + "\n".join(f"- {m['fact']}" for m in mem)


def ask(question, mem):
    """A fresh conversation every time. The only continuity is the store."""
    msgs = [{"role": "system", "content": SYSTEM + "\n\n" + render(mem)},
            {"role": "user", "content": question}]
    return chat(msgs, max_tokens=120)["content"].strip()


# --------------------------------------------------------------- 1. no memory
STORE.unlink(missing_ok=True)
banner(f"1. Two sessions, no memory   model={MODEL}")

mem = []
print("\n  Session 1")
print("  user  > I only ever order the eco-friendly packaging option.")
print(f"  agent < {ask('I only ever order the eco-friendly packaging option.', mem)}")

print("\n  Session 2 (new conversation, nothing carried over)")
q = "Which packaging should I use for my order?"
print(f"  user  > {q}")
print(f"  agent < {ask(q, mem)}")
print("""
  The model did not forget. It was never told. Each call is answered from
  scratch, so 'memory' has to be something your code stores and replays.""")

# --------------------------------------------------------------- 2. with memory
banner("2. The same two sessions, with a store")

remember([], "Customer always chooses eco-friendly packaging.",
         source="stated by customer, session 1")
print("\n  Written to memory.json:")
written = load()
print(f"    {written[0]['fact']}   (source: {written[0]['source']})")

# Session 2 reads the store back off disk. Nothing is carried in a variable --
# that is the point, and it is why load() exists rather than reusing the list
# remember() just returned.
print("\n  Session 2 (still a new conversation; memory read back from the file)")
mem = load()
print(f"  user  > {q}")
print(f"  agent < {ask(q, mem)}")
print("""
  Nothing about the model changed. The store put one line into the system
  prompt, and that is the entire mechanism behind every 'it remembers me'
  feature you have used.""")

# --------------------------------------------------------------- 3. poisoning
banner("3. One wrong write, and every later answer is wrong")

mem = remember(mem, "Customer's delivery address is 14 Bridge Street, Leeds.",
               source="inferred from an earlier message", confidence="inferred")
print("\n  A second fact is written. This one was inferred, not stated —")
print("  the customer never said it. Nothing marks it as less trustworthy")
print("  in the prompt, because render() prints every fact identically.\n")

for question in ["Where will my order be delivered?",
                 "Can you confirm my details before I check out?"]:
    print(f"  user  > {question}")
    print(f"  agent < {ask(question, mem)}\n")

print("""  The agent states the invented address as fact, confidently, in a fresh
  conversation with no way to know it was inferred. This is memory poisoning:
  a bad write is durable, is replayed as established context, and presents as
  the model getting worse rather than the store being wrong.

  Note what it is NOT: a hallucination in the usual sense. The model is
  reporting its context accurately. Your store lied to it.""")

# --------------------------------------------------------------- 4. the fixes
banner("4. Three things that make a store safe to trust")

def render_guarded(mem):
    lines = []
    for m in mem:
        mark = "" if m["confidence"] == "stated" else "  [UNCONFIRMED — verify before relying on it]"
        lines.append(f"- {m['fact']}{mark}")
    return "MEMORY:\n" + "\n".join(lines)


def ask_guarded(question, mem):
    sys_msg = (SYSTEM + " Facts marked UNCONFIRMED must be confirmed with the "
               "customer before you state them as fact.\n\n" + render_guarded(mem))
    return chat([{"role": "system", "content": sys_msg},
                 {"role": "user", "content": question}], max_tokens=120)["content"].strip()


print("\n  (a) Carry provenance into the prompt, not just into the file:\n")
print(f"  user  > Where will my order be delivered?")
print(f"  agent < {ask_guarded('Where will my order be delivered?', mem)}")

print("\n  (b) Forget. Nothing else here decays, so nothing else self-corrects.")
before = len(mem)
mem = [m for m in mem if m["confidence"] == "stated"]
save(mem)
print(f"      Dropped {before - len(mem)} unconfirmed fact(s); {len(mem)} remain.")
print(f"  agent < {ask('Where will my order be delivered?', mem)}")

print("\n  (c) Keep writes narrow. Compare what a transcript-dumping store costs:")
transcript = ("Customer said: 'hi', 'I only ever order the eco-friendly packaging "
              "option', 'ok thanks', 'and one more thing', 'never mind'. Agent said: "
              "'Hello!', 'Noted.', 'You're welcome.', 'Sure?', 'No problem.'")
print(f"      transcript-style write : {len(transcript):>4} chars")
print(f"      fact-style write       : {len(mem[0]['fact']):>4} chars")
print(f"      ratio                  : {len(transcript)/max(len(mem[0]['fact']),1):.1f}x, "
      "paid on every turn that retrieves it")

STORE.unlink(missing_ok=True)

banner("What you just learned")
print("""
  - The model has no memory. Every 'it remembers me' feature is your code
    writing something down and replaying it into a later prompt.

  - Long-term memory and retrieval are the same machinery pointed at
    different data. Everything in module 7 applies here, including the fact
    that a lookup always returns something.

  - A wrong write is worse than a wrong answer. An answer is discarded; a
    memory is replayed as established context into every future run, and the
    model has no way to doubt it. It looks like model degradation.

  - So writes deserve more suspicion than reads. Record provenance, surface it
    in the prompt, and distinguish what was stated from what was inferred.

  - Build forgetting on day one. It is the part everyone skips and the reason
    memory systems rot: preferences change, facts expire, and nothing in an
    append-only store ever corrects itself.

  - Store facts, not transcripts. You pay for the difference on every single
    turn that retrieves it.
""")
