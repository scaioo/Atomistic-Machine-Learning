import ijson
filepath = "../MPtrj_2022.9_full.json"
keys = set()

with open(filepath, "r") as f:
    parser = ijson.kvitems(f, '')  # '' means root-level
    for key, _ in parser:
        keys.add(key)
        if len(keys) >= 100:  # Safety stop (optional)
            break

print(keys)
