# Multilingual AI Fake News Detection & Fact Verification

Final-year engineering project foundation for **English, Hindi and Marathi**.

## Target system
- Text, URL, TXT and PDF input
- Automatic English/Hindi/Marathi language detection
- Traditional ML baselines (TF-IDF + Logistic Regression/SVM/Naive Bayes)
- Multilingual transformer fine-tuning (XLM-R, with MuRIL/IndicBERT comparison)
- Claim extraction and evidence retrieval
- Fact-checking evidence integration
- Source credibility signals
- Explainable, claim-level results
- SQLite history and dashboard
- Deployable Flask application

## Important status
This repository is the **build foundation**, not the final trained research model yet. The supplied 150-row demo dataset is retained only for local development. It must not be presented as the final evaluation dataset.

The final dataset will be assembled from documented public research datasets and carefully curated Marathi/English/Hindi sources, with provenance, duplicate checks and a fixed train/validation/test split.

## Hardware target
Designed for the user's Windows 11 laptop with RTX 4050 6 GB VRAM and 16 GB RAM. Transformer training will use small batches, mixed precision where supported, gradient accumulation, and sequence-length controls.

## Suggested environment
Python 3.11 or 3.12 is recommended for the project environment.

## First run
```powershell
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
python backend/app.py
```
Then open http://127.0.0.1:5000

## Environment variables
Copy `.env.example` to `.env` and add API keys only when those modules are enabled.

## Research questions
1. How does a multilingual transformer compare with TF-IDF baselines across English, Hindi and Marathi?
2. Does adding evidence retrieval improve claim-level verification compared with text-only classification?
3. How does performance differ by language?
4. How do source-credibility signals affect the final explanation without being treated as proof of truth?
