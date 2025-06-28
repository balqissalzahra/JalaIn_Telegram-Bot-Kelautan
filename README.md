# 🌊 JalaIn — Telegram Bot Informasi Kelautan & Perikanan Indonesia

**JalaIn** adalah bot Telegram berbasis AI dan data resmi pemerintah yang dirancang untuk memudahkan akses informasi sektor kelautan dan perikanan di Indonesia. Bot ini menyajikan data statistik, cuaca maritim, serta informasi tentang jenis ikan dan regulasi perikanan secara cepat, akurat, dan humanis.

---

## 🎓 Tugas Akhir Bootcamp Sanbercode

Proyek ini merupakan **Tugas Akhir Bootcamp Sanbercode Batch 5**, dikembangkan oleh **Balqis Alzahra** untuk mendemonstrasikan integrasi teknologi AI, data terbuka pemerintah, dan antarmuka percakapan melalui Telegram Bot.

---

## 🎯 Tujuan Pembuatan

- Meningkatkan literasi data dan keterbukaan informasi publik sektor kelautan dan perikanan.
- Menyediakan satu pintu akses data: statistik, cuaca, dan regulasi.
- Mengintegrasikan AI (Retrieval-Augmented Generation) untuk menjawab pertanyaan publik.

---

## ⚙️ Fitur Utama

| Perintah Telegram | Fungsi |
|-------------------|--------|
| `/start`          | Informasi pengantar bot |
| `/cuaca <lokasi>` | Menampilkan cuaca laut dari BMKG |
| `/produksi <tahun> [provinsi]` | Menampilkan statistik produksi ikan |
| `/tanya <pertanyaan>` | Menjawab pertanyaan seputar ikan dan regulasi (dengan LLM) |

Contoh:
```bash
/cuaca Gresik
/produksi 2023 Aceh
/tanya ciri ikan bandeng
/tanya Kepmen KKP No. 50/KEPMEN-KP/2017
```

---

## 🛠️ Teknologi yang Digunakan

- **Python** (core logic dan backend)
- **Telegram Bot API** (interaksi pengguna)
- **Google Gemini 1.5 Flash + LangChain** (untuk LLM retrieval)
- **ChromaDB** (penyimpanan vektor RAG)
- **SQLite** (database statistik perikanan)
- **BMKG Public API** (cuaca maritim)

---

## 🧱 Struktur Proyek

```
telegram_bot_kelautan/
│
├── bot/
│   └── main_bot.py
│
├── handler/
│   ├── cuaca_bmkg.py
│   ├── data_ikan.py
│   └── retrieval.py
│
├── data/              ← folder ini tidak disertakan di GitHub
│   └── data_ikan.db   ← disediakan via Google Drive
│
├── maritim_chroma/    ← hasil embedding ChromaDB (juga via Drive)
│
├── requirements.txt
├── README.md
└── .env.example
```

---

## 💾 Data Besar & Embedding

Karena keterbatasan GitHub (maks. 100 MB per file), data besar tidak disertakan dalam repo. Silakan unduh manual:

### 🔗 Link Google Drive:
- **Statistik & JSON** (`data penting` + `data_ikan.db`):  
  👉 https://drive.google.com/drive/folders/1EdxZ8O0fFjg3hdO9RtADBn37eZF6wA5W?usp=drive_link  
- **Vektor Embedding ChromaDB (`maritim_chroma`)**:  
  👉 https://drive.google.com/drive/folders/1zEmil5n2pLihNfwLTDf_jPQ6_4mDcKmj?usp=sharing

Setelah diunduh, letakkan ke dalam folder `data/` dan `maritim_chroma/`.

---

## 🚀 Cara Menjalankan Proyek

1. **Clone Repository**
```bash
git clone https://github.com/balqissalzahra/JalaIn_Telegram-Bot-Kelautan.git
cd JalaIn_Telegram-Bot-Kelautan
```

2. **Buat & Aktifkan Virtual Environment**
```bash
python -m venv rag_env
rag_env\Scripts\activate   # Windows
# atau
source rag_env/bin/activate  # Linux/macOS
```

3. **Install Requirements**
```bash
pip install -r requirements.txt
```

4. **Atur Token Telegram**
Buat file `.env` atau gunakan `.env.example`:
```
TELEGRAM_BOT_TOKEN=YOUR_TOKEN_HERE
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

5. **Jalankan Bot**
```bash
python bot/main_bot.py
```

---

## ✅ Status

✅ Cuaca Maritim – BMKG API  
✅ Statistik Produksi – SQLite  
✅ QA Jenis Ikan dan Regulasi – LLM + Chroma  
✅ Bot Telegram Aktif (via command)

---

## 🙏 Kontributor

**Balqis Alzahra**  
Tugas Akhir Bootcamp Sanbercode 2025  
[GitHub](https://github.com/balqissalzahra)
