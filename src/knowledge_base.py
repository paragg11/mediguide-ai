
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter


# Find the project root from this Python file.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Folder containing our educational medical documents.
DOCUMENTS_DIR = PROJECT_ROOT / "data" / "medical_reference"


def load_documents():
    """Read text files and attach source metadata."""
    documents = []

    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")
        text = " ".join(text.split())

        if text:
            documents.append(
                {
                    "text": text,
                    "metadata": {
                        "source": file_path.name,
                        "topic": "general_health",
                    },
                }
            )

    return documents


def split_documents(documents):
    """Split loaded documents into smaller chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = []

    for document in documents:
        text_chunks = splitter.split_text(document["text"])

        for chunk_number, chunk_text in enumerate(text_chunks):
            chunks.append(
                {
                    "text": chunk_text,
                    "metadata": {
                        **document["metadata"],
                        "chunk_id": chunk_number,
                    },
                }
            )

    return chunks


def main():
    documents = load_documents()
    chunks = split_documents(documents)

    print(f"Documents loaded: {len(documents)}")
    print(f"Chunks created: {len(chunks)}")

    for chunk in chunks:
        print("\n" + "-" * 50)
        print("Metadata:", chunk["metadata"])
        print("Text:", chunk["text"])


if __name__ == "__main__":
    main()
