import os
import csv
import datetime
import modules.global_variables as G

def update_file(path,field,content,type):
    is_exist = os.path.exists(path)
    with open(path, type, newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field)
        if not is_exist:
            writer.writeheader()
        writer.writerows(content)

def load_config(file_config):
    # Read config file and update module-level globals in modules.global_variables (G)
    if os.path.exists(file_config):
        slot_notexist = True
        tarif_notexist = True
        with open(file_config, 'r') as f:
            for line in f:
                if not line.strip() or line.startswith('#'):
                    continue
                key, value = line.strip().split('=')

                if key == 'TOTAL_SLOT':
                    G.TOTAL_SLOT = int(value)
                    slot_notexist = False
                elif key == 'TARIF_PER_JAM' or key == 'TARIF_DEFAULT':
                    G.TARIF_PER_JAM = float(value)
                    tarif_notexist = False
        if slot_notexist or tarif_notexist:
            with open(file_config, 'w') as f:
                f.writelines([f"TOTAL_SLOT={G.TOTAL_SLOT}\n", f"TARIF_PER_JAM={G.TARIF_PER_JAM}\n"])

#load FILE_PARKIR
def load_parkir(file_parkir):
    # Populate G.kendaraan_parkir from CSV
    if not os.path.exists(file_parkir):
        return
    with open(file_parkir, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get('plat_nomor') or not row.get('waktu_masuk'):
                continue
            try:
                G.kendaraan_parkir[row['plat_nomor']] = datetime.datetime.fromisoformat(row['waktu_masuk'])
            except Exception:
                continue

#Load FILE_HISTORY
def load_history(file_history):
    # Load history and aggregate total_pendapatan and jumlah_transaksi in G
    if not os.path.exists(file_history):
        return
    with open(file_history, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                G.total_pendapatan += float(row.get('tarif', 0))
                G.jumlah_transaksi += 1
            except Exception:
                continue