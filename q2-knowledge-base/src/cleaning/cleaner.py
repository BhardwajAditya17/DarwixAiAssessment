import re


def normalize_whitespace(text):
    """
    Normalize whitespace while preserving paragraph structure.
    """
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    text = "\n".join(line.rstrip() for line in text.split("\n"))

    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def clean_markdown(text):
    """
    Remove common navigation/boilerplate sections while
    preserving useful business content.
    """
    lines = text.splitlines()
    cleaned = []

    skip_section = False

    for line in lines:
        stripped = line.strip()

        if stripped.lower() in {
            "# navigation",
            "## navigation",
            "# menu",
            "## menu",
            "# footer",
            "## footer",
        }:
            skip_section = True
            continue

        if skip_section and stripped.startswith("#"):
            skip_section = False

        if skip_section:
            continue

        cleaned.append(line)

    return normalize_whitespace("\n".join(cleaned))


def standardize_terminology(text):
    """
    Standardize terminology used across the synthetic corpus.
    """

    replacements = {
        "professional experience": "years of experience",
        "work experience": "years of experience",
    }

    for old, new in replacements.items():
        text = re.sub(
            rf"\b{re.escape(old)}\b",
            new,
            text,
            flags=re.IGNORECASE,
        )

    return text


def clean_structured_content(content):
    """
    Preserve structured table data while normalizing
    string values inside rows.
    """

    if isinstance(content, list):
        cleaned_rows = []

        for row in content:
            if isinstance(row, dict):
                cleaned_row = {}

                for key, value in row.items():
                    if isinstance(value, str):
                        value = normalize_whitespace(value)

                    cleaned_row[key] = value

                cleaned_rows.append(cleaned_row)

            else:
                cleaned_rows.append(row)

        return cleaned_rows

    return content


def clean_document(document):
    """
    Clean a document while preserving its original structure
    and source metadata.
    """

    original_content = document.get("content", "")

    if isinstance(original_content, str):
        cleaned_content = clean_markdown(original_content)
        cleaned_content = standardize_terminology(cleaned_content)

    elif isinstance(original_content, list):
        cleaned_content = clean_structured_content(original_content)

    else:
        cleaned_content = original_content

    cleaned_document = document.copy()

    cleaned_document["content"] = cleaned_content

    original_size = len(str(original_content))
    cleaned_size = len(str(cleaned_content))

    cleaned_document["metadata"] = {
        **document.get("metadata", {}),
        "cleaning_applied": True,
        "original_character_count": original_size,
        "cleaned_character_count": cleaned_size,
    }

    return cleaned_document
