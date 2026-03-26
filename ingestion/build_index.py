import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import pickle
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

from rag.config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    VECTORSTORE_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL,
)
from ingestion.loader import load_txt_documents
from ingestion.splitter import split_documents


def infer_domain(source_name: str) -> str:
    name = source_name.lower()

    if "auto" in name or "vehicule" in name or "voiture" in name:
        return "auto"
    if "sante" in name or "maladie" in name or "prevoyance" in name:
        return "sante"
    if "habitation" in name or "logement" in name or "maison" in name:
        return "habitation"
    if "banque" in name or "immobilier" in name or "emprunteur" in name or "credit" in name:
        return "banque_immobilier"

    return "general"


def build_index():
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)

    documents = load_txt_documents(RAW_DATA_DIR)
    chunks = split_documents(
        documents,
        chunk_size=CHUNK_SIZE,
        overlap=CHUNK_OVERLAP
    )

    enriched_chunks = []
    for chunk in chunks:
        enriched_chunks.append(
            {
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"],
                "domain": infer_domain(chunk["source"]),
                "text": chunk["text"],
            }
        )

    with open(PROCESSED_DATA_DIR / "chunks.json", "w", encoding="utf-8") as f:
        json.dump(enriched_chunks, f, ensure_ascii=False, indent=2)

    model = SentenceTransformer(EMBEDDING_MODEL)
    texts = [chunk["text"] for chunk in enriched_chunks]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    embeddings = np.array(embeddings, dtype=np.float32)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    faiss.write_index(index, str(VECTORSTORE_DIR / "faiss_index.bin"))

    with open(VECTORSTORE_DIR / "documents.pkl", "wb") as f:
        pickle.dump(enriched_chunks, f)

    print("Index reconstruit avec succès.")


if __name__ == "__main__":
    build_index()