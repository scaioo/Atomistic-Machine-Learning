'''
import bz2
import ijson
import glob
import os

input_folder = "../Alexandria_dataset/"
files = sorted(glob.glob(os.path.join(input_folder, "alexandria_*.json.bz2")))

for file_path in files:
    file_name = os.path.basename(file_path)
    file_index = file_name.split("_")[1].split(".")[0]
    output_file = f"alex_{file_index}_compositions.txt"

    written = 0
    skipped = 0

    print(f"\n📦 Processing file: {file_name}")

    try:
        with bz2.open(file_path, "rt") as f, open(output_file, "w") as out_f:
            entries = ijson.items(f, "entries.item")
            for entry in entries:
                composition = entry.get("composition")
                if not composition:
                    skipped += 1
                    continue
                comp_str = ", ".join(f"{el}:{amt}" for el, amt in composition.items())
                out_f.write(f"{comp_str}\n")
                written += 1
        print(f"✅ Finished {file_name}: {written} compositions written, {skipped} skipped.")
        print(f"💾 Saved to: {output_file}")
    except Exception as e:
        print(f"❌ Failed to process {file_name}: {e}")
'''

import os
import bz2
import json
import re
from pymatgen.core import Composition

INPUT_DIR = "../Datasets/Alexandria_dataset/"
OUTPUT_DIR = "results/compositions"
CHUNK_SIZE = 100000

FILES_TO_PROCESS = [
    "alexandria_000.json.bz2",
    "alexandria_001.json.bz2",
    "alexandria_002.json.bz2",
    "alexandria_003.json.bz2",
    "alexandria_004.json.bz2",
    "alexandria_005.json.bz2",
    "alexandria_006.json.bz2",
    "alexandria_007.json.bz2",
    "alexandria_008.json.bz2",
    "alexandria_009.json.bz2",
    "alexandria_010.json.bz2",
    "alexandria_011.json.bz2",
    "alexandria_012.json.bz2",
    "alexandria_013.json.bz2",
    "alexandria_014.json.bz2",
    "alexandria_015.json.bz2",
    "alexandria_016.json.bz2",
    "alexandria_017.json.bz2",
    "alexandria_018.json.bz2",
    "alexandria_019.json.bz2",
    "alexandria_020.json.bz2",
    "alexandria_021.json.bz2",
    "alexandria_022.json.bz2",
    "alexandria_023.json.bz2",
    "alexandria_024.json.bz2",
    "alexandria_025.json.bz2",
    "alexandria_026.json.bz2",
    "alexandria_027.json.bz2",
    "alexandria_028.json.bz2",
    "alexandria_029.json.bz2",
    "alexandria_030.json.bz2",
    "alexandria_031.json.bz2",
    "alexandria_032.json.bz2",
    "alexandria_033.json.bz2",
    "alexandria_034.json.bz2",
    "alexandria_035.json.bz2",
    "alexandria_036.json.bz2",
    "alexandria_037.json.bz2",
    "alexandria_038.json.bz2",
    "alexandria_039.json.bz2",
    "alexandria_040.json.bz2",
    "alexandria_041.json.bz2",
    "alexandria_042.json.bz2",
    "alexandria_043.json.bz2",
    "alexandria_044.json.bz2",
    "alexandria_045.json.bz2",
    "alexandria_046.json.bz2",
    "alexandria_047.json.bz2",
    "alexandria_048.json.bz2",
    "alexandria_049.json.bz2",
    "alexandria_050.json.bz2",
]

def safe_json_loads(data_str):
    data_str = re.sub(r'\bNaN\b', '"NaN"', data_str)
    return json.loads(data_str)
'''
def process_entries(entries, start_idx=0):
    out = []
    for i, entry in enumerate(entries):
        comp_dict = entry.get("composition", {})
        comp = Composition(comp_dict)
        #reduced_formula = comp.reduced_formula
        #print(f"Entry {start_idx + i} - composition: {comp_dict}")
        #print(f"   → Reduced formula: {reduced_formula}")
        formatted_str = ", ".join(f"{el}:{amt}" for el, amt in comp_dict.items())
        out.append(formatted_str)
    return out'''

def process_entries(entries, start_idx=0):
    out = []
    for i, entry in enumerate(entries):
        comp_dict = entry.get("composition", {})
        data = entry.get("data", {})
        mat_id = data.get("mat_id", "unknown")

        comp = Composition(comp_dict)
        formatted_str = ", ".join(f"{el}:{amt}" for el, amt in comp_dict.items())

        out.append(f"{mat_id} {formatted_str}")
    return out


def process_file(filepath):
    filename = os.path.basename(filepath)
    output_file = os.path.join(OUTPUT_DIR, filename.replace(".json.bz2", "_compositions.txt"))

    print(f"Processing file: {filename}")
    try:
        with bz2.open(filepath, "rt") as f:
            raw = f.read()
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        try:
            data = safe_json_loads(raw)
        except Exception as e:
            print(f"Failed to parse JSON in {filename} after fallback: {e}")
            return

    entries = data.get("entries", [])
    print(f"Total entries found: {len(entries)}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(output_file, "w") as outf:
        for start in range(0, len(entries), CHUNK_SIZE):
            chunk = entries[start:start+CHUNK_SIZE]
            formulas = process_entries(chunk, start_idx=start)
            for f in formulas:
                outf.write(f + "\n")

    print(f"Done with {filename}: wrote {len(entries)} formulas to {output_file}\n")

def main():
    for filename in FILES_TO_PROCESS:
        fullpath = os.path.join(INPUT_DIR, filename)
        if not os.path.exists(fullpath):
            print(f"File not found: {filename}, skipping.")
            continue
        process_file(fullpath)

if __name__ == "__main__":
    main()
