"""Traditional ML baseline for research comparison."""
from pathlib import Path
import json
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
import joblib

ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = ROOT / "backend" / "models"


def train(csv_path: str, output_name: str = "tfidf_logreg.joblib"):
    df = pd.read_csv(csv_path).dropna(subset=["text", "label"])
    df["label"] = df["label"].str.lower()
    train_df, test_df = train_test_split(df, test_size=0.15, random_state=42, stratify=df["label"])
    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1,2), min_df=2, sublinear_tf=True)),
        ("clf", LogisticRegression(max_iter=1500, class_weight="balanced")),
    ])
    pipe.fit(train_df.text, train_df.label)
    pred = pipe.predict(test_df.text)
    p, r, f1, _ = precision_recall_fscore_support(test_df.label, pred, average="weighted", zero_division=0)
    metrics = {"accuracy": accuracy_score(test_df.label,pred), "precision":p,"recall":r,"f1":f1,"test_rows":len(test_df), "report":classification_report(test_df.label,pred,zero_division=0,output_dict=True)}
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, MODEL_DIR/output_name)
    (MODEL_DIR/"baseline_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics

if __name__ == "__main__":
    import sys
    print(train(sys.argv[1] if len(sys.argv)>1 else str(ROOT/"data/raw/demo_train.csv")))
