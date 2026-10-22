from pathlib import Path
import pandas as pd

INPUT = Path(
    "data/processed/hindi/hindi_classification_candidates.csv"
)

df = pd.read_csv(INPUT)

# Combine title and text
df["combined_text"] = (
    df["title"].fillna("").astype(str)
    + " "
    + df["text"].fillna("").astype(str)
)

# Patterns commonly appearing in Hindi fact-check articles
patterns = [
    "फैक्ट चेक",
    "फैक्टचेक",
    "फर्जी",
    "फेक न्यूज",
    "फेक न्यूज़",
    "झूठा दावा",
    "गलत दावा",
    "भ्रामक दावा",
    "भ्रामक",
    "वायरल दावा",
    "वायरल तस्वीर",
    "वायरल फोटो",
    "वायरल वीडियो",
    "दावे की सच्चाई",
    "दावे का सच",
    "पड़ताल",
    "सच्चाई",
    "सच क्या है",
    "क्या है सच",
    "Fact Check",
    "fact check",
]

# Mark possible fact-check articles
df["possible_factcheck"] = False

for pattern in patterns:
    df["possible_factcheck"] |= (
        df["combined_text"].str.contains(
            pattern,
            case=False,
            na=False,
            regex=False
        )
    )

print("=" * 60)
print("HINDI LABEL ANALYSIS")
print("=" * 60)

print("\nTotal articles:")
print(len(df))

print("\nPossible fact-check articles:")
print(df["possible_factcheck"].value_counts())

print("\nPossible fact-check by label:")
print(
    pd.crosstab(
        df["possible_factcheck"],
        df["label"]
    )
)

print("\nPercentage of each label that looks like fact-check:")
print(
    df.groupby("label")["possible_factcheck"]
    .mean()
    .mul(100)
    .round(2)
)

print("\nPossible fact-check by source:")
print(
    pd.crosstab(
        df["source_domain"],
        df["possible_factcheck"]
    )
)

# Show examples
print("\n" + "=" * 60)
print("FACT-CHECK CANDIDATE EXAMPLES")
print("=" * 60)

examples = df[
    df["possible_factcheck"]
].head(20)

for _, row in examples.iterrows():
    print("\nLABEL:", row["label"])
    print("SOURCE:", row["source_domain"])
    print("TITLE:", row["title"])
    print("TEXT:", row["text"][:250])

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)