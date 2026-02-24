# pinecone_client.py
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

def init_pinecone():
    api_key = os.getenv("PINECONE_API_KEY")
    region = os.getenv("PINECONE_ENV")
    index_name = os.getenv("PINECONE_INDEX")

    if not api_key or not region or not index_name:
        raise ValueError("Pinecone environment variables are missing")

    pc = Pinecone(api_key=api_key)

    existing_indexes = [idx.name for idx in pc.list_indexes()]

    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,               # ✅ REQUIRED
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region=region
            )
        )

    return pc, index_name