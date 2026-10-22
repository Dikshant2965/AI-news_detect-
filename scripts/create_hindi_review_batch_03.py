import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

input_file = (
    BASE
    / "data"
    / "processed"
    / "hindi"
    / "hindi_manual_review_queue.csv"
)

output_file = (
    BASE
    / "data"
    / "processed"
    / "hindi"
    / "hindi_manual_review_batch_03.csv"
)

# Load the remaining review queue
df = pd.read_csv(input_file)

# Remove candidates already reviewed in Batch 01 and Batch 02
reviewed_files = [
    BASE / "data" / "processed" / "hindi" / "hindi_verified_batch_01.csv",
    BASE / "data" / "processed" / "hindi" / "hindi_verified_batch_02.csv",
]

reviewed_ids = set()

for file in reviewed_files:
    if file.exists():
        reviewed_df = pd.read_csv(file)

        if "id" in reviewed_df.columns:
            reviewed_ids.update(reviewed_df["id"].astype(str))

# Make sure IDs are strings
df["id"] = df["id"].astype(str)

# Remove already reviewed IDs
remaining = df[~df["id"].isin(reviewed_ids)].copy()

# Take the next 20
batch = remaining.head(20).copy()

# Save Batch 03
batch.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print("=" * 70)
print("HINDI MANUAL REVIEW - BATCH 03")
print("=" * 70)

print("Total remaining candidates:", len(remaining))
print("Batch 03 size:", len(batch))

print("\nVerdicts:")
print(batch["verdict_candidate"].value_counts())

print("\nIDs:")
print(batch["id"].tolist())

print("\nSaved:")
print(output_file)