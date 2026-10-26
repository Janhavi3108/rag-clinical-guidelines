import json, pathlib
import faiss, numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

CHUNK_SIZE = 800
OVERLAP = 150

def load_pdfs(folder="data"):
    docs = []
    for p in sorted(pathlib.Path(folder).glob("*.pdf")):
        pages = PdfReader(p).pages
        empty = 0
        for i, page in enumerate(pages, start=1):
            text = (page.extract_text() or "").strip()
            if len(text) < 50:
                empty += 1
                continue
            docs.append({"source": p.name, "page": i, "text": text})
        print(f"{p.name}: {len(pages)} pages, {empty} empty/near-empty")
    return docs

def chunk(docs, size=CHUNK_SIZE, overlap=OVERLAP):
    out = []
    for d in docs:
        t, start = d["text"], 0
        while start < len(t):
            out.append({"id": len(out), "source": d["source"],
                        "page": d["page"], "text": t[start:start + size]})
            start += size - overlap
    return out

if __name__ == "__main__":
    chunks = chunk(load_pdfs())
    print(len(chunks), "chunks")
    model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    emb = model.encode([c["text"] for c in chunks],
                       normalize_embeddings=True, show_progress_bar=True)
    index = faiss.IndexFlatIP(emb.shape[1])
    index.add(np.asarray(emb, dtype="float32"))
    faiss.write_index(index, "index.faiss")
    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False)