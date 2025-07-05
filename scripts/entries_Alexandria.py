import lmdb
import os

base_path = "../Alexandria/alexandria_3D-pbe/"  # Adjust here

# Find all folders ending with .lmdb
lmdb_folders = [f for f in os.listdir(base_path) if f.endswith('.lmdb')]

for folder_name in lmdb_folders:
    lmdb_path = os.path.join(base_path, folder_name)
    print(f"Opening LMDB database: {folder_name}")
    
    env = lmdb.open(lmdb_path, readonly=True, lock=False)
    
    with env.begin() as txn:
        cursor = txn.cursor()
        for i, (key, value) in enumerate(cursor):
            print(f"  Key {i}: {key}")
            if i >= 5:  # Just print first 5 keys for each DB
                break
    env.close()
