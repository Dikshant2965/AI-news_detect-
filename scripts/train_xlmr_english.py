import pandas as pd
import numpy as np
import torch

from pathlib import Path
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding,
)
from sklearn.metrics import accuracy_score, precision_recall_fscore_support


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data" / "processed" / "english" / "splits"

OUTPUT_DIR = PROJECT_ROOT / "models" / "xlmr_english"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# SETTINGS
# ============================================================

MODEL_NAME = "FacebookAI/xlm-roberta-base"

LABELS = {
    "NOT ENOUGH INFO": 0,
    "REFUTES": 1,
    "SUPPORTS": 2,
}

ID_TO_LABEL = {
    0: "NOT ENOUGH INFO",
    1: "REFUTES",
    2: "SUPPORTS",
}


# ============================================================
# GPU CHECK
# ============================================================

print("=" * 60)
print("XLM-R ENGLISH TRAINING")
print("=" * 60)

print("PyTorch:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())

if torch.cuda.is_available():

    print(
        "GPU:",
        torch.cuda.get_device_name(0)
    )

    print(
        "GPU memory:",
        round(
            torch.cuda.get_device_properties(0).total_memory
            / 1024**3,
            2
        ),
        "GB"
    )

else:

    raise RuntimeError(
        "CUDA is not available. Stop training."
    )


# ============================================================
# LOAD DATA
# ============================================================

print("\nLoading datasets...")

train_df = pd.read_csv(
    DATA_DIR / "train.csv"
)

val_df = pd.read_csv(
    DATA_DIR / "validation.csv"
)

test_df = pd.read_csv(
    DATA_DIR / "test.csv"
)

print("Train:", len(train_df))
print("Validation:", len(val_df))
print("Test:", len(test_df))


# ============================================================
# PREPARE LABELS
# ============================================================

for df in [train_df, val_df, test_df]:

    df["label"] = df["verdict"].map(LABELS)


# ============================================================
# CREATE CLAIM + EVIDENCE TEXT
# ============================================================

def prepare_dataframe(df):

    result = pd.DataFrame()

    result["text"] = (
        "Claim: "
        + df["claim"].fillna("")
        + " Evidence: "
        + df["evidence"].fillna("")
    )

    result["label"] = df["label"].astype(int)

    return result


train_data = prepare_dataframe(train_df)
val_data = prepare_dataframe(val_df)
test_data = prepare_dataframe(test_df)


# ============================================================
# HUGGING FACE DATASETS
# ============================================================

train_dataset = Dataset.from_pandas(
    train_data,
    preserve_index=False
)

val_dataset = Dataset.from_pandas(
    val_data,
    preserve_index=False
)

test_dataset = Dataset.from_pandas(
    test_data,
    preserve_index=False
)


# ============================================================
# TOKENIZER
# ============================================================

print("\nLoading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)


def tokenize(batch):

    return tokenizer(
        batch["text"],
        truncation=True,
        max_length=256
    )


print("Tokenizing training data...")

train_dataset = train_dataset.map(
    tokenize,
    batched=True,
    batch_size=1000,
    remove_columns=["text"]
)

print("Tokenizing validation data...")

val_dataset = val_dataset.map(
    tokenize,
    batched=True,
    batch_size=1000,
    remove_columns=["text"]
)

print("Tokenizing test data...")

test_dataset = test_dataset.map(
    tokenize,
    batched=True,
    batch_size=1000,
    remove_columns=["text"]
)


# ============================================================
# MODEL
# ============================================================

print("\nLoading XLM-R model...")

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=3,
    id2label=ID_TO_LABEL,
    label2id=LABELS
)


# ============================================================
# DATA COLLATOR
# ============================================================

data_collator = DataCollatorWithPadding(
    tokenizer=tokenizer
)


# ============================================================
# METRICS
# ============================================================

def compute_metrics(eval_pred):

    predictions, labels = eval_pred

    predictions = np.argmax(
        predictions,
        axis=-1
    )

    accuracy = accuracy_score(
        labels,
        predictions
    )

    precision, recall, f1, _ = precision_recall_fscore_support(
        labels,
        predictions,
        average="macro",
        zero_division=0
    )

    return {
        "accuracy": accuracy,
        "macro_precision": precision,
        "macro_recall": recall,
        "macro_f1": f1,
    }


# ============================================================
# TRAINING ARGUMENTS
# ============================================================

training_args = TrainingArguments(

    output_dir=str(OUTPUT_DIR),

    num_train_epochs=1,

    per_device_train_batch_size=4,

    per_device_eval_batch_size=4,

    gradient_accumulation_steps=4,

    learning_rate=2e-5,

    weight_decay=0.01,

    fp16=True,

    eval_strategy="steps",

    eval_steps=1000,

    save_strategy="steps",

    save_steps=1000,

    save_total_limit=2,

    logging_steps=100,

    load_best_model_at_end=True,

    metric_for_best_model="macro_f1",

    greater_is_better=True,

    report_to="none",

    dataloader_num_workers=0,

    gradient_checkpointing=True,

)


# ============================================================
# TRAINER
# ============================================================

trainer = Trainer(

    model=model,

    args=training_args,

    train_dataset=train_dataset,

    eval_dataset=val_dataset,

    processing_class=tokenizer,

    data_collator=data_collator,

    compute_metrics=compute_metrics,
)


# ============================================================
# TRAIN
# ============================================================

print("\nStarting training...")

trainer.train()


# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("VALIDATION")
print("=" * 60)

validation_results = trainer.evaluate(
    eval_dataset=val_dataset
)

print(validation_results)


# ============================================================
# TEST
# ============================================================

print("\n" + "=" * 60)
print("FINAL TEST")
print("=" * 60)

test_results = trainer.evaluate(
    eval_dataset=test_dataset
)

print(test_results)


# ============================================================
# SAVE
# ============================================================

print("\nSaving model...")

trainer.save_model(
    OUTPUT_DIR / "final"
)

tokenizer.save_pretrained(
    OUTPUT_DIR / "final"
)

print("\n" + "=" * 60)
print("TRAINING COMPLETE")
print("=" * 60)

print("Model saved to:")
print(OUTPUT_DIR / "final")