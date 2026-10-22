import pandas as pd


INPUT_FILE = (
    "data/processed/hindi/"
    "hindi_fast_review_batch_01.csv"
)


df = pd.read_csv(INPUT_FILE)


print("\n" + "=" * 90)
print("HINDI FAST REVIEW — BATCH 01")
print("=" * 90)


for i, (_, row) in enumerate(df.iterrows(), start=1):

    print("\n" + "=" * 90)
    print(f"ARTICLE {i}/20")
    print("=" * 90)

    print(f"ID: {row['id']}")

    print(f"\nCLAIM:")
    print(row["claim_candidate"])

    print(f"\nAUTOMATIC VERDICT:")
    print(row["verdict_candidate"])

    print(f"\nCONCLUSION:")
    print(row["conclusion_sentence"])

    print(f"\nSOURCE:")
    print(row["source_domain_candidate"])

    print("\nREVIEW:")
    print("A = ACCEPT")
    print("C = CHANGE VERDICT")
    print("R = REJECT")