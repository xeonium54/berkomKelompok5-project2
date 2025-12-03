FILE_ADMIN =  'configuration/admin_credential.txt'
FILE_CONFIG = 'configuration/config.txt'
FILE_PARKIR = 'database/parkir.csv'
FILE_HISTORY = 'database/history_transaksi.csv'
FIELD_HISTORY = ['plat', 'masuk', 'keluar', 'durasi_jam', 'tarif']
FIELD_PARKIR = ['plat_nomor', 'waktu_masuk']

TOTAL_SLOT = 50
TARIF_PER_JAM = 3000.0

kendaraan_parkir = {} 
total_pendapatan = 0.0
jumlah_transaksi = 0
