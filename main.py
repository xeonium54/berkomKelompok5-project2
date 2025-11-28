import os
import datetime
import csv

FILE_ADMIN =  'admin_credential.txt'
FILE_PARKIR = 'parkir.csv'
FILE_HISTORY = 'history_transaksi.csv'
FIELD_HISTORY = ['plat', 'masuk', 'keluar', 'durasi_jam', 'tarif']
FIELD_PARKIR = ['plat_nomor', 'waktu_masuk']

TOTAL_SLOT = 50
TARIF_PER_JAM = 3000.0

kendaraan_parkir = {} 
total_pendapatan = 0.0
jumlah_transaksi = 0

admin_login_state = False

try:
    with open(FILE_PARKIR, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            kendaraan_parkir[row['plat_nomor']] = datetime.datetime.fromisoformat(row['waktu_masuk'])
except FileNotFoundError:
    pass 
except Exception as e:
    print(f"Gagal memuat {FILE_PARKIR}: {e}")

try:
    with open(FILE_HISTORY, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_pendapatan += float(row['tarif'])
            jumlah_transaksi += 1
except FileNotFoundError:
    pass
except Exception as e:
    print(f"[ERROR] Gagal memuat {FILE_HISTORY}: {e}")

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
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
        os.system('cls' if os.name == 'nt' else 'clear')
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
        os.system('cls' if os.name == 'nt' else 'clear')
        print(" --- CHECK IN ---")
        print("=" * 40)

        if len(kendaraan_parkir) == TOTAL_SLOT:
            print("Maaf parkir penuh.")
            input("\n[Enter] untuk kembali...")
            continue
        
        plat_nomor = input("Masukan plat nomor: ").upper()
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

        try:
            with open(FILE_PARKIR, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=FIELD_PARKIR)
                writer.writeheader()
                for plat, waktu in kendaraan_parkir.items():
                    writer.writerow({
                        'plat_nomor': plat, 
                        'waktu_masuk': waktu.isoformat()
                    })
        except IOError as e:
            print(f"[ERROR] Gagal menyimpan ke {FILE_PARKIR}: {e}")

        print(f"Kendaraan dengan plat nomor {plat_nomor} tercatat pada {waktu_masuk.strftime("%Y-%m-%d %H:%M:%S")}")
        input("\n[Enter] untuk kembali...")
    
    elif pilihan == '3': #check out
        os.system('cls' if os.name == 'nt' else 'clear')
        print(" --- CHECK OUT ---")
        print("=" * 40)

        plat_nomor = input("Masukan plat nomor: ").upper()

        if plat_nomor not in kendaraan_parkir:
            print("Plat nomor tidak valid/tidak ada")
            input("\n[Enter] untuk kembali...")
            continue

        waktu_masuk = kendaraan_parkir[plat_nomor]
        waktu_keluar = datetime.datetime.now()

        durasi_parkir = waktu_keluar - waktu_masuk
        durasi_detik = durasi_parkir.total_seconds()
        durasi_jam = durasi_detik / 3600
        jam_efektif = int((durasi_detik/3600) + ((durasi_detik % 3600) != 0))
        #note: perlu edge case kalau ternyata jam_efektif == 0

        tarif = jam_efektif * TARIF_PER_JAM

        print(f"\n--- Pembayaran {plat_nomor} ---")
        print(f"Waktu Masuk  : {waktu_masuk.strftime('%Y-%m-%d %H:%M')}")
        print(f"Waktu Keluar : {waktu_keluar.strftime('%Y-%m-%d %H:%M')}")
        print(f"Durasi Parkir: {durasi_parkir.total_seconds() / 60:.2f} menit")
        print(f"Dihitung     : {jam_efektif} jam")
        print(f"Tarif/Jam    : Rp {TARIF_PER_JAM:,.2f}")
        print(f"TOTAL BIAYA  : Rp {tarif:,.2f}")
        print("-" * 30)

        input("[Enter] untuk melakukan pembayaran...")

        del kendaraan_parkir[plat_nomor]

        try:
            with open(FILE_PARKIR, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=FIELD_PARKIR)
                writer.writeheader()
                for plat, waktu in kendaraan_parkir.items():
                    writer.writerow({
                        'plat_nomor': plat, 
                        'waktu_masuk': waktu.isoformat()
                    })
        except IOError as e:
            print(f"[ERROR] Gagal menyimpan ke {FILE_PARKIR}: {e}")

        history_baru = {
            'plat': plat_nomor,
            'masuk' : waktu_masuk.isoformat(),
            'keluar': waktu_keluar.isoformat(),
            'durasi_jam': jam_efektif,
            'tarif': tarif
        }

        total_pendapatan += tarif
        jumlah_transaksi += 1

        file_exists = os.path.exists(FILE_HISTORY)
        try:
            with open(FILE_HISTORY, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=FIELD_HISTORY)
                if not file_exists:
                    writer.writeheader() # Tulis header jika file baru
                writer.writerow(history_baru)
        except IOError as e:
            print(f"[ERROR] Gagal menyimpan ke {FILE_HISTORY}: {e}")


        print(f"Pembayaran {plat_nomor} sukses. Kendaraan keluar.")
        input("\n[Enter] untuk kembali...")
        
    elif pilihan == '4':
        pertama_kali = False
        if not admin_login_state:
            os.system('cls' if os.name == 'nt' else 'clear')
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
            os.system('cls' if os.name == 'nt' else 'clear')

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
                os.system('cls' if os.name == 'nt' else 'clear')
                terisi = len(kendaraan_parkir)
                kosong = TOTAL_SLOT - terisi
                print("\n--- Ketersediaan Slot ---")
                print(f"Total Kapasitas: {TOTAL_SLOT}")
                print(f"Slot Terisi    : {terisi}")
                print(f"Slot Tersedia  : {kosong}")
                print("-------------------------")

                print("\n--- Keuangan ---")
                print(f"Total Pendapatan: Rp {total_pendapatan:,.2f}")
                print(f"Total Transaksi : {jumlah_transaksi} kendaraan")
                print("-------------------------")
                input("\nTekan [Enter] untuk kembali...")
            elif pilihan_admin == '2':
                print("\n--- Riwayat Transaksi ---")
                try:
                    with open(FILE_HISTORY, 'r', newline='') as file:
                        reader = csv.DictReader(file)
                        rows = list(reader) 
                        if not rows:
                            print("Belum ada transaksi.")
                        else:
                            for x in rows:
                                waktu_keluar = datetime.datetime.fromisoformat(x['keluar'])
                                tarif = float(x['tarif'])
                                print(f"Plat: {x['plat']} | Keluar: {waktu_keluar.strftime('%H:%M')} | Biaya: Rp {tarif:,.2f}")
                                
                except FileNotFoundError:
                    print("Belum ada transaksi (file tidak ditemukan).")
                
                print("-------------------------")
                input("\n[Enter] untuk kembali...")
            elif pilihan_admin == '3':
                print(f"\nTarif saat ini: Rp {TARIF_PER_JAM:,.2f} / jam")
                try:
                    tarif_baru = float(input("Masukkan tarif baru per jam: "))
                    if tarif_baru < 0:
                        print("Tarif tidak boleh negatif.")
                    else:
                        TARIF_PER_JAM = tarif_baru
                        print(f"Tarif berhasil diubah menjadi Rp {TARIF_PER_JAM:,.2f} / jam")
                except ValueError:
                    print("[ERROR] Input tidak valid. Masukkan angka.")
                
                input("\n[Enter] untuk kembali...")

            elif pilihan_admin == '0':
                print("\nAnda telah logout")
                input("Tekan [Enter] untuk kembali ke menu utama...")
                break 
            else:
                print("\n[ERROR] Pilihan admin tidak valid.")
                input("\nTekan [Enter] untuk kembali...")
            continue
    elif pilihan == '0':
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\nMenutup aplikasi. Terima kasih.")
        break
    else:
        print("\n[ERROR]\nPilihan invalid. Silakan coba lagi.")
        input("\nTekan [Enter] untuk kembali...")