"""
Fusion layer for combining AI predictions and external fact-check results.
"""



def claims_match(submitted_claim: str, checked_claim: str) -> bool:
    """Require meaningful overlap between the submitted and checked claims."""
    import re

    stop_words = {
        "the", "is", "a", "an", "and", "or", "of", "to", "in",
        "on", "for", "with", "was", "were", "are", "has", "have",
        "had", "that", "this", "it", "did", "not", "no", "as",
        "by", "from", "at", "who", "which", "about", "after",
        "और", "का", "की", "के", "है", "हैं", "था", "थे", "को",
        "में", "पर", "से", "यह", "कि", "ने", "आणि", "आहे",
        "आहेत", "होते", "होती", "चा", "ची", "चे", "मध्ये", "वर",
        "यांनी", "की"
    }

    def words(text):
        return {
            token for token in re.findall(
                r"[^\W_]+", (text or "").lower(), flags=re.UNICODE
            )
            if len(token) > 1 and token not in stop_words
        }

    submitted_words = words(submitted_claim)
    checked_words = words(checked_claim)

    if not submitted_words or not checked_words:
        return False

    overlap = submitted_words & checked_words

# Reject claims that share the subject and location but
# describe a different action or event.
    if "born" in submitted_words and "born" not in checked_words:
        return False

    similarity = len(overlap) / len(submitted_words)

    # Require at least half of the submitted claim's key terms.
    return len(overlap) >= min(2, len(submitted_words)) and similarity >= 0.5

   


def normalize_rating(rating: str) -> str:
    if not rating:
        return ""

    value = rating.strip().lower()
    value = value.rstrip(".")

    if (
        value in {
            "false", "mostly false", "incorrect", "inaccurate",
            "false claim", "pants on fire", "tragically false",
        }
        or value.startswith("false.")
        or value.startswith("mostly false")
        or value.startswith("incorrect.")
        or value.startswith("inaccurate.")
    ):
        return "REFUTED"

    if value in {
        "true", "mostly true", "correct", "accurate",
        "true claim",
    }:
        return "SUPPORTED"

    if value in {
        "misleading", "missing context", "out of context",
        "partly false", "partly true", "half true",
        "mixture", "mixed",
    }:
        return "MISLEADING"

    return "UNKNOWN"

def calculate_confidence(
    verdict,
    model_prediction=None,
    supported=0,
    refuted=0,
    misleading=0,
    total=0
):
    # Preserve the confidence supplied by a built-in rule.
    if (
        model_prediction
        and model_prediction.get("source") == "Built-in knowledge rule"
    ):
        return (
            float(model_prediction.get("confidence", 1.0)) * 100,
            "built-in knowledge rule confidence",
        )

    # For conflicting or unverified assessments, do not
    # invent a combined confidence score.
    if verdict in {
        "CONFLICTING RESULTS",
        "CONFLICTING EVIDENCE",
        "INSUFFICIENT EVIDENCE",
        "INSUFFICIENT EVIDENCE TO ASSESS",
        "NOT YET VERIFIED — MODEL PREDICTS REAL",
        "NOT YET VERIFIED — MODEL PREDICTS FAKE",
    }:
        return 0.0, "no combined confidence calculated"

    # Report external fact-check agreement only for
    # a verdict that agrees with the evidence.
    if total > 0:
        if verdict == "LIKELY FALSE":
            return round((refuted / total) * 100, 1), "fact-check agreement"

        if verdict == "LIKELY TRUE":
            return round((supported / total) * 100, 1), "fact-check agreement"

        if verdict == "MISLEADING":
            return round((misleading / total) * 100, 1), "fact-check agreement"

    # If no usable fact-check result exists, use the
    # model probability when the model provides one.
    probabilities = (
        model_prediction.get("probabilities", {})
        if model_prediction else {}
    )

    if probabilities:
        highest = max(float(value) for value in probabilities.values())
        return round(highest * 100, 1), "AI model probability"

    return 0.0, "insufficient evidence"



def assess_news_evidence(
    news_sources: list[dict],
    submitted_claim: str = ""
) -> dict:
    """Report article text availability without treating it as proof."""

    articles_with_text = [
        item for item in news_sources
        if len((item.get("text") or "").split()) >= 80
    ]

    submitted_text_available = len((submitted_claim or "").split()) >= 80

    articles_examined = len(articles_with_text)

    if submitted_text_available:
        articles_examined += 1

    if articles_examined == 0:
        return {
            "result": "UNVERIFIED",
            "articles_examined": 0,
            "reason": (
                "No accessible article text was available for a "
                "meaningful evidence assessment."
            ),
        }

    return {
        "result": "UNVERIFIED",
        "articles_examined": articles_examined,
        "reason": (
            "Article text is available, but its contents have not yet "
            "been independently assessed against reliable evidence."
        ),
    }



