from pathlib import Path


def load_pdf_source(file_path: str) -> dict:
    path = Path(file_path)

    content = path.read_text(encoding="utf-8")

    title = path.stem.replace("_", " ").title()

    first_heading = None

    for line in content.splitlines():
        line = line.strip()

        if line.startswith("# "):
            first_heading = line[2:].strip()
            break

    if first_heading:
        title = first_heading

    return {
        "document_id": f"pdf_{path.stem}",
        "source_type": "pdf",
        "source_file": str(path),
        "title": title,
        "content": content,
        "metadata": {
            "file_name": path.name,
            "file_extension": path.suffix,
        },
    }
