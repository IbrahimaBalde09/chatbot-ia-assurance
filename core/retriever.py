import pickle
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer
from core.config import VECTORSTORE_DIR, EMBEDDING_MODEL, TOP_K


class Retriever:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.index = faiss.read_index(str(VECTORSTORE_DIR / "faiss_index.bin"))

        with open(VECTORSTORE_DIR / "documents.pkl", "rb") as f:
            self.documents = pickle.load(f)

    def search(self, query: str, top_k: int = TOP_K):
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(np.array(query_embedding, dtype=np.float32), top_k)

        results = []
        for idx in indices[0]:
            if idx != -1:
                results.append(self.documents[idx])

        return results