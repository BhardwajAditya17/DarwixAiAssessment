import re


PII_PATTERNS = {
    "email": re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    ),

    "phone": re.compile(
        r"(?<!\d)(?:\+91[-\s]?)?[6-9]\d{4}[-\s]?\d{5}(?!\d)"
    ),

    "name": re.compile(
        r"(?i)(?<=candidate name:\s)[A-Za-z]+(?:\s+[A-Za-z]+)+"
    ),
}


def redact_text(text):
    detected_pii = []

    for pii_type, pattern in PII_PATTERNS.items():

        matches = pattern.findall(text)

        if matches:
            detected_pii.extend(
                [pii_type] * len(matches)
            )

            text = pattern.sub(
                f"[REDACTED_{pii_type.upper()}]",
                text,
            )

    return text, sorted(set(detected_pii))


def redact_structured_content(content):
    detected_pii = set()

    if isinstance(content, list):

        cleaned_rows = []

        for row in content:

            if not isinstance(row, dict):
                cleaned_rows.append(row)
                continue

            cleaned_row = {}

            for key, value in row.items():

                if isinstance(value, str):

                    redacted_value, found = redact_text(value)

                    cleaned_row[key] = redacted_value
                    detected_pii.update(found)

                else:
                    cleaned_row[key] = value

            cleaned_rows.append(cleaned_row)

        return cleaned_rows, sorted(detected_pii)

    return content, []


def redact_document(document):

    content = document.get("content", "")

    if isinstance(content, str):

        redacted_content, detected_pii = redact_text(content)

    elif isinstance(content, list):

        redacted_content, detected_pii = redact_structured_content(
            content
        )

    else:

        redacted_content = content
        detected_pii = []

    redacted_document = document.copy()

    redacted_document["content"] = redacted_content

    redacted_document["metadata"] = {
        **document.get("metadata", {}),
        "pii_detected": len(detected_pii) > 0,
        "pii_types": detected_pii,
        "pii_redacted": len(detected_pii) > 0,
    }

    return redacted_document
