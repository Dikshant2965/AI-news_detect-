import pandas as pd

INPUT_FILE = "data/processed/hindi/hindi_claim_candidates_auto.csv"

df = pd.read_csv(INPUT_FILE)

# Keep only candidates where a verdict was detected
df = df[df["verdict_candidate"].notna()]
df = df[df["verdict_candidate"].astype(str).str.strip() != ""]

# Take a balanced sample
samples = []

for verdict in ["REFUTED", "MISLEADING", "SUPPORTED"]:

    subset = df[df["verdict_candidate"] == verdict]

    sample_size = min(5, len(subset))

    samples.append(
        subset.sample(
            n=sample_size,
            random_state=42
        )
    )

result = pd.concat(samples)

result = result[
    [
        "id",
        "title",
        "claim_candidate",
        "evidence_candidate",
        "verdict_candidate",
        "confidence",
        "source_domain"
    ]
]

print("\n========================================")
print("SAMPLE OF AUTOMATIC CLAIM CANDIDATES")
print("========================================")

for i, (_, row) in enumerate(result.iterrows(), start=1):

    print("\n" + "=" * 80)
    print(f"SAMPLE {i}")
    print("=" * 80)

    print("ID:")
    print(row["id"])

    print("\nTITLE:")
    print(row["title"])

    print("\nCLAIM CANDIDATE:")
    print(row["claim_candidate"])

    print("\nEVIDENCE CANDIDATE:")
    print(row["evidence_candidate"])

    print("\nVERDICT CANDIDATE:")
    print(row["verdict_candidate"])

    print("\nCONFIDENCE:")
    print(row["confidence"])

    print("\nSOURCE:")
    print(row["source_domain"])