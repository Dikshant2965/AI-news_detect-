import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "english"
    / "english_claim_verification.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "english"
    / "english_claim_verification_clean.csv"
)


df = pd.read_csv(INPUT_FILE)


# ------------------------------------------------------------
# Clean Wikipedia bracket markers
# ------------------------------------------------------------

def clean_text(text):

    if pd.isna(text):
        return ""

    text = str(text)

    text = text.replace("-LRB-", "(")
    text = text.replace("-RRB-", ")")

    text = text.replace("-LSB-", "[")
    text = text.replace("-RSB-", "]")

    # Normalize repeated whitespace
    text = " ".join(text.split())

    return text.strip()


df["claim"] = df["claim"].apply(clean_text)
df["evidence"] = df["evidence"].apply(clean_text)


# ------------------------------------------------------------
# Remove exact duplicate rows
# ------------------------------------------------------------

before = len(df)

df = df.drop_duplicates(
    subset=["claim", "evidence", "verdict"]
)

after = len(df)


# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


# ------------------------------------------------------------
# Report
# ------------------------------------------------------------

print("=" * 60)
print("ENGLISH DATASET CLEANING COMPLETE")
print("=" * 60)

print(f"Input rows:  {before}")
print(f"Output rows: {after}")
print(f"Duplicates removed: {before - after}")

print("\nVerdict distribution:")

print(
    df["verdict"].value_counts()
)

print("\nMissing values:")

print(
    df[
        ["claim", "evidence", "verdict", "language"]
    ].isna().sum()
)

print("\nSaved to:")

print(OUTPUT_FILE)