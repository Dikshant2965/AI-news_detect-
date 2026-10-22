import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

batch_file = BASE / "data" / "processed" / "hindi" / "hindi_manual_review_batch_02.csv"
sections_file = BASE / "data" / "processed" / "hindi" / "hindi_factcheck_sections.csv"

output_file = BASE / "data" / "processed" / "hindi" / "hindi_fast_review_batch_02.csv"

# Load files
batch = pd.read_csv(batch_file)
sections = pd.read_csv(sections_file)

print("Batch 02 columns:")
print(batch.columns.tolist())

print("\nFact-check sections columns:")
print(sections.columns.tolist())

# Merge using ID
merged = batch.merge(
    sections,
    on="id",
    how="left",
    suffixes=("_batch", "_section")
)

# Create consistent source columns
if "source_domain_candidate" not in merged.columns:
    if "source_domain" in merged.columns:
        merged["source_domain_candidate"] = merged["source_domain"]
    elif "source_domain_section" in merged.columns:
        merged["source_domain_candidate"] = merged["source_domain_section"]
    elif "source_domain_batch" in merged.columns:
        merged["source_domain_candidate"] = merged["source_domain_batch"]
    else:
        merged["source_domain_candidate"] = ""

if "source_url_candidate" not in merged.columns:
    if "source_url" in merged.columns:
        merged["source_url_candidate"] = merged["source_url"]
    elif "source_url_section" in merged.columns:
        merged["source_url_candidate"] = merged["source_url_section"]
    elif "source_url_batch" in merged.columns:
        merged["source_url_candidate"] = merged["source_url_batch"]
    else:
        merged["source_url_candidate"] = ""

# Required columns
columns = [
    "id",
    "title",
    "claim_candidate",
    "verdict_candidate",
    "conclusion_sentence",
    "source_domain_candidate",
    "source_url_candidate"
]

# Keep only columns that exist
available_columns = [c for c in columns if c in merged.columns]

merged = merged[available_columns]

# Save
merged.to_csv(output_file, index=False, encoding="utf-8-sig")

print("\nSUCCESS")
print("Rows:", len(merged))
print("Saved:", output_file)
print("\nColumns:")
print(merged.columns.tolist())