import datetime
import csv
import os
import modules.global_variables as G
from modules.utility import clear_screen

def dashboard(total_slot, kendaraan_parkir, jumlah_transaksi, total_pendapatan):
    clear_screen()
    terisi = len(kendaraan_parkir)
    kosong = total_slot - terisi
    print("\n--- Ketersediaan Slot ---")
    print(f"Total Kapasitas: {total_slot}")
    print(f"Slot Terisi    : {terisi}")
    print(f"Slot Tersedia  : {kosong}")
    print("-------------------------")

    print("\n--- Keuangan ---")
    print(f"Total Pendapatan: Rp {total_pendapatan:,.2f}")
    print(f"Total Transaksi : {jumlah_transaksi} kendaraan")
    print("-------------------------")
    input("\nTekan [Enter] untuk kembali...")

def riwayat_transaksi(file_history):
    print("\n--- Riwayat Transaksi ---")
    with open(file_history, 'r', newline='') as file:
        reader = csv.DictReader(file)
        rows = list(reader) 
        if not rows:
            print("Belum ada transaksi.")
        else:
            for x in rows:
                waktu_keluar = datetime.datetime.fromisoformat(x['keluar'])
                tarif = float(x['tarif'])
                print(f"Plat: {x['plat']} | Keluar: {waktu_keluar.strftime('%Y-%m-%d')} -- {waktu_keluar.strftime('%H:%M')} | Biaya: Rp {tarif:,.2f}")
    
    print("-------------------------")
    input("\n[Enter] untuk kembali...")

def update_tarif(tarif_baru, file_config=None):
    # Update the tarif value in the config file and in the global variables module
    if file_config is None:
        file_config = G.FILE_CONFIG

    G.TARIF_PER_JAM = tarif_baru

    newline = []
    # If file doesn't exist, create it with current values
    if not os.path.exists(file_config):
        with open(file_config, 'w') as file:
            file.writelines([f"TOTAL_SLOT={G.TOTAL_SLOT}\n", f"TARIF_PER_JAM={tarif_baru}\n"])
        return

    with open(file_config, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith("TARIF_PER_JAM="):
            newline.append(f"TARIF_PER_JAM={tarif_baru}\n")
        else:
            newline.append(line)

    with open(file_config, 'w') as file:
        file.writelines(newline)

def atur_tarif(tarif_baru, file_config=None):
    try:
        if tarif_baru < 0:
            print("Tarif tidak boleh negatif.")
        else:
            update_tarif(tarif_baru, file_config)
            print(f"Tarif berhasil diubah menjadi Rp {tarif_baru:,.2f} / jam")
    except ValueError:
        print("[ERROR] Input tidak valid. Masukkan angka.")
    input("\n[Enter] untuk kembali...")