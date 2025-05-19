#DATABASE GEJALA
gejala_list = {
    'G001': {'nama': 'Sirip Menguncup', 'bobot': 5},
    'G005': {'nama': 'Menabrak Dinding Aquarium', 'bobot': 3},
    'G006': {'nama': 'Bintik Emas/Berkarat', 'bobot': 5},
    'G007': {'nama': 'Pergerakan Insang Cepat', 'bobot': 1},
    'G009': {'nama': 'Sisik Tercopot', 'bobot': 3},
    'G015': {'nama': 'Bercak Putih seperti Kapas', 'bobot': 3},
    'G031': {'nama': 'Ikan Kurang Aktif', 'bobot': 3},
    'G004': {'nama': 'Bintik Putih pada Badan', 'bobot': 3}
}

#DATABASE PENYAKIT
database_penyakit = {
    'P003': {
        'nama': 'Velvet (Bintik Karat/Emas)',
        'gejala': {
            'G001': 5,
            'G005': 3,
            'G006': 5,
            'G007': 1,
            'G009': 3,
            'G015': 3
        }
    },
    'P002': {
        'nama': 'White Spot (Bintik Putih)',
        'gejala': {
            'G004': 3,
            'G005': 3,
            'G015': 3
        }
    }
}

#FUNGSI SIMILARITAS SORGENFREI
def hitung_sorgenfrei(gejala_lama, gejala_baru):
    a = sum(b for k, b in gejala_baru.items() if k in gejala_lama)
    b = sum(b for k, b in gejala_baru.items() if k not in gejala_lama)
    c = sum(b for k, b in gejala_lama.items() if k not in gejala_baru)
    if (a + b) * (a + c) == 0:
        return 0
    return (a ** 2) / ((a + b) * (a + c))

#FUNGSI K-NN BERBOBOT
def hitung_knn_berbobot(gejala_lama, gejala_baru, skor_sorgenfrei):
    total_bobot_sama = sum(
        bobot for kode, bobot in gejala_baru.items() if kode in gejala_lama
    )
    total_bobot_input = sum(gejala_baru.values())

    if total_bobot_input == 0:
        return 0

    return (skor_sorgenfrei * total_bobot_sama) / total_bobot_input

#PROGRAM UTAMA
def main():
    print("=== SISTEM DIAGNOSA PENYAKIT IKAN CUPANG ===")
    print("Pilih gejala yang dialami ikan (gunakan kode gejala):")
    
    for kode, info in gejala_list.items():
        print(f"{kode} - {info['nama']} (Bobot: {info['bobot']})")

    input_user = input("\nMasukkan kode gejala (pisahkan dengan koma, contoh: G001,G005,G006):\n> ")
    kode_terpilih = [k.strip().upper() for k in input_user.split(',') if k.strip().upper() in gejala_list]

    if not kode_terpilih:
        print("❌ Tidak ada gejala yang valid dimasukkan.")
        return

    gejala_baru = {kode: gejala_list[kode]['bobot'] for kode in kode_terpilih}

    print("\n🔍 Menghitung kemiripan dengan database penyakit...\n")
    hasil = []
    for kode_penyakit, data in database_penyakit.items():
        skor_sorgenfrei = hitung_sorgenfrei(data['gejala'], gejala_baru)
        skor_knn = hitung_knn_berbobot(data['gejala'], gejala_baru, skor_sorgenfrei)
        hasil.append((kode_penyakit, data['nama'], skor_sorgenfrei, skor_knn))

    hasil.sort(key=lambda x: x[3], reverse=True)

    print("=== HASIL DIAGNOSA ===")
    for kode, nama, s_sorgenfrei, s_knn in hasil:
        print(f"{kode} - {nama}")
        print(f"  Similarity (Sorgenfrei): {s_sorgenfrei:.4f}")
        print(f"  Skor Akhir (KNN):        {s_knn:.4f}\n")

    if hasil[0][3] < 0.6:
        print("⚠️  Kemiripan kurang dari 0.6 — perlu evaluasi pakar (revise).")
    else:
        print(f"✅ Diagnosa utama: {hasil[0][1]}")

if __name__ == "__main__":
    main()