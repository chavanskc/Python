"""Whoosh schema for the document search index."""

from whoosh.fields import ID, NUMERIC, TEXT, Schema


def build_schema() -> Schema:
    """
    Build the Whoosh schema used for the document search index.

    Fields: path (unique ID), filename (boosted full-text), doc_type
    (stored), content (full-text, stored so the LLM can read the whole
    document later), modified_time (stored, used for incremental reindexing).

    Returns:
        Schema: the Whoosh schema

    Example:
        from doc_search_chatbot.indexing.index_schema import build_schema
        build_schema()
    """
    return Schema(
        path=ID(stored=True, unique=True),
        filename=TEXT(stored=True, field_boost=2.0),
        doc_type=TEXT(stored=True),
        content=TEXT(stored=True),
        modified_time=NUMERIC(stored=True),
    )
