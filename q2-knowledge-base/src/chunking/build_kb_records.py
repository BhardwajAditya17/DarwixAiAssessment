import json
import hashlib
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "pii_redacted"
    / "redacted_documents.json"
)

OUTPUT_DIR = PROJECT_ROOT / "kb"
OUTPUT_FILE = OUTPUT_DIR / "records.json"


def generate_record_id(document_id, index):
    raw = f"{document_id}_{index}"
    short_hash = hashlib.md5(
        raw.encode("utf-8")
    ).hexdigest()[:8]

    return f"kb_{document_id}_{short_hash}"


def detect_category(document):
    """
    Assign a high-level category based on source and title.
    """

    title = document.get("title", "").lower()
    source_type = document.get("source_type", "").lower()

    if "faq" in title:
        return "faq"

    if "policy" in title:
        return "policy"

    if "eligibility" in title:
        return "qualification"

    if "requirement" in title:
        return "qualification"

    if "screening rule" in title:
        return "screening_rules"

    if "interview" in title:
        return "interview"

    if "application" in title or "candidate record" in title:
        return "candidate_data"

    if "careers" in title:
        return "company"

    if source_type == "website":
        return "website"

    if source_type == "marketing":
        return "marketing"

    return "general"


def create_record(document, content, index):

    metadata = document.get("metadata", {})

    return {
        "record_id": generate_record_id(
            document["document_id"],
            index,
        ),

        "document_id": document["document_id"],

        "title": document["title"],

        "content": content,

        "category": detect_category(document),

        "source": {
            "source_type": document.get("source_type"),
            "source_file": document.get("source_file"),
            "document_id": document.get("document_id"),
        },

        "version": metadata.get("version"),

        "status": metadata.get("status"),

        "pii": metadata.get(
            "pii_detected",
            False,
        ),

        "metadata": {
            "cleaning_applied": metadata.get(
                "cleaning_applied",
                False,
            ),
            "pii_redacted": metadata.get(
                "pii_redacted",
                False,
            ),
        },
    }


def build_records(documents):

    records = []

    for document in documents:

        content = document.get("content")

        # Text documents become one initial KB record.
        if isinstance(content, str):

            records.append(
                create_record(
                    document,
                    content,
                    0,
                )
            )

        # Structured tables become one record per row.
        elif isinstance(content, list):

            for index, row in enumerate(content):

                row_text = json.dumps(
                    row,
                    ensure_ascii=False,
                )

                records.append(
                    create_record(
                        document,
                        row_text,
                        index,
                    )
                )

    return records


def main():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        documents = json.load(f)

    records = build_records(documents)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            records,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print("Documents:", len(documents))
    print("KB records:", len(records))
    print("Output:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
