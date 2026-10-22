from pathlib import Path
import joblib


ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT / "backend" / "models" / "fake_news_pipeline.joblib"

_model = joblib.load(MODEL_PATH)


def predict_fake_news(text: str):
    text = (text or "").strip()

    if not text:
        return {
            "verdict": "UNKNOWN",
            "confidence": 0.0
        }

    prediction = _model.predict([text])[0]

    result = {
        "verdict": str(prediction),
        "confidence": None
    }

    if hasattr(_model, "predict_proba"):
        probabilities = _model.predict_proba([text])[0]
        classes = _model.classes_

        probability_map = {
            str(label): float(probability)
            for label, probability in zip(classes, probabilities)
        }

        result["probabilities"] = probability_map
        result["confidence"] = round(
            max(probability_map.values()) * 100,
            2
        )

    return result