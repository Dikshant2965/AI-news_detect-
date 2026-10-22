import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw/hindi")

files = {
    "AUTHENTIC": DATA_DIR / "authentic.xlsx",
    "FAKE": DATA_DIR / "fake.xlsx",
}

for label, file_path in files.items():

    print("\n" + "=" * 70)
    print(f"{label} DATASET")
    print("=" * 70)

    df = pd.read_excel(file_path)

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    print(list(df.columns))

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nFirst 3 rows:")
    print(df.head(3).to_string())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\nData types:")
    print(df.dtypes)