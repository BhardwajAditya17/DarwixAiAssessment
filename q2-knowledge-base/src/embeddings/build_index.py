import json
import pickle
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CHUNKS_FILE = PROJECT_ROOT / "kb" / "chunks.json"
INDEX_FILE = PROJECT_ROOT / "kb" / "vector.index"
METADATA_FILE = PROJECT_ROOT / "kb" / "vector_metadata.pkl"

MODEL_NAME = "all-MiniLM-L6-v2"


def main():

    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    # Only index chunks that are currently valid for retrieval.
    searchable_chunks = [
        chunk
        for chunk in chunks
        if chunk["metadata"].get("retrieval_enabled", True)
    ]

    print("Total chunks:", len(chunks))
    print("Searchable chunks:", len(searchable_chunks))

    model = SentenceTransformer(MODEL_NAME)

    texts = [
        chunk["content"]
        for chunk in searchable_chunks
    ]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    dimension = embeddings.shape[1]

    # Inner product on normalized vectors = cosine similarity.
    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    faiss.write_index(
        index,
        str(INDEX_FILE),
    )

    with open(METADATA_FILE, "wb") as f:
        pickle.dump(
            searchable_chunks,
            f,
        )

    print()
    print("Embedding dimension:", dimension)
    print("Indexed vectors:", index.ntotal)
    print("Index:", INDEX_FILE)
    print("Metadata:", METADATA_FILE)


if __name__ == "__main__":
    main()
