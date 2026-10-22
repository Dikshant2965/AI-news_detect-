from pathlib import Path
import pandas as pd

# Project paths
ROOT = Path(__file__).resolve().parents[1]

ENGLISH_PATH = Path(
    r"C:\Users\Dikshant Bedekar\Downloads"
    r"\Multilingual-Fake-News-Detection-College-Project-TXT-Datasets"
    r"\Final-Fake-News-Project\dataset\master_dataset.csv"
)

HINDI_PATH = ROOT / "data" / "processed" / "multilingual" / "hindi_cleaned.csv"
MARATHI_PATH = ROOT / "data" / "processed" / "multilingual" / "marathi_cleaned.csv"

OUTPUT_DIR = ROOT / "data" / "processed" / "multilingual"
OUTPUT_PATH = OUTPUT_DIR / "multilingual_fake_news_final.csv"


def main():
    print("Loading English dataset...")
    english = pd.read_csv(ENGLISH_PATH)

    # Keep only English records from the original master dataset.
    english = english[english["language"] == "English"].copy()

    english = english[["id", "language", "title", "text", "source_url", "label"]]

    print(f"English records: {len(english):,}")

    print("Loading cleaned Hindi dataset...")
    hindi = pd.read_csv(HINDI_PATH)

    print(f"Hindi records: {len(hindi):,}")

    print("Loading cleaned Marathi dataset...")
    marathi = pd.read_csv(MARATHI_PATH)

    print(f"Marathi records: {len(marathi):,}")

    # Standardize Hindi/Marathi to the same basic structure.
    hindi = hindi[["id", "language", "label", "text"]].copy()
    marathi = marathi[["id", "language", "label", "text"]].copy()

    hindi["title"] = ""
    hindi["source_url"] = ""

    marathi["title"] = ""
    marathi["source_url"] = ""

    hindi = hindi[["id", "language", "title", "text", "source_url", "label"]]
    marathi = marathi[["id", "language", "title", "text", "source_url", "label"]]

    # Combine all three languages.
    combined = pd.concat(
        [english, hindi, marathi],
        ignore_index=True
    )

    # Final audit.
    print("\n========== FINAL DATASET AUDIT ==========")
    print(f"Total records: {len(combined):,}")

    print("\nLanguage distribution:")
    print(combined["language"].value_counts())

    print("\nLabel distribution:")
    print(combined["label"].value_counts())

    print("\nLanguage × Label:")
    print(pd.crosstab(combined["language"], combined["label"]))

    print("\nMissing values:")
    print(combined.isna().sum())

    # Save.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    combined.to_csv(OUTPUT_PATH, index=False)

    print("\nSaved to:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()