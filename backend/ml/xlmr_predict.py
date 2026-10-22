import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification

ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT / "models" / "xlmr_english" / "final"

LABELS = {
    0: "NOT ENOUGH INFO",
    1: "REFUTES",
    2: "SUPPORTS"
}


class XLMRPredictor:
    def __init__(self):
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        print(f"Loading XLM-R from: {MODEL_PATH}")
        print(f"Using device: {self.device}")

        self.tokenizer = AutoTokenizer.from_pretrained(
            str(MODEL_PATH)
        )

        self.model = AutoModelForSequenceClassification.from_pretrained(
            str(MODEL_PATH)
        )

        self.model.to(self.device)
        self.model.eval()

        print("XLM-R loaded successfully.")

    def predict(self, claim, evidence=""):

        # Do not make a factual prediction without evidence.
        if not evidence.strip():
            return {
                "verdict": "NOT ENOUGH INFO",
                "confidence": 1.0,
                "probabilities": {
                    "NOT ENOUGH INFO": 1.0,
                    "REFUTES": 0.0,
                    "SUPPORTS": 0.0
                }
            }

        text = f"Claim: {claim} Evidence: {evidence}"

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=256
        )

        inputs = {
            key: value.to(self.device)
            for key, value in inputs.items()
        }

        with torch.no_grad():
            outputs = self.model(**inputs)

        probabilities = torch.softmax(
            outputs.logits,
            dim=-1
        )[0]

        predicted_id = int(
            torch.argmax(probabilities).item()
        )

        return {
            "verdict": LABELS[predicted_id],
            "confidence": round(
                float(probabilities[predicted_id].item()),
                4
            ),
            "probabilities": {
                LABELS[i]: round(
                    float(probabilities[i].item()),
                    4
                )
                for i in range(len(LABELS))
            }
        }


_predictor = None


def get_predictor():
    global _predictor

    if _predictor is None:
        _predictor = XLMRPredictor()

    return _predictor


def predict_english(claim, evidence=""):
    predictor = get_predictor()
    return predictor.predict(claim, evidence)