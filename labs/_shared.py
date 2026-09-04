"""Tiny helpers shared by the labs. Standard library only — no pip install.

Every lab talks to an OpenAI-compatible /v1/chat/completions endpoint. That is
deliberate: the same code runs against local Ollama, against a hosted API, or
against anything else that speaks the same shape. The only thing that changes
is BASE_URL, API_KEY and MODEL.
"""
import json
import os
import threading
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


class ProviderError(RuntimeError):
    """The provider answered and refused the request.

    Separate from a connection failure on purpose: a 400 means your payload was
    rejected (an unsupported option, a bad deployment name, a content filter),
    and the provider's own message is the thing worth reading. Labs catch this
    to report a capability difference rather than dying.
    """

    def __init__(self, status, message):
        super().__init__(message)
        self.status = status


# Token usage is carried out-of-band so it never lands in the message list and
# gets resent to the model. It is thread-local rather than a module global on
# purpose: lab 11 calls chat() concurrently in a ThreadPoolExecutor, and with a
# shared dict one worker can clear and overwrite another's usage in the gap
# between the call returning and the caller reading it -- silently corrupting
# the very token comparison that lab exists to make.
_usage = threading.local()


def last_usage():
    """Token usage from THIS thread's most recent chat() call."""
    return dict(getattr(_usage, "last", None) or {})


def chat(messages, tools=None, temperature=0, max_tokens=4096, response_format=None):
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
    # response_format is how a provider is told to constrain the output shape.
    # {"type": "json_object"} asks for valid JSON and nothing more;
    # {"type": "json_schema", ...} restricts generation to a schema. Lab 02b
    # measures the difference. Left out of the payload entirely when unset, so
    # providers that do not know the field are unaffected.
    if response_format:
        payload["response_format"] = response_format
    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            body = json.load(r)
            choice = body["choices"][0]
    except urllib.error.HTTPError as e:
        # The server answered and refused. That is a different problem from not
        # reaching it at all, and it is the provider's message that helps --
        # telling an Azure user to `ollama pull gpt-4.1` wastes their afternoon.
        detail = ""
        try:
            detail = e.read().decode(errors="replace")[:400]
        except Exception:
            pass
        raise ProviderError(e.code, f"HTTP {e.code} from {BASE_URL}: {detail or e.reason}")
    except urllib.error.URLError as e:
        raise SystemExit(
            f"\nCould not reach {BASE_URL} -- {e}\n"
            f"If you are running locally:   OLLAMA_CONTEXT_LENGTH=64000 ollama serve\n"
            f"                              ollama pull {MODEL}\n"
            f"If you are using a hosted provider, check LAB_BASE_URL and that\n"
            f"the host is reachable from here.\n"
        )
    msg = choice["message"]
    out = {"role": msg["role"], "content": msg.get("content") or ""}
    # usage is what every tracing tool is built on. Read it with last_usage().
    _usage.last = body.get("usage") or {}
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
