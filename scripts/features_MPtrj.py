'''
import ijson

input_file = "../MPtrj_2022.9_full.json"
output_file = "MPtrj_elements.txt"

def extract_elements_from_structure(structure):
    elements = set()
    for site in structure.get("sites", []):
        for species in site.get("species", []):
            elements.add(species.get("element"))
    return elements

with open(input_file, "r") as f, open(output_file, "w") as out_f:
    parser = ijson.kvitems(f, "")

    for top_id, top_data in parser:
        # top_data might be a dict of multiple sub-entries
        if isinstance(top_data, dict):
            # Check if it looks like a dict of entries
            if all(isinstance(v, dict) for v in top_data.values()):
                # Iterate sub-entries
                for sub_id, sub_entry in top_data.items():
                    try:
                        structure = sub_entry["structure"]
                        elements = extract_elements_from_structure(structure)
                        elements_str = " ".join(sorted(elements))
                        out_f.write(f"{sub_id}: {elements_str}\n")
                    except KeyError:
                        print(f"❌ Skipping {sub_id} due to missing 'structure' or 'sites'")
            else:
                # top_data is a single entry (rare case)
                try:
                    structure = top_data["structure"]
                    elements = extract_elements_from_structure(structure)
                    elements_str = " ".join(sorted(elements))
                    out_f.write(f"{top_id}: {elements_str}\n")
                except KeyError:
                    print(f"❌ Skipping {top_id} due to missing 'structure' or 'sites'")
        else:
            print(f"❌ Unexpected format for {top_id}")
'''

import ijson
from collections import defaultdict

input_file = "../MPtrj_2022.9_full.json"
output_file = "MPtrj_elements.txt"

def extract_elements_from_structure(structure):
    element_counts = defaultdict(float)  # accumulate float occu
    for site in structure.get("sites", []):
        for species in site.get("species", []):
            element = species.get("element")
            occu = species.get("occu", 1.0)  # default to 1 if missing
            element_counts[element] += occu
    return element_counts

with open(input_file, "r") as f, open(output_file, "w") as out_f:
    parser = ijson.kvitems(f, "")

    for top_id, top_data in parser:
        if isinstance(top_data, dict):
            if all(isinstance(v, dict) for v in top_data.values()):
                for sub_id, sub_entry in top_data.items():
                    try:
                        structure = sub_entry["structure"]
                        element_counts = extract_elements_from_structure(structure)
                        # Format as "Cs:2.0, Cr:1.0, Cu:1.0, F:6.0"
                        elements_str = ", ".join(f"{el}:{count:.1f}" for el, count in sorted(element_counts.items()))
                        out_f.write(f"{sub_id}\t{elements_str}\n")
                    except KeyError:
                        print(f"❌ Skipping {sub_id} due to missing 'structure' or 'sites'")
            else:
                try:
                    structure = top_data["structure"]
                    element_counts = extract_elements_from_structure(structure)
                    elements_str = ", ".join(f"{el}:{count:.1f}" for el, count in sorted(element_counts.items()))
                    out_f.write(f"{top_id}\t{elements_str}\n")
                except KeyError:
                    print(f"❌ Skipping {top_id} due to missing 'structure' or 'sites'")
        else:
            print(f"❌ Unexpected format for {top_id}")
