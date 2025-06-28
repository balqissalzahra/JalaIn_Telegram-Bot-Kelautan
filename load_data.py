# load_data.py

import json
from pathlib import Path
from chroma_setup import get_collection

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# === Load data ikan ===
ikan_path = Path("data/knowledge_ikan_asli.json")
if ikan_path.exists():
    print("🐟 Memuat data ikan...")
    raw = load_json(ikan_path)
    docs, metas = [], []
    for item in raw:
        teks = (
            f"Jenis Data: Ikan\n"
            f"Nama: {item.get('Nama Indonesia')}\n"
            f"Ilmiah: {item.get('Nama Ilmiah')}\n"
            f"Habitat: {item.get('Habitat Perairan')}\n"
            f"Karakteristik: {item.get('Karakteristik')}\n"
            f"Manfaat: {item.get('Manfaat')}"
        )
        docs.append(teks)
        metas.append(item)

    ids = [f"ikan-{i}" for i in range(len(docs))]
    print(f"📌 Jumlah dokumen ikan valid: {len(docs)}")
    get_collection("ikan").add_texts(docs, metadatas=metas, ids=ids)
    print("✅ Data ikan dimuat ke Chroma.")
else:
    print("⚠️ File ikan tidak ditemukan.")

# === Load data regulasi ===
reg_path = Path("data/knowledge_regulasi_asli.json")
if reg_path.exists():
    print("\n📘 Memuat data regulasi...")
    raw = load_json(reg_path)
    docs, metas = [], []
    for item in raw:
        teks = (
            f"Jenis Data: Regulasi\n"
            f"{item.get('jenis')} No {item.get('nomor')} Tahun {item.get('tahun')}\n"
            f"Tentang: {item.get('tentang')}\n"
            f"Status: {item.get('status')}\n"
            f"Link: {item.get('url')}"
        )
        docs.append(teks)
        metas.append(item)

    ids = [f"regulasi-{i}" for i in range(len(docs))]
    print(f"📌 Jumlah dokumen regulasi valid: {len(docs)}")
    get_collection("regulasi").add_texts(docs, metadatas=metas, ids=ids)
    print("✅ Data regulasi dimuat ke Chroma.")
else:
    print("⚠️ File regulasi tidak ditemukan.")
