"""Builds and incrementally updates the on-disk search index from the source folder."""

import logging
from pathlib import Path

from whoosh import index

from doc_search_chatbot.ingestion.document import Document
from doc_search_chatbot.ingestion.file_scanner import ScannedFile, scan_files
from doc_search_chatbot.ingestion.image_ocr import extract_text_from_image
from doc_search_chatbot.ingestion.pdf_extractor import extract_text_from_pdf
from doc_search_chatbot.ingestion.text_extractor import extract_text
from doc_search_chatbot.indexing.index_schema import build_schema

logger = logging.getLogger(__name__)

_EXTRACTORS = {
    "text": extract_text,
    "pdf": extract_text_from_pdf,
    "image": extract_text_from_image,
}


def open_or_create_index(index_dir: Path) -> index.Index:
    """
    Open the on-disk search index, creating it (and its folder) if missing.

    Args:
        index_dir (Path): folder where the Whoosh index lives
    Returns:
        index.Index: the opened Whoosh index

    Example:
        from pathlib import Path
        from doc_search_chatbot.indexing.index_builder import open_or_create_index
        open_or_create_index(Path("index_store"))
    """
    index_dir.mkdir(parents=True, exist_ok=True)
    if index.exists_in(str(index_dir)):
        return index.open_dir(str(index_dir))
    return index.create_in(str(index_dir), build_schema())


def reindex(source_dir: Path, index_dir: Path) -> dict[str, int]:
    """
    Scan the source folder and add/update every changed file in the index.
    Files whose modified time matches what's already indexed are skipped.
    Files that fail to extract are logged and skipped, not fatal.

    Args:
        source_dir (Path): folder containing the documents to index
        index_dir (Path): folder where the Whoosh index lives
    Returns:
        dict[str, int]: counts for "indexed", "skipped", "errored"

    Example:
        from pathlib import Path
        from doc_search_chatbot.indexing.index_builder import reindex
        reindex(Path("C:/MyDocuments"), Path("index_store"))
    """
    ix = open_or_create_index(index_dir)
    existing_mtimes = _read_existing_mtimes(ix)
    counts = {"indexed": 0, "skipped": 0, "errored": 0}

    writer = ix.writer()
    try:
        for scanned in scan_files(source_dir):
            path_str = str(scanned.path)
            if existing_mtimes.get(path_str) == scanned.mtime:
                counts["skipped"] += 1
                continue
            try:
                _index_one_file(writer, scanned)
                counts["indexed"] += 1
            except Exception:
                logger.exception("Failed to extract/index %s", scanned.path)
                counts["errored"] += 1
        writer.commit()
    except Exception:
        writer.cancel()
        raise

    return counts


def _read_existing_mtimes(ix: index.Index) -> dict[str, float]:
    """Return {path: modified_time} for every document already in the index."""
    with ix.searcher() as searcher:
        return {doc["path"]: doc["modified_time"] for doc in searcher.documents()}


def _index_one_file(writer, scanned: ScannedFile) -> None:
    """Extract text for one scanned file and write/update it in the index."""
    extractor = _EXTRACTORS[scanned.doc_type]
    document = Document(
        path=str(scanned.path),
        filename=scanned.path.name,
        doc_type=scanned.doc_type,
        text=extractor(scanned.path),
        mtime=scanned.mtime,
    )
    writer.update_document(
        path=document.path,
        filename=document.filename,
        doc_type=document.doc_type,
        content=document.text,
        modified_time=document.mtime,
    )
