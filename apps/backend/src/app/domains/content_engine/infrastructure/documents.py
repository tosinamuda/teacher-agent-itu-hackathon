"""The text of a teacher's document: plain text, Markdown, Word or PDF."""

from __future__ import annotations

from io import BytesIO
from pathlib import PurePath

MAX_DOCUMENT_BYTES = 5 * 1024 * 1024
READABLE = (".txt", ".md", ".docx", ".pdf")


class DocumentUnreadableError(ValueError):
    """The document is not one the app can read; the message says what it takes."""


def _docx(data: bytes) -> str:
    from docx import Document

    document = Document(BytesIO(data))
    lines = [paragraph.text for paragraph in document.paragraphs]
    for table in document.tables:
        for row in table.rows:
            lines.append(" | ".join(cell.text.strip() for cell in row.cells))
    return "\n".join(lines)


def _pdf(data: bytes) -> str:
    from pypdf import PdfReader

    return "\n\n".join(page.extract_text() or "" for page in PdfReader(BytesIO(data)).pages)


def document_text(filename: str, data: bytes) -> str:
    """The document's text, or a refusal that says why it cannot be read."""
    if len(data) > MAX_DOCUMENT_BYTES:
        raise DocumentUnreadableError("the document is larger than 5 MB")
    suffix = PurePath(filename).suffix.lower()
    try:
        if suffix in (".txt", ".md"):
            text = data.decode("utf-8", errors="replace")
        elif suffix == ".docx":
            text = _docx(data)
        elif suffix == ".pdf":
            text = _pdf(data)
        else:
            raise DocumentUnreadableError(f"send one of {', '.join(READABLE)}")
    except DocumentUnreadableError:
        raise
    except Exception as error:  # noqa: BLE001 - any parser failure means the file is unreadable
        raise DocumentUnreadableError(f"the {suffix} file could not be read") from error
    if not text.strip():
        raise DocumentUnreadableError("the document has no text; a scanned PDF needs typed text")
    return text.strip()
