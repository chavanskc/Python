"""Walks the source documents folder and classifies each file by type."""

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from doc_search_chatbot.config import IMAGE_EXTENSIONS, PDF_EXTENSIONS, TEXT_EXTENSIONS


@dataclass
class ScannedFile:
    """A file found on disk, classified but not yet text-extracted."""

    path: Path
    doc_type: str
    mtime: float


def scan_files(source_dir: Path) -> Iterator[ScannedFile]:
    """
    Walk a folder and yield every supported file, classified by type.
    Files with unsupported extensions are silently skipped.

    Args:
        source_dir (Path): folder to walk recursively
    Returns:
        Iterator[ScannedFile]: one entry per supported file found

    Example:
        from pathlib import Path
        from doc_search_chatbot.ingestion.file_scanner import scan_files
        list(scan_files(Path("C:/MyDocuments")))
    """
    for path in source_dir.rglob("*"):
        if not path.is_file():
            continue
        doc_type = _classify(path)
        if doc_type is None:
            continue
        yield ScannedFile(path=path, doc_type=doc_type, mtime=path.stat().st_mtime)


def _classify(path: Path) -> str | None:
    """Return "text"/"pdf"/"image" for a supported extension, else None."""
    suffix = path.suffix.lower()
    if suffix in TEXT_EXTENSIONS:
        return "text"
    if suffix in PDF_EXTENSIONS:
        return "pdf"
    if suffix in IMAGE_EXTENSIONS:
        return "image"
    return None
