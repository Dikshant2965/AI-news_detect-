"""Language detection for English, Hindi and Marathi."""

import re
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 42

# Common Hindi words/expressions
HINDI = {
    "है", "हैं", "और", "में", "का", "की", "के", "को",
    "नहीं", "किया", "कि", "बताया", "घोषणा", "होगा",
    "थे", "था", "यह", "एक", "से", "पर", "ने",
    "सरकार", "सभी", "नागरिकों", "रुपये", "मुफ्त",
    "देने", "दी", "दिया", "करने", "लिए"
}

# Common Marathi words/expressions
MARATHI = {
    "आहे", "आहेत", "आणि", "मध्ये", "म्हणाले", "सांगितले",
    "होणार", "करण्‍यात", "यांनी", "च्या", "ला", "नाही",
    "होते", "होता", "हे", "एक", "वर", "ने",
    "सरकारने", "सर्व", "नागरिकांना", "रुपये", "मोफत",
    "देण्याची", "केली", "आहे", "ही", "बातमी", "पाठवा"
}

ENGLISH = {
    "the", "is", "are", "was", "were", "and", "or", "of",
    "to", "in", "on", "for", "with", "this", "that", "a",
    "an", "contains", "contain", "news", "said", "has", "have"
}


def detect_language(text: str) -> str:
    text = (text or "").strip()

    if not text:
        return "English"

    # Extract Devanagari words.
    devanagari_words = re.findall(r"[\u0900-\u097F]+", text)

    if devanagari_words:
        words = set(devanagari_words)

        mr = len(words & MARATHI)
        hi = len(words & HINDI)

        # Strong Marathi indicators.
        if mr > hi:
            return "Marathi"

        # Strong Hindi indicators.
        if hi > mr:
            return "Hindi"

        # Check for Marathi-specific endings/patterns.
        marathi_patterns = [
            r"आहेत",
            r"आहे",
            r"आणि",
            r"ने$",
            r"ला$",
            r"च्या$",
            r"मध्ये",
            r"यांनी",
            r"देण्याची",
        ]

        hindi_patterns = [
            r"है$",
            r"हैं$",
            r"और",
            r"में$",
            r"का$",
            r"की$",
            r"के$",
            r"को$",
            r"नहीं",
            r"होगा",
        ]

        mr_pattern_score = sum(
            bool(re.search(pattern, word))
            for word in devanagari_words
            for pattern in marathi_patterns
        )

        hi_pattern_score = sum(
            bool(re.search(pattern, word))
            for word in devanagari_words
            for pattern in hindi_patterns
        )

        if mr_pattern_score > hi_pattern_score:
            return "Marathi"

        if hi_pattern_score > mr_pattern_score:
            return "Hindi"

        return "Hindi/Marathi"

    # Latin-script English detection.
    latin_words = set(
        re.findall(r"[A-Za-z]+", text.lower())
    )

    english_matches = len(latin_words & ENGLISH)

    if english_matches >= 1:
        return "English"

    try:
        code = detect(text)
    except Exception:
        return "English"

    if code == "en":
        return "English"

    return "English"
