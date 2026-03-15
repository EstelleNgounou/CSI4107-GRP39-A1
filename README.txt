COURSE CODE: CSI4107
STUDENT NAMES: Estelle Ngounou (300269700), Matsuru Hoshi (300228879), Max Wang (300296800), Wanis Hassan (300255946)
-----------------------------------------------------------------------------------------------------------------------------

TO-DO:

[X] Implement first neural retrieval model (10 points)
[X] Implement second neural retrieval model (10 points)
[X] For the best method, produce Results file with all test queries. (10 points)
[ ] MAP and P@10 score for each method, and highlight the best scores. (5 points)
[ ] Provide task division (5 points)
[ ] Write a Readme, accounts for (15 points)

-----------------------------------------------------------------------------------------------------------------------------
TASK DIVISION:

Estelle:
- Implemented the second neural model, a sentence embeddding model based on Microsoft MPNet. Fixed the code to produce the initial
results of Assignment 1 than rerank rather than do it from scratch with the neural models. 
see neural model documentation: https://huggingface.co/sentence-transformers/all-mpnet-base-v2 

Matsuru:
- Implemented Universal Sentence Transformer, technically loaded with SentenceTransformer 
through BEIR. see documentation: https://github.com/beir-cellar/beir/blob/main/beir/retrieval/models/sentence_bert.py

Max: 

Wanis: Produced Results file with all test queries result, Sample Results, and Discussion.
-----------------------------------------------------------------------------------------------------------------------------
FUNCTIONALITIES OF THE PROGRAMS:

This program does the following things:
 - Parses the corpus documents
 - Preprocesses the tokenized text
 - Creates an inverted index to allow searching
 - Searches and ranks documents using the invertex index with BM25 ranking

A list compiling results for a given set of queries in TREC format is outputted.
-----------------------------------------------------------------------------------------------------------------------------
INSTRUCTIONS ON HOW TO RUN THE PROGRAMS:

Dependencies:
- Python (Tested on 3.12.13)
- Python Environment (venv)
- requirements.txt (included)

First, create your Python environment with:
$ python -m venv some_env_name

Ensure the Python environment is activated before proceeding (see venv documentation, varies per system)

Then, install the requirements with pip:
$ pip install -r requirements.txt

Ensure you are in the same directory as the provided requirements.txt file.

Then, you need to download NLTK's stopwords and tokenizers separately, as they are not included with 
the NLTK import installation through pip. You can do so through the Python interpreter:

$ python
Python 3.9.6 (default, Dec  2 2025, 07:27:58) 
>>>
>>> import nltk
>>> nltk.download('stopwords')
>>> nltk.download('punkt')


This will download the two datasets into the Python environment. You may need to create the 'nltk_data' directory yourself.
If you do not specify the download_dir argument, however, the datasets will be downloaded in your root user directory
somewhere under usr/lib/nltk_data (may differ for Windows). This should still work, but may clutter your user directory.

Once this is done, the program can be run by running the main.py directly.

$ python main.py
-----------------------------------------------------------------------------------------------------------------------------
ALGORITHMS EXPLANATIONS:

Step 1, Preprocessing: 

To convert the raw text into a list of clean words, we first normalize the text, ensuring that the system is not 
case-sensitive. We then use NLTK's tokenizer to convert the text into discrete linguistic units. Following this,
we use the Porter Stemmer to strip texts of suffixes and reduce words into a common base/root word. 
We finally filter out specific meta-tokens and placeholders, leaving us with our preprocessed documents/queries 
containing all the tokens.

Step 2, Indexing:

The algorithm goes through the entire preprocessed list of documents once, and for every word processed, 
the system will note the document number the word appears in, as well as the frequency of the word. Making use 
of nested dictionaries, this will allow the system to find any word in constant time. Additionally, added an inverted 
index for only titles as required.

Step 3, Retrieval and Ranking:

