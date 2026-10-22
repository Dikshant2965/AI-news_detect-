# Final Project Specification

## Final label space
The user-facing system will report one of:
- Likely True
- Likely False
- Partially Supported / Mixed Evidence
- Misleading
- Insufficient Evidence

The ML classifier itself remains a binary fake/real model in the first research experiment. The richer user-facing labels are produced by combining classifier output with claim-level evidence and source signals.

## Final model study
1. TF-IDF + Naive Bayes
2. TF-IDF + Logistic Regression
3. TF-IDF + Linear SVM
4. XLM-RoBERTa-base
5. MuRIL-base-cased
6. IndicBERT (where access and compatibility permit)

The best model is selected from measured validation/test results; it is not predetermined.

## Target dataset accounting
We will report the exact final counts after acquisition and deduplication. We will not claim a target count as if it already exists.

Every record will have at minimum:
- id
- text
- title (if available)
- language
- label
- source_url (if legally/publicly usable)
- publisher
- publication_date (if available)
- dataset_source
- license/provenance note

## Split
Initial research protocol: approximately 70% train / 15% validation / 15% test, stratified by language and label. Duplicate/near-duplicate and translated leakage will be checked before splitting.

## Fact verification
The evidence layer will retrieve externally available fact-check/evidence records. It will never manufacture a citation. If evidence cannot be retrieved, the system reports insufficient evidence rather than treating absence as proof of falsehood.

## Privacy
User submissions are not required to be stored. If history is enabled, the UI will provide an explicit choice and the database will store only what the user elects to retain.
