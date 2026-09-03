"""Multi-agent: when splitting the work helps, and when it quietly corrupts it.

Module: docs/02-agents/multi-agent.md

Two orchestrations, same task, measured. Then the failure that decides the
architecture: what happens when two agents write to the same thing.

    python3 labs/11-multi-agent/lab.py

Works against Ollama, OpenAI or Azure OpenAI. See labs/README.md.
"""
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _shared import chat, banner, MODEL, LAST_USAGE  # noqa: E402

# A tiny corpus. Three topics, deliberately independent of each other -- which
# is the condition the whole lab is about.
CORPUS = {
    "shipping": ("Standard shipping is 3-5 business days and free above 40 GBP. "
                 "Express is next-day for 6.99 GBP, ordered before 3pm. "
                 "We do not ship to PO boxes."),
    "returns": ("Returns accepted within 30 days, unused and in original packaging. "
                "Refunds are issued to the original payment method within 5 working "
                "days of receipt. Return postage is paid by the customer unless the "
                "item is faulty."),
    "warranty": ("All electronics carry a 24-month warranty covering manufacturing "
                 "defects. Accidental damage is not covered. Warranty claims require "
                 "the original order number."),
}

QUESTION = ("A customer bought a faulty electronic item 20 days ago and wants to "
            "return it for a refund. Summarise, in three short bullets, what applies: "
            "the return window, who pays return postage, and whether the warranty is "
            "relevant.")


def usage_of(_):
    return dict(LAST_USAGE)


def one_call(prompt, max_tokens=400):
    r = chat([{"role": "user", "content": prompt}], max_tokens=max_tokens)
    return r["content"].strip(), dict(LAST_USAGE)


# ------------------------------------------------------------ A. single agent
banner(f"A. One agent, whole corpus in context   model={MODEL}")

all_docs = "\n\n".join(f"[{k}] {v}" for k, v in CORPUS.items())
t0 = time.time()
single_answer, single_usage = one_call(
    f"Reference material:\n{all_docs}\n\n{QUESTION}")
single_time = time.time() - t0
single_tokens = single_usage.get("total_tokens", 0)

print(f"\n{single_answer}\n")
print(f"  calls: 1   tokens: {single_tokens}   wall time: {single_time:.1f}s")

# ------------------------------------------------ B. supervisor + sub-agents
banner("B. A supervisor and three specialists, run in parallel")

SUB = ("You are a {topic} specialist. Using only this reference, answer in one "
       "sentence what it says that bears on the question. If nothing does, reply "
       "exactly: NOT RELEVANT.\n\nReference: {doc}\n\nQuestion: {q}")

t0 = time.time()
with ThreadPoolExecutor(max_workers=3) as ex:
    futures = {topic: ex.submit(one_call, SUB.format(topic=topic, doc=doc, q=QUESTION), 200)
               for topic, doc in CORPUS.items()}
    findings = {t: f.result() for t, f in futures.items()}

notes = "\n".join(f"- {t}: {ans}" for t, (ans, _) in findings.items())
synth_answer, synth_usage = one_call(
    f"Specialist findings:\n{notes}\n\nUsing only those findings, {QUESTION}")
multi_time = time.time() - t0

multi_tokens = sum(u.get("total_tokens", 0) for _, u in findings.values()) \
    + synth_usage.get("total_tokens", 0)

print("\n  Specialist findings:")
for t, (ans, _) in findings.items():
    print(f"    {t:<9} {ans[:88]}")
print(f"\n{synth_answer}\n")
print(f"  calls: {len(CORPUS) + 1}   tokens: {multi_tokens}   wall time: {multi_time:.1f}s")

# ------------------------------------------------------------- the comparison
banner("The trade, measured")
print(f"""
                       one agent      supervisor + 3
  model calls                  1                   {len(CORPUS) + 1}
  total tokens          {single_tokens:>8}            {multi_tokens:>8}
  wall time             {single_time:>7.1f}s            {multi_time:>7.1f}s
  token ratio                                   {multi_tokens / max(single_tokens, 1):.2f}x
""")
print("""  On a corpus this small the single agent wins outright: the whole corpus
  fits, so splitting it buys nothing and costs an extra round of calls plus
  the tokens to pass findings back.

  The supervisor only starts paying when the sources are too large to hold at
  once, or slow enough that running them concurrently beats running them in
  sequence. Note that wall time, not token count, is the thing parallelism
  improves -- you spend MORE tokens to wait LESS.""")

