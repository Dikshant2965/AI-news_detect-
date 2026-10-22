import pandas as pd

# Load the current annotation file
file_path = "data/processed/hindi/hindi_manual_annotation_20.csv"
df = pd.read_csv(file_path)

# ID of the article we are annotating
target_id = "HIN_007879"

# Annotation for HIN_007879
df.loc[df["id"] == target_id, "claim"] = (
    "यह तस्वीर वाराणसी के गंगा किनारे की है और इसमें दिख रही इमारतें बनारस की हैं।"
)

df.loc[df["id"] == target_id, "evidence"] = (
    "गूगल रिवर्स इमेज सर्च से पता चला कि वायरल तस्वीर वाराणसी की नहीं, "
    "बल्कि दुबई के पाम जुमेराह की है। इसलिए तस्वीर को वाराणसी का बताने वाला दावा गलत है।"
)

df.loc[df["id"] == target_id, "verdict"] = "REFUTED"

df.loc[df["id"] == target_id, "evidence_source"] = (
    "Google reverse image search and fact-check investigation"
)

df.loc[df["id"] == target_id, "review_notes"] = (
    "The viral image was claimed to show a view of Varanasi, "
    "but the fact-check traced it to Palm Jumeirah in Dubai. "
    "The image has no connection to Varanasi."
)

df.loc[df["id"] == target_id, "review_status"] = "reviewed"

# Save the updated file
df.to_csv(file_path, index=False, encoding="utf-8-sig")

print(f"Updated {target_id} successfully.")