from pathlib import Path
import pandas as pd

INPUT = Path("data/processed/hindi/hindi_clean.csv")
OUTPUT = Path("data/processed/hindi/hindi_classification_candidates.csv")

df = pd.read_csv(INPUT)

print("Original dataset:", len(df))

# Sources that contain both authentic and fake labels.
# These are more useful for classification because
# the model cannot simply learn "this source = fake".
source_counts = (
    df.groupby(["source_domain", "label"])
    .size()
    .unstack(fill_value=0)
)

print("\nSource label distribution:")
print(source_counts)

# Keep only sources having BOTH labels
usable_sources = source_counts[
    (source_counts.get(0, 0) > 0) &
    (source_counts.get(1, 0) > 0)
].index.tolist()

print("\nSources containing both labels:")
for source in usable_sources:
    print(" -", source)

candidate_df = df[df["source_domain"].isin(usable_sources)].copy()

print("\nCandidate dataset size:", len(candidate_df))

print("\nCandidate label distribution:")
print(candidate_df["label"].value_counts())

# Balance the classes
min_count = candidate_df["label"].value_counts().min()

print("\nBalancing each class to:", min_count)

balanced_parts = []

for label in sorted(candidate_df["label"].unique()):
    part = candidate_df[candidate_df["label"] == label]

    # Fixed random_state makes the selection reproducible
    part = part.sample(
        n=min_count,
        random_state=42
    )

    balanced_parts.append(part)

balanced_df = pd.concat(
    balanced_parts,
    ignore_index=True
)

# Shuffle final dataset
balanced_df = balanced_df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

print("\nFINAL CANDIDATE DATASET")
print("Rows:", len(balanced_df))

print("\nLabels:")
print(balanced_df["label"].value_counts())

print("\nSources:")
print(balanced_df["source_domain"].value_counts())

# Save
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

balanced_df.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved to:")
print(OUTPUT)