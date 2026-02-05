import json

input_file = "data/scifact/queries.jsonl"
output_file = "data/scifact/test_queries_odd.tsv"

with open(input_file, "r", encoding="utf-8") as fin, \
     open(output_file, "w", encoding="utf-8") as fout:

    for line in fin:
        q = json.loads(line)
        qid = int(q["_id"])
        if qid % 2 == 1:  # odd queries only
            fout.write(f"{qid}\t{q['text']}\n")
