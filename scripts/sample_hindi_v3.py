import pandas as pd


INPUT_FILE = (
    "data/processed/hindi/"
    "hindi_claim_candidates_auto_v3.csv"
)

df = pd.read_csv(INPUT_FILE)

# Only high-confidence candidates
df = df[
    df["confidence"] == "high"
].copy()

print("\n========================================")
print("V3 HIGH-CONFIDENCE SAMPLE")
print("========================================")

print("Total high-confidence:", len(df))


# Take 5 from each major category
samples = []

for verdict in ["REFUTED", "MISLEADING", "SUPPORTED"]:

    subset = df[
        df["verdict_candidate"] == verdict
    ]

    if len(subset) > 0:

        n = min(5, len(subset))

        samples.append(
            subset.sample(
                n=n,
                random_state=42
            )
        )


if samples:

    result = pd.concat(samples)

else:

    result = df.head(15)


for i, (_, row) in enumerate(
    result.iterrows(),
    start=1
):

    print("\n" + "=" * 80)
    print(f"SAMPLE {i}")
    print("=" * 80)

    print("\nID:")
    print(row["id"])

    print("\nCLAIM:")
    print(row["claim_candidate"])

    print("\nCONCLUSION SENTENCE:")
    print(row["conclusion_sentence"])

    print("\nVERDICT:")
    print(row["verdict_candidate"])

    print("\nMATCHED PHRASE:")
    print(row["matched_conclusion_phrase"])

    print("\nSOURCE:")
    print(row["source_domain"])