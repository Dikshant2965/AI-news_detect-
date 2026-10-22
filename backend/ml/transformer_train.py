"""Fine-tune a multilingual transformer for binary fake-news classification.

Run only after the final curated dataset has been assembled.
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from datasets import Dataset
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from sklearn.metrics import accuracy_score, precision_recall_fscore_support


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--model", default="FacebookAI/xlm-roberta-base")
    ap.add_argument("--output", default="backend/models/transformer")
    ap.add_argument("--epochs", type=int, default=2)
    ap.add_argument("--batch-size", type=int, default=2)
    args = ap.parse_args()

    df = pd.read_csv(args.csv).dropna(subset=["text","label"]).copy()
    labels = {"fake":0,"real":1}
    df["labels"] = df.label.str.lower().map(labels)
    train_df, test_df = train_test_split(df, test_size=0.15, random_state=42, stratify=df.labels)
    train_df, val_df = train_test_split(train_df, test_size=0.17647, random_state=42, stratify=train_df.labels)  # ~15% total
    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForSequenceClassification.from_pretrained(args.model, num_labels=2, id2label={0:"FAKE",1:"REAL"}, label2id=labels)

    def tokenize(batch):
        return tok(batch["text"], truncation=True, max_length=384)
    tr = Dataset.from_pandas(train_df[["text","labels"]], preserve_index=False).map(tokenize, batched=True)
    va = Dataset.from_pandas(val_df[["text","labels"]], preserve_index=False).map(tokenize, batched=True)
    te = Dataset.from_pandas(test_df[["text","labels"]], preserve_index=False).map(tokenize, batched=True)
    tr.set_format("torch"); va.set_format("torch"); te.set_format("torch")

    def metrics(eval_pred):
        logits, y = eval_pred
        pred = np.argmax(logits, axis=-1)
        p,r,f,_ = precision_recall_fscore_support(y,pred,average="weighted",zero_division=0)
        return {"accuracy":accuracy_score(y,pred),"precision":p,"recall":r,"f1":f}

    out = Path(args.output)
    training = TrainingArguments(output_dir=str(out), num_train_epochs=args.epochs, per_device_train_batch_size=args.batch_size, per_device_eval_batch_size=args.batch_size, gradient_accumulation_steps=4, learning_rate=2e-5, weight_decay=0.01, eval_strategy="epoch", save_strategy="epoch", load_best_model_at_end=True, metric_for_best_model="f1", fp16=True, logging_steps=25, report_to="none")
    trainer = Trainer(model=model, args=training, train_dataset=tr, eval_dataset=va, processing_class=tok, compute_metrics=metrics)
    trainer.train()
    print("TEST METRICS:", trainer.evaluate(te))
    trainer.save_model(str(out)); tok.save_pretrained(str(out))

if __name__ == "__main__": main()
