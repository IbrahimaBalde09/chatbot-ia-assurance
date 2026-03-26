from pathlib import Path


def load_txt_documents(folder_path: Path) -> list[dict]:
    documents = []

    for file_path in folder_path.glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if content:
            documents.append(
                {
                    "source": file_path.name,
                    "text": content
                }
            )

    return documents