# DocSearchChatbot — Design

## 1. Overview

DocSearchChatbot searches a local folder of personal documents — plain text
files, PDFs, pictures, and scanned/photographed document images — and
returns the file(s) matching a natural-language-style query. Nothing is
uploaded anywhere; extraction, indexing, and search all run locally.

## 2. Scope boundary

**Phase 1 (this document, built now):**
- Ingest all 4 document types from a source folder.
- Extract text (native for text files/PDFs, OCR for images and scanned PDFs).
- Build a local full-text search index.
- CLI that takes a query, finds the matching file(s), and — using a local
  Ollama LLM reading the extracted text — answers the query directly (e.g.
  the actual HSA dollar figure off a W2), always alongside the source file
  path(s) so the answer is checkable. If Ollama isn't running, the CLI
  falls back to just returning matching file paths + snippets.

**Phase 2 (separate, future, not built now):**
- Anthropic API as an alternative, swappable `LLMClient` (higher accuracy,
  paid) — the interface already supports this, only a concrete client is
  deferred.
- File view / copy-to-folder actions.
- Google Docs/Drive search.
- A GUI (e.g. Streamlit) in place of the CLI.

**Why Ollama moved into Phase 1 but Anthropic stayed in Phase 2:** the
original file-paths-only Phase 1 was scoped to prove out ingestion/OCR/
indexing before adding any answer-generation layer, not to avoid cost —
Ollama is free either way. Since it's free, the user chose to fold it in
now rather than defer it. The Anthropic API stays deferred because it's a
paid, separate-billing alternative, not because it's technically harder.

## 3. Architecture overview

Four components, wired together only by `cli.py`:

- **`ingestion/`** — turns files on disk into `Document` objects (path +
  extracted text + metadata). One module per document type/concern.
- **`indexing/`** — builds and queries a local full-text (BM25) search
  index from a stream of `Document` objects.
- **`llm/`** — an `LLMClient` interface (`base.py`) plus one concrete
  implementation, `OllamaClient` (`ollama_client.py`), that calls a local
  Ollama server. A future Anthropic client (Phase 2) implements the same
  interface with no changes needed elsewhere.
- **`query/`** — thin orchestration: `answer_query(text) -> QueryResult`,
  where `QueryResult` holds an optional LLM-generated `answer` plus the
  ranked `results` (paths/snippets) it was grounded in. Returns data only,
  never prints — so a future GUI can call the exact same function as the
  CLI.

`cli.py` is the only place that prints or reads input; it calls
`index_builder` (to reindex) and `query_service` (to search). See the block
diagram below for the same picture with exact file/function references.

## 4. Block diagram — components & code references

Static component view (no branching/decisions — just what depends on what).
Every box names the actual file and the function/class you'd open to see
that piece of behavior.

```mermaid
flowchart LR
    CLI["cli.py<br/>main() / _run_reindex() / _run_query()"]

    subgraph ING["ingestion/"]
        direction TB
        FS["file_scanner.py<br/>scan_files()"]
        TE["text_extractor.py<br/>extract_text()"]
        PE["pdf_extractor.py<br/>extract_text_from_pdf()"]
        PR["pdf_rasterizer.py<br/>rasterize_pdf_pages()"]
        OCR["image_ocr.py<br/>ocr_image() / extract_text_from_image()"]
        DOC["document.py<br/>Document"]
    end

    subgraph IDX["indexing/"]
        direction TB
        IB["index_builder.py<br/>reindex() / open_or_create_index()"]
        SCH["index_schema.py<br/>build_schema()"]
        SR["search.py<br/>search() / SearchResult"]
    end

    subgraph LLMBOX["llm/"]
        direction TB
        BASE["base.py<br/>LLMClient"]
        OLL["ollama_client.py<br/>OllamaClient.generate()"]
    end

    subgraph QRY["query/"]
        QS["query_service.py<br/>answer_query() / QueryResult"]
    end

    CFG["config.py<br/>SOURCE_DOCS_DIR, INDEX_DIR,<br/>OLLAMA_HOST, OLLAMA_MODEL"]
    STORE[("index_store/<br/>on-disk Whoosh index")]
    SERVER[("Ollama server<br/>localhost:11434")]

    CLI -->|"1) Reindex"| IB
    IB --> FS
    FS -->|".txt/.md/.csv"| TE
    FS -->|".pdf"| PE
    PE --> PR --> OCR
    FS -->|"image"| OCR
    TE --> DOC
    PE --> DOC
    OCR --> DOC
    DOC --> IB
    IB --> SCH
    IB --> STORE

    CLI -->|"2) Ask"| QS
    QS --> SR
    SR --> STORE
    QS --> OLL
    OLL -.->|"implements"| BASE
    OLL --> SERVER

    CFG -.-> FS
    CFG -.-> IB
    CFG -.-> OLL
```

## 5. Ingestion & indexing flow

```mermaid
flowchart TD
    A[Source folder] --> B["file_scanner.scan_files()"]
    B --> C{Already indexed<br/>and unchanged?<br/>mtime match}
    C -- yes --> Z[Skip]
    C -- no --> D{File type}
    D -- .txt/.md/.csv --> E["text_extractor.extract_text()"]
    D -- .pdf --> F["pdf_extractor.extract_text_from_pdf()"]
    F --> G{Text layer<br/>found?}
    G -- yes --> H["document.Document"]
    G -- no, scanned PDF --> I["pdf_rasterizer.rasterize_pdf_pages()"]
    I --> J["image_ocr.ocr_image()"]
    D -- image/photo --> J2["image_ocr.extract_text_from_image()"]
    J --> H
    J2 --> H
    E --> H
    H --> K["index_builder._index_one_file()<br/>(writer.update_document)"]
    K --> L[(On-disk search index<br/>index_store/)]
```

