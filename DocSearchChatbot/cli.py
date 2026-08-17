from pathlib import Path

from doc_search_chatbot import config
from doc_search_chatbot.indexing.index_builder import reindex
from doc_search_chatbot.query.query_service import answer_query

MENU = """
1) Reindex documents
2) Ask a question
3) Change documents folder
4) Quit
"""


def main():
    """Run the interactive reindex/ask/change-folder/quit menu loop."""
    source_dir = _resolve_source_dir()

    while True:
        print(f"\nDocuments folder: {source_dir}")
        print(MENU)
        choice = input("Choose an option (1-4): ").strip()

        if choice == "4":
            print("Goodbye!")
            break

        if choice == "1":
            _run_reindex(source_dir)
        elif choice == "2":
            _run_query()
        elif choice == "3":
            source_dir = _prompt_for_source_dir()
        else:
            print("Invalid option. Please choose 1-4.")


def _resolve_source_dir() -> Path:
    """Use DOC_SEARCH_SOURCE_DIR if it's set and valid, else prompt for a folder."""
    if config.SOURCE_DOCS_DIR and config.SOURCE_DOCS_DIR.exists():
        return config.SOURCE_DOCS_DIR
    print("No documents folder configured (set DOC_SEARCH_SOURCE_DIR to skip this prompt next time).")
    return _prompt_for_source_dir()


def _prompt_for_source_dir() -> Path:
    """Repeatedly ask for a folder path until an existing directory is given."""
    while True:
        raw_path = input("Enter the full path to your documents folder: ").strip().strip('"')
        path = Path(raw_path)
        if path.is_dir():
            return path
        print("That folder doesn't exist. Try again.")


def _run_reindex(source_dir: Path):
    """Reindex source_dir and print the resulting indexed/skipped/errored counts."""
    counts = reindex(source_dir, config.INDEX_DIR)
    print(f"Indexed: {counts['indexed']}, skipped (unchanged): {counts['skipped']}, errored: {counts['errored']}")


def _run_query():
    """Prompt for a question and print the LLM answer (if any) and matching files."""
    query_text = input("Ask a question: ").strip()
    if not query_text:
        return

    result = answer_query(query_text)

    if result.answer:
        print(f"\nAnswer: {result.answer}\n")
    elif not result.results:
        print("No matching documents found.")
    else:
        print("\n(Local LLM unavailable -- showing matching documents only)\n")

    for i, item in enumerate(result.results, start=1):
        print(f"{i}. {item.filename}  ({item.path})")
        print(f"   {item.snippet}\n")


if __name__ == "__main__":
    main()
