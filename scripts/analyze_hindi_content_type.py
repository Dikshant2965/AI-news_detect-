import pandas as pd
import re

FILE = "data/processed/hindi/hindi_clean.csv"

df = pd.read_csv(FILE)

print("=" * 70)
print("HINDI CONTENT TYPE ANALYSIS")
print("=" * 70)


# --------------------------------------------------
# KEYWORDS / PATTERNS
# --------------------------------------------------

factcheck_patterns = [
    r"fact[\s-]?check",
    r"फैक्ट[\s-]?चेक",
    r"फर्जी",
    r"फ़र्ज़ी",
    r"फेक न्यूज़",
    r"फेक न्यूज",
    r"फर्जी खबर",
    r"झूठा दावा",
    r"झूठी खबर",
    r"गलत दावा",
    r"वायरल दावा",
    r"वायरल तस्वीर",
    r"वायरल वीडियो",
    r"वायरल पोस्ट",
    r"असली नहीं",
    r"फर्जी दावा",
    r"भ्रामक दावा",
    r"misleading",
    r"fake news",
    r"false claim",
    r"viral claim",
    r"fact check"
]


# --------------------------------------------------
# COMBINE TITLE + TEXT
# --------------------------------------------------

df["combined_text"] = (
    df["title"].fillna("").astype(str)
    + " "
    + df["text"].fillna("").astype(str)
)


# --------------------------------------------------
# DETECT FACT-CHECK PATTERNS
# --------------------------------------------------

pattern = "|".join(factcheck_patterns)

df["factcheck_keyword_match"] = (
    df["combined_text"]
    .str.contains(
        pattern,
        case=False,
        regex=True,
        na=False
    )
)


# --------------------------------------------------
# DETECT FACT-CHECK DOMAINS
# --------------------------------------------------

factcheck_domains = [
    "boomlive.in",
    "vishvasnews.com"
]

df["factcheck_domain"] = df["source_domain"].apply(
    lambda domain: any(
        fc_domain in str(domain).lower()
        for fc_domain in factcheck_domains
    )
)


# --------------------------------------------------
# COMBINE SIGNALS
# --------------------------------------------------

df["possible_factcheck"] = (
    df["factcheck_keyword_match"]
    | df["factcheck_domain"]
)


# --------------------------------------------------
# RESULTS
# --------------------------------------------------

print("\nTotal articles:")
print(len(df))

print("\nPossible fact-check articles:")
print(
    df["possible_factcheck"]
    .value_counts()
)


print("\nPossible fact-check by label:")

print(
    pd.crosstab(
        df["possible_factcheck"],
        df["label"]
    ).rename(
        columns={
            0: "Authentic",
            1: "Fake"
        }
    )
)


# --------------------------------------------------
# DOMAIN BREAKDOWN
# --------------------------------------------------

print("\nFact-check candidates by source:")

print(
    df[df["possible_factcheck"]]
    ["source_domain"]
    .value_counts()
)


# --------------------------------------------------
# SHOW EXAMPLES
# --------------------------------------------------

print("\n" + "=" * 70)
print("SAMPLE FACT-CHECK CANDIDATES")
print("=" * 70)

sample = df[df["possible_factcheck"]].head(20)

for _, row in sample.iterrows():

    label = (
        "Authentic"
        if row["label"] == 0
        else "Fake"
    )

    print("\n----------------------------------------")
    print("Source:", row["source_domain"])
    print("Label:", label)
    print("Title:", row["title"])


# --------------------------------------------------
# SAVE ANALYSIS
# --------------------------------------------------

output_file = "data/processed/hindi/hindi_content_analysis.csv"

df.drop(
    columns=["combined_text"]
).to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print("\n" + "=" * 70)
print("Analysis saved to:")
print(output_file)
print("=" * 70)