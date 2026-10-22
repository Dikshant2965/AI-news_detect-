from pathlib import Path
import pandas as pd

INPUT = Path(
    "data/processed/hindi/hindi_classification_candidates.csv"
)

df = pd.read_csv(INPUT)

print("=" * 60)
print("HINDI CANDIDATE DATASET QUALITY CHECK")
print("=" * 60)

print("\nDataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

# --------------------------------------------------
# Missing values
# --------------------------------------------------

print("\nMissing values:")
print(df.isnull().sum())

# --------------------------------------------------
# Text lengths
# --------------------------------------------------

df["title_length"] = df["title"].fillna("").astype(str).str.len()
df["text_length"] = df["text"].fillna("").astype(str).str.len()

print("\nTitle length statistics:")
print(df["title_length"].describe())

print("\nText length statistics:")
print(df["text_length"].describe())

# --------------------------------------------------
# Very short articles
# --------------------------------------------------

short_titles = df[df["title_length"] < 10]
short_texts = df[df["text_length"] < 50]

print("\nVery short titles (<10 characters):")
print(len(short_titles))

print("\nVery short texts (<50 characters):")
print(len(short_texts))

# --------------------------------------------------
# Duplicate content
# --------------------------------------------------

duplicate_content = df.duplicated(
    subset=["title", "text"]
).sum()

print("\nDuplicate title + text rows:")
print(duplicate_content)

# --------------------------------------------------
# Label distribution
# --------------------------------------------------

print("\nLabel distribution:")
print(df["label"].value_counts())

# --------------------------------------------------
# Source distribution
# --------------------------------------------------

print("\nSource distribution:")
print(df["source_domain"].value_counts())

# --------------------------------------------------
# Language check
# --------------------------------------------------

print("\nLanguage values:")
print(df["language"].value_counts())

# --------------------------------------------------
# Sample articles
# --------------------------------------------------

print("\n" + "=" * 60)
print("SAMPLE AUTHENTIC ARTICLES")
print("=" * 60)

for _, row in df[df["label"] == 0].head(5).iterrows():
    print("\nTITLE:", row["title"])
    print("TEXT:", str(row["text"])[:300])

print("\n" + "=" * 60)
print("SAMPLE FAKE ARTICLES")
print("=" * 60)

for _, row in df[df["label"] == 1].head(5).iterrows():
    print("\nTITLE:", row["title"])
    print("TEXT:", str(row["text"])[:300])

print("\n" + "=" * 60)
print("QUALITY CHECK COMPLETE")
print("=" * 60)