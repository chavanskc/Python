"""LLMClient interface: any backend (Ollama now, Anthropic later) implements this."""

from typing import Protocol


class LLMClient(Protocol):
    """
    Interface for a text-generation backend used to answer a query from
    grounding text pulled out of the user's documents.

    Example:
        from doc_search_chatbot.llm.base import LLMClient
        from doc_search_chatbot.llm.ollama_client import OllamaClient

        client: LLMClient = OllamaClient()
        client.generate("What is 2 + 2?")
    """

    def generate(self, prompt: str) -> str:
        """
        Generate a text response for the given prompt.

        Args:
            prompt (str): the full prompt, including any grounding context
        Returns:
            str: the model's response text
        """
        ...
