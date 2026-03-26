import pickle
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer
from rag.config import VECTORSTORE_DIR, EMBEDDING_MODEL, TOP_K


class Retriever:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.index = faiss.read_index(str(VECTORSTORE_DIR / "faiss_index.bin"))

        with open(VECTORSTORE_DIR / "documents.pkl", "rb") as f:
            self.documents = pickle.load(f)

    def search(self, query: str, domain: str = "general", top_k: int = TOP_K):
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        query_embedding = np.array(query_embedding, dtype=np.float32)

        # On récupère plus large, puis on filtre par domaine
        scores, indices = self.index.search(query_embedding, top_k * 4)

        results = []
        seen = set()

        for idx, score in zip(indices[0], scores[0]):
            if idx == -1:
                continue

            doc = self.documents[idx]

            if domain != "general" and doc.get("domain") != domain:
                continue

            text = doc["text"].strip()
            if text in seen:
                continue

            seen.add(text)

            results.append(
                {
                    "source": doc["source"],
                    "chunk_id": doc.get("chunk_id"),
                    "domain": doc.get("domain", "general"),
                    "text": text,
                    "score": float(score),
                }
            )

            if len(results) >= top_k:
                break

        return results