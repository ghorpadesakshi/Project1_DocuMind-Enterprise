# ingest.py
import os
from PyPDF2 import PdfReader

DATA_DIR = "data"
OUTPUT_FILE = "document.txt"

all_text = []

for file in os.listdir(DATA_DIR):
    if file.endswith(".pdf"):
        pdf_path = os.path.join(DATA_DIR, file)
        reader = PdfReader(pdf_path)

        for page in reader.pages:
            text = page.extract_text()
            if text:
                all_text.append(text)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(all_text))

print("✅ PDF ingestion complete. Text saved to document.txt")