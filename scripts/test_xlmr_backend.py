import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.ml.xlmr_predict import predict_english


result = predict_english(
    "The Earth is the third planet from the Sun.",
    "Earth is the third planet from the Sun."
)

print("\n" + "=" * 60)
print("XLM-R BACKEND TEST")
print("=" * 60)

print("Verdict:", result["verdict"])
print("Confidence:", result["confidence"])
print("Probabilities:")

for label, probability in result["probabilities"].items():
    print(f"  {label}: {probability}")

print("=" * 60)