import os
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX")

# Initialize clients
client = OpenAI(api_key=OPENAI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)


def ask_question(query, top_k=5):
    """
    Ask a question about the uploaded document stored in Pinecone.
    Automatically answers page count questions if asked.
    """

    # 1️⃣ Embed the query
    query_embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding

    # 2️⃣ Query Pinecone
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    # 3️⃣ Handle "page count" questions
    if "page" in query.lower() and "how many" in query.lower():
        # Check metadata for total_pages
        for match in results.matches:
            total_pages = match.metadata.get("total_pages")
            if total_pages:
                return f"The document has {total_pages} pages."
        return "Sorry, I could not determine the number of pages."

    # 4️⃣ Otherwise, combine context for normal questions
    context = "\n".join([match.metadata["text"] for match in results.matches if "text" in match.metadata])

    prompt = f"""
You are a helpful AI assistant. Answer the following question using ONLY the context below.
Context:
{context}

Question:
{query}
Answer:
"""

    # 5️⃣ Ask GPT
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    return completion.choices[0].message.content.strip()