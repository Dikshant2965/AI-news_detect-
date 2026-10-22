import pandas as pd
import re
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = (
    "data/processed/hindi/"
    "hindi_factcheck_sections.csv"
)

OUTPUT_FILE = (
    "data/processed/hindi/"
    "hindi_claim_candidates_auto_v3.csv"
)


# ============================================================
# LOAD
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("Original articles:", len(df))


# ============================================================
# CLEAN TEXT
# ============================================================

df["conclusion_section"] = (
    df["conclusion_section"]
    .fillna("")
    .astype(str)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)


# Keep reasonably substantial sections
df = df[
    df["conclusion_section"].str.len() >= 300
].copy()

print(
    "Sections >= 300 characters:",
    len(df)
)


# ============================================================
# CONCLUSION PATTERNS
# ============================================================

REFUTED_PATTERNS = [

    # Explicit false/fake conclusions
    r"दावा\s+झूठा\s+है",
    r"दावा\s+गलत\s+है",
    r"दावा\s+फर्जी\s+है",
    r"दावा\s+झूठा\s+साबित",
    r"दावा\s+गलत\s+साबित",

    r"दावा\s+गलत\s+पाया\s+गया",
    r"दावा\s+गलत\s+पाया\s+गई",

    r"पोस्ट\s+फर्जी\s+पाई\s+गई",
    r"पोस्ट\s+फर्जी\s+पाया\s+गया",

    r"वायरल\s+पोस्ट\s+फर्जी",
    r"वायरल\s+खबर\s+फर्जी",

    r"कोई\s+सच्चाई\s+नहीं",
    r"इस\s+दावे\s+में\s+कोई\s+सच्चाई\s+नहीं",

    r"साफ\s+है\s+कि.*गलत",
    r"स्पष्ट\s+है\s+कि.*गलत",

    r"दावा\s+सही\s+नहीं\s+है",
]


MISLEADING_PATTERNS = [

    r"दावा\s+भ्रामक\s+है",

    r"वायरल\s+पोस्ट\s+भ्रामक\s+है",

    r"वायरल\s+तस्वीर\s+भ्रामक\s+है",

    r"वायरल\s+वीडियो\s+भ्रामक\s+है",

    r"वायरल\s+खबर\s+भ्रामक\s+है",

    r"पोस्ट\s+भ्रामक\s+है",

    r"तस्वीर\s+भ्रामक\s+है",

    r"वीडियो\s+भ्रामक\s+है",

    r"वायरल.*दावा\s+भ्रामक\s+है",

    r"गलत\s+दावे\s+के\s+साथ\s+वायरल",

    r"भ्रामक\s+दावे\s+के\s+साथ\s+वायरल",
]


SUPPORTED_PATTERNS = [

    # Deliberately very strict
    r"दावा\s+सही\s+है",

    r"दावा\s+सही\s+साबित\s+हुआ",

    r"दावा\s+सही\s+पाया\s+गया",

    r"वायरल\s+दावा\s+सही\s+है",

    r"वायरल\s+पोस्ट\s+सही\s+है",

    r"वायरल\s+खबर\s+सही\s+है",
]


# ============================================================
# FIND CONCLUSION PHRASE
# ============================================================

def find_pattern_matches(text, patterns):

    matches = []

    for pattern in patterns:

        for match in re.finditer(
            pattern,
            text,
            flags=re.IGNORECASE
        ):

            matches.append({
                "phrase": match.group(),
                "start": match.start(),
                "end": match.end()
            })

    return matches


# ============================================================
# GET SENTENCE AROUND MATCH
# ============================================================

def get_context_sentence(text, start, end):

    # Hindi/English sentence boundaries
    sentence_pattern = r"[।!?]"

    left_candidates = [
        m.end()
        for m in re.finditer(
            sentence_pattern,
            text[:start]
        )
    ]

    if left_candidates:
        left = left_candidates[-1]
    else:
        left = max(0, start - 250)

    right_match = re.search(
        sentence_pattern,
        text[end:]
    )

    if right_match:
        right = end + right_match.end()
    else:
        right = min(
            len(text),
            end + 300
        )

    sentence = text[left:right].strip()

    return sentence


# ============================================================
# DETECT VERDICT
# ============================================================

def detect_verdict(text):

    refuted = find_pattern_matches(
        text,
        REFUTED_PATTERNS
    )

    misleading = find_pattern_matches(
        text,
        MISLEADING_PATTERNS
    )

    supported = find_pattern_matches(
        text,
        SUPPORTED_PATTERNS
    )

    all_matches = []

    for item in refuted:
        all_matches.append(
            ("REFUTED", item)
        )

    for item in misleading:
        all_matches.append(
            ("MISLEADING", item)
        )

    for item in supported:
        all_matches.append(
            ("SUPPORTED", item)
        )

    if not all_matches:
        return "", "", "", "none"

    categories = set(
        item[0]
        for item in all_matches
    )

    # Conflicting explicit conclusions
    if len(categories) > 1:

        return (
            "",
            "",
            "",
            "conflict"
        )

    # Use the LAST conclusion occurrence
    verdict, match = max(
        all_matches,
        key=lambda item: item[1]["start"]
    )

    context = get_context_sentence(
        text,
        match["start"],
        match["end"]
    )

    return (
        verdict,
        match["phrase"],
        context,
        "high"
    )


# ============================================================
# CLEAN CLAIM
# ============================================================

def clean_claim(title):

    title = str(title).strip()

    title = re.sub(
        r"^\s*फैक्ट\s*चेक\s*:\s*",
        "",
        title,
        flags=re.IGNORECASE
    )

    title = re.sub(
        r"^\s*Fact\s*Check\s*:\s*",
        "",
        title,
        flags=re.IGNORECASE
    )

    title = re.sub(
        r"^\s*FACT\s*CHECK\s*:\s*",
        "",
        title,
        flags=re.IGNORECASE
    )

    return title.strip()


# ============================================================
# BUILD
# ============================================================

rows = []

for _, row in df.iterrows():

    text = row["conclusion_section"]

    (
        verdict,
        matched_phrase,
        conclusion_sentence,
        confidence
    ) = detect_verdict(text)

    claim = clean_claim(
        row["title"]
    )

    rows.append({

        "id":
            row["id"],

        "title":
            row["title"],

        "source_domain":
            row["source_domain"],

        "source_url":
            row["source_url"],

        "claim_candidate":
            claim,

        "conclusion_sentence":
            conclusion_sentence,

        "verdict_candidate":
            verdict,

        "matched_conclusion_phrase":
            matched_phrase,

        "confidence":
            confidence,

        "review_status":
            "needs_manual_review"
    })


result = pd.DataFrame(rows)


# ============================================================
# SAVE
# ============================================================

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
# REPORT
# ============================================================

print("\n========================================")
print("HINDI CLAIM CANDIDATE DATASET V3")
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