import os
import csv
import datetime
import modules.global_variables as G

def update_file(path,field,content,type):
    is_exist = os.path.exists(path)
    with open(path, type, newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field)
        if type == 'w' or not is_exist:
            writer.writeheader()
        writer.writerows(content)

def load_config(file_config):
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
    if not os.path.exists(file_parkir):
        return
    with open(file_parkir, 'r', newline='') as f:
        reader = csv.DictReader(f)
        expected_fields = {'plat_nomor', 'waktu_masuk'}
        if not reader.fieldnames or not expected_fields.issubset(set(reader.fieldnames)):
            f.seek(0)
            raw = list(csv.reader(f))
            repaired = []
            for row in raw:
                if len(row) == 2:
                    plat, waktu = row[0].strip(), row[1].strip()
                    slot_id = ''
                elif len(row) >= 3:
                    plat, slot_id, waktu = row[0].strip(), row[1].strip(), row[2].strip()
                else:
                    continue
                repaired.append({'plat_nomor': plat, 'slot_id': slot_id, 'waktu_masuk': waktu})

            if repaired:
                update_file(file_parkir, G.FIELD_PARKIR, repaired, 'w')

            for row in repaired:
                try:
                    plat = row['plat_nomor']
                    waktu = datetime.datetime.fromisoformat(row['waktu_masuk'])
                    G.kendaraan_parkir[plat] = waktu
                    if row.get('slot_id'):
                        if row['slot_id']:
                            G.slot_assignment[row['slot_id']] = plat
                except Exception:
                    continue
            return

        f.seek(0)
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get('plat_nomor') or not row.get('waktu_masuk'):
                continue
            try:
                plat = row['plat_nomor']
                waktu = datetime.datetime.fromisoformat(row['waktu_masuk'])
                G.kendaraan_parkir[plat] = waktu
                if row.get('slot_id'):
                    if row['slot_id']:
                        G.slot_assignment[row['slot_id']] = plat
            except Exception:
                continue

#Load FILE_HISTORY
def load_history(file_history):
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