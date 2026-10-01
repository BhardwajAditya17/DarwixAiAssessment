import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.retrieval import KnowledgeBaseRetriever


TEST_QUERIES = [
    {
        "id": "Q1",
        "question": "What are the eligibility requirements for the Software Engineer Intern position?",
        "expected_category": "qualification",
        "expected_keywords": [
            "0-1 years",
            "Java",
            "Python",
            "Data Structures",
            "Git",
            "REST APIs",
            "6 month"
        ]
    },
    {
        "id": "Q2",
        "question": "What rules does the screening agent have to follow?",
        "expected_category": "policy",
        "expected_keywords": [
            "job requirements",
            "invent",
            "information",
            "experience",
            "preferred skills"
        ]
    },
    {
        "id": "Q3",
        "question": "What happens during the candidate screening process?",
        "expected_category": "general",
        "expected_keywords": [
            "screening"
        ]
    },
    {
        "id": "Q4",
        "question": "Can preferred skills become mandatory requirements?",
        "expected_category": "policy",
        "expected_keywords": [
            "preferred",
            "mandatory"
        ]
    },
    {
        "id": "Q5",
        "question": "Does passing the initial screening guarantee an interview or employment?",
        "expected_category": "faq",
        "expected_keywords": [
            "does not guarantee",
            "interview",
            "employment"
        ]
    }
]


def evaluate_result(test, results):
    if not results:
        return {
            "verdict": "incorrect",
            "reason": "No results were retrieved."
        }

    top_result = results[0]

    combined_text = " ".join(
        result["content"].lower()
        for result in results[:3]
    )

    matched_keywords = [
        keyword
        for keyword in test["expected_keywords"]
        if keyword.lower() in combined_text
    ]

    category_match = any(
        result["category"] == test["expected_category"]
        for result in results[:3]
    )

    if len(matched_keywords) >= 2 and category_match:
        verdict = "correct"
    elif len(matched_keywords) >= 1 or category_match:
        verdict = "partially correct"
    else:
        verdict = "incorrect"

    return {
        "verdict": verdict,
        "top_score": top_result["score"],
        "top_record_id": top_result["record_id"],
        "top_title": top_result["title"],
        "top_category": top_result["category"],
        "matched_keywords": matched_keywords,
        "category_match": category_match,
        "reason": (
            f"Retrieved {len(results)} results. "
            f"Top result was '{top_result['title']}' "
            f"with score {top_result['score']:.4f}."
        )
    }


def main():
    retriever = KnowledgeBaseRetriever()

    evaluation_results = []

    for test in TEST_QUERIES:
        print("\n" + "=" * 80)
        print(f"{test['id']}: {test['question']}")
        print("=" * 80)

        results = retriever.search(
            test["question"],
            top_k=5
        )

        evaluation = evaluate_result(test, results)

        print("\nTop retrieved records:")

        for i, result in enumerate(results, start=1):
            print(
                f"{i}. {result['title']} | "
                f"category={result['category']} | "
                f"score={result['score']:.4f} | "
                f"version={result['version']} | "
                f"status={result['status']}"
            )

        print("\nVerdict:", evaluation["verdict"])
        print("Reason:", evaluation["reason"])

        evaluation_results.append({
            "test_id": test["id"],
            "user_question": test["question"],
            "expected_category": test["expected_category"],
            "retrieved_results": results,
            "evaluation": evaluation
        })

    output_file = Path("evaluation/retrieval_results.json")

    with open(output_file, "w") as f:
        json.dump(
            evaluation_results,
            f,
            indent=2
        )

    print("\n" + "=" * 80)
    print("Evaluation complete.")
    print("Results saved to:", output_file)
    print("=" * 80)


if __name__ == "__main__":
    main()
