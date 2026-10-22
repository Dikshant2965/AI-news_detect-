import pandas as pd

INPUT_FILE = (
    "data/processed/hindi/"
    "hindi_manual_review_queue.csv"
)

OUTPUT_FILE = (
    "data/processed/hindi/"
    "hindi_manual_review_batch_01.csv"
)

df = pd.read_csv(INPUT_FILE)

# Take 10 REFUTED + 10 MISLEADING
refuted = df[
    df["verdict_candidate"] == "REFUTED"
].head(10)

misleading = df[
    df["verdict_candidate"] == "MISLEADING"
].head(10)

batch = pd.concat(
    [refuted, misleading],
    ignore_index=True
)

batch.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("\n========================================")
print("HINDI MANUAL REVIEW BATCH 01")
print("========================================")

print("Total:", len(batch))

print("\nVerdicts:")
print(
    batch["verdict_candidate"].value_counts()
)

print("\nIDs:")
print(
    batch["id"].tolist()
)

print("\nSaved:")
print(OUTPUT_FILE)