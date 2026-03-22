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


def query(prompt: str, model: str = DEFAULT_PROMPT_MODEL, **kwargs) -> str | None:
    options = {**DEFAULT_PROMPT_OPTIONS, **kwargs}
    try:
        response: ChatResponse = chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            options=options,
        )
        return response.message.content
    except Exception:
        return None


def embed(texts: list[str], model: str = DEFAULT_EMBEDDING_MODEL) -> np.ndarray:
    embs = []
    for text in texts:
        resp = ollama.embed(model=model, input=text, truncate=True)
        embs.append(resp.embeddings[0])
    return np.array(embs, dtype="float32")
