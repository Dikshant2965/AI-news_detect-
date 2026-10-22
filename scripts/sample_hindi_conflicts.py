import pandas as pd

INPUT_FILE = (
    "data/processed/hindi/"
    "hindi_claim_candidates_auto_v2.csv"
)

df = pd.read_csv(INPUT_FILE)

conflicts = df[
    df["confidence"] == "conflict"
].copy()

print("\n========================================")
print("HINDI VERDICT CONFLICTS")
print("========================================")

print("Total conflicts:", len(conflicts))

# Show first 15 conflicts
sample = conflicts.head(15)

for i, (_, row) in enumerate(
    sample.iterrows(),
    start=1
):

    print("\n" + "=" * 80)
    print(f"CONFLICT {i}")
    print("=" * 80)

    print("ID:")
    print(row["id"])

    print("\nTITLE:")
    print(row["title"])

    print("\nEVIDENCE:")
    print(row["evidence_candidate"])

    print("\nMATCHED PHRASES:")
    print(row["matched_conclusion_phrase"])

    print("\nSOURCE:")
    print(row["source_domain"])