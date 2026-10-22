import pandas as pd

# Load the current annotation file
file_path = "data/processed/hindi/hindi_manual_annotation_20.csv"
df = pd.read_csv(file_path)

# ID of the article we are annotating
target_id = "HIN_006576"

# Annotation for HIN_006576
df.loc[df["id"] == target_id, "claim"] = (
    "अमित शाह और ममता बनर्जी की यह तस्वीर बंगाल चुनाव को लेकर "
    "हुई हालिया मुलाकात की है और दोनों बंगाल चुनाव को लेकर मिले थे।"
)

df.loc[df["id"] == target_id, "evidence"] = (
    "इंडिया टुडे इस बात की पुष्टि नहीं कर सका कि मुलाकात के दौरान "
    "बंगाल चुनाव को लेकर कोई चर्चा हुई थी। हालांकि, जांच में स्पष्ट "
    "हुआ कि वायरल तस्वीर हाल-फिलहाल की नहीं बल्कि महीनों पुरानी है।"
)

df.loc[df["id"] == target_id, "verdict"] = "MISLEADING"

df.loc[df["id"] == target_id, "evidence_source"] = (
    "AFWA fact-check investigation"
)

df.loc[df["id"] == target_id, "review_notes"] = (
    "The fact-check could not confirm whether Amit Shah and Mamata Banerjee "
    "discussed the Bengal election during the meeting. However, it established "
    "that the viral photograph was several months old and was not a recent "
    "image related to the Bengal election."
)

df.loc[df["id"] == target_id, "review_status"] = "reviewed"

# Save the updated file
df.to_csv(file_path, index=False, encoding="utf-8-sig")

print(f"Updated {target_id} successfully.")