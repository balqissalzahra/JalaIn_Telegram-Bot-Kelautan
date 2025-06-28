# 🌊 JalaIn — Telegram Bot Informasi Kelautan & Perikanan Indonesia

JalaIn adalah sebuah **bot Telegram berbasis AI dan data resmi pemerintah** yang dirancang untuk membantu masyarakat, nelayan, akademisi, dan pengambil kebijakan dalam mengakses informasi sektor kelautan dan perikanan secara cepat, mudah, dan humanis.

---

## 🎯 Tujuan Pembuatan

Bot ini dibuat sebagai bagian dari **Tugas Akhir Bootcamp Sanbercode Batch 5** dengan tujuan:

- Meningkatkan literasi data dan akses informasi publik di sektor kelautan dan perikanan.
- Mengintegrasikan berbagai jenis data (statistik, cuaca maritim, dan regulasi) dalam satu pintu.
- Menyediakan layanan berbasis AI (Retrieval-Augmented Generation) untuk menjawab pertanyaan seputar ikan dan regulasi perikanan.

---

## ⚙️ Fitur Utama

1. **📍 /cuaca <lokasi>**
   - Menampilkan prakiraan cuaca maritim dari BMKG secara real-time.
   - Contoh: `/cuaca Gresik`

2. **📊 /produksi <tahun> [provinsi]**
   - Menampilkan statistik produksi perikanan nasional maupun provinsi.
   - Contoh: `/produksi 2023 Aceh`

3. **🧠 /tanya <pertanyaan>**
   - Menjawab pertanyaan tentang jenis ikan & regulasi perikanan menggunakan LLM (Gemini) + ChromaDB.
   - Contoh: `/tanya ciri ikan bandeng` atau `/tanya Kepmen KKP No. 50/KEPMEN-KP/2017`

---

## 🛠️ Cara Kerja Sistem

### 1. Teknologi Digunakan
- **Python**: Bahasa pemrograman utama
- **Telegram Bot API**: Interaksi pengguna
- **LangChain + Google Gemini 1.5 Flash**: Untuk QA berbasis LLM
- **ChromaDB**: Penyimpanan vektor data statis (ikan & regulasi)
- **SQLite**: Database statistik perikanan
- **BMKG Public API**: Cuaca maritim real-time

### 2. Struktur Data
- `data/data_ikan.db`: Statistik perikanan
- `maritim_chroma/`: Vektor data cuaca
- `data penting/`: Berisi JSON & FAISS index (tidak diunggah ke GitHub)

---

## 🚀 Instalasi & Menjalankan Bot

### 1. Clone Repository
```bash
git clone https://github.com/balqissalzahra/JalaIn_Telegram-Bot-Kelautan.git
cd JalaIn_Telegram-Bot-Kelautan
