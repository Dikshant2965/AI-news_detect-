import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

batch_file = (
    BASE / "data" / "processed" / "hindi"
    / "hindi_manual_review_batch_04.csv"
)

sections_file = (
    BASE / "data" / "processed" / "hindi"
    / "hindi_factcheck_sections.csv"
)

output_file = (
    BASE / "data" / "processed" / "hindi"
    / "hindi_fast_review_batch_04.csv"
)

batch = pd.read_csv(batch_file)
sections = pd.read_csv(sections_file)

merged = batch.merge(
    sections,
    on="id",
    how="left",
    suffixes=("_batch", "_section")
)

if "source_domain_candidate" not in merged.columns:
    if "source_domain_batch" in merged.columns:
        merged["source_domain_candidate"] = merged["source_domain_batch"]
    elif "source_domain_section" in merged.columns:
        merged["source_domain_candidate"] = merged["source_domain_section"]
    else:
        merged["source_domain_candidate"] = ""

if "source_url_candidate" not in merged.columns:
    if "source_url_batch" in merged.columns:
        merged["source_url_candidate"] = merged["source_url_batch"]
    elif "source_url_section" in merged.columns:
        merged["source_url_candidate"] = merged["source_url_section"]
    else:
        merged["source_url_candidate"] = ""

columns = [
    "id",
    "claim_candidate",
    "verdict_candidate",
    "conclusion_sentence",
    "source_domain_candidate",
    "source_url_candidate"
]

merged = merged[columns]

merged.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print("=" * 70)
print("HINDI FAST REVIEW BATCH 04")
print("=" * 70)

print("Rows:", len(merged))

print("\nSaved:")
print(output_file)