import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

INPUT = "data/processed/hindi/hindi_translation_pilot_100.csv"
OUTPUT = "data/processed/hindi/hindi_translation_pilot_100_translated.csv"

MODEL_ID = "Helsinki-NLP/opus-mt-en-hi"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Loading translation model on {DEVICE}...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID).to(DEVICE)
model.eval()

df = pd.read_csv(INPUT)

def translate_batch(texts, batch_size=8):
    results = []

    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]

        inputs = tokenizer(
            batch,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        ).to(DEVICE)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=256
            )

        decoded = tokenizer.batch_decode(
            outputs,
            skip_special_tokens=True
        )

        results.extend(decoded)

        print(
            f"Translated {min(start + batch_size, len(texts))}/{len(texts)}"
        )

    return results


print("\nTranslating claims...")
df["claim_hi"] = translate_batch(df["claim"].fillna("").tolist())

print("\nTranslating evidence...")
df["evidence_hi"] = translate_batch(df["evidence"].fillna("").tolist())

df.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

print("\nTranslation complete.")
print(f"Saved: {OUTPUT}")
print(f"Rows: {len(df)}")

print("\nLabel distribution:")
print(df["verdict"].value_counts())

print("\nSample:")
print(df[["claim", "claim_hi", "verdict"]].head(3).to_string())