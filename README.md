# red-pen.ink
# Backend Setup

## Prerequisites

### uv
```bash
curl -Lsf https://astral.sh/uv/install.sh | sh
```

### Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Pull the default models:
```bash
ollama pull qwen3-embedding:0.6b
ollama pull gemma3:4b
```

---

## Install & Run
```bash
cd backend/python
uv sync
source .venv/bin/activate
uvicorn feedback.app:app --port 8080
```

> Windows: `.venv\Scripts\activate`