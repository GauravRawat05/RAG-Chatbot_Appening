import os
from dotenv import load_dotenv
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq

load_dotenv()

# Reconnect to the same Chroma DB we built in ingest.py
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)

#Set up the LLM
llm = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"))

# Define the shared state that flows through the graph
class RAGState(TypedDict):
    question: str
    context_chunks: List[str]
    scores: List[float]
    confidence: str
    answer: str

# Retrieve
def retrieve(state: RAGState) -> RAGState:
    results = vectorstore.similarity_search_with_score(state["question"], k=3)
    state["context_chunks"] = [doc.page_content for doc, score in results]
    state["scores"] = [score for doc, score in results]
    return state

# Generate
def generate(state: RAGState) -> RAGState:
    context = "\n\n".join(state["context_chunks"])
    prompt = f"""Answer the question using ONLY the context below.If the answer is not in the context, say "I don't know based on the provided document."
    Context: {context}
    Question: {state["question"]}
    Answer:"""
    response = llm.invoke(prompt)
    state["answer"] = response.content
    avg_distance = sum(state["scores"]) / len(state["scores"])
    state["confidence"] = round(max(0, 1 - avg_distance), 2)
    return state

graph = StateGraph(RAGState)
graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate)
graph.set_entry_point("retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)

rag_app = graph.compile()