## 6. Query flow

```mermaid
flowchart TD
    U["User types a query in cli.py: _run_query()"] --> Q["query_service.answer_query()"]
    Q --> S["search.search()<br/>(BM25 via Whoosh)"]
    S --> R["search._fuzzy_filename_fallback()<br/>(only if zero BM25 hits)"]
    R --> RES["list[SearchResult]:<br/>path, snippet, full text, score"]
    RES --> AV{Ollama<br/>reachable?}
    AV -- yes --> LLM["OllamaClient.generate()<br/>via query_service._build_prompt()"]
    LLM --> QR["QueryResult(answer, results)"]
    AV -- no, exception caught in<br/>query_service._try_generate_answer() --> QR2["QueryResult(answer=None, results)"]
    QR --> CLI["cli.py: _run_query() prints<br/>answer, then source file paths"]
    QR2 --> CLI

    CLI -.-> P2[["Phase 2 (not built):<br/>Anthropic API client<br/>+ view/copy actions"]]
```

## 7. Data model

| `Document` (ingestion) | Whoosh schema field (indexing) |
|---|---|
| `path: Path` | `path` (stored, unique ID) |
| `filename: str` | `filename` (indexed, boosted) |
| `doc_type: str` | `doc_type` (stored) |
| `text: str` | `content` (indexed AND stored, so the full text can be handed to the LLM, not just a snippet) |
| `mtime: float` | `modified_time` (stored, used for incremental skip) |

## 8. Config & privacy

- `SOURCE_DOCS_DIR` (the user's real document folder) and `INDEX_DIR`
  (where the on-disk index lives) are set in `config.py`, both configurable
  via environment variables, and both stay **outside** version control.
- `OLLAMA_HOST` (default `http://localhost:11434`) and `OLLAMA_MODEL`
  (default `llama3.1`) are also set in `config.py`, env-var-overridable.
  Extracted document text sent to Ollama stays on the local machine — the
  Ollama server runs locally, nothing is sent to a remote API in Phase 1.
- `index_store/` (the default `INDEX_DIR`) is excluded via the workspace
  `.gitignore` — it contains extracted text from personal documents (birth
  certificates, bank statements, W2s) and must never be committed.
- Source documents themselves are never copied into the repo.

**Where to put your documents:** anywhere on disk — the folder can stay
exactly where it already is. Ingestion is read-only (`file_scanner.scan_files`
walks it, the extractors read each file); nothing is ever moved, copied, or
modified. The one hard rule: keep it **outside** `DocSearchChatbot/`, since
that folder is inside the git repo and personal documents must never end up
git-tracked.

**Setting `SOURCE_DOCS_DIR`:**
- Environment variable, before launching (PowerShell):
  `$env:DOC_SEARCH_SOURCE_DIR = "C:\path\to\your\documents"` — lasts for
  that terminal session only. Set it as a permanent Windows user environment
  variable (System Properties → Environment Variables) to avoid repeating this.
- **At runtime, no restart needed:** `cli.py` prompts for the folder
  interactively on startup if the environment variable isn't set (or points
  somewhere that doesn't exist), and menu option "Change documents folder"
  lets you switch to a different folder mid-session — useful for pointing
  at more than one document collection without restarting or touching
  environment variables at all.

## 9. Non-functional notes

- **Incremental reindexing:** a file is only re-extracted/re-indexed if its
  `mtime` differs from what's stored in the index.
- **Error handling:** unreadable or corrupt files are logged and skipped;
  one bad file never aborts a full reindex run.
- **Logging:** basic logging (file processed, OCR fallback triggered, file
  skipped/errored) to stdout.

## 10. Out of scope for Phase 1

- Anthropic API as an LLM backend (the interface supports it; only the
  concrete client is deferred to Phase 2).
- Google Docs/Drive search.
- Any GUI.
- File view / copy-to-folder actions.

## 11. Appendix — library choices & cost

| Concern | Library | Install | Cost |
|---|---|---|---|
| Plain text (.txt/.md/.csv) | stdlib | built-in | $0 |
| PDF text-layer extraction | `pypdf` | pip | $0 |
| Scanned-PDF page rasterization | `PyMuPDF` (`fitz`) | pip | $0 (AGPL-3.0, fine for personal use) |
| Image OCR | `Pillow` + `pytesseract` | pip | $0 |
| OCR engine | Tesseract OCR (UB-Mannheim build) | system installer | $0, one-time |
| Fuzzy filename matching | `rapidfuzz` | pip | $0 |
| Full-text search & ranking | `whoosh` (or actively-maintained fork) | pip | $0 |
| Local LLM answer generation | `ollama` (official Python client) + Ollama app (system install) + a pulled model, e.g. `llama3.1` (~4.7GB) | pip + system installer + one-time model download | $0, runs entirely on your machine |

Phase 1 has zero ongoing API cost — Ollama runs locally and is free. Phase 2
adds the Anthropic API as an alternative, higher-accuracy `LLMClient`: it's
billed separately at console.anthropic.com (a claude.ai Pro/Max chat
subscription does not cover API usage), while Ollama remains the zero-cost
option.
