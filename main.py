from fastapi import FastAPI
from pydantic import BaseModel
from rag_pipeline import rag_app

app = FastAPI()

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")

def chat(request: ChatRequest):
    result = rag_app.invoke({"question": request.question})

    return {
        "answer": result["answer"],
        "context_chunks": result["context_chunks"],
        "confidence": result["confidence"]  # placeholder — we'll add real scoring in Step 6
    }