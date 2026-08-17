"""OCR text extraction for images (photos of documents, or rasterized PDF pages)."""

from pathlib import Path

import pytesseract
from PIL import Image

from doc_search_chatbot.config import TESSERACT_CMD

if Path(TESSERACT_CMD).exists():
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


def ocr_image(image: Image.Image) -> str:
    """
    Run OCR (Tesseract) on an already-loaded image and return the recognized text.

    Args:
        image (Image.Image): a Pillow image, e.g. from a photo or a rasterized PDF page
    Returns:
        str: OCR-recognized text, possibly empty if nothing was readable

    Example:
        from doc_search_chatbot.ingestion.image_ocr import ocr_image
        from PIL import Image
        ocr_image(Image.open("scanned_w2.jpg"))
    """
    return pytesseract.image_to_string(image)


def extract_text_from_image(file_path: Path) -> str:
    """
    Run OCR (Tesseract) on an image file and return the recognized text.

    Args:
        file_path (Path): path to an image file (.png/.jpg/.jpeg/.tiff/.bmp)
    Returns:
        str: OCR-recognized text, possibly empty if nothing was readable

    Example:
        from doc_search_chatbot.ingestion.image_ocr import extract_text_from_image
        extract_text_from_image(Path("scanned_w2.jpg"))
    """
    with Image.open(file_path) as image:
        return ocr_image(image)
