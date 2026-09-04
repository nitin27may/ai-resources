"""Lab 06 — retrieval, built by hand, and the case where it fails.

No vector database. Embeddings in a Python list and cosine similarity in four
lines, because the mechanism is that small and hiding it behind a database is
what stops people understanding why retrieval misses.

Then the interesting half: a question where pure vector search retrieves the
wrong chunk with high confidence, and what fixes it.

Run:  python3 labs/06-local-rag/lab.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from _shared import chat, embed, cosine, banner, MODEL, EMBED_MODEL  # noqa: E402

# A deliberately awkward corpus: several chunks are about refunds, and only one
# carries the actual number. This is what real corpora look like.
DOCS = [
    "Our returns process is designed to be straightforward. Customers can begin a return from the orders page at any time.",
    "The refund window is 30 days from the delivery date. After 30 days we cannot issue a refund.",
    "Refunds are processed back to the original payment method. Most banks post the credit within five working days.",
    "For damaged goods, contact support before returning the item. Damaged items are handled separately from ordinary returns.",
    "Exchange requests follow the same timeline as returns and are subject to stock availability.",
    "Policy RET-14 governs bulk trade returns: orders above 50 units require prior authorisation from the account manager.",
]


def retrieve(query, doc_vecs, k=2):
    qv = embed([query])[0]
    scored = sorted(((cosine(qv, v), d) for v, d in zip(doc_vecs, DOCS)), reverse=True)
    return scored[:k]


def keyword_score(query, doc):
    """A crude BM25 stand-in: exact term overlap. Real systems use BM25, but the
    property that matters is the same -- an exact token match scores, and rare
    tokens are exactly where dense embeddings are weakest."""
    q = {w.strip(".,?").lower() for w in query.split() if len(w) > 2}
    d = {w.strip(".,?").lower() for w in doc.split() if len(w) > 2}
    return len(q & d) / len(q) if q else 0.0


def answer(query, context):
    msgs = [
        {"role": "system", "content":
         "Answer ONLY from the provided context. If the context does not contain "
         "the answer, say 'not in the provided context'. Answer in one sentence."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"},
    ]
    return chat(msgs, max_tokens=200)["content"].strip()


banner(f"Indexing {len(DOCS)} chunks with {EMBED_MODEL}")
vecs = embed(DOCS)
print(f"\n  {len(vecs)} vectors, {len(vecs[0])} dimensions each")
print("  the entire 'vector database' is a Python list\n")

# ---------------------------------------------------------------- it works
banner("1. A question the corpus answers directly")
q1 = "How long do I have to request a refund?"
hits = retrieve(q1, vecs)
print(f"\n  Q: {q1}\n")
for score, d in hits:
    print(f"    {score:.3f}  {d[:72]}...")
print(f"\n  A: {answer(q1, chr(10).join(d for _, d in hits))}\n")

# ------------------------------------------------- it works, until it doesn't
banner("2. The identifier question — on six documents")
q2 = "What does RET-14 cover?"
hits = retrieve(q2, vecs, k=1)
print(f"\n  Q: {q2}   (k=1, so the top hit IS the answer)\n")
for score, d in hits:
    print(f"    {score:.3f}  {d[:70]}...")
print(f"\n  correct chunk ranked first: {'RET-14' in hits[0][1]}")
print("""
  It works. That is the point of this step, and it is a trap: retrieval on a
  toy corpus always looks fine. Six chunks about five distinct topics are
  trivially separable. Nothing you learn here transfers.""")

# --------------------------------------------------------- now make it fail
banner("3. The same question, with 40 plausible neighbours added")
DISTRACT = [
    f"Section {i}: returns for category {i} follow the standard process. "
    f"Orders may be returned within the stated window subject to condition checks."
    for i in range(1, 41)
]
big = DOCS + DISTRACT
big_vecs = vecs + embed(DISTRACT)
qv = embed([q2])[0]

dense = sorted(((cosine(qv, v), d) for v, d in zip(big_vecs, big)), reverse=True)[:3]
print(f"\n  corpus: {len(big)} chunks (was {len(DOCS)})\n  Q: {q2}\n")
print("  dense only:")
for score, d in dense:
    mark = "  <- the answer" if "RET-14" in d else ""
    print(f"    {score:.3f}  {d[:62]}...{mark}")
dense_rank = next((i for i, (_, d) in enumerate(dense, 1) if "RET-14" in d), None)

hyb = sorted(((0.5 * cosine(qv, v) + 0.5 * keyword_score(q2, d), d)
              for v, d in zip(big_vecs, big)), reverse=True)[:3]
print("\n  hybrid (dense + exact keyword):")
for score, d in hyb:
    mark = "  <- the answer" if "RET-14" in d else ""
    print(f"    {score:.3f}  {d[:62]}...{mark}")
hyb_rank = next((i for i, (_, d) in enumerate(hyb, 1) if "RET-14" in d), None)

dense_margin = dense[0][0] - dense[1][0]
hyb_margin = hyb[0][0] - hyb[1][0]
print(f"\n  rank of the answer   dense: {dense_rank or '>3'}    hybrid: {hyb_rank or '>3'}")
print(f"  margin over runner-up  dense: {dense_margin:.3f}   hybrid: {hyb_margin:.3f}")
print(f"""
  Both still rank it first -- so read the margin, not the rank. Dense is
  {dense_margin:.3f} from being wrong; hybrid is {hyb_margin:.3f}. That gap is
  the whole story. Adding forty bland neighbours nearly buried the answer under
  dense similarity alone, and the exact-match signal restored the separation.

  Scale that from 46 chunks to 46,000 and the dense margin goes negative. You
  will not see it happen -- you will just start getting confident wrong answers,
  because retrieval always returns something.""")
print(f"\n  A (dense):  {answer(q2, dense[0][1])}")
print(f"  A (hybrid): {answer(q2, hyb[0][1])}\n")

# -------------------------------------------------------- grounding check
banner("4. A question the corpus does NOT answer")
q3 = "What is your policy on gift cards?"
hits = retrieve(q3, vecs)
print(f"\n  Q: {q3}\n")
for score, d in hits:
    print(f"    {score:.3f}  {d[:72]}...")
print(f"\n  A: {answer(q3, chr(10).join(d for _, d in hits))}\n")
print("""  Note the scores are still respectable. Cosine similarity always returns
  a nearest neighbour -- there is no 'nothing matched'. Retrieval cannot tell
  you the answer is absent; only the instruction to refuse can.""")

banner("What you just learned")
print(f"""
  - Retrieval is embed, compare, take the top k. A vector database adds speed
    and scale, not a different idea.

  - Toy corpora lie. Six chunks about five topics are trivially separable, so
    everything works and nothing you measured transfers. Retrieval quality is a
    property of scale and of how similar your near-misses are.

  - Read the margin, not the rank. At {len(big)} chunks dense still ranked the
    answer first, by {dense_margin:.3f}. That is not a working system; that is a
    system about to stop working. Hybrid held a margin {hyb_margin / max(dense_margin, 1e-9):.0f}x wider on the same query.

  - Hybrid is the highest-leverage change in most RAG systems and costs almost
    nothing. Anthropic measured a dense-only pipeline at a 5.7% top-20 failure
    rate, 2.9% with BM25 added, and 1.9% with a reranker on top.

  - There is no empty result. The nearest neighbour to an unanswerable question
    is still returned, with a plausible score. Everything protecting you from a
    confident wrong answer lives in the prompt and in verification, not in the
    index.

  - Embedding dimensions are model-specific. Change the embedding model and the
    index must be rebuilt -- it is not a config swap.
""")
