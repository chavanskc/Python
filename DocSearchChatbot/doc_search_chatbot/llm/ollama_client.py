"""LLMClient implementation backed by a local Ollama server."""

import ollama

from doc_search_chatbot.config import OLLAMA_HOST, OLLAMA_MODEL


class OllamaClient:
    """
    Generates text using a locally running Ollama server. Implements the
    LLMClient interface (doc_search_chatbot.llm.base.LLMClient).

    Args:
        host (str): Ollama server URL, defaults to config.OLLAMA_HOST
        model (str): model name to use, defaults to config.OLLAMA_MODEL

    Example:
        from doc_search_chatbot.llm.ollama_client import OllamaClient
        client = OllamaClient()
        client.generate("What is 2 + 2?")
    """

    def __init__(self, host: str = OLLAMA_HOST, model: str = OLLAMA_MODEL):
        self._client = ollama.Client(host=host)
        self._model = model

    def generate(self, prompt: str) -> str:
        """
        Generate a text response for the given prompt using the local model.

        Args:
            prompt (str): the full prompt, including any grounding context
        Returns:
            str: the model's response text

        Example:
            from doc_search_chatbot.llm.ollama_client import OllamaClient
            OllamaClient().generate("Summarize: ...")
        """
        response = self._client.generate(model=self._model, prompt=prompt)
        return response["response"]
