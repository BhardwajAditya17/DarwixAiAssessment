import json
from pathlib import Path

from pii_redaction import redact_document


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cleaned_documents"
    / "versioned_documents.json"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "pii_redacted"
)

OUTPUT_FILE = OUTPUT_DIR / "redacted_documents.json"
REPORT_FILE = OUTPUT_DIR / "pii_report.json"


def main():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        documents = json.load(f)

    redacted_documents = [
        redact_document(document)
        for document in documents
    ]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            redacted_documents,
            f,
            indent=2,
            ensure_ascii=False,
        )

    pii_report = []

    for document in redacted_documents:

        metadata = document.get("metadata", {})

        if metadata.get("pii_detected"):

            pii_report.append({
                "document_id": document["document_id"],
                "title": document["title"],
                "pii_types": metadata["pii_types"],
            })

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            pii_report,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"Processed {len(redacted_documents)} documents")
    print(f"Documents containing PII: {len(pii_report)}")

    for item in pii_report:
        print(
            item["document_id"],
            "->",
            ", ".join(item["pii_types"])
        )

    print(f"\nOutput: {OUTPUT_FILE}")
    print(f"Report: {REPORT_FILE}")


if __name__ == "__main__":
    main()
