import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

queue_file = (
    BASE / "data" / "processed" / "hindi"
    / "hindi_manual_review_queue.csv"
)

output_file = (
    BASE / "data" / "processed" / "hindi"
    / "hindi_final_review_batch_33.csv"
)

# Load complete review queue
queue = pd.read_csv(queue_file)

# Load already reviewed batches
reviewed_files = [
    BASE / "data" / "processed" / "hindi"
    / "hindi_verified_batch_01.csv",

    BASE / "data" / "processed" / "hindi"
    / "hindi_verified_batch_02.csv",

    BASE / "data" / "processed" / "hindi"
    / "hindi_verified_batch_03.csv",

    BASE / "data" / "processed" / "hindi"
    / "hindi_verified_batch_04.csv",
]

reviewed_ids = set()

for file in reviewed_files:
    df = pd.read_csv(file)
    reviewed_ids.update(df["id"].astype(str))

print("=" * 70)
print("HINDI FINAL REVIEW BATCH")
print("=" * 70)

print("Total queue:", len(queue))
print("Already reviewed:", len(reviewed_ids))

# Keep only remaining candidates
remaining = queue[
    ~queue["id"].astype(str).isin(reviewed_ids)
].copy()

print("Remaining candidates:", len(remaining))

# Safety check
if len(remaining) != 33:
    print("\nWARNING:")
    print("Expected 33 remaining candidates.")
    print("Found:", len(remaining))
    print("Please check the batch files before continuing.")

# Select useful columns
columns = [
    "id",
    "claim_candidate",
    "conclusion_sentence",
    "verdict_candidate",
    "confidence",
    "source_domain_candidate",
    "source_url_candidate"
]

# Keep only columns that actually exist
columns = [c for c in columns if c in remaining.columns]

remaining = remaining[columns]

remaining.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print("\nFinal batch:")
print(remaining.head())

print("\nAutomatic verdict distribution:")
print(remaining["verdict_candidate"].value_counts())

print("\nSaved:")
print(output_file)