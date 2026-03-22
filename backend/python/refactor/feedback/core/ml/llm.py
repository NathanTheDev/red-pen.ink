from functools import cached_property

import numpy as np
import ollama
from ollama import ChatResponse, chat

DEFAULT_EMBEDDING_MODEL = "qwen3-embedding:0.6b"
DEFAULT_PROMPT_MODEL = "gemma3:4b"
DEFAULT_PROMPT_OPTIONS = {
    "temperature": 0.3,
    "top_p": 0.85,
    "top_k": 20,
}


class LLM:
    def __init__(
        self,
        prompt_model: str = DEFAULT_PROMPT_MODEL,
        embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    ) -> None:
        self.prompt_model = prompt_model
        self.embedding_model = embedding_model
        self._pull(prompt_model)
        self._pull(embedding_model)

    def _pull(self, model: str) -> None:
        ollama.pull(model)

    def query(self, prompt: str, **kwargs) -> str | None:
        options = {**DEFAULT_PROMPT_OPTIONS, **kwargs}
        try:
            response: ChatResponse = chat(
                model=self.prompt_model,
                messages=[{"role": "user", "content": prompt}],
                options=options,
            )
            return response.message.content
        except Exception:
            return None

    def embed(self, texts: list[str]) -> np.ndarray:
        embs = []
        for text in texts:
            resp = ollama.embed(model=self.embedding_model, input=text, truncate=True)
            embs.append(resp.embeddings[0])
        return np.array(embs, dtype="float32")

    @cached_property
    def embedding_dimension(self) -> int:
        resp = ollama.embed(model=self.embedding_model, input=" ", truncate=True)
        return len(resp.embeddings[0])


llm = LLM()
