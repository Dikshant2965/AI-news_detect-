import pandas as pd
from pathlib import Path
from urllib.parse import urlparse

# --------------------------------------------------
# PATHS
# --------------------------------------------------

DATA_DIR = Path("data/raw/hindi")
OUTPUT_DIR = Path("data/processed/hindi")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

AUTHENTIC_FILE = DATA_DIR / "authentic.xlsx"
FAKE_FILE = DATA_DIR / "fake.xlsx"


# --------------------------------------------------
# HELPER FUNCTION
# --------------------------------------------------

def extract_domain(url):
    """Extract domain name from a URL."""
    try:
        return urlparse(str(url)).netloc.lower()
    except Exception:
        return ""


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

print("=" * 70)
print("HINDI FAKE NEWS DATASET PREPROCESSING")
print("=" * 70)

print("\nLoading authentic dataset...")
authentic = pd.read_excel(AUTHENTIC_FILE)

print("Loading fake dataset...")
fake = pd.read_excel(FAKE_FILE)


# --------------------------------------------------
# ADD LABELS
# --------------------------------------------------

authentic["label"] = 0
fake["label"] = 1

print("\nLabels assigned:")
print("0 = Authentic")
print("1 = Fake")


# --------------------------------------------------
# ADD LANGUAGE
# --------------------------------------------------

authentic["language"] = "hi"
fake["language"] = "hi"


# --------------------------------------------------
# COMBINE DATASETS
# --------------------------------------------------

df = pd.concat(
    [authentic, fake],
    ignore_index=True
)

print("\nRaw combined dataset:")
print(f"Rows: {len(df)}")


# --------------------------------------------------
# RENAME COLUMNS
# --------------------------------------------------

df = df.rename(
    columns={
        "Title": "title",
        "Summary": "text",
        "URL": "source_url",
        "Authors": "author",
        "dates": "published_date"
    }
)


# --------------------------------------------------
# REMOVE UNNECESSARY COLUMN
# --------------------------------------------------

if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])


# --------------------------------------------------
# EXTRACT SOURCE DOMAIN
# --------------------------------------------------

df["source_domain"] = df["source_url"].apply(extract_domain)


# --------------------------------------------------
# KEEP ONLY OUR STANDARD COLUMNS
# --------------------------------------------------

columns = [
    "title",
    "text",
    "source_url",
    "source_domain",
    "author",
    "published_date",
    "language",
    "label"
]

df = df[columns]


# --------------------------------------------------
# BASIC CLEANING
# --------------------------------------------------

# Convert important text columns to strings
for column in ["title", "text", "source_url", "source_domain", "author"]:
    df[column] = df[column].fillna("").astype(str)

# Remove leading/trailing whitespace
for column in ["title", "text", "source_url", "source_domain", "author"]:
    df[column] = df[column].str.strip()


# --------------------------------------------------
# REMOVE EMPTY ARTICLES
# --------------------------------------------------

before_empty = len(df)

df = df[
    (df["title"].str.len() > 0) &
    (df["text"].str.len() > 0)
].copy()

removed_empty = before_empty - len(df)


# --------------------------------------------------
# CHECK DUPLICATE URLs
# --------------------------------------------------

duplicate_urls = df["source_url"].duplicated().sum()


# --------------------------------------------------
# REMOVE DUPLICATE URLs
# --------------------------------------------------

before_url_dedup = len(df)

df = df.drop_duplicates(
    subset=["source_url"],
    keep="first"
).copy()

removed_url_duplicates = before_url_dedup - len(df)


# --------------------------------------------------
# CHECK DUPLICATE TITLE + TEXT
# --------------------------------------------------

duplicate_content = df.duplicated(
    subset=["title", "text"]
).sum()


# --------------------------------------------------
# REMOVE DUPLICATE CONTENT
# --------------------------------------------------

before_content_dedup = len(df)

df = df.drop_duplicates(
    subset=["title", "text"],
    keep="first"
).copy()

removed_content_duplicates = (
    before_content_dedup - len(df)
)


# --------------------------------------------------
# RESET INDEX
# --------------------------------------------------

df = df.reset_index(drop=True)


# --------------------------------------------------
# CREATE OUR OWN ID
# --------------------------------------------------

df.insert(
    0,
    "id",
    [
        f"HIN_{i:06d}"
        for i in range(1, len(df) + 1)
    ]
)


# --------------------------------------------------
# DATASET REPORT
# --------------------------------------------------

print("\n" + "=" * 70)
print("DATASET REPORT")
print("=" * 70)

print(f"\nOriginal authentic articles: {len(authentic)}")
print(f"Original fake articles:      {len(fake)}")
print(f"Original total:              {len(authentic) + len(fake)}")

print(f"\nRemoved empty articles:       {removed_empty}")

print(f"Duplicate URLs found:        {duplicate_urls}")
print(f"Duplicate URLs removed:      {removed_url_duplicates}")

print(f"Duplicate content found:     {duplicate_content}")
print(f"Duplicate content removed:   {removed_content_duplicates}")

print(f"\nFINAL DATASET SIZE:           {len(df)}")


# --------------------------------------------------
# LABEL DISTRIBUTION
# --------------------------------------------------

print("\nLabel distribution:")

print(
    df["label"]
    .value_counts()
    .sort_index()
    .rename(
        index={
            0: "Authentic",
            1: "Fake"
        }
    )
)


# --------------------------------------------------
# SOURCE DISTRIBUTION
# --------------------------------------------------

print("\nTop 15 sources:")

print(
    df["source_domain"]
    .value_counts()
    .head(15)
)


# --------------------------------------------------
# MISSING VALUES
# --------------------------------------------------

print("\nMissing values:")

print(df.isnull().sum())


# --------------------------------------------------
# SAVE CLEAN DATASET
# --------------------------------------------------

output_file = OUTPUT_DIR / "hindi_clean.csv"

df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print("\n" + "=" * 70)
print("SUCCESS")
print("=" * 70)

print(f"\nClean dataset saved to:")
print(output_file)

print("\nHindi preprocessing completed.")