import re


def split_into_paragraphs(text):
    text = text.strip()

    if not text:
        return []

    paragraphs = re.split(r"\n\s*\n", text)

    return [
        paragraph.strip()
        for paragraph in paragraphs
        if paragraph.strip()
    ]


def chunk_text(text, max_chars=900, overlap_chars=150):
    paragraphs = split_into_paragraphs(text)

    chunks = []
    current = ""

    for paragraph in paragraphs:

        if len(paragraph) > max_chars:

            if current:
                chunks.append(current.strip())
                current = ""

            start = 0

            while start < len(paragraph):

                end = start + max_chars
                piece = paragraph[start:end].strip()

                if piece:
                    chunks.append(piece)

                start = end - overlap_chars

            continue

        candidate = (
            paragraph
            if not current
            else current + "\n\n" + paragraph
        )

        if len(candidate) <= max_chars:
            current = candidate

        else:
            if current:
                chunks.append(current.strip())

            overlap = current[-overlap_chars:] if current else ""

            current = (
                overlap + "\n\n" + paragraph
                if overlap
                else paragraph
            )

    if current:
        chunks.append(current.strip())

    return chunks
