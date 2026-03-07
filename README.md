📄 DocuMind AI
DocuMind AI is an intelligent document question-answering system that allows users to upload PDF files and interact with them through a chat interface. The application processes the uploaded document, converts it into vector embeddings, stores them in a vector database, and retrieves relevant information to answer user queries using an AI model.
The system enables users to quickly extract insights from documents without manually reading the entire content.

🚀 Features:
📄 PDF Upload – Upload documents directly from the browser
🧠 AI-Powered Question Answering – Ask questions about the document
🔍 Semantic Search – Uses embeddings to retrieve relevant context
💬 Chat Interface – Interactive chat UI similar to ChatGPT
⚡ Fast Retrieval – Powered by vector search using Pinecone
🧹 Automatic Document Replacement – New uploads replace previous vectors
📊 Metadata Extraction – Stores page information for better context retrieval

🏗️ Tech Stack:
Frontend:
HTML
CSS
JavaScript

Backend:
Python
FastAPI

AI & NLP:
OpenAI API (Embeddings + LLM)

Vector Database:
Pinecone

PDF Processing:
PyPDF

⚙️ How It Works
1️⃣User uploads a PDF document through the frontend.
2️⃣The backend reads the document using PyPDF.
3️⃣The text is split into smaller chunks.
4️⃣Each chunk is converted into embeddings using OpenAI Embedding Model.
5️⃣The embeddings are stored in Pinecone Vector Database.

When the user asks a question:
The question is converted into an embedding.
Pinecone retrieves the most relevant text chunks.
The retrieved context is sent to the OpenAI model.
The AI generates a response based on the document content.

📂 Project Structure
DocuMind-AI
│
├── backend
│   ├── main.py
│   ├── ingestion.py
│   ├── retrieval.py
│
├── frontend
│   ├── index.html
│   ├── style.css
│   ├── script.js
│
├── .env
├── requirements.txt
└── README.md
🔑 Environment Variables

Create a .env file and add:

OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX=your_index_name

▶️ Running the Project
Install dependencies
pip install -r requirements.txt

Run the server
uvicorn main:app --reload

Open the application
http://127.0.0.1:8000/frontend/index.html

🎯 Future Improvements
Multi-document support
Chat history memory
Streaming responses
Source citations with page numbers
Drag and drop file upload

📌 Use Cases
Research document analysis
Study material summarization
Business report understanding
Legal document review
Technical documentation search
