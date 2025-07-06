from collections import defaultdict

# Paths to your files
alex_file = "results/compositions/alexandria_compositions.txt"
mptrj_file = "MPtrj_elements.txt"
output_file = "results/common_compositions.txt"

# Function to read file and build a dict: composition_str → list of material IDs
def load_compositions(filepath):
    comp_to_ids = defaultdict(list)
    with open(filepath, "r") as f:
        for line in f:
            parts = line.strip().split(maxsplit=1)
            if len(parts) != 2:
                continue
            mat_id, composition = parts
            # Normalize composition (remove spaces around commas for consistency)
            composition = ", ".join(part.strip() for part in composition.split(","))
            comp_to_ids[composition].append(mat_id)
    return comp_to_ids

# Load both files
alex_comps = load_compositions(alex_file)
mptrj_comps = load_compositions(mptrj_file)

# Find compositions present in both files
common_comps = set(alex_comps.keys()) & set(mptrj_comps.keys())
print(f"Found {len(common_comps)} common compositions.")

# Write to output file
with open(output_file, "w") as out:
    for comp in sorted(common_comps):
        alex_ids = ", ".join(alex_comps[comp])
        mptrj_ids = ", ".join(mptrj_comps[comp])
        out.write(f"Composition: {comp}\t")
        out.write(f"  Alexandria IDs: {alex_ids}\t")
        out.write(f"  MPtrj IDs: {mptrj_ids}\n")

print(f"\n✅ Common compositions and their IDs written to {output_file}")
