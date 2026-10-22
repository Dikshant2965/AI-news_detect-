import pandas as pd


INPUT_FILE = (
    "data/processed/hindi/"
    "hindi_manual_review_queue.csv"
)

OUTPUT_FILE = (
    "data/processed/hindi/"
    "hindi_manual_review_batch_02.csv"
)


df = pd.read_csv(INPUT_FILE)

# Remove Batch 01 IDs
batch_01_ids = [
    "HIN_007479",
    "HIN_007002",
    "HIN_008563",
    "HIN_007307",
    "HIN_007616",
    "HIN_007537",
    "HIN_007177",
    "HIN_007229",
    "HIN_008558",
    "HIN_008571",
    "HIN_007575",
    "HIN_006653",
    "HIN_007434",
    "HIN_007603",
    "HIN_007404",
    "HIN_006424",
    "HIN_008162",
    "HIN_007705",
    "HIN_007012",
    "HIN_008116",
]

remaining = df[
    ~df["id"].isin(batch_01_ids)
].copy()

# Random sample from remaining candidates
batch = remaining.sample(
    n=min(20, len(remaining)),
    random_state=2026
)

batch.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("\n========================================")
print("HINDI MANUAL REVIEW BATCH 02")
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