# The interesting failure is not cost. Check whether splitting the work lost
# something the single agent had, which is the whole case against multi-agent.
dropped = [t for t, (ans, _) in findings.items() if "NOT RELEVANT" in ans.upper()]
for topic in dropped:
    in_single = topic in single_answer.lower()
    in_multi = topic in synth_answer.lower() and "not relevant" not in synth_answer.lower()
    if in_single and not in_multi:
        print(f"""
  Look at '{topic}'. The single agent used it in its answer. The {topic}
  specialist, seeing only its own document, judged it NOT RELEVANT -- and it
  was right about its own document and wrong about the question.

  That judgement is now final. The supervisor cannot recover information a
  sub-agent decided not to return, because it never saw the source. The
  answers above are not merely more expensive; one of them is worse.

  This is the concrete form of the argument against multi-agent systems:
  sub-agents lose the context that made the connection visible.""")
        break
else:
    if dropped:
        print(f"""
  On this run the specialists that answered NOT RELEVANT ({', '.join(dropped)})
  did not cost the final answer anything. Run it again -- this is exactly the
  kind of failure that is intermittent, which is what makes it dangerous.

  The risk is structural: a sub-agent seeing only its own slice decides what
  is relevant, and the supervisor cannot recover what was never returned.""")

# --------------------------------------------------------- the write conflict
banner("Now the part that decides the architecture")

DOC = {"text": "Refund policy: refunds are issued within 5 working days."}

EDIT = ("Here is a document:\n\n{doc}\n\nYou are the {role}. Rewrite the document "
        "to reflect your requirement, and output ONLY the rewritten document text, "
        "one sentence.\n\nYour requirement: {req}")

editors = [
    ("finance officer", "refunds must be issued within 14 working days to allow for reconciliation"),
    ("customer advocate", "refunds must be issued within 2 working days to keep customers happy"),
]

print("\n  Two agents, each given the same document and told to edit it.")
print("  They are not told about each other -- which is exactly what happens")
print("  when sub-agents run in parallel.\n")
print(f"  original  > {DOC['text']}")

with ThreadPoolExecutor(max_workers=2) as ex:
    edits = list(ex.map(lambda e: one_call(EDIT.format(doc=DOC["text"], role=e[0], req=e[1]), 150),
                        editors))

for (role, _), (text, _) in zip(editors, edits):
    print(f"  {role:<18}> {text.splitlines()[0][:100]}")

print("""
  Both edits are individually correct and mutually exclusive. There is no
  merge: whichever write lands last wins, silently, and the policy your
  customers see depends on thread scheduling.

  Nothing in the model caused this. Parallel writers to shared state is an
  ordinary concurrency bug, and giving the writers judgement makes it worse,
  because each one produces a plausible result that hides the conflict.""")

banner("What you just learned")
print(f"""
  - Multi-agent is not a quality upgrade. Here it cost {multi_tokens / max(single_tokens,1):.1f}x the tokens to
    answer the same question, because every sub-agent carries its own context
    and the findings have to be passed back.

  - Parallelism buys wall time, not tokens. Reach for it when the sources are
    too big for one context or too slow in sequence -- not because the work
    'feels like a team'.

  - The criterion that actually separates the cases is reading versus writing.
    Independent read-only sub-tasks compose by concatenation. Writes to shared
    state do not compose at all.

  - So: parallelise the reading, keep one writer. That is the rule that
    reconciles the two well-known posts arguing opposite conclusions about
    multi-agent systems, one day apart, in 2025.

  - Before reaching for a second agent, try one agent with more tools, then one
    agent with better retrieval. Most teams that reach for multi-agent have not
    exhausted either.

  - Everything you built earlier now applies N times over: budgets, tracing,
    idempotency. Debugging 'why did it do that?' across four agents needs
    correlated traces from the start.
""")
