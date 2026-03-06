from fastapi import FastAPI, UploadFile, File
from app.api.ingestion import ingest_document
from app.api.retrieval import ask_question

app = FastAPI()

@app.get("/")
def home():
    return {"message": "DocuMind API Running"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    result = await ingest_document(file)
    return {"message": result}

@app.get("/ask")
def ask(query: str):
    answer = ask_question(query)
    return {"answer": answer}