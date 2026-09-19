# RAG-Based AI Chatbot — Agentic AI eBook

A Retrieval-Augmented Generation (RAG) chatbot built in Python using **LangGraph**, **ChromaDB**, and **Groq**. It answers questions strictly based on the content of the *Agentic AI eBook* (Konverge AI) — no outside knowledge, no hallucination.

Built as part of the AI Engineering Intern interview task for Appening Infotech.

---

## Tech Stack

- **LangGraph** — orchestrates the retrieve → generate pipeline
- **ChromaDB** — vector database
- **HuggingFace `all-MiniLM-L6-v2`** — local embedding model (free, runs on CPU)
- **Groq (`openai/gpt-oss-20b`)** — LLM for answer generation
- **FastAPI** — serves the chatbot as a REST API
- **pypdf** — PDF text extraction

No UI — API only, as per task requirements.

## Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/GauravRawat05/RAG-Chatbot_Appening
cd RAG-Chatbot_Appening
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Groq API key
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_key_here
```
Get a free key at [console.groq.com](https://console.groq.com).

### 5. Start the API server
```bash
uvicorn main:app --reload
```
Server runs at `http://127.0.0.1:8000`

### 6. Test it
Open `http://127.0.0.1:8000/docs` for the interactive Swagger UI.
**Response shape:**
```json
{
  "answer": "...",
  "context_chunks": ["...", "...", "..."],
  "confidence": 0.62
}
```

---

## Notes

- The chatbot only answers from the ebook's content. If a question falls outside the document's scope, it responds: *"I don't know based on the provided document."*
- `confidence` is a heuristic score (`1 - average retrieval distance`, clamped to 0–1) — It reflects how closely the retrieved chunks matched the question, not factual correctness.