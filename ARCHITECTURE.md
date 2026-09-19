# Architecture

## Overview

```
┌─────────────────────────────────────────────────────────┐
│  OFFLINE (run once): ingest.py                          │
│                                                         │
│  PDF → extract text → chunk → embed → store in ChromaDB │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  ONLINE: main.py → rag_pipeline.py        │
│                                                         │
│  Question → [LangGraph: retrieve → generate] → Answer   │
└─────────────────────────────────────────────────────────┘
```

---

## 1. Ingestion (`ingest.py`)

Task: Makes a 60-page PDF becomes ~117 chunks, each stored as a vector in a local ChromaDB collection.

---

## 2. Query Pipeline (`rag_pipeline.py`)

Built as a **LangGraph** with two nodes and a linear edge:

```
retrieve → generate → END
```

### Node: `retrieve`
- Embeds the incoming question with the same model used during ingestion (critical — mismatched embedding models would break similarity search).
- Calls `vectorstore.similarity_search_with_score(question, k=3)` — returns the 3 closest chunks plus a distance score per chunk (lower distance = closer semantic match).

### Node: `generate`
- Joins the 3 retrieved chunks into one context block.
- Sends a strict prompt to the LLM (Groq, `openai/gpt-oss-20b`):
  > "Answer using ONLY the context below. If the answer is not in the context, say 'I don't know based on the provided document.'"
- This instruction is what enforces groundedness — the model is explicitly told not to fall back on its own training knowledge.
- Converts the average retrieval distance into a 0–1 confidence score: `confidence = max(0, 1 - avg_distance)`.

---

## 3. API Layer (`main.py`)

- FastAPI exposes a single `POST /chat` endpoint.
- On each call, `rag_app.invoke({"question": ...})` runs the full retrieve→generate graph and returns:
  ```json
  {
    "answer": "...",
    "context_chunks": ["...", "...", "..."],
    "confidence": 0.62
  }
  ```

---
