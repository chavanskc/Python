"""Text extraction for plain-text files (.txt/.md/.csv)."""

from pathlib import Path


def extract_text(file_path: Path) -> str:
    """
    Read the full contents of a plain-text file.

    Args:
        file_path (Path): path to a .txt/.md/.csv file
    Returns:
        str: the file's text content

    Example:
        from doc_search_chatbot.ingestion.text_extractor import extract_text
        extract_text(Path("notes.txt"))
    """
    return file_path.read_text(encoding="utf-8", errors="replace")
