from telegram.ext import ApplicationBuilder, CommandHandler
from handler.cuaca_bmkg import cuaca_handler
from handler.retrieval import retrieval_handler
from handler.data_ikan import produksi_handler
import os
from dotenv import load_dotenv

# ===========================
# 🔐 Load Token
# ===========================
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ===========================
# 🚀 Inisialisasi Bot
# ===========================
app = ApplicationBuilder().token(TOKEN).build()

# ===========================
# 📢 Perintah /start
# ===========================
async def start(update, context):
    pesan = (
        "🌊 *Selamat datang di Bot Kelautan & Perikanan Indonesia!* 🇮🇩🐟\n\n"
        "Bot ini dikembangkan untuk memudahkan akses informasi penting di sektor kelautan dan perikanan secara cepat, akurat, dan humanis langsung lewat Telegram.\n\n"
        "🧠 Didukung oleh teknologi AI dan data resmi pemerintah, bot ini dapat:\n"
        "• Menyajikan prakiraan *cuaca maritim* dari BMKG\n"
        "• Memberikan *data statistik perikanan* terbaru (berbasis SQLite)\n"
        "• Menjawab pertanyaan tentang *ikan* dan *regulasi perikanan* (dengan LLM)\n\n"
        "📌 *Contoh perintah:*\n"
        "`/cuaca Gresik` — info cuaca laut\n"
        "`/tanya ciri ikan bandeng?` — tanya jenis ikan\n"
        "`/tanya Kepmen KKP No. 50/KEPMEN-KP/2017` — tanya regulasi\n"
        "`/produksi 2023 Aceh` — statistik provinsi\n\n"
        "📎 *Sumber Data*: BMKG, KKP, Fishbase, JDIH KKP\n"
        "_Bot ini dibangun oleh Balqis Alzahra sebagai bagian dari Tugas Akhir Bootcamp Sanbercode Batch 5._"
    )
    await update.message.reply_text(pesan, parse_mode="Markdown")

# ===========================
# ✅ Daftar Perintah Bot
# ===========================
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("cuaca", cuaca_handler))
app.add_handler(CommandHandler("tanya", retrieval_handler))
app.add_handler(CommandHandler("produksi", produksi_handler))

# ===========================
# ▶️ Jalankan Bot
# ===========================
if __name__ == "__main__":
    print("✅ Bot Telegram aktif...")
    app.run_polling()
