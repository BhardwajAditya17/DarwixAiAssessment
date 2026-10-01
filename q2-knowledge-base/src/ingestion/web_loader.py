from pathlib import Path


def load_markdown_file(file_path: str, source_type: str = "website") -> dict:
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
        "document_id": f"{source_type}_{path.stem}",
        "source_type": source_type,
        "source_file": str(path),
        "title": title,
        "content": content,
        "metadata": {
            "file_name": path.name,
            "file_extension": path.suffix,
        },
    }
