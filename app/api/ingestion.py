import os
import tempfile
from dotenv import load_dotenv
from pypdf import PdfReader
from openai import OpenAI
from pinecone import Pinecone

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX")

# Initialize OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)


def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


async def ingest_document(file):

    # Save uploaded PDF
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    reader = PdfReader(tmp_path)

    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    chunks = chunk_text(text)

    # Create embeddings
    embeddings = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunks
    )

    vectors = []

    for i, emb in enumerate(embeddings.data):
        vectors.append({
            "id": str(i),
            "values": emb.embedding,
            "metadata": {"text": chunks[i]}
        })

    # Store in Pinecone
    index.upsert(vectors=vectors)

    return "Document successfully stored in Pinecone"