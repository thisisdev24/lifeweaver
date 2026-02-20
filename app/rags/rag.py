import os, json
from app.embeddings.embed import embed_texts

# Simple FAISS wrapper stub (requires faiss-cpu installed)
try:
    import faiss
except Exception:
    faiss = None

INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "faiss.index")


def rag_query(query: str, top_k: int = 3):
    # Stub: perform naive embedding-based similarity if FAISS exists; otherwise return dummy results.
    if faiss is None:
        return [
            {
                "id": "dummy1",
                "score": 0.5,
                "snippet": "FAISS not installed in container. Install faiss-cpu.",
            }
        ]
    qvec = embed_texts([query])
    # load index (not implemented fully)
    return [{"id": "stub", "score": 0.9, "snippet": "Example result"}]
