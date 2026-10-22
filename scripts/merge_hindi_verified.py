import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

HINDI_DIR = BASE / "data" / "processed" / "hindi"

files = [
    HINDI_DIR / "hindi_verified_batch_01.csv",
    HINDI_DIR / "hindi_verified_batch_02.csv",
    HINDI_DIR / "hindi_verified_batch_03.csv",
    HINDI_DIR / "hindi_verified_batch_04.csv",
    HINDI_DIR / "hindi_verified_batch_05_final_33.csv",
]

output_file = HINDI_DIR / "hindi_claim_verification_final.csv"

print("=" * 60)
print("MERGING HINDI VERIFIED CLAIM DATA")
print("=" * 60)

dataframes = []

for file in files:
    if not file.exists():
        print(f"\nERROR: File not found:")
        print(file)
        raise SystemExit(1)

    df = pd.read_csv(file)
    print(f"{file.name}: {len(df)} rows")
    dataframes.append(df)

# Combine all batches
final_df = pd.concat(dataframes, ignore_index=True)

print("\nTotal rows before duplicate check:", len(final_df))

# Remove duplicate IDs if any
before = len(final_df)
final_df = final_df.drop_duplicates(subset=["id"], keep="first")
duplicates_removed = before - len(final_df)

print("Duplicate IDs removed:", duplicates_removed)
print("Final rows:", len(final_df))

# Verdict distribution
print("\nVerdict distribution:")
print(final_df["verified_verdict"].value_counts())

# Review status
print("\nReview status:")
print(final_df["review_status"].value_counts())

# Save
final_df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print("\n" + "=" * 60)
print("FINAL HINDI DATASET CREATED")
print("=" * 60)
print(output_file)