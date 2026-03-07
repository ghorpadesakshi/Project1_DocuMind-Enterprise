from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.api.ingestion import ingest_document
from app.api.retrieval import ask_question

app = FastAPI()

# Serve frontend folder
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


# Open frontend page
@app.get("/")
def home():
    return FileResponse("frontend/index.html")


# Upload PDF and ingest
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    result = await ingest_document(file)
    return {"message": result}


# Ask question
@app.post("/ask")
async def ask(question: str = Form(...)):
    answer = ask_question(question)
    return {"answer": answer}