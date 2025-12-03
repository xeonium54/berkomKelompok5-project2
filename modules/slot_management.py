COLUMNS = ['A', 'B', 'C', 'D', 'E']
ROWS = list(range(1, 11))

def sisa_slot(total_slot, kendaraan_parkir):
    terisi = len(kendaraan_parkir)
    return total_slot - terisi

def generate_slot_id(column, row):
    """Generate slot ID from column (A-E) and row (1-10). E.g., 'A1', 'E10'."""
    return f"{column}{row}"

def parse_slot_id(slot_id):
    """Parse slot ID into column and row. E.g., 'A1' -> ('A', 1)."""
    if not slot_id or len(slot_id) < 2:
        return None, None
    column = slot_id[0].upper()
    try:
        row = int(slot_id[1:])
        if column in COLUMNS and row in ROWS:
            return column, row
    except ValueError:
        pass
    return None, None

def display_slot_matrix(occupied_slots):
    if isinstance(occupied_slots, dict):
        occupied_set = set(occupied_slots.keys())
    else:
        occupied_set = set(occupied_slots)
    
    lines = []
    lines.append("\n--- Parking Slot Matrix ---")
    lines.append("     " + "  ".join(COLUMNS))
    lines.append("   " + "-" * 16)
    
    for row in ROWS:
        row_display = f"{row:2d} | "
        for col in COLUMNS:
            slot_id = generate_slot_id(col, row)
            if slot_id in occupied_set:
                row_display += "[X] "  
            else:
                row_display += "[ ] " 
        lines.append(row_display)
    
    lines.append("   " + "-" * 16)
    lines.append("[X] = Occupied  [ ] = Available")
    return "\n".join(lines)

def select_slot():
    while True:
        user_input = input("\nPilih slot (Contoh: A1, B5): ").strip().upper()
        column, row = parse_slot_id(user_input)
        if column and row:
            slot_id = generate_slot_id(column, row)
            return slot_id
        else:
            print("[ERROR] Format tidak valid. Gunakan format A1-E10 (kolom A-E, baris 1-10).")