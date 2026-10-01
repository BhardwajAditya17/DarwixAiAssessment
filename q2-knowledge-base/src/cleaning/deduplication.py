import hashlib
import re
from difflib import SequenceMatcher


def normalize_for_comparison(text):
    """
    Create a normalized representation for duplicate comparison.
    """
    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()


def content_hash(content):
    """
    Generate an exact-content hash.
    """
    normalized = normalize_for_comparison(content)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def similarity_score(content_a, content_b):
    """
    Calculate a simple near-duplicate similarity score.
    """
    a = normalize_for_comparison(content_a)
    b = normalize_for_comparison(content_b)

    return SequenceMatcher(None, a, b).ratio()


def find_duplicates(documents, similarity_threshold=0.90):
    """
    Detect exact and near-duplicate documents.

    Returns:
        duplicate_groups
    """

    duplicate_groups = []
    visited = set()

    normalized_contents = {
        doc["document_id"]: normalize_for_comparison(
            doc.get("content", "")
        )
        for doc in documents
    }

    for i, doc_a in enumerate(documents):

        if doc_a["document_id"] in visited:
            continue

        group = [doc_a["document_id"]]

        for doc_b in documents[i + 1:]:

            if doc_b["document_id"] in visited:
                continue

            score = similarity_score(
                normalized_contents[doc_a["document_id"]],
                normalized_contents[doc_b["document_id"]],
            )

            if score >= similarity_threshold:
                group.append(doc_b["document_id"])

        if len(group) > 1:
            duplicate_groups.append(group)
            visited.update(group)

    return duplicate_groups


def detect_document_version(document):
    """
    Detect version/status information from document metadata/content.
    """

    content = str(document.get("content", ""))

    version_match = re.search(
        r"version\s*[:\-]?\s*([0-9]+(?:\.[0-9]+)*)",
        content,
        flags=re.IGNORECASE,
    )

    status = None

    if re.search(r"\bsuperseded\b", content, re.IGNORECASE):
        status = "superseded"
    elif re.search(r"\bactive\b", content, re.IGNORECASE):
        status = "active"

    version = version_match.group(1) if version_match else None

    return {
        "version": version,
        "status": status,
    }


def annotate_versions(documents):
    """
    Add version information to document metadata.
    """

    annotated = []

    for document in documents:
        document = document.copy()

        version_info = detect_document_version(document)

        document["metadata"] = {
            **document.get("metadata", {}),
            "version": version_info["version"],
            "status": version_info["status"],
        }

        annotated.append(document)

    return annotated
