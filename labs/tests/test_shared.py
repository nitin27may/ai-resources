"""Tests for the helpers every lab depends on. Standard library only.

Run:  python3 -m unittest discover -s labs/tests -v
      python3 labs/tests/test_shared.py

Nothing here starts a model or touches a network -- urlopen is replaced for the
duration of each test, so this runs in CI for free and in under a second.

These cover the guarantees in `_shared.py` that are invisible in normal use and
so break silently:

  * usage accounting survives concurrency. Lab 11 reads it from worker threads
    and its entire point is a token comparison.
  * provider-private fields never reach the message list. That is what lets the
    same lab code run against Ollama, OpenAI and Azure without edits.
"""
import io
import json
import sys
import threading
import time
import unittest
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import _shared  # noqa: E402


# --------------------------------------------------------------- the stubs
class _Body:
    """A stand-in for the object urlopen returns: a context manager over bytes."""

    def __init__(self, payload, delay=0.0):
        self.payload = payload
        self.delay = delay

    def __enter__(self):
        if self.delay:
            time.sleep(self.delay)
        return io.BytesIO(json.dumps(self.payload).encode())

    def __exit__(self, *exc):
        return False


class _FakeHTTP:
    """Swap urllib.request.urlopen for `responder` while inside the block.

    `responder(n)` is called with a 1-based request number, so a test can make
    each call answer differently -- which is how the concurrency case below
    tells whose usage it got back.
    """

    def __init__(self, responder):
        self.responder = responder
        self.sent = []
        self._lock = threading.Lock()
        self._real = None

    def __enter__(self):
        self._real = urllib.request.urlopen

        def fake(req, timeout=None):
            with self._lock:
                self.sent.append(json.loads(req.data.decode()))
                n = len(self.sent)
            return self.responder(n)

        urllib.request.urlopen = fake
        return self

    def __exit__(self, *exc):
        urllib.request.urlopen = self._real
        return False


def completion(content="ok", usage=None, finish_reason="stop", tool_calls=None, extra=None):
    message = {"role": "assistant", "content": content}
    if tool_calls:
        message["tool_calls"] = tool_calls
    if extra:
        message.update(extra)
    return {"choices": [{"message": message, "finish_reason": finish_reason}],
            "usage": usage if usage is not None else {"total_tokens": 1}}


# ------------------------------------------------------------ the tests
class UsageAccounting(unittest.TestCase):

    def test_usage_does_not_leak_between_threads(self):
        """Regression for the bug that made lab 11's token ratio unreliable.

        Usage used to live in a module-global dict that chat() cleared and
        rewrote per call. A concurrent worker could overwrite it in the gap
        between chat() returning and the caller reading it, so a specialist
        could be billed another specialist's tokens -- or one count could be
        used twice. The staggered delays reproduce that interleaving on
        purpose: against the old code most threads read the wrong number.
        """
        def responder(n):
            # Later calls answer later, so early threads finish while the
            # slower ones are still in flight. That is the whole window.
            return _Body(completion(content=f"r{n}", usage={"total_tokens": n * 1000}),
                         delay=0.05 * n)

        def call(_):
            reply = _shared.chat([{"role": "user", "content": "x"}])
            time.sleep(0.08)          # widen the gap between call and read
            return reply["content"], _shared.last_usage()["total_tokens"]

        with _FakeHTTP(responder):
            with ThreadPoolExecutor(max_workers=5) as pool:
                results = list(pool.map(call, range(5)))

        for content, tokens in results:
            expected = int(content[1:]) * 1000
            self.assertEqual(
                tokens, expected,
                f"reply {content} read usage {tokens}, expected {expected} — "
                "usage leaked between threads")

    def test_last_usage_hands_back_a_copy(self):
        """A caller must not be able to corrupt the next reader's numbers."""
        with _FakeHTTP(lambda n: _Body(completion(usage={"total_tokens": 42}))):
            _shared.chat([{"role": "user", "content": "x"}])
        first = _shared.last_usage()
        first["total_tokens"] = 999999
        self.assertEqual(_shared.last_usage()["total_tokens"], 42)

    def test_usage_absent_is_empty_not_stale(self):
        """A provider that omits usage must not leave the previous call's."""
        with _FakeHTTP(lambda n: _Body(completion(usage={"total_tokens": 7}))):
            _shared.chat([{"role": "user", "content": "x"}])
        self.assertEqual(_shared.last_usage().get("total_tokens"), 7)
        with _FakeHTTP(lambda n: _Body(completion(usage=None) | {"usage": None})):
            _shared.chat([{"role": "user", "content": "x"}])
        self.assertEqual(_shared.last_usage(), {})


