"""Tiny helpers shared by the labs. Standard library only — no pip install.

Every lab talks to an OpenAI-compatible /v1/chat/completions endpoint. That is
deliberate: the same code runs against local Ollama, against a hosted API, or
against anything else that speaks the same shape. The only thing that changes
is BASE_URL, API_KEY and MODEL.
"""
import json
import os
import urllib.error
import urllib.request

BASE_URL = os.getenv("LAB_BASE_URL", "http://127.0.0.1:11434/v1")
API_KEY = os.getenv("LAB_API_KEY", "ollama")  # Ollama ignores it; hosted APIs don't
# Default is a NON-reasoning model on purpose. Reasoning models interleave a
# long thinking trace and can spend their whole output budget on it, which
# obscures the mechanism these labs exist to show. Module 6 covers that
# behaviour deliberately; here it is just noise.
#   ollama pull qwen2.5:14b
MODEL = os.getenv("LAB_MODEL", "qwen2.5:14b")


LAST_USAGE = {}


def chat(messages, tools=None, temperature=0, max_tokens=4096):
    """One request to the model. Returns a portable assistant message dict.

    Note what gets stripped. Reasoning models served over an OpenAI-compatible
    endpoint often return a non-standard extra field (Ollama calls it
    `reasoning`). It is provider-private: the OpenAI SDK drops it, Anthropic
    requires signed thinking blocks instead, and Google uses thought
    signatures. None of them interoperate. So we keep role/content/tool_calls
    -- the fields every provider agrees on -- and let the rest go.
    """
    payload = {"model": MODEL, "messages": messages, "temperature": temperature,
               "max_tokens": max_tokens}
    if tools:
        payload["tools"] = tools
    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            body = json.load(r)
            choice = body["choices"][0]
    except urllib.error.URLError as e:
        raise SystemExit(
            f"\nCould not reach {BASE_URL} -- {e}\n"
            f"Is the model server running?  OLLAMA_CONTEXT_LENGTH=64000 ollama serve\n"
            f"Is the model pulled?          ollama pull {MODEL}\n"
        )
    msg = choice["message"]
    out = {"role": msg["role"], "content": msg.get("content") or ""}
    # usage is what every tracing tool is built on. Carried out-of-band so it
    # never lands in the message list and gets resent to the model.
    LAST_USAGE.clear()
    LAST_USAGE.update(body.get("usage") or {})
    if msg.get("tool_calls"):
        out["tool_calls"] = msg["tool_calls"]
    # A reasoning model can spend its whole output budget thinking and return
    # empty content. That is a truncation, not a refusal -- surface it loudly
    # rather than letting the learner debug a silent blank.
    if choice.get("finish_reason") == "length" and not out["content"]:
        out["content"] = (
            "[truncated: the model used its entire output budget on internal "
            "reasoning and produced no answer. Raise max_tokens, or ask a "
            "question that needs less deliberation.]"
        )
    return out


def banner(text):
    print(f"\n{'=' * 68}\n{text}\n{'=' * 68}")


EMBED_MODEL = os.getenv("LAB_EMBED_MODEL", "nomic-embed-text")


def embed(texts):
    """Embed a list of strings. Returns a list of float vectors.

    Same endpoint shape as chat(): swap BASE_URL and this runs against a hosted
    provider instead. Dimensions differ per model, so an index built with one
    embedding model cannot be queried with another -- switching means reindexing.
    """
    payload = {"model": EMBED_MODEL, "input": texts}
    req = urllib.request.Request(
        f"{BASE_URL}/embeddings",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return [d["embedding"] for d in json.load(r)["data"]]
    except urllib.error.URLError as e:
        raise SystemExit(
            f"\nCould not reach {BASE_URL} -- {e}\n"
            f"Pull the embedding model first:  ollama pull {EMBED_MODEL}\n"
        )


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(x * x for x in b) ** 0.5
    return dot / (na * nb) if na and nb else 0.0
