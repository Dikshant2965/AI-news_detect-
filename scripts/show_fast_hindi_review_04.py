import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

file_path = (
    BASE
    / "data"
    / "processed"
    / "hindi"
    / "hindi_fast_review_batch_04.csv"
)

df = pd.read_csv(file_path)

print("=" * 100)
print("HINDI MANUAL REVIEW - BATCH 04")
print("=" * 100)

print(f"\nTotal rows: {len(df)}\n")

for i, row in df.iterrows():

    print("\n" + "=" * 100)
    print(f"ITEM {i + 1} / {len(df)}")
    print("=" * 100)

    print(f"ID: {row['id']}")

    print("\nCLAIM:")
    print(row["claim_candidate"])

    print("\nAUTO VERDICT:")
    print(row["verdict_candidate"])

    print("\nCONCLUSION / EVIDENCE:")
    print(row["conclusion_sentence"])

    print("\nSOURCE DOMAIN:")
    print(row["source_domain_candidate"])

    print("\nSOURCE URL:")
    print(row["source_url_candidate"])

print("\n" + "=" * 100)
print("END OF BATCH 04")
print("=" * 100)