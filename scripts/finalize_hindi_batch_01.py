import pandas as pd
from pathlib import Path


INPUT_FILE = (
    "data/processed/hindi/"
    "hindi_fast_review_batch_01.csv"
)

OUTPUT_FILE = (
    "data/processed/hindi/"
    "hindi_verified_batch_01.csv"
)


df = pd.read_csv(INPUT_FILE)


# ============================================================
# ALL 20 WERE VALIDATED
# ============================================================

df["verified_verdict"] = df["verdict_candidate"]

df["review_status"] = "reviewed"

df["review_notes"] = (
    "Automatic verdict manually validated against "
    "the original fact-check conclusion."
)


# ============================================================
# EVIDENCE
# ============================================================

df["verified_evidence"] = df[
    "conclusion_sentence"
]


# ============================================================
# CLAIM
# ============================================================

df["verified_claim"] = df[
    "claim_candidate"
]


# ============================================================
# EVIDENCE SOURCE
# ============================================================

df["evidence_source"] = (
    "Fact-check investigation / source cited in article"
)


# ============================================================
# FINAL COLUMNS
# ============================================================

result = df[
    [
        "id",
        "verified_claim",
        "verified_evidence",
        "verified_verdict",
        "evidence_source",
        "review_notes",
        "source_domain_candidate",
        "source_url_candidate",
        "review_status"
    ]
].copy()


# ============================================================
# SAVE
# ============================================================

Path(
    OUTPUT_FILE
).parent.mkdir(
    parents=True,
    exist_ok=True
)

result.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


print("\n========================================")
print("HINDI VERIFIED BATCH 01")
print("========================================")

print("Rows:", len(result))

print("\nVerdicts:")
print(
    result["verified_verdict"].value_counts()
)

print("\nReview status:")
print(
    result["review_status"].value_counts()
)

print("\nSaved:")
print(OUTPUT_FILE)