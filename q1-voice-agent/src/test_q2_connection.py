from src.q2_retriever import Q2KnowledgeRetriever


def main():
    retriever = Q2KnowledgeRetriever()

    results = retriever.search(
        "Is React mandatory for the Software Engineer Intern position?",
        top_k=3
    )

    print("=" * 60)
    print("Q2 RETRIEVAL FROM Q1")
    print("=" * 60)

    for i, result in enumerate(results, 1):
        print(f"\nResult {i}")
        print(f"Title: {result.get('title')}")
        print(f"Score: {result.get('score')}")
        print(f"Category: {result.get('category')}")
        print(f"Source: {result.get('source')}")
        print(f"Content: {result.get('content')[:300]}...")


if __name__ == "__main__":
    main()