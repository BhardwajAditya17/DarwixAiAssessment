import json
from pathlib import Path

from chunker import chunk_text


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "kb" / "records.json"
OUTPUT_FILE = PROJECT_ROOT / "kb" / "chunks.json"


def build_chunks(records):

    chunks = []

    for record in records:

        content = record["content"]

        if record["category"] in {
            "qualification",
            "screening_rules",
            "candidate_data",
        }:
            text_chunks = [content]

        else:
            text_chunks = chunk_text(
                content,
                max_chars=900,
                overlap_chars=150,
            )

        for index, chunk in enumerate(text_chunks):

            chunks.append({
                "chunk_id": f"{record['record_id']}_chunk_{index}",
                "record_id": record["record_id"],
                "document_id": record["document_id"],
                "title": record["title"],
                "content": chunk,
                "category": record["category"],
                "source": record["source"],
                "version": record["version"],
                "status": record["status"],
                "pii": record["pii"],
                "chunk_index": index,
                "metadata": {
                    "chunk_size": len(chunk),
                    "retrieval_enabled": (
                        record["status"] != "superseded"
                    ),
                },
            })

    return chunks


def main():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        records = json.load(f)

    chunks = build_chunks(records)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            chunks,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print("KB records:", len(records))
    print("Chunks:", len(chunks))
    print("Output:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
