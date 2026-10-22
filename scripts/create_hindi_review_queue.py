import pandas as pd
from pathlib import Path


INPUT_FILE = (
    "data/processed/hindi/"
    "hindi_claim_candidates_auto_v3.csv"
)

OUTPUT_FILE = (
    "data/processed/hindi/"
    "hindi_manual_review_queue.csv"
)


# ============================================================
# LOAD
# ============================================================

df = pd.read_csv(INPUT_FILE)


# ============================================================
# KEEP ONLY HIGH-CONFIDENCE REFUTED / MISLEADING
# ============================================================

queue = df[
    (df["confidence"] == "high") &
    (
        df["verdict_candidate"].isin(
            ["REFUTED", "MISLEADING"]
        )
    )
].copy()


# ============================================================
# REMOVE DUPLICATE IDS
# ============================================================

queue = queue.drop_duplicates(
    subset=["id"]
)


# ============================================================
# CREATE REVIEW COLUMNS
# ============================================================

queue["verified_claim"] = ""

queue["verified_evidence"] = ""

queue["verified_verdict"] = ""

queue["evidence_source"] = ""

queue["review_notes"] = ""

queue["review_status"] = "needs_manual_review"


# ============================================================
# SELECT USEFUL COLUMNS
# ============================================================

queue = queue[
    [
        "id",
        "title",
        "source_domain",
        "source_url",

        "claim_candidate",
        "conclusion_sentence",

        "verdict_candidate",
        "matched_conclusion_phrase",

        "verified_claim",
        "verified_evidence",
        "verified_verdict",
        "evidence_source",
        "review_notes",

        "review_status"
    ]
]


# ============================================================
# SAVE
# ============================================================

Path(
    OUTPUT_FILE
).parent.mkdir(
    parents=True,
    exist_ok=True
)

queue.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# REPORT
# ============================================================

print("\n========================================")
print("HINDI MANUAL REVIEW QUEUE")
print("========================================")

print(
    "Total candidates:",
    len(queue)
)

print("\nCandidate verdicts:")

print(
    queue["verdict_candidate"]
    .value_counts()
)

print("\nReview status:")

print(
    queue["review_status"]
    .value_counts()
)

print("\nSaved:")

print(
    OUTPUT_FILE
)