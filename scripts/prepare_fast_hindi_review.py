import pandas as pd
from pathlib import Path


FACTCHECK_FILE = (
    "data/processed/hindi/"
    "hindi_factcheck_sections.csv"
)

QUEUE_FILE = (
    "data/processed/hindi/"
    "hindi_manual_review_batch_01.csv"
)

OUTPUT_FILE = (
    "data/processed/hindi/"
    "hindi_fast_review_batch_01.csv"
)


# ============================================================
# LOAD
# ============================================================

queue = pd.read_csv(QUEUE_FILE)

factchecks = pd.read_csv(FACTCHECK_FILE)


# ============================================================
# KEEP ONLY REQUIRED ORIGINAL SECTIONS
# ============================================================

factchecks = factchecks[
    [
        "id",
        "title",
        "source_domain",
        "source_url",
        "conclusion_section"
    ]
].copy()


# ============================================================
# MERGE
# ============================================================

merged = queue.merge(
    factchecks,
    on="id",
    how="left",
    suffixes=("_candidate", "_original")
)


# ============================================================
# CREATE SIMPLE REVIEW FIELDS
# ============================================================

merged["review_verdict"] = ""

merged["review_status"] = "PENDING"


# ============================================================
# SAVE
# ============================================================

columns = [
    "id",
    "title_candidate",
    "source_domain_candidate",
    "source_url_candidate",

    "claim_candidate",
    "conclusion_sentence",

    "verdict_candidate",
    "matched_conclusion_phrase",

    "conclusion_section",

    "review_verdict",
    "review_status"
]

merged = merged[columns]


Path(
    OUTPUT_FILE
).parent.mkdir(
    parents=True,
    exist_ok=True
)

merged.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# PRINT
# ============================================================

print("\n========================================")
print("FAST HINDI REVIEW BATCH")
print("========================================")

print(
    "Articles:",
    len(merged)
)

print("\nColumns:")
print(
    merged.columns.tolist()
)

print("\nSaved:")
print(OUTPUT_FILE)