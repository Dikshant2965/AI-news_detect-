import json
import csv
from pathlib import Path
from collections import defaultdict


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

FEVER_FILE = PROJECT_ROOT / "data" / "raw" / "english" / "train.jsonl"

WIKI_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "english"
    / "wiki-pages"
    / "wiki-pages"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "english"
OUTPUT_FILE = OUTPUT_DIR / "english_claim_verification.csv"


# ============================================================
# SETTINGS
# ============================================================

# Start with a smaller number so we can test everything safely.
# Once confirmed, we can process the full dataset.
MAX_CLAIMS = None


# ============================================================
# STEP 1: LOAD FEVER CLAIMS
# ============================================================

print("=" * 60)
print("STEP 1: Loading FEVER claims")
print("=" * 60)

claims = []

with FEVER_FILE.open("r", encoding="utf-8") as f:

    for line in f:

        if not line.strip():
            continue

        record = json.loads(line)

        claims.append(record)

        if MAX_CLAIMS is not None and len(claims) >= MAX_CLAIMS:
         break


print(f"Loaded claims: {len(claims)}")


# ============================================================
# STEP 2: EXTRACT REQUIRED WIKIPEDIA PAGE IDS
# ============================================================

print("\n" + "=" * 60)
print("STEP 2: Extracting required Wikipedia pages")
print("=" * 60)


# Map:
#
# Wikipedia page ID
#       ↓
# required sentence numbers
#
# Example:
#
# Nikolaj_Coster-Waldau -> {7}
# Fox_Broadcasting_Company -> {0}

required_pages = defaultdict(set)


for record in claims:

    evidence_groups = record.get("evidence", [])

    for group in evidence_groups:

        for evidence_item in group:

            if len(evidence_item) < 4:
                continue

            page_id = evidence_item[2]
            sentence_id = evidence_item[3]

            required_pages[page_id].add(sentence_id)


print(f"Unique Wikipedia pages required: {len(required_pages)}")


# ============================================================
# STEP 3: SCAN WIKIPEDIA FILES
# ============================================================

print("\n" + "=" * 60)
print("STEP 3: Scanning Wikipedia dump")
print("=" * 60)

wiki_sentences = {}

wiki_files = sorted(WIKI_DIR.glob("wiki-*.jsonl"))

print(f"Wikipedia files found: {len(wiki_files)}")


for file_index, wiki_file in enumerate(wiki_files, start=1):

    print(
        f"Processing file {file_index}/{len(wiki_files)}: "
        f"{wiki_file.name}"
    )

    with wiki_file.open("r", encoding="utf-8") as f:

        for line in f:

            if not line.strip():
                continue

            try:
                page = json.loads(line)
            except json.JSONDecodeError:
                continue

            page_id = page.get("id")

            if page_id not in required_pages:
                continue

            required_sentence_ids = required_pages[page_id]

            lines = page.get("lines", "")

            for line_data in lines.splitlines():

                parts = line_data.split("\t", 1)

                if len(parts) != 2:
                    continue

                try:
                    sentence_id = int(parts[0])
                except ValueError:
                    continue

                if sentence_id in required_sentence_ids:

                    wiki_sentences[
                        (page_id, sentence_id)
                    ] = parts[1]


print(f"Evidence sentences found: {len(wiki_sentences)}")


# ============================================================
# STEP 4: BUILD CLAIM + EVIDENCE DATASET
# ============================================================

print("\n" + "=" * 60)
print("STEP 4: Building claim verification dataset")
print("=" * 60)

rows = []


for record in claims:

    claim_id = record.get("id")
    claim = record.get("claim", "")
    label = record.get("label", "")

    evidence_sentences = []

    # FEVER may contain multiple evidence groups.
    # We collect all available evidence sentences.

    for group in record.get("evidence", []):

        group_sentences = []

        for evidence_item in group:

            if len(evidence_item) < 4:
                continue

            page_id = evidence_item[2]
            sentence_id = evidence_item[3]

            sentence = wiki_sentences.get(
                (page_id, sentence_id)
            )

            if sentence:

                group_sentences.append(
                    f"[{page_id}] {sentence}"
                )

        if group_sentences:

            evidence_sentences.extend(group_sentences)

    # Remove duplicates while preserving order.

    unique_evidence = list(
        dict.fromkeys(evidence_sentences)
    )

    evidence_text = " ".join(unique_evidence)

    rows.append(
        {
            "id": claim_id,
            "claim": claim,
            "evidence": evidence_text,
            "verdict": label,
            "language": "en"
        }
    )


# ============================================================
# STEP 5: SAVE CSV
# ============================================================

print("\n" + "=" * 60)
print("STEP 5: Saving dataset")
print("=" * 60)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


with OUTPUT_FILE.open(
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "id",
            "claim",
            "evidence",
            "verdict",
            "language"
        ]
    )

    writer.writeheader()

    writer.writerows(rows)


# ============================================================
# STEP 6: SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)

print(f"Output file:")
print(OUTPUT_FILE)

print(f"\nRows created: {len(rows)}")

print("\nVerdict distribution:")

counts = defaultdict(int)

for row in rows:
    counts[row["verdict"]] += 1

for verdict, count in counts.items():

    print(
        f"  {verdict}: {count}"
    )


print("\nRows with evidence:")

rows_with_evidence = sum(
    1
    for row in rows
    if row["evidence"].strip()
)

print(
    f"  {rows_with_evidence}/{len(rows)}"
)

print("\nFirst 3 records:\n")

for row in rows[:3]:

    print("-" * 60)

    print("ID:", row["id"])

    print("Claim:", row["claim"])

    print("Verdict:", row["verdict"])

    print("Evidence:", row["evidence"][:1000])