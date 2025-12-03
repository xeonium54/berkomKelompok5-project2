import os
import datetime
import csv
import modules.global_variables as G
from modules.database import update_file, load_config, load_history, load_parkir
from modules.utility import clear_screen, create_listofdict
from modules.payment import hitung_durasi, hitung_jam_efektif, bayar
from modules.admin import dashboard, riwayat_transaksi, atur_tarif

FILE_ADMIN =  G.FILE_ADMIN
FILE_CONFIG = G.FILE_CONFIG
FILE_PARKIR = G.FILE_PARKIR
FILE_HISTORY = G.FILE_HISTORY
FIELD_HISTORY = G.FIELD_HISTORY
FIELD_PARKIR = G.FIELD_PARKIR

TOTAL_SLOT = G.TOTAL_SLOT
TARIF_PER_JAM = G.TARIF_PER_JAM

kendaraan_parkir = {} 
total_pendapatan = 0.0
jumlah_transaksi = 0

admin_login_state = False

load_config(FILE_CONFIG)
load_parkir(FILE_PARKIR)
load_history(FILE_HISTORY)

#MAIN MENU
while True:
    clear_screen()
    print("\n--- MENU UTAMA ---")
    print(f"Slot Tersedia: {TOTAL_SLOT - len(kendaraan_parkir)}")
    print("--------------------")
    print("1. Cek Slot")
    print("2. Check-In")
    print("3. Check-Out")
    print("4. Login sebagai Admin")
    print("0. Keluar Aplikasi")
    
    pilihan = input("Pilih menu (0-4): ")
    
    if pilihan == '1': #cek slot
        clear_screen()
        terisi = len(kendaraan_parkir)
        kosong = TOTAL_SLOT - terisi

        print(" --- CEK KETERSEDIAAN ---")
        print("=" * 40)
        print(f"Total slot: {TOTAL_SLOT}")
        print(f"Slot tersedia: {kosong}")
        print(f"Slot terisi: {terisi}")
        print("-------------------------")
        input("\n[Enter] untuk kembali...")
        
    elif pilihan == '2': #check in
        clear_screen()
        print(" --- CHECK IN ---")
        print("=" * 40)

        if len(kendaraan_parkir) == TOTAL_SLOT:
            print("Maaf parkir penuh.")
            input("\n[Enter] untuk kembali...")
            continue
        
        plat_nomor = input("Masukan plat nomor: ").upper().strip()
        if plat_nomor == '':
            print("Plat nomor tidak boleh kosong")
            input("\n[Enter] untuk kembali...")
            continue
        
        if plat_nomor in kendaraan_parkir:
            print(f"[ERROR]\nKendaraan dengan plat nomor {plat_nomor} sudah ada")
            input("\n[Enter] untuk kembali...")
            continue
        waktu_masuk = datetime.datetime.now()

        kendaraan_parkir[plat_nomor] = waktu_masuk

        kendaraan_parkir_baru = create_listofdict(kendaraan_parkir, 'plat_nomor', 'waktu_masuk')

        update_file(FILE_PARKIR, FIELD_PARKIR, kendaraan_parkir_baru, 'w')

        print(f"Kendaraan dengan plat nomor {plat_nomor} tercatat pada {waktu_masuk.strftime("%Y-%m-%d %H:%M:%S")}")
        input("\n[Enter] untuk kembali...")

    elif pilihan == '3': #check out
        clear_screen()
        print(" --- CHECK OUT ---")
        print("=" * 40)

        plat_nomor = input("Masukan plat nomor: ").upper().strip()

        if plat_nomor not in kendaraan_parkir:
            print("Plat nomor tidak valid/tidak ada")
            input("\n[Enter] untuk kembali...")
            continue

        waktu_masuk = kendaraan_parkir[plat_nomor]
        waktu_keluar = datetime.datetime.now()

        durasi_parkir = hitung_durasi(waktu_masuk, waktu_keluar)
        jam_efektif = hitung_jam_efektif(durasi_parkir)

        tarif_akhir = jam_efektif * TARIF_PER_JAM

        bayar(plat_nomor, waktu_masuk, waktu_keluar, durasi_parkir, jam_efektif, TARIF_PER_JAM, tarif_akhir)

        del kendaraan_parkir[plat_nomor]

        kendaraan_parkir_baru = create_listofdict(kendaraan_parkir, 'plat_nomor', 'waktu_masuk')

        update_file(FILE_PARKIR, FIELD_PARKIR, kendaraan_parkir_baru, 'w')

        history_baru = [{
            'plat': plat_nomor,
            'masuk' : waktu_masuk.isoformat(),
            'keluar': waktu_keluar.isoformat(),
            'durasi_jam': jam_efektif,
            'tarif': tarif_akhir
        }]

        total_pendapatan += tarif_akhir
        jumlah_transaksi += 1

        update_file(FILE_HISTORY, FIELD_HISTORY, history_baru, 'a')

        print(f"Pembayaran {plat_nomor} sukses. Kendaraan keluar.")
        input("\n[Enter] untuk kembali...")
    
    elif pilihan == '4':
        pertama_kali = False
        if not admin_login_state:
            clear_screen()
            print("\n--- Login Admin ---")

            try:
                with open(FILE_ADMIN, 'r') as file:
                    creds = file.read()
                    stored_user, stored_pass = creds.split(':')
            except (FileNotFoundError, IndexError, ValueError):
                print(f"File kredensial '{FILE_ADMIN}' tidak ditemukan atau rusak.")
                input("\nTekan [Enter] untuk kembali...")
                admin_login_state = False

            username = input('Username: ')
            password = input('Password: ')

            if username == stored_user and password == stored_pass:
                admin_login_state = True
            else:
                print("Username atau password salah.")
                input("\nTekan [Enter] untuk kembali...")
                admin_login_state = False
        else:
            pertama_kali = True

        while True:
            clear_screen()
            if pertama_kali:
                print("Login berhasil")
                pertama_kali = False

            print("\n--- MENU ADMIN ---")
            print("1. Lihat Dashboard")
            print("2. Lihat Riwayat Transaksi")
            print("3. Atur Tarif Parkir")
            print("0. Logout (Kembali ke Menu Utama)")

            pilihan_admin = input("Pilih menu admin (0-3): ")
            if pilihan_admin == '1':
                dashboard(TOTAL_SLOT, kendaraan_parkir, jumlah_transaksi, total_pendapatan)
            elif pilihan_admin == '2':
                riwayat_transaksi(FILE_HISTORY)
            elif pilihan_admin == '3':
                print(f"\nTarif saat ini: Rp {TARIF_PER_JAM:,.2f} / jam")
                tarif_baru = float(input("Masukkan tarif baru per jam: "))
                atur_tarif(tarif_baru)
            elif pilihan_admin == '0':
                print("\nAnda telah logout")
                input("Tekan [Enter] untuk kembali ke menu utama...")
                break 
            else:
                print("\n[ERROR] Pilihan admin tidak valid.")
                input("\nTekan [Enter] untuk kembali...")
            continue
    
    elif pilihan == '0':
        clear_screen()
        print("\nMenutup aplikasi. Terima kasih.")
        break
    else:
        print("\n[ERROR]\nPilihan invalid. Silakan coba lagi.")
        input("\n[Enter] untuk kembali...")