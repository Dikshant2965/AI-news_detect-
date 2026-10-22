import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "english"
    / "english_claim_verification_clean.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "english"
    / "splits"
)

RANDOM_STATE = 42


# Load
df = pd.read_csv(INPUT_FILE)

print("Original rows:", len(df))


# Remove duplicate claims
df = df.drop_duplicates(
    subset=["claim"],
    keep="first"
).reset_index(drop=True)

print("After duplicate removal:", len(df))


# First: 80% train, 20% temporary
train_df, temp_df = train_test_split(
    df,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=df["verdict"]
)


# Split remaining 20% into:
# 10% validation
# 10% test
val_df, test_df = train_test_split(
    temp_df,
    test_size=0.50,
    random_state=RANDOM_STATE,
    stratify=temp_df["verdict"]
)


# Create directory
OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# Save
train_df.to_csv(
    OUTPUT_DIR / "train.csv",
    index=False,
    encoding="utf-8-sig"
)

val_df.to_csv(
    OUTPUT_DIR / "validation.csv",
    index=False,
    encoding="utf-8-sig"
)

test_df.to_csv(
    OUTPUT_DIR / "test.csv",
    index=False,
    encoding="utf-8-sig"
)


print("\n" + "=" * 60)
print("ENGLISH DATASET SPLIT COMPLETE")
print("=" * 60)

print("\nTrain:", len(train_df))
print("Validation:", len(val_df))
print("Test:", len(test_df))

print("\nTrain distribution:")
print(train_df["verdict"].value_counts())

print("\nValidation distribution:")
print(val_df["verdict"].value_counts())

print("\nTest distribution:")
print(test_df["verdict"].value_counts())

print("\nSaved to:")
print(OUTPUT_DIR)