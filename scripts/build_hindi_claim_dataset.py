from pathlib import Path
import pandas as pd


INPUT = Path(
    "data/processed/hindi/hindi_factcheck_sections.csv"
)

OUTPUT = Path(
    "data/processed/hindi/hindi_claim_verification_working.csv"
)


df = pd.read_csv(INPUT)


# --------------------------------------------------
# Keep only articles where we found a possible
# conclusion/investigation section.
# --------------------------------------------------

df = df[
    df["conclusion_indicator"].notna()
].copy()


# --------------------------------------------------
# Create a clean working structure
# --------------------------------------------------

claim_df = pd.DataFrame({
    "id": df["id"],
    "title": df["title"],
    "source_domain": df["source_domain"],
    "source_url": df["source_url"],
    "conclusion_indicator": df["conclusion_indicator"],
    "conclusion_section": df["conclusion_section"],
})


# --------------------------------------------------
# Add empty fields that we will annotate later.
# These are NOT automatically generated labels.
# --------------------------------------------------

claim_df["claim"] = ""

claim_df["evidence"] = ""

claim_df["verdict"] = ""

claim_df["evidence_source"] = ""


# --------------------------------------------------
# Add review status
# --------------------------------------------------

claim_df["review_status"] = "needs_manual_review"


# --------------------------------------------------
# Save
# --------------------------------------------------

OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

claim_df.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8-sig"
)


# --------------------------------------------------
# Statistics
# --------------------------------------------------

print("=" * 60)
print("HINDI CLAIM-VERIFICATION WORKING DATASET")
print("=" * 60)

print("\nSource articles:")
print(len(df))

print("\nWorking dataset rows:")
print(len(claim_df))

print("\nColumns:")
print(claim_df.columns.tolist())

print("\nReview status:")
print(
    claim_df["review_status"].value_counts()
)

print("\nSaved to:")
print(OUTPUT)

print("\n" + "=" * 60)
print("DATASET CREATED")
print("=" * 60)