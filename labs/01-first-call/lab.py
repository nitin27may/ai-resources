"""Lab 01 — your first call to a model you control.

Goal: see the raw shape of a chat completion, and prove your local model works
before anything more complicated depends on it.

Run:  python3 labs/01-first-call/lab.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from _shared import chat, banner, MODEL, BASE_URL  # noqa: E402

banner(f"Talking to {MODEL} at {BASE_URL}")

# A "conversation" is just a list of role/content dicts. There is no session,
# no server-side memory. You resend the whole list every single turn — that is
# the entire mechanism, and it is why context budget becomes a problem later.
messages = [
    {"role": "system", "content": "You answer in one short sentence."},
    {"role": "user", "content": "What is a token, in the LLM sense?"},
]

reply = chat(messages)
print(f"\nrole:    {reply['role']}")
print(f"content: {reply['content']}\n")

banner("Now watch the statelessness")

# Ask a follow-up WITHOUT appending the previous turn. The model has no idea
# what "it" refers to, because nothing carried over.
forgetful = chat([{"role": "user", "content": "Give me one short example of one."}])
print(f"\nWithout history: {forgetful['content'][:160]}\n")

# Now the same follow-up WITH the history appended. This is 'memory'.
messages.append(reply)
messages.append({"role": "user", "content": "Give me one short example of one."})
remembering = chat(messages)
print(f"With history:    {remembering['content'][:160]}\n")

banner("What you just learned")
print("""
  - A conversation is a list you own and resend in full on every request.
  - The model is stateless. 'Memory' is you appending to that list.
  - Everything later in this path -- context budgets, compaction, the agent
    loop itself -- exists because of those two facts.

  Look at labs/_shared.py before moving on. chat() keeps only role, content
  and tool_calls. Reasoning models return an extra provider-specific field
  that does not survive a move to another provider, so we drop it. That one
  decision is what makes every lab here portable.
""")
