from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

reader = PdfReader("Ebook-Agentic-AI.pdf")

raw_text = ""
for page in reader.pages:
    raw_text += page.extract_text() + "\n"

print(f"Loaded {len(reader.pages)} pages, {len(raw_text)} characters")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)
chunks = splitter.split_text(raw_text)

print(f"Split into {len(chunks)} chunks")
print(chunks[0])

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

#Creating and storing chunks in Chroma
vectorstore = Chroma.from_texts(
    texts=chunks,
    embedding=embedding_model,
    persist_directory="chroma_db"
)

print("Chunks stored in Chroma successfully")