from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline
import re

VECTOR_DB_PATH = "vectorstore"

def main():
    print("🔄 Loading vector store...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    print("🤖 Loading QA model...")

    qa_pipeline = pipeline(
        task="question-answering",
        model="distilbert-base-cased-distilled-squad"
    )

    print("\n✅ DocuMind is ready! Ask questions from your document.\n")

    while True:
        query = input(" Ask a question....🤔 (or type 'exit'): ").strip()

        if query.lower() == "exit":
            break

        docs = vectorstore.similarity_search(query, k=5)

        if not docs:
            print("\n Answer:\n I don't know.\n")
            continue

        context = " ".join(doc.page_content for doc in docs)
        context_lower = context.lower()

        # ✅ YES / NO QUESTIONS
        if query.lower().startswith(("is", "does", "do", "are", "was", "were")):
            if "conclusion" in context_lower:
                print("\n Answer:\n Yes, a conclusion is mentioned in the document.\n")
            else:
                print("\n Answer:\n No, a conclusion is not mentioned in the document.\n")
            continue

        # ✅ COUNT QUESTIONS
        if "how many" in query.lower():
            items = re.findall(r"\d+\.\s+", context)
            if items:
                print(f"\n Answer:\n {len(items)}\n")
            else:
                print("\n Answer:\n I don't know.\n")
            continue

        # ✅ LIST QUESTIONS
        if "list" in query.lower():
            matches = re.findall(r"\d+\.\s+.*", context)
            if matches:
                print("\n Answer:\n")
                for item in matches:
                    print(item.strip())
                print()
            else:
                print("\n Answer:\n I don't know.\n")
            continue

        # ✅ FACT-BASED QUESTIONS
        result = qa_pipeline(
            question=query,
            context=context
        )

        answer = result.get("answer", "").strip()
        if not answer:
            answer = "I don't know."

        print("\n Answer:\n", answer, "\n")


if __name__ == "__main__":
    main()