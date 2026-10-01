import json
from pathlib import Path

from deduplication import find_duplicates, annotate_versions


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cleaned_documents"
    / "cleaned_documents.json"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cleaned_documents"
    / "versioned_documents.json"
)

REPORT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cleaned_documents"
    / "deduplication_report.json"
)


def main():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        documents = json.load(f)

    documents = annotate_versions(documents)

    duplicate_groups = find_duplicates(documents)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            documents,
            f,
            indent=2,
            ensure_ascii=False,
        )

    report = {
        "total_documents": len(documents),
        "duplicate_groups": duplicate_groups,
        "duplicate_group_count": len(duplicate_groups),
    }

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            report,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"Processed {len(documents)} documents")
    print(f"Duplicate groups found: {len(duplicate_groups)}")

    for group in duplicate_groups:
        print("Duplicate/near-duplicate group:", group)

    print("\nVersion information:")

    for document in documents:
        metadata = document["metadata"]

        if metadata.get("version") or metadata.get("status"):
            print(
                document["document_id"],
                "-> version:",
                metadata.get("version"),
                "| status:",
                metadata.get("status"),
            )

    print(f"\nOutput: {OUTPUT_FILE}")
    print(f"Report: {REPORT_FILE}")


if __name__ == "__main__":
    main()
