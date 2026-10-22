import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

input_file = (
    BASE
    / "data"
    / "processed"
    / "hindi"
    / "hindi_claim_verification_final.csv"
)

output_file = (
    BASE
    / "data"
    / "processed"
    / "hindi"
    / "hindi_claim_verification_clean.csv"
)

df = pd.read_csv(input_file)

clean_df = pd.DataFrame({
    "id": df["id"],
    "claim": df["verified_claim"],
    "evidence": df["verified_evidence"],
    "verdict": df["verified_verdict"],
    "evidence_source": df["evidence_source"],
    "language": "hi",
    "review_status": df["review_status"]
})

print("=" * 60)
print("CLEAN HINDI CLAIM VERIFICATION DATASET")
print("=" * 60)

print("Rows:", len(clean_df))
print("Columns:", clean_df.columns.tolist())

print("\nMissing values:")
print(clean_df.isna().sum())

print("\nVerdicts:")
print(clean_df["verdict"].value_counts())

print("\nLanguages:")
print(clean_df["language"].value_counts())

clean_df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved:")
print(output_file)