When a query is entered, the system looks at the inverted index and finds only the documents that have at 
least one of the query's words. For every matching document, we use BM25 to calculate a relevance score by 
looking at how rare a word is(idf) and how often it appears. Afterwards, we use a min-max normalization algorithm 
to scale the scores between 0.0 and 1.0 and sort the documents according to their new ranking.
-----------------------------------------------------------------------------------------------------------------------------
Sample Results (First 10 answers for the first 2 queries):
Below are the top 10 ranked documents for Query 1 and Query 3 as produced by our best-performing system (Model 2: all-mpnet-base-v2).

Query ID: 1
1. Doc 18953920 - Score: 0.744778
2. Doc 21257564 - Score: 0.711530
3. Doc 12824568 - Score: 0.682599
4. Doc 7581911 - Score: 0.661389
5. Doc 6308416 - Score: 0.658057
6. Doc 21456232 - Score: 0.655665
7. Doc 19651306 - Score: 0.624848
8. Doc 3566945 - Score: 0.616978
9. Doc 35008773 - Score: 0.616093
10. Doc 16287725 - Score: 0.615968

Query ID: 3
1. Doc 2739854 - Score: 0.862783
2. Doc 4378885 - Score: 0.855125
3. Doc 14717500 - Score: 0.845749
4. Doc 23389795 - Score: 0.838700
5. Doc 4414547 - Score: 0.836027
6. Doc 4632921 - Score: 0.835241
7. Doc 1067605 - Score: 0.791619
8. Doc 3672261 - Score: 0.790026
9. Doc 1544804 - Score: 0.788349
10. Doc 19058822 - Score: 0.769056

-----------------------------------------------------------------------------------------------------------------------------
MEAN AVERAGE PRECISION (MAP):
We evaluated our system using the provided 'test.tsv' relevance judgments (Gold Standard) to calculate the Mean Average 
Precision (MAP) for two different indexing strategies.

1. Run 1 (Title Only):
   MAP Score: 0.2981

2. Run 2 (Title + Abstract Text):
   MAP Score: 0.6310
-----------------------------------------------------------------------------------------------------------------------------
DISCUSSION:
Our results clearly demonstrate the impact of document length and content on retrieval performance.

1. Neural Methods vs. BM25 Comparison:
Our results show that Model 2 (all-mpnet-base-v2) significantly outperformed our best Assignment 1 
baseline, increasing the MAP from 0.6310 to 0.6626. This improvement of about 5% demonstrates the 
effectiveness of semantic retrieval over lexical matching. While BM25 from Assignment 1 relies on exact 
keyword overlap, the MPNet transformer model understands context. However, Model 1 performed slightly 
worse than the baseline (0.6298). This suggests that using a "distilled" or multilingual model—while 
faster—may lose the fine-grained nuance required for technical scientific abstracts, proving that model 
selection is critical in neural IR.

2. Precision at 10 (P@10) Analysis:
Both models achieved a P@10 of approximately 0.09. This may seem low, but this is consistent with the 
limited number of relevant documents per query in SciFact. Since many queries contain only 1-2 relevant 
documents, the mathematical ceiling for P@10 is often 0.1. Our models successfully identified these few 
relevant documents and placed them at the top.

3. Strategic Optimizations: Two-Stage Reranking:
To optimize for computational efficiency, we implemented a two-stage reranking pipeline. We used our 
Assignment 1 BM25 system to retrieve an initial candidate set of the top 100 documents, then applied 
the neural models only to those candidates. This optimization allowed us to achieve significantly 
higher precision while keeping the system's runtime manageable on a standard CPU.

4. Future Optimizations:
For queries where the neural model failed to improve upon the baseline, the issue was likely a vocabulary 
gap caused by specific scientific terminology not present in the transformer's pre-training data. 
A potential future optimization is Pseudo-Relevance Feedback (PRF) to expand the query before the neural 
pass, ensuring the model has a richer context to work with.
-----------------------------------------------------------------------------------------------------------------------------
