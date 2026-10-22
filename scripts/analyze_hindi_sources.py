import pandas as pd

FILE = "data/processed/hindi/hindi_clean.csv"

df = pd.read_csv(FILE)

print("=" * 70)
print("HINDI SOURCE BIAS ANALYSIS")
print("=" * 70)

# --------------------------------------------------
# Overall label distribution
# --------------------------------------------------

print("\nOverall labels:")
print(
    df["label"]
    .value_counts()
    .rename(index={
        0: "Authentic",
        1: "Fake"
    })
)

# --------------------------------------------------
# Source x Label table
# --------------------------------------------------

print("\nSource vs Label:")
print()

source_label = pd.crosstab(
    df["source_domain"],
    df["label"]
)

source_label = source_label.rename(
    columns={
        0: "Authentic",
        1: "Fake"
    }
)

print(source_label.sort_values(
    by=list(source_label.columns),
    ascending=False
).head(20))

# --------------------------------------------------
# Percentage of labels within each source
# --------------------------------------------------

print("\nLabel percentages within each source:")
print()

source_percentage = pd.crosstab(
    df["source_domain"],
    df["label"],
    normalize="index"
) * 100

source_percentage = source_percentage.rename(
    columns={
        0: "Authentic %",
        1: "Fake %"
    }
)

print(
    source_percentage
    .round(2)
    .sort_values(
        by="Fake %",
        ascending=False
    )
    .head(20)
)

# --------------------------------------------------
# Number of unique sources
# --------------------------------------------------

print("\nUnique source domains:")
print(df["source_domain"].nunique())

# --------------------------------------------------
# Label distribution by source
# --------------------------------------------------

print("\nTop sources with article counts:")

source_counts = (
    df["source_domain"]
    .value_counts()
    .head(20)
)

print(source_counts)

print("\nAnalysis complete.")