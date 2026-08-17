"""Full-text (BM25) search over the document index."""

from dataclasses import dataclass
from pathlib import Path

from rapidfuzz import fuzz, process
from whoosh.qparser import MultifieldParser

from doc_search_chatbot.indexing.index_builder import open_or_create_index


@dataclass
class SearchResult:
    """
    One ranked search hit, with enough text for an LLM to read the full document.

    Args:
        path (str): absolute path to the source file
        filename (str): base filename
        doc_type (str): one of "text", "pdf", "image"
        snippet (str): short excerpt for display
        content (str): the document's full extracted text
        score (float): ranking score (higher is a better match)

    Example:
        from doc_search_chatbot.indexing.search import SearchResult
        SearchResult(path="C:/docs/w2.pdf", filename="w2.pdf", doc_type="pdf",
                      snippet="...", content="...", score=4.2)
    """

    path: str
    filename: str
    doc_type: str
    snippet: str
    content: str
    score: float


def search(query_text: str, index_dir: Path, limit: int = 5) -> list[SearchResult]:
    """
    Run a BM25 full-text search against the document index.

    Args:
        query_text (str): the user's natural-language-style query
        index_dir (Path): folder where the Whoosh index lives
        limit (int): maximum number of results to return
    Returns:
        list[SearchResult]: ranked results, best match first

    Example:
        from pathlib import Path
        from doc_search_chatbot.indexing.search import search
        search("Bank of America statement", Path("index_store"))
    """
    ix = open_or_create_index(index_dir)
    parser = MultifieldParser(["filename", "content"], schema=ix.schema)
    query = parser.parse(query_text)

    with ix.searcher() as searcher:
        hits = searcher.search(query, limit=limit)
        if hits:
            return [_to_result(hit) for hit in hits]
        return _fuzzy_filename_fallback(query_text, searcher, limit)


def _to_result(hit) -> SearchResult:
    """Convert a Whoosh search hit into a SearchResult."""
    content = hit["content"]
    return SearchResult(
        path=hit["path"],
        filename=hit["filename"],
        doc_type=hit["doc_type"],
        snippet=hit.highlights("content") or content[:200],
        content=content,
        score=hit.score,
    )


def _fuzzy_filename_fallback(query_text: str, searcher, limit: int) -> list[SearchResult]:
    """
    When no BM25 keyword hits are found (e.g. a misspelled name), fall back
    to fuzzy-matching the query against indexed filenames.
    """
    docs = list(searcher.documents())
    if not docs:
        return []

    filenames = [doc["filename"] for doc in docs]
    matches = process.extract(query_text, filenames, scorer=fuzz.WRatio, limit=limit)

    results = []
    for _, score, doc_index in matches:
        doc = docs[doc_index]
        content = doc["content"]
        results.append(SearchResult(
            path=doc["path"],
            filename=doc["filename"],
            doc_type=doc["doc_type"],
            snippet=content[:200],
            content=content,
            score=score,
        ))
    return results
