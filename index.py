import os
import subprocess

# Set JAVA_HOME
os.environ["JAVA_HOME"] = r"C:\Program Files\Eclipse Adoptium\jdk-21.0.10.7-hotspot"

# Add Java bin to PATH
java_bin = r"C:\Program Files\Eclipse Adoptium\jdk-21.0.10.7-hotspot\bin"
os.environ["PATH"] = java_bin + os.pathsep + os.environ.get("PATH", "")

# Index 1: Titles only
cmd_titles = [
    "python", "-m", "pyserini.index.lucene",
    "--collection", "JsonCollection",
    "--input", "data/scifact_titles_only",  # Directory, not file
    "--index", "indexes/scifact_titles_only",
    "--generator", "DefaultLuceneDocumentGenerator",
    "--threads", "4",
    "--storePositions",
    "--storeDocvectors",
    "--storeRaw"
]

print("Indexing titles only...")
result = subprocess.run(cmd_titles, capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("Errors:", result.stderr)

# Index 2: Title + Text 
cmd_title_text = [
    "python", "-m", "pyserini.index.lucene",
    "--collection", "JsonCollection",
    "--input", "data/scifact_title_text",  # Directory, not file
    "--index", "indexes/scifact_title_text",
    "--generator", "DefaultLuceneDocumentGenerator",
    "--threads", "4",
    "--storePositions",
    "--storeDocvectors",
    "--storeRaw"
]

print("\nIndexing title + text...")
result = subprocess.run(cmd_title_text, capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("Errors:", result.stderr)

print("\nIndexing complete!")