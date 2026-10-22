import json
from pathlib import Path
from collections import Counter

BASE = Path(__file__).resolve().parents[1]

file_path = (
    BASE
    / "data"
    / "raw"
    / "english"
    / "train.jsonl"
)

print("=" * 70)
print("FEVER ENGLISH DATASET INSPECTION")
print("=" * 70)

if not file_path.exists():
    print("\nERROR: FEVER file not found:")
    print(file_path)
    raise SystemExit(1)

labels = Counter()
total = 0
empty_evidence = 0
claims = []
sample_records = []

with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue

        record = json.loads(line)
        total += 1

        label = record.get("label")
        labels[label] += 1

        claim = record.get("claim", "")
        claims.append(claim)

        evidence = record.get("evidence")

        if not evidence:
            empty_evidence += 1

        if len(sample_records) < 5:
            sample_records.append(record)

print("\nTotal records:", total)

print("\nLabel distribution:")
for label, count in labels.items():
    print(f"{label}: {count}")

print("\nRecords without evidence:")
print(empty_evidence)

print("\nUnique claims:")
print(len(set(claims)))

print("\n" + "=" * 70)
print("SAMPLE RECORDS")
print("=" * 70)

for i, record in enumerate(sample_records, 1):
    print(f"\n--- SAMPLE {i} ---")
    print("ID:", record.get("id"))
    print("Claim:", record.get("claim"))
    print("Label:", record.get("label"))
    print("Evidence:", record.get("evidence"))

print("\n" + "=" * 70)
print("INSPECTION COMPLETE")
print("=" * 70)