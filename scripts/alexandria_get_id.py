from matsciml.lightning.data_utils import MatSciMLDataModule

filepath = "../Alexandria/alexandria_3D_scan"
datamodule = MatSciMLDataModule(
    dataset="AlexandriaDataset",  # Correct registered name
    train_path=filepath,
    batch_size=32,
)

# Initialize the dataset
datamodule.setup()
dataset = datamodule.train_dataloader().dataset  # or datamodule.train_dataset if accessible

# Extract all entry_ids
entry_ids = [sample["entry_id"] for sample in dataset]

# Write them to a file
with open("alexandria_ID.txt", "w") as f:
    for eid in entry_ids:
        f.write(f"{eid}\n")

print(f"Saved {len(entry_ids)} entry IDs to alexandria_ID.txt")
