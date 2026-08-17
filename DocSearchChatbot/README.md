# DocSearchChatbot

## Purpose
A local chatbot that searches a folder of personal documents — plain text
files, PDFs, pictures, and scanned/photographed document images — and
answers questions like "get me the birth certificate of John Smith" or
"what was my HSA contribution for 2024 from my W2." Documents never leave
your machine: extraction, indexing, search, and (optionally) answer
generation all run locally. See [DESIGN.md](DESIGN.md) for the full
architecture and flow diagrams.

**Phase 1 (this version):** ingest all 4 document types, build a local
search index, and answer questions — grounded in the matching document's
text via a local Ollama model — always alongside the source file path(s).
If Ollama isn't running, it falls back to just showing matching files.
**Not yet built:** Anthropic API backend, Google Drive search, a GUI, and
file view/copy actions — see DESIGN.md section 9 for the full list.

## Structure
- `doc_search_chatbot/` — this project's library package.
  - `config.py` — `SOURCE_DOCS_DIR`, `INDEX_DIR`, `OLLAMA_HOST`/`OLLAMA_MODEL`,
    all environment-variable-configurable.
  - `ingestion/` — turns files into `Document`s: `text_extractor.py` (.txt/
    .md/.csv), `pdf_extractor.py` (PDF text layer, OCR fallback for scanned
    PDFs), `pdf_rasterizer.py` (renders PDF pages to images), `image_ocr.py`
    (Tesseract OCR), `file_scanner.py` (walks and classifies the source folder).
  - `indexing/` — `index_schema.py` (Whoosh schema), `index_builder.py`
    (incremental reindexing), `search.py` (BM25 search with a fuzzy-filename
    fallback for misspelled queries).
  - `llm/` — `base.py` (the `LLMClient` interface), `ollama_client.py` (the
    local Ollama implementation).
  - `query/` — `query_service.py`: `answer_query()` ties search + the LLM
    together and returns data only; it's what both `cli.py` and any future
    GUI call.
- `cli.py` — entry point: interactive menu (reindex / ask / quit) that
  calls into `doc_search_chatbot`. No logic of its own.
- `DESIGN.md` — architecture, flow diagrams, scope boundaries, library/cost
  reference.
- `index_store/` — the on-disk search index (gitignored — contains
  extracted text from your personal documents).

## How to run
Prerequisites (one-time):
1. Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
   (Windows installer).
2. Install [Ollama](https://ollama.com/download) and pull a model:
   `ollama pull llama3.1`
3. Install the Python dependencies (see `requirements.txt`).

Then, from this folder:
```
D:\Software\Python_venv\venv_1\Scripts\python.exe cli.py
```
If `DOC_SEARCH_SOURCE_DIR` isn't set, the CLI prompts for your documents
folder on startup (any folder on disk — nothing is copied or moved, just
read). To skip the prompt, set it beforehand:
```
set DOC_SEARCH_SOURCE_DIR=C:\path\to\your\documents
```
Choose `1` to build/update the index, `2` to ask a question, or `3` to
switch to a different documents folder without restarting.

## How to import & reuse
```python
from doc_search_chatbot.indexing.index_builder import reindex
from doc_search_chatbot.query.query_service import answer_query
from pathlib import Path

reindex(Path("C:/MyDocuments"), Path("index_store"))
result = answer_query("Bank of America statement")
result.answer     # LLM-generated answer, or None if Ollama unavailable
result.results    # ranked [SearchResult(path, filename, snippet, ...)]
```

## Features / Changelog
- 2026-08-16: Phase 1 scaffold and design (ingestion for text/PDF/image
  documents with OCR fallback, Whoosh full-text search with fuzzy-filename
  fallback, local Ollama-backed answer generation, CLI)
- 2026-08-16: CLI prompts for the documents folder at startup when
  `DOC_SEARCH_SOURCE_DIR` isn't set, and gained a "change documents folder"
  menu option to switch at runtime without restarting
