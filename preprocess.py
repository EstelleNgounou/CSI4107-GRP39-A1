import json
import os

# input file for both 
input_file = "data/scifact/corpus.jsonl"

# first output file
output_dir_text = "data/scifact_title_text"
os.makedirs(output_dir_text, exist_ok=True)
output_file_text = os.path.join(output_dir_text, "corpus.jsonl")

# reads the original corpus file and creates a id-contents output file
with open(input_file, "r", encoding="utf-8") as fin, \
     open(output_file_text, "w", encoding="utf-8") as fout:

    # iterates over the line in the input file
    for line in fin:
        # reads the line
        doc = json.loads(line)
        
        # new line with id, title and text
        new_doc = {
            "id": doc["_id"],
            "contents": doc["title"] + " " + doc["text"]  # Title + Text
        }
        
        # writes to output file
        fout.write(json.dumps(new_doc) + "\n")

print(f"Created title+text corpus at: {output_file_text}")

# second output file
output_dir_title = "data/scifact_titles_only"
os.makedirs(output_dir_title, exist_ok=True)
output_file_title = os.path.join(output_dir_title, "corpus.jsonl")

# reads the original corpus file and creates a id-title output file
with open(input_file, "r", encoding="utf-8") as fin, \
     open(output_file_title, "w", encoding="utf-8") as fout:

    # iterates over the line in the input file
    for line in fin:
        doc = json.loads(line)
        
        # new line with id and title
        new_doc = {
            "id": doc["_id"],
            "contents": doc["title"]  # ONLY title
        }
        
        # writes to output file
        fout.write(json.dumps(new_doc) + "\n")

print(f"Created titles-only corpus at: {output_file_title}")
