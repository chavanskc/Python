from doc_search_chatbot import config
from doc_search_chatbot.indexing.index_builder import reindex
from doc_search_chatbot.query.query_service import answer_query

MENU = """
1) Reindex documents
2) Ask a question
3) Quit
"""


def main():
    if not config.SOURCE_DOCS_DIR or not config.SOURCE_DOCS_DIR.exists():
        print("Set the DOC_SEARCH_SOURCE_DIR environment variable to your documents folder, then rerun.")
        return

    while True:
        print(MENU)
        choice = input("Choose an option (1-3): ").strip()

        if choice == "3":
            print("Goodbye!")
            break

        if choice == "1":
            _run_reindex()
        elif choice == "2":
            _run_query()
        else:
            print("Invalid option. Please choose 1-3.")


def _run_reindex():
    counts = reindex(config.SOURCE_DOCS_DIR, config.INDEX_DIR)
    print(f"Indexed: {counts['indexed']}, skipped (unchanged): {counts['skipped']}, errored: {counts['errored']}")


def _run_query():
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
