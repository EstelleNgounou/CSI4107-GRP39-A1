import json
import os

# ===== Title + Text =====
input_file = "data/scifact/corpus.jsonl"
output_dir_text = "data/scifact_title_text"
os.makedirs(output_dir_text, exist_ok=True)
output_file_text = os.path.join(output_dir_text, "corpus.jsonl")

with open(input_file, "r", encoding="utf-8") as fin, \
     open(output_file_text, "w", encoding="utf-8") as fout:

    for line in fin:
        doc = json.loads(line)
        
        new_doc = {
            "id": doc["_id"],
            "contents": doc["title"] + " " + doc["text"]  # Title + Text
        }
        
        fout.write(json.dumps(new_doc) + "\n")

print(f"Created title+text corpus at: {output_file_text}")

# ===== Titles Only =====
output_dir_title = "data/scifact_titles_only"
os.makedirs(output_dir_title, exist_ok=True)
output_file_title = os.path.join(output_dir_title, "corpus.jsonl")

with open(input_file, "r", encoding="utf-8") as fin, \
     open(output_file_title, "w", encoding="utf-8") as fout:

    for line in fin:
        doc = json.loads(line)
        
        new_doc = {
            "id": doc["_id"],
            "contents": doc["title"]  # ONLY title
        }
        
        fout.write(json.dumps(new_doc) + "\n")

print(f"Created titles-only corpus at: {output_file_title}")

# Verify they're different
print("\n=== Verification ===")
with open(output_file_text, "r") as f:
    sample_text = json.loads(f.readline())
    print(f"Title+Text sample (first 100 chars): {sample_text['contents'][:100]}")

with open(output_file_title, "r") as f:
    sample_title = json.loads(f.readline())
    print(f"Titles-only sample: {sample_title['contents']}")