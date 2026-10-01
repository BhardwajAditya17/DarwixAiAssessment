import json
import pickle
from pathlib import Path
import faiss
from sentence_transformers import SentenceTransformer


Q2_ROOT = Path(__file__).resolve().parent.parent
INDEX_FILE = str(Q2_ROOT / "kb" / "vector.index")
METADATA_FILE = str(Q2_ROOT / "kb" / "vector_metadata.pkl")
MODEL_NAME = "all-MiniLM-L6-v2"


class KnowledgeBaseRetriever:

    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.index = faiss.read_index(INDEX_FILE)

        with open(METADATA_FILE, "rb") as f:
            self.metadata = pickle.load(f)

    def search(self, query, top_k=5):
        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, index in zip(scores[0], indices[0]):

            if index == -1:
                continue

            chunk = self.metadata[index]

            results.append({
                "score": float(score),
                "chunk_id": chunk["chunk_id"],
                "record_id": chunk["record_id"],
                "title": chunk["title"],
                "content": chunk["content"],
                "category": chunk["category"],
                "source": chunk["source"],
                "version": chunk["version"],
                "status": chunk["status"]
            })

        return results


def main():

    retriever = KnowledgeBaseRetriever()

    query = input("\nEnter your question: ")

    results = retriever.search(query, top_k=5)

    print("\n" + "=" * 70)
    print("RETRIEVAL RESULTS")
    print("=" * 70)

    for i, result in enumerate(results, start=1):

        print(f"\nResult {i}")
        print("-" * 70)

        print("Score:", round(result["score"], 4))
        print("Chunk ID:", result["chunk_id"])
        print("Record ID:", result["record_id"])
        print("Title:", result["title"])
        print("Category:", result["category"])
        print("Version:", result["version"])
        print("Status:", result["status"])

        print("\nSource:")
        print(result["source"])

        print("\nContent:")
        print(result["content"])


if __name__ == "__main__":
    main()
