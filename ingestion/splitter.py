def split_text(text: str, chunk_size: int = 500, overlap: int = 80) -> list[str]:
    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start += chunk_size - overlap

    return chunks


def split_documents(documents: list[dict], chunk_size: int = 500, overlap: int = 80) -> list[dict]:
    all_chunks = []

    for doc in documents:
        chunks = split_text(doc["text"], chunk_size=chunk_size, overlap=overlap)

        for i, chunk in enumerate(chunks):
            all_chunks.append(
                {
                    "source": doc["source"],
                    "chunk_id": i,
                    "text": chunk
                }
            )

    return all_chunks