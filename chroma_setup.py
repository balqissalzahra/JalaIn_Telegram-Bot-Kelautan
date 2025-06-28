# chroma_setup.py

import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load .env kalau belum
load_dotenv()

# Pastikan API Key tersedia
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("❌ GOOGLE_API_KEY belum disetel di .env")

# Gunakan langsung saat instansiasi
embedding = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=api_key  # 🔥 INI WAJIB
)

def get_collection(collection_name: str):
    return Chroma(
        collection_name=collection_name,
        persist_directory="./maritim_chroma",
        embedding_function=embedding,
    )
