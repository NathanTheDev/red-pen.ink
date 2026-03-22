import faiss
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


def generate(prompt: str, model: str = DEFAULT_PROMPT_MODEL, **kwargs) -> str | None:
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


def build_index(tags: list[str]) -> tuple[faiss.Index, list[str]]:
    embs = embed(tags)
    dim = embs.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embs)  # type: ignore
    return index, tags


def search(
    query: str, index: faiss.Index, tags: list[str], k: int = 5
) -> list[tuple[float, str]]:
    q_vec = embed([query])
    scores, indices = index.search(q_vec, k)  # type: ignore
    return [
        (float(scores[0][i]), tags[indices[0][i]])
        for i in range(k)
        if indices[0][i] != -1
    ]
