# 🌊 JalaIn — AI-Powered Marine & Fisheries Information Bot

> **Democratizing access to Indonesia's marine sector data through conversational AI**

JalaIn is a Python-based Telegram bot that integrates Retrieval-Augmented Generation (RAG), real-time maritime weather data, and a structured fisheries database — enabling public users, researchers, and policymakers to query complex marine information through natural language.

---

## 📸 Demo
![JalaIn Demo](JalaIn%20Telegram%20Bot.gif)

---

## 🎯 Problem & Motivation

Indonesia's marine and fisheries data is scattered across multiple government platforms (KKP, BMKG, BPS) — often inaccessible to the general public, fishermen, and researchers without technical expertise. JalaIn consolidates these into a single conversational interface, lowering the barrier to data access.

---

## ⚙️ Features

| Command | Function |
|---|---|
| `/cuaca <lokasi>` | Real-time maritime weather from BMKG API |
| `/produksi <tahun> [provinsi]` | Fisheries production statistics by region & year |
| `/tanya <pertanyaan>` | AI-powered Q&A on fish species & fisheries regulations (LLM + RAG) |

**Example queries:**
```
/cuaca Gresik
/produksi 2023 Aceh
/tanya ciri ikan bandeng
/tanya Kepmen KKP No. 50/KEPMEN-KP/2017
```

---

## 🧠 Architecture

```
User (Telegram)
      │
      ▼
 Telegram Bot API
      │
      ├──► /cuaca    → BMKG Public API  → Real-time weather response
      │
      ├──► /produksi → SQLite DB        → Structured fisheries statistics
      │
      └──► /tanya    → LangChain + Gemini 1.5 Flash
                              │
                              └──► ChromaDB (vector store)
                                        │
                                        └──► KKP regulations + species data (embedded docs)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.x |
| Bot interface | Telegram Bot API |
| LLM | Google Gemini 1.5 Flash |
| RAG orchestration | LangChain |
| Vector database | ChromaDB |
| Structured data | SQLite |
| Weather data | BMKG Public API |

---

## 📁 Project Structure

```
JalaIn_Telegram-Bot-Kelautan/
│
├── bot/
│   └── main_bot.py          ← Entry point, command routing
│
├── handler/
│   ├── cuaca_bmkg.py        ← BMKG API integration
│   ├── data_ikan.py         ← SQLite query handler
│   └── retrieval.py         ← RAG retrieval logic
│
├── maritim_chroma/          ← ChromaDB vector embeddings (via Drive)
├── data/                    ← Fisheries DB + source documents (via Drive)
│
├── chroma_setup.py          ← Embedding pipeline setup
├── load_data.py             ← Data ingestion scripts
├── requirements.txt
└── .env.example
```

---

## 🚀 Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/balqissalzahra/JalaIn_Telegram-Bot-Kelautan.git
cd JalaIn_Telegram-Bot-Kelautan
```

**2. Set up environment**
```bash
python -m venv rag_env
source rag_env/bin/activate   # Linux/macOS
# or
rag_env\Scripts\activate      # Windows

pip install -r requirements.txt
```

**3. Configure API keys**
```bash
cp .env.example .env
# Fill in your TELEGRAM_BOT_TOKEN and GOOGLE_API_KEY
```

**4. Download data assets**

Large files (ChromaDB embeddings + SQLite DB) are hosted on Google Drive due to GitHub's file size limits:
- 📂 [Fisheries data & SQLite DB](https://drive.google.com/drive/folders/1EdxZ8O0fFjg3hdO9RtADBn37eZF6wA5W?usp=drive_link)
- 📂 [ChromaDB vector embeddings](https://drive.google.com/drive/folders/1zEmil5n2pLihNfwLTDf_jPQ6_4mDcKmj?usp=sharing)

Place downloaded folders into `data/` and `maritim_chroma/`.

**5. Run the bot**
```bash
python bot/main_bot.py
```

---

## 📊 Data Sources

| Source | Data Type |
|---|---|
| KKP (Ministry of Marine Affairs) | Fisheries production statistics, regulations |
| BMKG | Real-time maritime weather |
| Government regulations | Fisheries policy documents (embedded via RAG) |

---

## 🔮 Potential Extensions

- Web dashboard (Streamlit/Power BI) for fisheries trend visualization
- Multi-language support (Bahasa + English)
- Integration with BPS (Statistics Indonesia) for broader agromaritim data
- Deployment on cloud (Railway / Render) for persistent uptime

---

## 👩 Author

**Balqis Alzahra**
Research & Data Analyst | Marine Science Graduate | AI Enthusiast

Built as capstone project for Sanbercode AI Bootcamp (2025), combining domain expertise in marine policy with applied AI development.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/balqissalzahra/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/balqissalzahra)
