import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import joblib


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data" / "processed" / "english" / "splits"
MODEL_DIR = PROJECT_ROOT / "models" / "english_baseline"

MODEL_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Load datasets
# --------------------------------------------------

train_df = pd.read_csv(DATA_DIR / "train.csv")
val_df = pd.read_csv(DATA_DIR / "validation.csv")
test_df = pd.read_csv(DATA_DIR / "test.csv")

print("Train:", len(train_df))
print("Validation:", len(val_df))
print("Test:", len(test_df))


# --------------------------------------------------
# Combine claim + evidence
# --------------------------------------------------

def make_text(df):
    return (
        df["claim"].fillna("")
        + " [SEP] "
        + df["evidence"].fillna("")
    )


X_train = make_text(train_df)
X_val = make_text(val_df)
X_test = make_text(test_df)

y_train = train_df["verdict"]
y_val = val_df["verdict"]
y_test = test_df["verdict"]


# --------------------------------------------------
# TF-IDF
# --------------------------------------------------

print("\nCreating TF-IDF features...")

vectorizer = TfidfVectorizer(
    max_features=100000,
    ngram_range=(1, 2),
    min_df=2,
    sublinear_tf=True
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_val_tfidf = vectorizer.transform(X_val)
X_test_tfidf = vectorizer.transform(X_test)

print("Train TF-IDF shape:", X_train_tfidf.shape)
print("Validation TF-IDF shape:", X_val_tfidf.shape)
print("Test TF-IDF shape:", X_test_tfidf.shape)


# --------------------------------------------------
# Logistic Regression
# --------------------------------------------------

print("\nTraining Logistic Regression...")

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    n_jobs=-1
)

model.fit(X_train_tfidf, y_train)


# --------------------------------------------------
# Validation
# --------------------------------------------------

val_predictions = model.predict(X_val_tfidf)

print("\n" + "=" * 60)
print("VALIDATION RESULTS")
print("=" * 60)

print("Accuracy:", accuracy_score(y_val, val_predictions))

print(
    classification_report(
        y_val,
        val_predictions,
        digits=4
    )
)


# --------------------------------------------------
# Final test evaluation
# --------------------------------------------------

test_predictions = model.predict(X_test_tfidf)

print("\n" + "=" * 60)
print("FINAL TEST RESULTS")
print("=" * 60)

print("Accuracy:", accuracy_score(y_test, test_predictions))

print(
    classification_report(
        y_test,
        test_predictions,
        digits=4
    )
)


# --------------------------------------------------
# Save model
# --------------------------------------------------

joblib.dump(
    model,
    MODEL_DIR / "logistic_regression.joblib"
)

joblib.dump(
    vectorizer,
    MODEL_DIR / "tfidf_vectorizer.joblib"
)

print("\nModels saved to:")
print(MODEL_DIR)