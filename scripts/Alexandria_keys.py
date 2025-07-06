import bz2
import ijson
import json
from decimal import Decimal

def convert_decimal(obj):
    if isinstance(obj, list):
        return [convert_decimal(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj

input_file = "../Datasets//Alexandria_dataset/alexandria_000.json.bz2"

with bz2.open(input_file, "rt") as f:
    parser = ijson.items(f, "entries.item")
    first_entry = next(parser)  # get the first entry
    print("Keys in the first entry:", list(first_entry.keys()))
    print("Sample data from the first entry:")
    first_entry = convert_decimal(first_entry)  # 🔧 convert Decimals to float
    print(json.dumps(first_entry, indent=2))  # now it works!
