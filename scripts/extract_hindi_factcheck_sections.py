from pathlib import Path
import pandas as pd
import re

INPUT = Path(
    "data/processed/hindi/hindi_classification_candidates.csv"
)

df = pd.read_csv(INPUT)

factchecks = df[df["label"] == 1].copy()

# Phrases that commonly introduce the conclusion of a fact-check
conclusion_patterns = [
    "पड़ताल में यह साफ हुआ",
    "पड़ताल में साफ हुआ",
    "पड़ताल में यह पता चला",
    "पड़ताल में पता चला",
    "फैक्ट चेक में",
    "हमारी पड़ताल",
    "हमने पाया",
    "पाया कि",
    "दावे की सच्चाई",
    "दावे का सच",
    "इससे साबित होता है",
    "इससे यह साबित होता है",
    "इस बात की पुष्टि",
    "यह दावा गलत",
    "यह दावा झूठा",
    "यह दावा भ्रामक",
    "दावा भ्रामक",
    "दावा झूठा",
    "दावा गलत",
    "सच यह है",
    "सच्चाई यह है",
]

def find_conclusion(text):
    text = str(text)

    positions = []

    for pattern in conclusion_patterns:
        position = text.lower().find(pattern.lower())

        if position != -1:
            positions.append((position, pattern))

    if not positions:
        return None, None

    # Take the earliest conclusion indicator
    position, pattern = min(positions, key=lambda x: x[0])

    # Extract a surrounding section
    start = max(0, position - 100)
    end = min(len(text), position + 600)

    section = text[start:end]

    return pattern, section


results = []

for _, row in factchecks.iterrows():

    pattern, section = find_conclusion(
        row["text"]
    )

    results.append({
        "id": row["id"],
        "title": row["title"],
        "source_domain": row["source_domain"],
        "source_url": row["source_url"],
        "conclusion_indicator": pattern,
        "conclusion_section": section,
    })


result_df = pd.DataFrame(results)

print("=" * 60)
print("HINDI FACT-CHECK CONCLUSION ANALYSIS")
print("=" * 60)

print("\nTotal fact-check articles:")
print(len(result_df))

print("\nArticles where a conclusion indicator was found:")
print(
    result_df["conclusion_indicator"]
    .notna()
    .sum()
)

print("\nArticles without a detected conclusion indicator:")
print(
    result_df["conclusion_indicator"]
    .isna()
    .sum()
)

print("\nMost common conclusion indicators:")

print(
    result_df["conclusion_indicator"]
    .value_counts()
    .head(20)
)

print("\n" + "=" * 60)
print("SAMPLE EXTRACTED CONCLUSIONS")
print("=" * 60)

samples = result_df[
    result_df["conclusion_indicator"].notna()
].head(15)

for _, row in samples.iterrows():

    print("\n" + "-" * 50)

    print("TITLE:")
    print(row["title"])

    print("\nINDICATOR:")
    print(row["conclusion_indicator"])

    print("\nEXTRACT:")
    print(row["conclusion_section"])


# Save results
OUTPUT = Path(
    "data/processed/hindi/hindi_factcheck_sections.csv"
)

OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

result_df.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

print("\nSaved to:")
print(OUTPUT)

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)