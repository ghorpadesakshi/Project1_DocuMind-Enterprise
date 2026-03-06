import os
from dotenv import load_dotenv
import google.generativeai as genai

# ===============================
# Load API key
# ===============================
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env")

genai.configure(api_key=API_KEY)

# ===============================
# Find a working Gemini model
# ===============================
model_name = None
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        model_name = m.name
        break

if not model_name:
    raise RuntimeError("❌ No Gemini model available for generateContent")

print(f"✅ Using Gemini model: {model_name}")

model = genai.GenerativeModel(model_name)

# ===============================
# Load document text
# ===============================
DOC_FILE = "document.txt"

if not os.path.exists(DOC_FILE):
    raise FileNotFoundError("❌ document.txt not found. Run ingest.py first.")

with open(DOC_FILE, "r", encoding="utf-8") as f:
    DOCUMENT_TEXT = f.read()

SYSTEM_PROMPT = f"""
You are a document-based assistant.

RULES:
- Answer ONLY using the document below
- If information is missing, say exactly: I don't know.
- Do NOT use outside knowledge
- Be clear and concise

DOCUMENT:
{DOCUMENT_TEXT}
"""

print("\n📘 DocuMind QA System (Gemini – AUTO MODEL)")
print("Type 'exit' to quit")

# ===============================
# Main loop
# ===============================
while True:
    question = input("\nAsk a question (or exit): ").strip()
    if question.lower() in ["exit", "quit"]:
        break

    try:
        response = model.generate_content(
            SYSTEM_PROMPT + "\n\nQuestion: " + question
        )
        print("\n✅ Answer:")
        print(response.text.strip())
    except Exception as e:
        print("❌ Error:", e)