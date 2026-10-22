from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "multilingual" / "multilingual_fake_news_final.csv"


def main():
    print("Loading final multilingual dataset...")
    df = pd.read_csv(DATA_PATH)

    X = df["text"].astype(str)
    y = df["label"]

    # Keep the test set completely unseen during training.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print(f"Training records: {len(X_train):,}")
    print(f"Test records:     {len(X_test):,}")

    model = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                analyzer="char",
                ngram_range=(2, 6),
                min_df=2,
                max_features=200000,
                sublinear_tf=True,
            ),
        ),
        (
            "clf",
            LogisticRegression(
                class_weight="balanced",
                max_iter=1500,
                solver="liblinear",
            ),
        ),
    ])

    print("\nTraining baseline model...")
    model.fit(X_train, y_train)

    print("\n========== OVERALL RESULTS ==========")

    predictions = model.predict(X_test)

    print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}")
    print()
    print(classification_report(y_test, predictions, digits=4))

    # Evaluate separately for each language.
    test_df = df.loc[X_test.index].copy()
    test_df["prediction"] = predictions

    print("\n========== LANGUAGE RESULTS ==========")

    for language in ["English", "Hindi", "Marathi"]:
        subset = test_df[test_df["language"] == language]

        if len(subset) == 0:
            continue

        accuracy = accuracy_score(
            subset["label"],
            subset["prediction"]
        )

        print(f"\n{language} ({len(subset):,} test records):")

        print(
            classification_report(
                subset["label"],
                subset["prediction"],
                digits=4
            )
        )


if __name__ == "__main__":
    main()