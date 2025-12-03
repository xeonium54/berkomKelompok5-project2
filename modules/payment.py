def hitung_durasi(waktu_masuk, waktu_keluar):
    durasi_parkir = waktu_keluar - waktu_masuk
    return durasi_parkir

def hitung_jam_efektif(durasi_parkir):
        durasi_detik = durasi_parkir.total_seconds()
        jam_efektif = int((durasi_detik/3600) + ((durasi_detik % 3600) != 0))
        if jam_efektif == 0: jam_efektif=1

        return jam_efektif

def bayar(plat_nomor, waktu_masuk, waktu_keluar, durasi_parkir, jam_efektif, tarif_per_jam, tarif):
    print(f"\n--- Pembayaran {plat_nomor} ---")
    print(f"Waktu Masuk  : {waktu_masuk.strftime('%Y-%m-%d %H:%M')}")
    print(f"Waktu Keluar : {waktu_keluar.strftime('%Y-%m-%d %H:%M')}")
    print(f"Durasi Parkir: {durasi_parkir.total_seconds() / 60:.2f} menit")
    print(f"Dihitung     : {jam_efektif} jam")
    print(f"Tarif/Jam    : Rp {tarif_per_jam:,.2f}")
    print(f"TOTAL BIAYA  : Rp {tarif:,.2f}")
    print("-" * 30)

    input("[Enter] untuk melakukan pembayaran...")