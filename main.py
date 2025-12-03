import datetime
import modules.global_variables as G
from modules.database import update_file, load_config, load_history, load_parkir
from modules.utility import clear_screen, create_listofdict
from modules.payment import hitung_durasi, hitung_jam_efektif, bayar
from modules.slot_management import display_slot_matrix, select_slot, generate_slot_id
from modules.admin import dashboard, riwayat_transaksi, atur_tarif

FILE_ADMIN =  G.FILE_ADMIN
FILE_CONFIG = G.FILE_CONFIG
FILE_PARKIR = G.FILE_PARKIR
FILE_HISTORY = G.FILE_HISTORY
FIELD_HISTORY = G.FIELD_HISTORY
FIELD_PARKIR = G.FIELD_PARKIR

TOTAL_SLOT = G.TOTAL_SLOT
TARIF_PER_JAM = G.TARIF_PER_JAM

admin_login_state = False

load_config(FILE_CONFIG)
load_parkir(FILE_PARKIR)
load_history(FILE_HISTORY)

#MAIN MENU
while True:
    clear_screen()
    print("\n--- MENU UTAMA ---")
    print(f"Slot Tersedia: {TOTAL_SLOT - len(G.kendaraan_parkir)}")
    print("--------------------")
    print("1. Cek Slot")
    print("2. Check-In")
    print("3. Check-Out")
    print("4. Login sebagai Admin")
    print("0. Keluar Aplikasi")
    
    pilihan = input("Pilih menu (0-4): ")
    
    if pilihan == '1': #cek slot
        clear_screen()
        terisi = len(G.kendaraan_parkir)
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

        if len(G.kendaraan_parkir) == TOTAL_SLOT:
            print("Maaf parkir penuh.")
            input("\n[Enter] untuk kembali...")
            continue
        
        plat_nomor = input("Masukan plat nomor: ").upper().strip()
        if plat_nomor == '':
            print("Plat nomor tidak boleh kosong")
            input("\n[Enter] untuk kembali...")
            continue
        
        if plat_nomor in G.kendaraan_parkir:
            print(f"[ERROR]\nKendaraan dengan plat nomor {plat_nomor} sudah ada")
            input("\n[Enter] untuk kembali...")
            continue
        
        # Display slot matrix and let user select a slot
        print(display_slot_matrix(G.slot_assignment))
        
        while True:
            slot_id = select_slot()
            if slot_id in G.slot_assignment:
                print(f"[ERROR] Slot {slot_id} sudah terisi.")
            else:
                break
        
        waktu_masuk = datetime.datetime.now()

        G.kendaraan_parkir[plat_nomor] = waktu_masuk
        G.slot_assignment[slot_id] = plat_nomor

        # Build parkir.csv records with slot_id from slot_assignment mapping
        parkir_records = []
        for plat in G.kendaraan_parkir.keys():
            slot_for_plat = ''
            for sid, p in G.slot_assignment.items():
                if p == plat:
                    slot_for_plat = sid
                    break
            parkir_records.append({
                'plat_nomor': plat,
                'slot_id': slot_for_plat,
                'waktu_masuk': G.kendaraan_parkir[plat].isoformat()
            })

        update_file(FILE_PARKIR, FIELD_PARKIR, parkir_records, 'w')

        print(f"Kendaraan dengan plat nomor {plat_nomor} tercatat pada slot {slot_id} ({waktu_masuk.strftime("%Y-%m-%d %H:%M:%S")})")
        input("\n[Enter] untuk kembali...")

    elif pilihan == '3': #check out
        clear_screen()
        print(" --- CHECK OUT ---")
        print("=" * 40)

        plat_nomor = input("Masukan plat nomor: ").upper().strip()

        if plat_nomor not in G.kendaraan_parkir:
            print("Plat nomor tidak valid/tidak ada")
            input("\n[Enter] untuk kembali...")
            continue

        waktu_masuk = G.kendaraan_parkir[plat_nomor]
        waktu_keluar = datetime.datetime.now()

        durasi_parkir = hitung_durasi(waktu_masuk, waktu_keluar)
        jam_efektif = hitung_jam_efektif(durasi_parkir)

        tarif_akhir = jam_efektif * TARIF_PER_JAM

        bayar(plat_nomor, waktu_masuk, waktu_keluar, durasi_parkir, jam_efektif, TARIF_PER_JAM, tarif_akhir)

        # Find and free the slot
        slot_id_to_free = None
        for slot_id, plate in G.slot_assignment.items():
            if plate == plat_nomor:
                slot_id_to_free = slot_id
                break
        
        del G.kendaraan_parkir[plat_nomor]
        if slot_id_to_free:
            del G.slot_assignment[slot_id_to_free]

        # Rebuild parkir.csv with remaining vehicles and their slot assignments
        parkir_records = []
        for plat in G.kendaraan_parkir.keys():
            slot_for_plat = ''
            for sid, p in G.slot_assignment.items():
                if p == plat:
                    slot_for_plat = sid
                    break
            parkir_records.append({
                'plat_nomor': plat,
                'slot_id': slot_for_plat,
                'waktu_masuk': G.kendaraan_parkir[plat].isoformat()
            })

        update_file(FILE_PARKIR, FIELD_PARKIR, parkir_records, 'w')

        history_baru = [{
            'plat': plat_nomor,
            'masuk' : waktu_masuk.isoformat(),
            'keluar': waktu_keluar.isoformat(),
            'durasi_jam': jam_efektif,
            'tarif': tarif_akhir
        }]

        G.total_pendapatan += tarif_akhir
        G.jumlah_transaksi += 1

        update_file(FILE_HISTORY, FIELD_HISTORY, history_baru, 'a')

        print(f"Pembayaran {plat_nomor} sukses. Kendaraan keluar dari slot {slot_id_to_free}.")
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
                dashboard(TOTAL_SLOT, G.kendaraan_parkir, G.jumlah_transaksi, G.total_pendapatan)
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