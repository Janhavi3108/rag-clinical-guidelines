import json
import faiss, numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en-v1.5")
index = faiss.read_index("index.faiss")
chunks = json.load(open("chunks.json", encoding="utf-8"))
PREFIX = "Represent this sentence for searching relevant passages: "

def search(q, k=3):
    v = model.encode([PREFIX + q], normalize_embeddings=True)
    scores, ids = index.search(np.asarray(v, dtype="float32"), k)
    return [(float(s), chunks[i]) for s, i in zip(scores[0], ids[0])]

for q in [
    "At what age should screening start for women?",
    "What screening test does India's national programme use?",
    "What does WHO recommend as the primary screening test?",
    "What is the treatment for stage IB cervical cancer?",
    "What is the capital of France?",
]:
    print("\nQ:", q)
    for s, c in search(q):
        print(f"  {s:.3f} {c['source']} p.{c['page']}: {c['text'][:120]!r}")