def analyze(
    model_prediction=None,
    fact_checks=None,
    news_sources=None,
    submitted_claim=""
):
    
    fact_checks = fact_checks or []
    news_sources = news_sources or []
    
    # Assess news coverage separately from formal fact-checks.
    news_assessment = assess_news_evidence(
    news_sources,
    submitted_claim
)


    normalized = []

    # Keep only fact-checks that match the submitted claim.
    for item in fact_checks:
        checked_claim = str(item.get("claim", ""))

        if not claims_match(submitted_claim, checked_claim):
            continue
        print(
            "DEBUG MATCHED FACT-CHECK:",
            repr(checked_claim),
            "| rating:",
            repr(item.get("rating")),
            "| publisher:",
            repr(item.get("publisher"))
        )

        normalized.append({
            "claim": checked_claim,
            "publisher": item.get("publisher"),
            "rating": item.get("rating"),
            "normalized_rating": normalize_rating(
                item.get("rating", "")
            ),
            "url": item.get("url"),
        })

    supported = sum(
        1 for item in normalized
        if item["normalized_rating"] == "SUPPORTED"
    )

    refuted = sum(
        1 for item in normalized
        if item["normalized_rating"] == "REFUTED"
    )

    misleading = sum(
        1 for item in normalized
        if item["normalized_rating"] == "MISLEADING"
    )


    
           # Normalize the model prediction.
    model_verdict = str(
        model_prediction.get("verdict", "")
        if model_prediction else ""
    ).strip().upper()

    if model_verdict not in {"REAL", "FAKE"}:
        model_verdict = "UNKNOWN"

    # Count fact-check results with unrecognized ratings.
    unknown = sum(
        1 for item in normalized
        if item["normalized_rating"] == "UNKNOWN"
    )

    # Assess fact-check evidence independently.
    if refuted > 0 and supported > 0:
        evidence_result = "MIXED"
    elif refuted > 0:
        evidence_result = "REFUTES"
    elif supported > 0:
        evidence_result = "SUPPORTS"
    elif misleading > 0:
        evidence_result = "MISLEADING"
    elif unknown > 0:
        evidence_result = "UNKNOWN"
    else:
        evidence_result = "NO RELEVANT EVIDENCE"

    
    # Evidence-first verdict: the model cannot verify a claim by itself.
    if evidence_result == "MIXED":
        final_verdict = "UNVERIFIED — CONFLICTING FACT-CHECKS"

    elif evidence_result == "MISLEADING":
        final_verdict = "MISLEADING"

    elif evidence_result == "REFUTES":
        final_verdict = "LIKELY FALSE"

    elif evidence_result == "SUPPORTS":
        final_verdict = "LIKELY TRUE"

    else:
        final_verdict = "UNVERIFIED"



        # News coverage is separate from fact-check evidence.
    news_source_count = len(news_sources)

    if news_source_count > 0:
        news_coverage = "NEWS RESULTS FOUND — RELEVANCE NOT VERIFIED"
    else:
        news_coverage = "NO NEWS RESULTS FOUND"

    news_publishers = []

    for item in news_sources:
        publisher = item.get("publisher")

        if publisher and publisher not in news_publishers:
            news_publishers.append(publisher)

    confidence, confidence_source = calculate_confidence(
        verdict=final_verdict,
        model_prediction=model_prediction,
        supported=supported,
        refuted=refuted,
        misleading=misleading,
        total=len(normalized)
    )

    return {
        "verdict": final_verdict,
        "evidence_result": evidence_result,
        "news_coverage": news_coverage,
        "news_assessment": news_assessment,

        "confidence": confidence,

        "confidence_source": confidence_source,

        "signals": {
            "model_available": model_prediction is not None,

            "model_verdict": (
                model_prediction.get("verdict")
                if model_prediction
                else None
            ),

            "fact_check_results": len(normalized),

            "fact_check_refuted": refuted,

            "fact_check_supported": supported,

            "fact_check_misleading": misleading,

            "fact_check_unknown": unknown,

            "news_sources": news_source_count,
        },

        "fact_check_summary": {
            "supported": supported,
            "refuted": refuted,
            "misleading": misleading,
            "total": len(normalized),
        },

                "model_prediction": model_prediction,

        "fact_checks": normalized,

        "news_sources": news_sources,

        "news_summary": {
            "total_sources": news_source_count,
            "unique_publishers": len(news_publishers),
            "publishers": news_publishers,
        },
    }