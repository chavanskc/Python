"""PDF text extraction: uses the PDF's text layer, falling back to OCR for scanned PDFs."""

from pathlib import Path

from pypdf import PdfReader

from doc_search_chatbot.ingestion.image_ocr import ocr_image
from doc_search_chatbot.ingestion.pdf_rasterizer import rasterize_pdf_pages

MIN_TEXT_LAYER_LENGTH = 20


def extract_text_from_pdf(file_path: Path) -> str:
    """
    Extract text from a PDF, using its embedded text layer when present and
    falling back to OCR (via page rasterization) for scanned/image-only PDFs.

    Args:
        file_path (Path): path to a .pdf file
    Returns:
        str: extracted (or OCR'd) text content

    Example:
        from doc_search_chatbot.ingestion.pdf_extractor import extract_text_from_pdf
        extract_text_from_pdf(Path("statement.pdf"))
    """
    reader = PdfReader(file_path)
    text_layer = "\n".join(page.extract_text() or "" for page in reader.pages)

    if len(text_layer.strip()) >= MIN_TEXT_LAYER_LENGTH:
        return text_layer

    pages = rasterize_pdf_pages(file_path)
    return "\n".join(ocr_image(page) for page in pages)
