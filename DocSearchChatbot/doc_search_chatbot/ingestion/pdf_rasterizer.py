"""Renders PDF pages to images, for OCR fallback on scanned (text-less) PDFs."""

from pathlib import Path

import pymupdf as fitz
from PIL import Image


def rasterize_pdf_pages(file_path: Path) -> list[Image.Image]:
    """
    Render every page of a PDF to a PIL Image.

    Args:
        file_path (Path): path to a .pdf file
    Returns:
        list[Image.Image]: one image per page, in page order

    Example:
        from doc_search_chatbot.ingestion.pdf_rasterizer import rasterize_pdf_pages
        rasterize_pdf_pages(Path("scanned_statement.pdf"))
    """
    pages = []
    with fitz.open(file_path) as pdf:
        for page in pdf:
            pixmap = page.get_pixmap()
            image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
            pages.append(image)
    return pages
