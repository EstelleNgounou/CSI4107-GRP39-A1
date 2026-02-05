import os
import subprocess

# -------------------------------
# Java environment
# -------------------------------
os.environ["JAVA_HOME"] = r"C:\Program Files\Eclipse Adoptium\jdk-21.0.10.7-hotspot"
java_bin = os.path.join(os.environ["JAVA_HOME"], "bin")
os.environ["PATH"] = java_bin + os.pathsep + os.environ.get("PATH", "")
os.environ["JPYPE_JVM_DLL"] = os.path.join(java_bin, "server", "jvm.dll")


# Experiments: only differ in the index
experiments = {
    "titles_only_index": "indexes/scifact_titles_only",
    "title_text_index": "indexes/scifact_title_text"
}

query_file = "data/scifact/test_queries_odd.tsv"  # same for both


# Run retrieval
for exp_name, index_path in experiments.items():
    cmd = [
        "python", "-m", "pyserini.search.lucene",
        "--index", index_path,             # <-- different index
        "--topics", query_file,            # <-- same queries
        "--output", f"results_{exp_name}.txt",
        "--bm25",
        "--hits", "100"
    ]

    print(f"\nRunning retrieval for {exp_name}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)

print("\nAll retrieval experiments completed!")
