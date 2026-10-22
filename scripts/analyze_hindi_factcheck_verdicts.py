from pathlib import Path
import pandas as pd

INPUT = Path(
    "data/processed/hindi/hindi_classification_candidates.csv"
)

df = pd.read_csv(INPUT)

df["combined_text"] = (
    df["title"].fillna("").astype(str)
    + " "
    + df["text"].fillna("").astype(str)
)

# --------------------------------------------------
# Verdict-related phrases
# --------------------------------------------------

verdict_patterns = {
    "false": [
        "झूठा दावा",
        "दावा झूठा",
        "गलत दावा",
        "दावा गलत",
        "फर्जी दावा",
        "फर्जी खबर",
        "फेक न्यूज",
        "अफवाह",
        "भ्रामक दावा",
        "दावा है भ्रामक",
        "सच नहीं",
        "सही नहीं",
        "गलत है",
        "झूठ है",
        "नहीं है",
    ],

    "true": [
        "दावा सही है",
        "दावा सच है",
        "सही दावा",
        "सच है",
        "वास्तव में",
        "सही पाया",
    ],

    "misleading": [
        "भ्रामक",
        "आंशिक रूप से सही",
        "अधूरा सच",
        "गलत संदर्भ",
        "भ्रामक तरीके से",
    ]
}

# --------------------------------------------------
# Detect possible verdict language
# --------------------------------------------------

for verdict, patterns in verdict_patterns.items():

    column = f"verdict_{verdict}"

    df[column] = False

    for pattern in patterns:
        df[column] |= df["combined_text"].str.contains(
            pattern,
            case=False,
            na=False,
            regex=False
        )

# --------------------------------------------------
# Print statistics
# --------------------------------------------------

print("=" * 60)
print("HINDI FACT-CHECK VERDICT ANALYSIS")
print("=" * 60)

factcheck_df = df[df["label"] == 1].copy()

print("\nTotal fact-check candidates:")
print(len(factcheck_df))

for verdict in verdict_patterns:

    column = f"verdict_{verdict}"

    count = factcheck_df[column].sum()

    percentage = (
        count / len(factcheck_df) * 100
    )

    print(
        f"\n{verdict.upper()}: "
        f"{count} ({percentage:.2f}%)"
    )

# --------------------------------------------------
# Show examples
# --------------------------------------------------

print("\n" + "=" * 60)
print("VERDICT EXAMPLES")
print("=" * 60)

for verdict in verdict_patterns:

    column = f"verdict_{verdict}"

    print("\n" + "-" * 50)
    print(verdict.upper())

    examples = factcheck_df[
        factcheck_df[column]
    ].head(5)

    for _, row in examples.iterrows():

        print("\nTITLE:")
        print(row["title"])

        print("\nTEXT:")
        print(row["text"][:500])

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)