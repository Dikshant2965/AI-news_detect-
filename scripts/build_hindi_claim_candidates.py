import pandas as pd
import re
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = "data/processed/hindi/hindi_factcheck_sections.csv"

OUTPUT_FILE = (
    "data/processed/hindi/hindi_claim_candidates_auto_v2.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("Original articles:", len(df))


# ============================================================
# KEEP SUBSTANTIAL SECTIONS
# ============================================================

df["conclusion_section"] = (
    df["conclusion_section"]
    .fillna("")
    .astype(str)
    .str.strip()
)

candidates = df[
    df["conclusion_section"].str.len() >= 300
].copy()

print("Sections >= 300 characters:", len(candidates))


# ============================================================
# STRONG CONCLUSION PATTERNS
# ============================================================

# IMPORTANT:
# We deliberately use COMPLETE conclusion phrases.
# Words such as "सही", "सच", "पुष्टि" alone are NOT enough.

REFUTED_PATTERNS = [
    r"दावा\s+झूठा\s+है",
    r"दावा\s+गलत\s+है",
    r"दावा\s+भ्रामक\s+है",
    r"वायरल\s+पोस्ट\s+भ्रामक\s+है",
    r"वायरल\s+तस्वीर\s+गलत\s+है",
    r"वायरल\s+वीडियो\s+गलत\s+है",
    r"वायरल\s+खबर\s+गलत\s+है",
    r"कोई\s+सच्चाई\s+नहीं",
    r"दावे\s+में\s+कोई\s+सच्चाई\s+नहीं",
    r"दावे\s+में\s+सच्चाई\s+नहीं",
    r"दावा\s+झूठा\s+साबित",
    r"दावा\s+गलत\s+साबित",
    r"गलत\s+दावे\s+के\s+साथ\s+वायरल",
    r"फर्जी\s+बताकर",
    r"फर्जी\s+है",
    r"फोटोशॉप्ड\s+है",
    r"फोटोशॉप\s+किया\s+गया",
]


MISLEADING_PATTERNS = [
    r"दावा\s+भ्रामक\s+है",
    r"वायरल\s+पोस्ट\s+भ्रामक\s+है",
    r"वायरल\s+तस्वीर\s+भ्रामक\s+है",
    r"वायरल\s+वीडियो\s+भ्रामक\s+है",
    r"वायरल\s+खबर\s+भ्रामक\s+है",
    r"पोस्ट\s+भ्रामक\s+है",
    r"तस्वीर\s+भ्रामक\s+है",
    r"गलत\s+दावे\s+के\s+साथ\s+वायरल",
    r"भ्रामक\s+दावे\s+के\s+साथ\s+वायरल",
]


SUPPORTED_PATTERNS = [
    r"दावा\s+सही\s+है",
    r"दावा\s+सही\s+साबित\s+हुआ",
    r"दावा\s+सही\s+पाया\s+गया",
    r"वायरल\s+दावा\s+सही\s+है",
    r"वायरल\s+खबर\s+सही\s+है",
    r"वायरल\s+पोस्ट\s+सही\s+है",
]


# ============================================================
# FIND STRONGEST CONCLUSION
# ============================================================

def find_matches(text, patterns):

    matches = []

    for pattern in patterns:

        for match in re.finditer(
            pattern,
            text,
            flags=re.IGNORECASE
        ):
            matches.append({
                "phrase": match.group(),
                "position": match.start()
            })

    return matches


def detect_verdict(text):

    text = str(text)

    refuted = find_matches(
        text,
        REFUTED_PATTERNS
    )

    misleading = find_matches(
        text,
        MISLEADING_PATTERNS
    )

    supported = find_matches(
        text,
        SUPPORTED_PATTERNS
    )

    all_matches = []

    for match in refuted:
        all_matches.append(
            ("REFUTED", match)
        )

    for match in misleading:
        all_matches.append(
            ("MISLEADING", match)
        )

    for match in supported:
        all_matches.append(
            ("SUPPORTED", match)
        )

    # Nothing strong enough was found
    if not all_matches:
        return "", "", "none"

    # --------------------------------------------------------
    # If multiple categories are detected, do NOT guess.
    # --------------------------------------------------------

    categories = set(
        verdict for verdict, _ in all_matches
    )

    if len(categories) > 1:

        return (
            "",
            "",
            "conflict"
        )

    # Exactly one category
    verdict = all_matches[0][0]

    # Use the latest matching phrase because fact-check
    # conclusions are commonly toward the end.
    latest = max(
        all_matches,
        key=lambda item: item[1]["position"]
    )

    matched_phrase = latest[1]["phrase"]

    return (
        verdict,
        matched_phrase,
        "high"
    )


# ============================================================
# CLAIM CLEANING
# ============================================================

def clean_claim(title):

    title = str(title).strip()

    prefixes = [
        r"^फैक्ट\s*चेक\s*:\s*",
        r"^Fact\s*Check\s*:\s*",
        r"^FACT\s*CHECK\s*:\s*",
    ]

    for pattern in prefixes:
        title = re.sub(
            pattern,
            "",
            title,
            flags=re.IGNORECASE
        )

    return title.strip()


# ============================================================
# EVIDENCE EXTRACTION
# ============================================================

def extract_evidence(text):

    text = str(text).replace("\\n", "\n")

    markers = [
        "नतीजा",
        "नतीजे",
        "इसलिए",
        "पड़ताल में",
        "पड़ताल से",
        "जांच में",
        "जांच करने पर",
        "फैक्ट चेक में",
        "रिवर्स सर्च",
        "गूगल रिवर्स",
        "सर्च करने पर",
        "हमने पाया",
    ]

    positions = []

    for marker in markers:

        position = text.find(marker)

        if position != -1:
            positions.append(position)

    if not positions:
        return text[:1500].strip()

    # Start from the earliest useful investigation marker
    start = min(positions)

    evidence = text[start:start + 1500]

    return evidence.strip()


# ============================================================
# BUILD DATASET
# ============================================================

output_rows = []

for _, row in candidates.iterrows():

    text = row["conclusion_section"]

    verdict, matched_phrase, confidence = detect_verdict(
        text
    )

    claim = clean_claim(
        row["title"]
    )

    evidence = extract_evidence(
        text
    )

    output_rows.append({

        "id": row["id"],

        "title": row["title"],

        "source_domain":
            row["source_domain"],

        "source_url":
            row["source_url"],

        "claim_candidate":
            claim,

        "evidence_candidate":
            evidence,

        "verdict_candidate":
            verdict,

        "matched_conclusion_phrase":
            matched_phrase,

        "confidence":
            confidence,

        "review_status":
            "needs_manual_review",
    })


# ============================================================
# SAVE
# ============================================================

result = pd.DataFrame(
    output_rows
)

Path(
    OUTPUT_FILE
).parent.mkdir(
    parents=True,
    exist_ok=True
)

result.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# SUMMARY
# ============================================================

print("\n========================================")
print("HINDI CLAIM CANDIDATE DATASET V2")
print("========================================")

print(
    "Rows:",
    len(result)
)

print("\nVerdict candidates:")

print(
    result["verdict_candidate"]
    .replace("", "NO_VERDICT")
    .value_counts()
)

print("\nConfidence:")

print(
    result["confidence"]
    .value_counts()
)

print("\nSaved:")

print(
    OUTPUT_FILE
)