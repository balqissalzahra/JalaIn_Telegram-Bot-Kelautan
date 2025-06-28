import json
import requests
from telegram import Update
from telegram.ext import ContextTypes

# === Load data referensi wilayah maritim dari JSON ===
with open("data/perairan_bmkg.json", "r", encoding="utf-8") as f:
    perairan_list = json.load(f)

# === Fungsi pencari URL berdasarkan input pengguna ===
def cari_url_dari_kata(wilayah_input):
    wilayah_input = wilayah_input.lower()
    for item in perairan_list:
        nama = item.get("nama", "").lower()
        if wilayah_input in nama:
            return item.get("endpoint")
    return None

# === Handler untuk perintah /cuaca ===
async def cuaca_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Contoh: /cuaca Surabaya")
        return

    wilayah = " ".join(context.args)
    url = cari_url_dari_kata(wilayah)

    if not url:
        contoh = ["Surabaya", "Merauke", "Obi"]
        teks = (
            f"⚠️ Wilayah tidak ditemukan. Gunakan nama wilayah maritim seperti:\n"
            f"{', '.join([f'<u>{c}</u>' for c in contoh])}"
        )
        await update.message.reply_text(teks, parse_mode="HTML")
        return

    try:
        res = requests.get(url)
        data = res.json()
        info = data["data"][0]  # ambil data hari ini

        pesan = (
            f"📍 <b>{data['name']}</b>\n"
            f"🗓️ {info['time_desc']}\n"
            f"🌦️ Cuaca: {info['weather']}\n"
            f"🌊 Gelombang: {info['wave_desc']} ({info['wave_cat']})\n"
            f"💨 Angin: {info['wind_from']} ke {info['wind_to']}, "
            f"{info['wind_speed_min']}–{info['wind_speed_max']} knot\n"
            f"⚠️ Peringatan: {info['warning_desc']}\n\n"
            f"<i>Sumber: BMKG</i>"
        )
        await update.message.reply_text(pesan, parse_mode="HTML")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Gagal mengambil data BMKG: {e}")
