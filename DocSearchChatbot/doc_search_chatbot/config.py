"""
Central configuration for DocSearchChatbot, read from environment variables
with sensible local defaults.
"""

import os
from pathlib import Path

_source_dir_env = os.environ.get("DOC_SEARCH_SOURCE_DIR")
SOURCE_DOCS_DIR = Path(_source_dir_env) if _source_dir_env else None
INDEX_DIR = Path(os.environ.get("DOC_SEARCH_INDEX_DIR", str(Path(__file__).resolve().parent.parent / "index_store")))

TEXT_EXTENSIONS = {".txt", ".md", ".csv"}
PDF_EXTENSIONS = {".pdf"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tiff", ".bmp"}

OLLAMA_HOST = os.environ.get("DOC_SEARCH_OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("DOC_SEARCH_OLLAMA_MODEL", "llama3.1")

TESSERACT_CMD = os.environ.get("DOC_SEARCH_TESSERACT_CMD", r"C:\Program Files\Tesseract-OCR\tesseract.exe")

SEARCH_RESULT_LIMIT = 5
