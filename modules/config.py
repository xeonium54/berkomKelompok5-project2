import os

FILE_ADMIN =  'admin_credential.txt'
FILE_PARKIR = 'parkir.csv'
FILE_HISTORY = 'history_transaksi.csv'
FIELD_HISTORY = ['plat', 'masuk', 'keluar', 'durasi_jam', 'tarif']
FIELD_PARKIR = ['plat_nomor', 'waktu_masuk']

TOTAL_SLOT = 0
TARIF_PER_JAM = 0.0

def load_from_txt():

    global TOTAL_SLOT, TARIF_PER_JAM
    
    # Cek file config.txt di folder root
    if os.path.exists('../configuration/config.txt'):
        with open('../configuration/config.txt', 'r') as f:
            for line in f:
                # Lewati baris kosong atau komentar
                if not line.strip() or line.startswith('#'):
                    continue
                
                # Pisahkan Key dan Value
                key, value = line.strip().split('=')
                
                # Update variable sesuai Key
                if key == 'TOTAL_SLOT':
                    TOTAL_SLOT = int(value)      # Konversi ke Integer
                elif key == 'TARIF_PER_JAM':
                    TARIF_PER_JAM = float(value) # Konversi ke Float


load_from_txt()