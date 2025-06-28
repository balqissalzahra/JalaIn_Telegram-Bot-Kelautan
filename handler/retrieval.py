import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from telegram import Update
from telegram.ext import ContextTypes

# ================================
# 🔑 API Key
# ================================
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# ================================
# 🔤 Embedding
# ================================
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# ================================
# 🧠 Load Chroma VectorDB
# ================================
vectordb = Chroma(
    persist_directory="./maritim_chroma",
    embedding_function=embedding,
    collection_name="maritim",
)

# ================================
# 🔮 LLM
# ================================
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.3,
)

# ================================
# 🐟 Prompt: Ikan
# ================================
prompt_ikan = PromptTemplate.from_template("""
Jawablah pertanyaan tentang IKAN secara faktual dan ringkas.
Tulis maksimal 3 kalimat saja.

Fokuskan pada:
- Nama ilmiah
- Karakteristik
- Habitat
- Penyebaran
- Manfaat (jika ada)

Gunakan bahasa yang singkat dan mudah dipahami.

Context:
{context}

Pertanyaan: {question}
""")

# ================================
# 📜 Prompt: Regulasi
# ================================
prompt_regulasi = PromptTemplate.from_template("""
Jawablah pertanyaan tentang REGULASI PERIKANAN secara faktual dan jelas.
Tulis maksimal 4–5 baris dengan struktur berikut:

Nama Regulasi: ...
Tahun: ...
Jenis Regulasi: ...
Pokok Bahasan: ...
Status: ...
Tautan Resmi: ...

Jika tidak ada jawaban yang relevan, jawab:
"Informasi tidak tersedia dalam basis data kami."

Context:
{context}

Pertanyaan: {question}
""")

# ================================
# 🔍 Deteksi Query
# ================================
def pilih_prompt(query: str):
    keywords_ikan = [
        "ikan", "lele", "bandeng", "kakap", "kerapu", "udang", "cumi", "tuna", 
        "rumput laut", "karakteristik", "habitat", "nama ilmiah", "sebaran", 
        "manfaat", "morfologi", "jenis ikan", "ikan air tawar", "ikan laut"
    ]

    keywords_regulasi = [
        "regulasi", "peraturan", "aturan", "uu", "undang-undang", 
        "permen", "kepmen", "nomor", "tahun", "izin", "zonasi", 
        "perikanan tangkap", "budidaya", "konservasi", "perda", "sanksi", 
        "pengawasan", "dokumen hukum"
    ]

    query_lower = query.lower()
    if any(keyword in query_lower for keyword in keywords_regulasi):
        return prompt_regulasi
    if any(keyword in query_lower for keyword in keywords_ikan):
        return prompt_ikan
    return prompt_ikan  # default fallback

# ================================
# 🤖 Handler Telegram: /tanya
# ================================
async def retrieval_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Ketik pertanyaan, contoh:\n/tanya ciri ikan kakap\n/tanya Kepmen KKP No. 50/2017")
        return

    query = " ".join(context.args)
    try:
        prompt = pilih_prompt(query)
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=vectordb.as_retriever(),
            chain_type="stuff",
            chain_type_kwargs={"prompt": prompt}
        )
        result = qa_chain.invoke({"query": query})
        response = result["result"]

        if prompt == prompt_regulasi:
            # Format output regulasi
            lines = response.strip().split("\n")
            detail = {}
            for line in lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    detail[key.strip().lower()] = value.strip()

            pesan = (
                f"📘 *Regulasi Perikanan*\n\n"
                f"*Nama*: {detail.get('nama regulasi', '-')}\n"
                f"*Tahun*: {detail.get('tahun', '-')}\n"
                f"*Jenis*: {detail.get('jenis regulasi', '-')}\n"
                f"*Tentang*: {detail.get('pokok bahasan', '-')}\n"
                f"*Status*: {detail.get('status', '-')}\n"
                f"*Tautan*: {detail.get('tautan resmi', '-')}"
            )
            await update.message.reply_text(pesan, parse_mode="Markdown")
        else:
            await update.message.reply_text(response)

    except Exception as e:
        await update.message.reply_text(f"❌ Terjadi error: {e}")
