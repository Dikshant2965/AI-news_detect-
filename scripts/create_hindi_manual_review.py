from pathlib import Path
import pandas as pd


# --------------------------------------------------
# Files
# --------------------------------------------------

ORIGINAL = Path(
    "data/processed/hindi/hindi_classification_candidates.csv"
)

SAMPLE = Path(
    "data/processed/hindi/hindi_claim_review_sample_20.csv"
)

OUTPUT = Path(
    "data/processed/hindi/hindi_manual_annotation_20.csv"
)


# --------------------------------------------------
# Load data
# --------------------------------------------------

original_df = pd.read_csv(ORIGINAL)
sample_df = pd.read_csv(SAMPLE)


# --------------------------------------------------
# Select the 20 sample IDs
# --------------------------------------------------

sample_ids = sample_df["id"].tolist()

review_df = original_df[
    original_df["id"].isin(sample_ids)
].copy()


# Keep the same order as the sample
review_df["sample_order"] = review_df["id"].apply(
    lambda x: sample_ids.index(x)
)

review_df = review_df.sort_values(
    "sample_order"
).drop(
    columns=["sample_order"]
)


# --------------------------------------------------
# Create annotation columns
# --------------------------------------------------

review_df["claim"] = ""

review_df["evidence"] = ""

review_df["verdict"] = ""

review_df["evidence_source"] = ""

review_df["review_notes"] = ""

review_df["review_status"] = "needs_manual_review"


# --------------------------------------------------
# Select useful columns
# --------------------------------------------------

review_df = review_df[
    [
        "id",
        "title",
        "text",
        "source_domain",
        "source_url",
        "claim",
        "evidence",
        "verdict",
        "evidence_source",
        "review_notes",
        "review_status",
    ]
]


# --------------------------------------------------
# Save
# --------------------------------------------------

OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

review_df.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8-sig"
)


print("=" * 60)
print("HINDI MANUAL ANNOTATION DATASET")
print("=" * 60)

print("\nRows:")
print(len(review_df))

print("\nColumns:")
print(review_df.columns.tolist())

print("\nSaved to:")
print(OUTPUT)

print("\n" + "=" * 60)
print("READY FOR MANUAL ANNOTATION")
print("=" * 60)