import json
from pathlib import Path

from cleaner import clean_document


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cleaned_documents"
    / "ingested_documents.json"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cleaned_documents"
)

OUTPUT_FILE = OUTPUT_DIR / "cleaned_documents.json"


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        documents = json.load(f)

    cleaned_documents = [
        clean_document(document)
        for document in documents
    ]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            cleaned_documents,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"Cleaned {len(cleaned_documents)} documents")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
