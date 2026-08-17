"""Shared data model for an ingested, text-extracted file."""

from dataclasses import dataclass


@dataclass
class Document:
    """
    A single ingested file with its extracted text and basic metadata.

    Args:
        path (str): absolute path to the source file
        filename (str): base filename, e.g. "w2_2024.pdf"
        doc_type (str): one of "text", "pdf", "image"
        text (str): extracted (or OCR'd) text content
        mtime (float): source file's last-modified time (epoch seconds),
            used to detect changes for incremental reindexing

    Example:
        from doc_search_chatbot.ingestion.document import Document
        doc = Document(path="C:/docs/w2_2024.pdf", filename="w2_2024.pdf",
                        doc_type="pdf", text="...", mtime=1700000000.0)
    """

    path: str
    filename: str
    doc_type: str
    text: str
    mtime: float
