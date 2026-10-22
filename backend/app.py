

import re

from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv
from pathlib import Path
from core.language import detect_language
from core.extraction import from_url, from_txt, from_pdf, ExtractionError
from services.source_credibility import analyze as source_analyze
from services.evidence import EvidenceProvider
from services.fusion import analyze as fusion_analyze
from services.knowledge_rules import check_known_claim
from ml.fake_news_predict import predict_fake_news
load_dotenv()
ROOT = Path(__file__).resolve().parents[1]
app = Flask(__name__, static_folder=str(ROOT/"frontend"), static_url_path="")
evidence = EvidenceProvider()

@app.get("/")
def home(): return send_from_directory(ROOT/"frontend", "index.html")

@app.post("/api/analyze")
def analyze():
    try:
        data = request.get_json(silent=True) or {}
        text = (data.get("text") or "").strip()
        source_url = (data.get("url") or "").strip() or None
        evidence_text = (data.get("evidence") or "").strip()
        article_downloaded = False

        if source_url:
            original_text = text

            try:
                fetched_text, meta = from_url(source_url)

                if fetched_text and fetched_text.strip():
                    text = fetched_text.strip()
                    article_downloaded = True
                else:
                    text = original_text
            except Exception as exc:
                if not original_text:
                    return jsonify({
                        "error": "This article could not be downloaded from the provided URL. Please paste the article headline or text instead."
                    }), 400

                meta = {}
                text = original_text
        else:
            meta = {}

        if not text:
            return jsonify({
                "error": "The article could not be downloaded. Please provide a headline or short snippet."
            }), 400

        lang = detect_language(text)
        source = source_analyze(source_url)
        # The baseline classifier is intentionally not called the final AI model yet.
        
        
        claims = [text[:1500]]

        fact_check_query = (meta.get("title") or "").strip()
        if not fact_check_query:
            fact_check_query = re.split(
                r"(?<=[.!?])\s+", claims[0], maxsplit=1
            )[0].strip()

        fact_check_query = fact_check_query[:250]

        fact_checks = []
        news_sources = []
        wiki_evidence = []

        try:
            # Search the headline and several distinct article sentences.
            sentences = [
                sentence.strip()
                for sentence in re.split(r"(?<=[.!?])\s+", claims[0])
                if len(sentence.strip().split()) >= 6
            ]

            queries = []
            if fact_check_query:
                queries.append(fact_check_query)

            for sentence in sentences:
                query = sentence[:250]
                if query and query.lower() not in {
                    existing.lower() for existing in queries
                }:
                    queries.append(query)

                if len(queries) >= 5:
                    break

            combined_results = []
            seen = set()

            for query in queries:
                print("DEBUG FACT-CHECK QUERY:", query)

                for item in evidence.search(query):
                    result_key = (
                        item.get("url")
                        or (
                            item.get("claim", "").strip().lower(),
                            item.get("publisher", "").strip().lower()
                        )
                    )

                    if result_key not in seen:
                        seen.add(result_key)
                        combined_results.append(item)

                    if len(combined_results) >= 10:
                        break

                if len(combined_results) >= 10:
                    break

            fact_checks = combined_results[:10]
            if not fact_checks:
                print(
                    "No existing Google Fact Check results found; "
                    "using news coverage separately."
                )
                print("DEBUG FACT CHECKS:", fact_checks)

        except Exception as exc:
            print("Fact-check error:", exc)

        # Retrieve current news articles separately.
        # News articles are supporting context, not proof by themselves.
        try:
            news_sources = evidence.news_evidence(claims[0])[:8]
            print("DEBUG NEWS SOURCES:", len(news_sources))
        except Exception as exc:
            print("News retrieval error:", exc)



        # Baseline fake-news model for fallback/default prediction.
        fake_news_prediction = predict_fake_news(text)
        prediction = fake_news_prediction

        if lang.lower() in ["en", "english"]:
            known_claim = check_known_claim(claims[0])

            if known_claim:
                prediction = known_claim
            else:
                prediction = fake_news_prediction

        
        final_assessment = fusion_analyze(
            model_prediction=prediction,
            fact_checks=fact_checks,
            news_sources=news_sources,
            submitted_claim=claims[0]
        )


        return jsonify({
            "language": lang,
            "input": meta,
            "url": source_url,
            "article_downloaded": article_downloaded,
            "source": source,
            "claims": claims,
            "evidence": evidence_text,
            "fact_checks": fact_checks,
            "evidence_sources": wiki_evidence,
            "news_sources": news_sources,
            "baseline_prediction": fake_news_prediction,
            "prediction": prediction,
            "final_prediction": final_assessment.get("model_prediction", prediction),
            "assessment": final_assessment,
            "status": "FAKE_REAL_DETECTOR_ACTIVE",
        })

    except ExtractionError as exc:
        return jsonify({"error":str(exc)}), 400
    except Exception as exc:
        return jsonify({"error":str(exc)}), 500

@app.post("/api/upload")
def upload():
    f=request.files.get("file")
    if not f: return jsonify({"error":"No file supplied."}),400
    try:
        if f.filename.lower().endswith(".txt"): text,meta=from_txt(f.read())
        elif f.filename.lower().endswith(".pdf"): text,meta=from_pdf(f.read())
        else: return jsonify({"error":"Only TXT and PDF are supported."}),400
        return jsonify({"text":text,"metadata":meta,"language":detect_language(text)})
    except ExtractionError as exc: return jsonify({"error":str(exc)}),400

@app.get("/api/health")
def health(): return jsonify({"status":"ok","stage":"foundation"})

if __name__ == "__main__": app.run(host="127.0.0.1",port=5000,debug=True)
