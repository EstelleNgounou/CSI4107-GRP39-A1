import time
from parser import *
from preprocessing import *
from indexing import *
from ranking import *
from beir_ranking import rank_documents
import beir_ranking
from utils import *
import os

##################################################################################
# This program does the following things:
# - Parses the corpus documents
# - Preprocesses the tokenized text
# - Creates an inverted index to allow searching
# - Searches and ranks documents using the invertex index with BM25 ranking
#
# A list compiling results for a given set of queries in TREC format is outputted.
#
##################################################################################
# This program was adapted from Mark Revera's to work on the scifact dataset.
#
# Notable Changes:
# - Added some comments to clarify code
# - Added .tsv support for the queries 
#
##################################################################################

# path to existing dataset
dataset = "data/scifact"  # Change to dataset being used
doc_folder_path = dataset + '/corpus.jsonl'
query_file_path = dataset + '/test_queries_odd.tsv'

# names for files to be saved/created
index_file_path = 'inverted_index.json'
preprocessed_docs_path = 'preprocessed_documents.json'
preprocessed_queries_path = 'preprocessed_queries.json'

start_time = time.time()

print("Parsing documents")
documents = []
queries = parse_queries_from_file(query_file_path)

# Parse and preprocess documents
if os.path.exists(preprocessed_docs_path):
    print("Loading preprocessed documents")
    documents = load_preprocessed_data(preprocessed_docs_path)
else:
    print("Preprocessing documents")
    documents = parse_documents_from_file(doc_folder_path)
    documents = preprocess_documents(documents)
    save_preprocessed_data(documents, preprocessed_docs_path)

# Parse and preprocess queries
if os.path.exists(preprocessed_queries_path):
    print("Loading preprocessed queries")
    queries = load_preprocessed_data(preprocessed_queries_path)
else:
    print("Preprocessing queries")
    queries = preprocess_queries(parse_queries_from_file(query_file_path))
    save_preprocessed_data(queries, preprocessed_queries_path)

queries = sorted(queries, key=lambda q: int(q['num']))
start_time = time.time()

# Build or load inverted index
#TITLE ONLY
index_file_title = 'inverted_index_title.json'

if os.path.exists(index_file_title):
    inverted_index_title = load_inverted_index(index_file_title)
else:
    print("Building Title Only Inverted Index")
    start_time = time.time()
    inverted_index_title = build_inverted_index(documents, index_type = 'title_only')
    end_time = time.time()
    save_inverted_index(inverted_index_title,index_file_title)
    
doc_frequency = {word: len(docs) for word, docs in inverted_index_title.items()}
sorted_words = sorted(doc_frequency.items(), key=lambda item: item[1], reverse=True)
doc_lengths_title = calculate_document_lengths(documents)

# FULL DOCUMENT
index_file_full = 'inverted_index_full.json'

if os.path.exists(index_file_full):
    inverted_index_full = load_inverted_index(index_file_full)
else:
    print("Building Full Inverted Index")
    start_time = time.time()
    inverted_index_full = build_inverted_index(documents, index_type = 'full')
    end_time = time.time()
    save_inverted_index(inverted_index_full,index_file_full)

doc_frequency = {word: len(docs) for word, docs in inverted_index_full.items()}
sorted_words = sorted(doc_frequency.items(), key=lambda item: item[1], reverse=True)
#print("Sample of Most Frequent Tokens: " + str(sorted_words[:10]))

doc_lengths_full = calculate_document_lengths(documents)

beir_results = {}


#Run 1: Title Only
# print("RUN 1 - TITLE ONLY")  
# bm25_title = BM25(inverted_index_title, doc_lengths_title) 
# results_file_title = "Results_Title.txt"
# start_time = time.time()
# writeResults(results_file_title, queries, bm25_title, top_k=100)
# end_time = time.time()
# print(f" Ranking complete in {end_time - start_time:.2f} seconds")

# #Run 2: Full Text  
print("RUN 2 - FULL")
bm25_full = BM25(inverted_index_full, doc_lengths_title) 
results_file_title = "Results_Full.txt"
start_time = time.time()
writeResults(results_file_title, queries, bm25_full, top_k=100)
end_time = time.time()
print(f" Ranking complete in {end_time - start_time:.2f} seconds")
#model_name = "BeIR/sparta-msmarco-distilbert-base-v1"
#model_type = "sparta"

# model_name = "msmarco-distilbert-base-v3"
# model_type = "sentence-bert"

#First neural model 
model_name1 = "distiluse-base-multilingual-cased-v1"
model_type1 = "use"

start_time = time.time()
results_file1 = "Results_Model1.txt"
results1 = rank_documents(documents, queries, bm25_model=bm25_full, model_name=model_name1)  # Set rerank=True for Cross-Encoder models
end_time = time.time()
beir_ranking.save_results(results1, results_file1,"neural_run1")
print(f"\nTime taken to rank documents: {end_time - start_time:.2f} seconds")

print(f"Ranking results written to {results_file1}")

#Second neural model
model_name2 = "all-mpnet-base-v2"
model_type2 = "use"

start_time = time.time()
results_file2 = "Results_Model2.txt"
results2 = rank_documents(documents, queries, bm25_model=bm25_full,model_name=model_name2)  # Set rerank=True for Cross-Encoder models
end_time = time.time()
beir_ranking.save_results(results2, results_file2, "neural_run2")
print(f"\nTime taken to rank documents: {end_time - start_time:.2f} seconds")

print(f"Ranking results written to {results_file2}")