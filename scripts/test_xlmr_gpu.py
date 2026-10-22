import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


MODEL_NAME = "FacebookAI/xlm-roberta-base"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("=" * 60)
print("XLM-R GPU TEST")
print("=" * 60)

print("PyTorch:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
print("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU")


print("\nLoading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Tokenizer loaded.")


print("\nLoading XLM-R model...")

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=3
)

model.to(device)

print("Model loaded.")
print("Device:", device)


# Test sentence pair
claim = "The Earth revolves around the Sun."
evidence = "The Earth orbits the Sun once approximately every year."


inputs = tokenizer(
    claim,
    evidence,
    return_tensors="pt",
    truncation=True,
    max_length=256
)

inputs = {
    key: value.to(device)
    for key, value in inputs.items()
}


print("\nRunning inference...")

with torch.no_grad():

    outputs = model(**inputs)


print("Inference successful.")

print("Logits:", outputs.logits)

print("\nGPU memory allocated:")

if torch.cuda.is_available():

    print(
        round(
            torch.cuda.memory_allocated() / 1024**2,
            2
        ),
        "MB"
    )

print("\n" + "=" * 60)
print("XLM-R GPU TEST PASSED")
print("=" * 60)