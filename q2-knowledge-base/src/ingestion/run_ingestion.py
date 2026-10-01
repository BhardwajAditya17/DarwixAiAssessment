from pathlib import Path
import json

from web_loader import load_markdown_file
from pdf_loader import load_pdf_source
from table_loader import load_csv_file


RAW_DIR = Path("data/raw")
OUTPUT_FILE = Path("data/processed/cleaned_documents/ingested_documents.json")


def ingest_markdown_directory(directory: Path, source_type: str):
    documents = []

    for file_path in sorted(directory.glob("*.md")):
        if source_type == "pdf":
            document = load_pdf_source(str(file_path))
        else:
            document = load_markdown_file(
                str(file_path),
                source_type=source_type
            )

        documents.append(document)

    return documents


def ingest_csv_directory(directory: Path):
    documents = []

    for file_path in sorted(directory.glob("*.csv")):
        documents.append(load_csv_file(str(file_path)))

    return documents


def main():
    documents = []

    documents.extend(
        ingest_markdown_directory(
            RAW_DIR / "website",
            "website"
        )
    )

    documents.extend(
        ingest_markdown_directory(
            RAW_DIR / "pdfs",
            "pdf"
        )
    )

    documents.extend(
        ingest_markdown_directory(
            RAW_DIR / "forms",
            "form"
        )
    )

    documents.extend(
        ingest_markdown_directory(
            RAW_DIR / "marketing",
            "marketing"
        )
    )

    documents.extend(
        ingest_csv_directory(
            RAW_DIR / "tables"
        )
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(
            documents,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(f"Ingested {len(documents)} documents")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
