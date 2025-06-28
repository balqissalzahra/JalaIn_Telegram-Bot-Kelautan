import sqlite3
from telegram import Update
from telegram.ext import ContextTypes

DB_PATH = "data/data_ikan.db"

# Format angka gaya Indonesia
def format_angka(n):
    return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_nilai(n, satuan):
    angka = format_angka(n)
    if "juta" in satuan.lower():
        return f"Rp {angka} juta"
    elif "ribu" in satuan.lower():
        return f"Rp {angka} ribu"
    return f"Rp {angka}"

# Handler Telegram
async def produksi_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Gunakan format:\n/produksi <tahun> [provinsi]\n\n"
            "Contoh:\n/produksi 2023\n/produksi 2023 Aceh"
        )
        return

    tahun = context.args[0]
    provinsi = " ".join(context.args[1:]).upper() if len(context.args) > 1 else None

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        query = """
        SELECT Sheet, Kelompok, Volume, Nilai, Satuan_Volume, Satuan_Nilai, 
               `Kabupaten/Kota`, `Jenis Alat Tangkap` 
        FROM produksi_ikan 
        WHERE Tahun = ?
        """
        params = [tahun]
        if provinsi:
            query += " AND UPPER(Provinsi) = ?"
            params.append(provinsi)

        rows = cursor.execute(query, params).fetchall()
        conn.close()

        if not rows:
            await update.message.reply_text("⚠️ Data tidak ditemukan untuk input tersebut.")
            return

        sektor_data = {}
        kelompok_ikan = {}
        kabupaten = {}
        alat_tangkap = {}

        # Filter untuk Top Ikan dan Kabupaten
        valid_sektor_top = ["Tangkap Laut", "Tangkap Darat", "Budidaya Pembesaran"]

        for sheet, kelompok, volume, nilai, sat_vol, sat_nilai, kab, alat in rows:
            sektor = sheet.strip()
            sektor_data.setdefault(sektor, {
                "volume": 0.0, "nilai": 0.0,
                "satuan_vol": sat_vol, "satuan_nil": sat_nilai,
                "sub": {}
            })
            sektor_data[sektor]["volume"] += volume
            sektor_data[sektor]["nilai"] += nilai

            if sektor in ["Tangkap Laut", "Tangkap Darat"]:
                sektor_data.setdefault("Perikanan Tangkap", {
                    "volume": 0.0, "nilai": 0.0,
                    "satuan_vol": "ton", "satuan_nil": "ribu rupiah",
                    "sub": {}
                })
                sektor_data["Perikanan Tangkap"]["volume"] += volume
                sektor_data["Perikanan Tangkap"]["nilai"] += nilai
                sektor_data["Perikanan Tangkap"]["sub"].setdefault(sektor, {"volume": 0.0, "nilai": 0.0})
                sektor_data["Perikanan Tangkap"]["sub"][sektor]["volume"] += volume
                sektor_data["Perikanan Tangkap"]["sub"][sektor]["nilai"] += nilai

            # Hanya kelompok ikan dari sektor tertentu dan satuan ton
            if sektor in valid_sektor_top and sat_vol.lower() == "ton":
                kelompok_ikan[kelompok] = kelompok_ikan.get(kelompok, 0.0) + volume
                kabupaten[kab] = kabupaten.get(kab, 0.0) + volume

            # Alat tangkap tetap dihitung semuanya
            if alat:
                alat_tangkap[alat] = alat_tangkap.get(alat, 0.0) + volume

        # Format sektor produksi
        sektor_order = ["Perikanan Tangkap", "Budidaya Pembesaran", "Budidaya Pembenihan", "Budidaya Ikan Hias"]
        sektor_text = ""
        for s in sektor_order:
            if s not in sektor_data:
                continue
            val = sektor_data[s]
            sektor_text += f"• {s}: {format_angka(val['volume'])} {val['satuan_vol']} | {format_nilai(val['nilai'], val['satuan_nil'])}\n"
            if s == "Perikanan Tangkap":
                for sub in ["Tangkap Laut", "Tangkap Darat"]:
                    if sub in val.get("sub", {}):
                        v = val["sub"][sub]
                        sektor_text += f"  {sub}: {format_angka(v['volume'])} ton | {format_nilai(v['nilai'], 'ribu rupiah')}\n"

        # Format Top 3
        top_ikan = sorted(kelompok_ikan.items(), key=lambda x: x[1], reverse=True)[:3]
        top_kab = sorted(kabupaten.items(), key=lambda x: x[1], reverse=True)[:3]
        top_alat = sorted(alat_tangkap.items(), key=lambda x: x[1], reverse=True)[:3]

        rincian_ikan = "\n".join([f"• {k}: {format_angka(v)} ton" for k, v in top_ikan])
        rincian_kab = "\n".join([f"• {k}: {format_angka(v)} ton" for k, v in top_kab])
        rincian_alat = "\n".join([f"• {k}: {format_angka(v)} ton" for k, v in top_alat])

        filter_str = f"Tahun {tahun}"
        if provinsi:
            filter_str += f", Provinsi: *{provinsi.title()}*"

        pesan = (
            f"📊 *Data Produksi Perikanan*\n_{filter_str}_\n\n"
            f"🐟 *Total Volume & Nilai:*\n{sektor_text}\n"
            f"🔎 *Top 3 Volume Kelompok Ikan:*\n{rincian_ikan}\n\n"
            f"🔎 *Top 3 Volume Kota/Kabupaten Produsen Ikan:*\n{rincian_kab}\n\n"
            f"🔎 *Top 3 Volume Alat Penangkapan Ikan:*\n{rincian_alat}"
        )

        await update.message.reply_text(pesan, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Gagal membaca data: {e}")
