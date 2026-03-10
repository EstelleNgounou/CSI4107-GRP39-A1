#beir_ranking.py
import beir
from beir.retrieval import models
from beir.retrieval.search.dense import DenseRetrievalExactSearch as DRES
from beir.reranking import Rerank
from beir.retrieval.evaluation import EvaluateRetrieval
import json
from ranking import BM25

def load_model(model_name, model_type, documents=None, inverted_index=None, doc_lengths=None):
    if model_type == "bm25":
        if documents is None or inverted_index is None or doc_lengths is None:
            raise ValueError("Documents, inverted_index, and doc_lengths are required for BM25.")
        return BM25(inverted_index, doc_lengths)
    elif model_type == "use":
        return DRES(models.SentenceBERT(model_name), batch_size=64)
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
def combine_scores(scores1, scores2, weight1=0.5, weight2=0.5):
    combined_scores = {}
    for doc_id in scores1:
        combined_scores[doc_id] = scores1[doc_id] * weight1
    for doc_id in scores2:
        if doc_id in combined_scores:
            combined_scores[doc_id] += scores2[doc_id] * weight2
        else:
            combined_scores[doc_id] = scores2[doc_id] * weight2
    return combined_scores

def rank_documents(documents, queries, model_name, bm25_model, top_k_bm25=1000):

    # Build corpus
    corpus = {}
    for doc in documents:
        corpus[doc['DOCNO']] = {
            "text": " ".join(doc['HEAD'] + doc['TEXT'])
        }

    # Build query dict
    query_dict = {query['num']: " ".join(query['title'] + query['query'] + query['narrative']) for query in queries}

    # Step 1: BM25 retrieval
    bm25_results = {}
    for query in queries:
        qid = query["num"]
        tokens = query["title"] + query["query"] + query["narrative"]
        ranked_docs = bm25_model.rank_documents(tokens)
        bm25_results[qid] = {
            doc_id: score for doc_id, score in ranked_docs[:top_k_bm25]
        }

    # Step 2: Dense retrieval over BM25 candidates only
    model = DRES(models.SentenceBERT(model_name), batch_size=64)
    retriever = EvaluateRetrieval(model, score_function="cos_sim")

    # Build a reduced corpus of only BM25 candidate docs (much faster than full corpus)
    candidate_corpus = {}
    for qid, doc_scores in bm25_results.items():
        for doc_id in doc_scores:
            if doc_id in corpus:
                candidate_corpus[doc_id] = corpus[doc_id]

    # Run dense retrieval over candidate corpus
    dense_results = retriever.retrieve(candidate_corpus, query_dict)

    # Step 3: Combine BM25 + dense scores (score fusion)
    combined_results = {}
    for qid in bm25_results:
        bm25_scores = bm25_results.get(qid, {})
        dense_scores = dense_results.get(qid, {})

        # Normalise BM25 scores to [0, 1]
        bm25_max = max(bm25_scores.values(), default=1)
        bm25_norm = {doc_id: score / bm25_max for doc_id, score in bm25_scores.items()}

        # cos_sim is in [-1, 1], shift to [0, 1]
        dense_norm = {doc_id: (score + 1) / 2 for doc_id, score in dense_scores.items()}

        combined_results[qid] = combine_scores(bm25_norm, dense_norm, weight1=0.4, weight2=0.6)

    return combined_results

def save_results(results, output_file, run_name="neural_run"):
    with open(output_file, "w") as f:
        for query_id, docs in results.items():
            
            # sort documents by score descending
            ranked_docs = sorted(docs.items(), key=lambda x: x[1], reverse=True)
            for rank, (doc_id, score) in enumerate(ranked_docs[:100], start=1):
                f.write(f"{query_id} Q0 {doc_id} {rank} {score:.6f} {run_name}\n")

# Example usage:
# corpus, queries, qrels = GenericDataLoader("scifact/").load(split="test")
# results = rank_documents(corpus, queries, model_name="msmarco-distilbert-base-tas-b", model_type="sentence-bert")
# save_results(results, "Results.json")
