

from pathlib import Path
import sys

# Add the project root to Python's import path.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import chromadb
from sentence_transformers import SentenceTransformer

from src.knowledge_base import load_documents, split_documents

DB_PATH = PROJECT_ROOT / "chroma_db"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "chroma_db"

# A compact model that works for general semantic search.
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def build_vector_store():
    """Embed medical chunks and store them in ChromaDB."""

    documents = load_documents()
    chunks = split_documents(documents)

    if not chunks:
        raise ValueError("No text chunks found. Check your reference documents.")

    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    client = chromadb.PersistentClient(path=str(DB_PATH))

    # Rebuild the demo collection each time this script runs.
    collection_name = "mediguide_knowledge"

    try:
        client.delete_collection(collection_name)
    except Exception:
        pass

    collection = client.create_collection(name=collection_name)

    texts = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]
    ids = [f"medical_chunk_{i}" for i in range(len(chunks))]

    embeddings = model.encode(texts, normalize_embeddings=True)

    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings.tolist(),
    )

    print(f"Stored {collection.count()} chunks in ChromaDB.")

    return collection, model


def search_knowledge_base(query, collection, model, top_k=3):
    """Return the most semantically similar chunks."""

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True,
    )[0]

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=min(top_k, collection.count()),
    )

    matches = []

    for i, text in enumerate(results["documents"][0]):
        matches.append(
            {
                "text": text,
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            }
        )

    return matches


def main():
    collection, model = build_vector_store()

    while True:
        query = input("\nAsk a health-information question (or type 'exit'): ")

        if query.strip().lower() == "exit":
            break

        if not query.strip():
            print("Please enter a question.")
            continue

        matches = search_knowledge_base(query, collection, model)

        print("\nRetrieved reference passages:")

        for match in matches:
            print("\n" + "-" * 50)
            print("Source:", match["metadata"]["source"])
            print("Topic:", match["metadata"]["topic"])
            print("Distance:", round(match["distance"], 4))
            print("Text:", match["text"])


if __name__ == "__main__":
    main()
