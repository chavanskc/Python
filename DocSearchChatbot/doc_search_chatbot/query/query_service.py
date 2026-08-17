"""
Answers a user query by searching the index and, if a local LLM is
reachable, asking it to read the top matching document(s) and answer
directly. Returns data only -- callers (cli.py today, a GUI later) do all
printing.
"""

import logging
from dataclasses import dataclass
from pathlib import Path

from doc_search_chatbot.config import INDEX_DIR, SEARCH_RESULT_LIMIT
from doc_search_chatbot.indexing.search import SearchResult, search
from doc_search_chatbot.llm.base import LLMClient
from doc_search_chatbot.llm.ollama_client import OllamaClient

logger = logging.getLogger(__name__)

CONTEXT_DOCUMENT_LIMIT = 2
CONTENT_CHAR_LIMIT = 6000


@dataclass
class QueryResult:
    """
    The outcome of a query: an optional LLM answer, plus the source results it's grounded in.

    Args:
        answer (str | None): LLM-generated answer, or None if no LLM was reachable
        results (list[SearchResult]): ranked search results the answer (if any) is grounded in

    Example:
        from doc_search_chatbot.query.query_service import QueryResult
        QueryResult(answer="$1,200", results=[])
    """

    answer: str | None
    results: list[SearchResult]


def answer_query(query_text: str, index_dir: Path = INDEX_DIR, llm_client: LLMClient | None = None) -> QueryResult:
    """
    Search the document index for a query and, if an LLM backend is
    reachable, generate a direct answer grounded in the top matching
    document(s). Falls back to search-results-only if the LLM call fails.

    Args:
        query_text (str): the user's natural-language-style query
        index_dir (Path): folder where the Whoosh index lives
        llm_client (LLMClient | None): backend to use; defaults to a local
            Ollama client
    Returns:
        QueryResult: the LLM answer (or None) and ranked search results

    Example:
        from doc_search_chatbot.query.query_service import answer_query
        answer_query("Get me the birth certificate of John Smith")
    """
    results = search(query_text, index_dir, limit=SEARCH_RESULT_LIMIT)
    if not results:
        return QueryResult(answer=None, results=[])

    answer = _try_generate_answer(query_text, results, llm_client or OllamaClient())
    return QueryResult(answer=answer, results=results)


def _try_generate_answer(query_text: str, results: list[SearchResult], client: LLMClient) -> str | None:
    """Ask the LLM client to answer using the top results; return None if it's unreachable/fails."""
    try:
        prompt = _build_prompt(query_text, results[:CONTEXT_DOCUMENT_LIMIT])
        return client.generate(prompt)
    except Exception:
        logger.warning("LLM unavailable, falling back to search results only", exc_info=True)
        return None


def _build_prompt(query_text: str, context_results: list[SearchResult]) -> str:
    """Build a grounding prompt from the query and the top search results' full text."""
    documents = "\n\n".join(
        f"Document: {result.filename}\nContent:\n{result.content[:CONTENT_CHAR_LIMIT]}"
        for result in context_results
    )
    return (
        "Answer the question using only the document text below. "
        "If the answer isn't in the text, say you couldn't find it.\n\n"
        f"{documents}\n\n"
        f"Question: {query_text}\n"
        "Answer concisely."
    )