class MessagePortability(unittest.TestCase):

    def test_provider_private_fields_are_dropped(self):
        """Ollama returns `reasoning`; no other provider accepts it back.

        Anything kept here gets appended to the message list and resent on the
        next turn, which is what breaks a lab when you switch provider.
        """
        with _FakeHTTP(lambda n: _Body(completion(extra={"reasoning": "thinking...",
                                                        "vendor_id": "abc"}))):
            reply = _shared.chat([{"role": "user", "content": "x"}])
        self.assertEqual(set(reply), {"role", "content"})

    def test_tool_calls_survive(self):
        calls = [{"id": "call_0", "type": "function",
                  "function": {"name": "get_stock", "arguments": '{"sku": "ABC-1"}'}}]
        with _FakeHTTP(lambda n: _Body(completion(content=None, tool_calls=calls))):
            reply = _shared.chat([{"role": "user", "content": "x"}])
        self.assertEqual(reply["tool_calls"], calls)
        self.assertEqual(reply["content"], "")   # never None -- labs concatenate it

    def test_truncated_reasoning_is_surfaced_not_blank(self):
        """A reasoning model can spend its whole budget thinking and return "".

        Left alone that looks like a refusal and sends the learner debugging
        their prompt, so chat() replaces it with an explanation.
        """
        with _FakeHTTP(lambda n: _Body(completion(content="", finish_reason="length"))):
            reply = _shared.chat([{"role": "user", "content": "x"}])
        self.assertIn("truncated", reply["content"])
        self.assertIn("max_tokens", reply["content"])

    def test_response_format_omitted_unless_asked(self):
        """Providers that do not know the field must be unaffected by it."""
        with _FakeHTTP(lambda n: _Body(completion())) as http:
            _shared.chat([{"role": "user", "content": "x"}])
            self.assertNotIn("response_format", http.sent[0])
            _shared.chat([{"role": "user", "content": "x"}],
                         response_format={"type": "json_object"})
            self.assertEqual(http.sent[1]["response_format"], {"type": "json_object"})


class ProviderErrors(unittest.TestCase):

    def test_http_error_carries_the_providers_own_message(self):
        """A 400 means the payload was rejected. The provider's text is the
        thing that helps -- telling an Azure user to `ollama pull` does not."""
        def responder(n):
            raise urllib.error.HTTPError(
                "http://x/v1/chat/completions", 404, "Not Found", {},
                io.BytesIO(b'{"error":{"code":"DeploymentNotFound"}}'))

        with _FakeHTTP(responder):
            with self.assertRaises(_shared.ProviderError) as caught:
                _shared.chat([{"role": "user", "content": "x"}])
        self.assertEqual(caught.exception.status, 404)
        self.assertIn("DeploymentNotFound", str(caught.exception))

    def test_unreachable_host_exits_with_guidance(self):
        """Not the same failure as a refusal, and it needs different advice."""
        def responder(n):
            raise urllib.error.URLError("Connection refused")

        with _FakeHTTP(responder):
            with self.assertRaises(SystemExit) as caught:
                _shared.chat([{"role": "user", "content": "x"}])
        self.assertIn("Could not reach", str(caught.exception))


class Similarity(unittest.TestCase):

    def test_cosine_bounds_and_degenerate_input(self):
        self.assertAlmostEqual(_shared.cosine([1, 0], [1, 0]), 1.0)
        self.assertAlmostEqual(_shared.cosine([1, 0], [0, 1]), 0.0)
        self.assertAlmostEqual(_shared.cosine([1, 0], [-1, 0]), -1.0)
        self.assertEqual(_shared.cosine([0, 0], [1, 0]), 0.0)   # no ZeroDivisionError


if __name__ == "__main__":
    unittest.main(verbosity=2)
