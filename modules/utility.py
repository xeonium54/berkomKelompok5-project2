import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_listofdict(dict, key_a, key_b):
    listofobject = []
    for a, b in dict.items():
        listofobject.append({
            key_a: a, 
            key_b: b.isoformat()
        })
    return listofobject