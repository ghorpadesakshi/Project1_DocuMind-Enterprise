from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

PDF_PATH = "data/company_policy.pdf"   # make sure path is correct
VECTOR_DB_PATH = "vectorstore"

def ingest_pdf():
    print("📄 Loading PDF...")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    print("✂️ Splitting text...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)

    print("🧠 Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("💾 Saving vector store...")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(VECTOR_DB_PATH)

    print("✅ Ingestion complete!")

    docs = vectorstore.similarity_search("test", k=3)
    for i, doc in enumerate(docs):
        print(f"\n--- Chunk {i+1} ---")
        print(doc.page_content[:300])

if __name__ == "__main__":
    ingest_pdf()