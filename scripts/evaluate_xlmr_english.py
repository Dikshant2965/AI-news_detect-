import os
import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix
)

MODEL_PATH = "models/xlmr_english/final"
TEST_PATH = "data/processed/english/splits/test.csv"

LABELS = {
    0: "NOT ENOUGH INFO",
    1: "REFUTES",
    2: "SUPPORTS"
}

print("=" * 60)
print("XLM-R ENGLISH MODEL EVALUATION")
print("=" * 60)

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"Device: {device}")

if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")

# Load test data
df = pd.read_csv(TEST_PATH)

print(f"Test samples: {len(df)}")

claims = df["claim"].fillna("").astype(str)
evidence = df["evidence"].fillna("").astype(str)

texts = (
    "Claim: " + claims
    + " Evidence: " + evidence
)


labels = df["verdict"].map({
    "NOT ENOUGH INFO": 0,
    "REFUTES": 1,
    "SUPPORTS": 2
}).values

# Load tokenizer and model
print("\nLoading model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)

model.to(device)
model.eval()

print("Model loaded successfully.")

# Prediction
predictions = []

print("\nRunning predictions...")

batch_size = 8

for i in range(0, len(texts), batch_size):

    batch_texts = [
    str(x) for x in texts.iloc[i:i + batch_size].tolist()
    ]

    encoded = tokenizer(
        batch_texts,
        padding=True,
        truncation=True,
        max_length=256,
        return_tensors="pt"
    )

    encoded = {
        key: value.to(device)
        for key, value in encoded.items()
    }

    with torch.no_grad():
        outputs = model(**encoded)

    batch_predictions = torch.argmax(
        outputs.logits,
        dim=1
    ).cpu().numpy()

    predictions.extend(batch_predictions)

    if (i // batch_size) % 100 == 0:
        print(f"Processed {min(i + batch_size, len(texts))}/{len(texts)}")

# Metrics
accuracy = accuracy_score(labels, predictions)

precision, recall, f1, _ = precision_recall_fscore_support(
    labels,
    predictions,
    average="macro",
    zero_division=0
)

print("\n" + "=" * 60)
print("RESULTS")
print("=" * 60)

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"Macro F1 : {f1:.4f}")

print("\n" + "=" * 60)
print("PER-CLASS RESULTS")
print("=" * 60)

print(
    classification_report(
        labels,
        predictions,
        target_names=[
            LABELS[0],
            LABELS[1],
            LABELS[2]
        ],
        digits=4,
        zero_division=0
    )
)

print("=" * 60)
print("CONFUSION MATRIX")
print("=" * 60)

cm = confusion_matrix(labels, predictions)

print("\nRows = Actual")
print("Columns = Predicted\n")

print("                 NEI   REFUTES   SUPPORTS")

for i, row in enumerate(cm):
    print(
        f"{LABELS[i]:15s}",
        row
    )

print("\nEvaluation complete.")