COURSE CODE: CSI4107
STUDENT NAMES: Estelle Ngounou (300269700), Matsuru Hoshi (300228879), Max Wang (300296800), Wanis Hassan (300255946)
-----------------------------------------------------------------------------------------------------------------------------

TO-DO:

[X] Implement first neural retrieval model (10 points)
[ ] Implement second neural retrieval model (10 points)
[ ] For the best method, produce Results file with all test queries. (10 points)
[ ] MAP and P@10 score for each method, and highlight the best scores. (5 points)
[ ] Provide task division (5 points)
[ ] Write a Readme, accounts for (15 points)

-----------------------------------------------------------------------------------------------------------------------------
TASK DIVISION:

Estelle:

Matsuru:
- Implemented Universal Sentence Transformer, technically loaded with SentenceTransformer 
through BEIR. see documentation: https://github.com/beir-cellar/beir/blob/main/beir/retrieval/models/sentence_bert.py

Max: 

Wanis: 
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
SYSTEM STATS AND RESULTS:
1. Vocabulary Size:
   45088 unique tokens.

2. Sample of 100 Tokens:
   ['.', 'of', 'the', 'and', ',', 'in', 'to', 'a', ')', '(', 'that', 'for', 'with', 'is', 'by', 'we', 'are', 'thi', 
   'as', 'from', 'an', 'on', 'cell', 'these', 'wa', 'result', 'or', 'studi', 'be', 'were', 'use', 'have', 'at', 'not', 'which', 
   'it', 'activ', 'but', ':', 'show', 'increas', 'express', 'function', 'also', 'ha', 'between', 'protein', 'effect', 'suggest', 
   'associ', 'here', 'been', 'may', 'develop', 'role', '%', 'gene', 'factor', 'can', 'both', 'their', 'includ', 'human', 'control', 
   'regul', 'diseas', ';', 'mechan', 'respons', 'identifi', 'patient', 'howev', 'data', 'than', 'differ', 'our', 'level', 'conclus', 
   'dure', 'provid', 'method', 'more', 'model', 'other', 'compar', 'all', 'into', 'demonstr', 'analysi', 'after', 'treatment', 'import', 
   'find', 'requir', 'two', 'target', 'induc', 'gener', 'potenti', 'specif']

3. Sample Results (First 10 answers for the first 2 queries):

Query ID: 1
1. Doc 18953920 - Score: 1.0000
2. Doc 21257564 - Score: 0.8849
3. Doc 10906636 - Score: 0.7913
4. Doc 7581911 - Score: 0.7834
5. Doc 20155713 - Score: 0.7760
6. Doc 36480032 - Score: 0.7625
7. Doc 26071782 - Score: 0.7261
8. Doc 13231899 - Score: 0.7088
9. Doc 40584205 - Score: 0.6862
10. Doc 12824568 - Score: 0.6818

Query ID: 3
1. Doc 2739854 - Score: 1.0000
2. Doc 4414547 - Score: 0.9742
3. Doc 4378885 - Score: 0.9309
4. Doc 4632921 - Score: 0.9302
5. Doc 3672261 - Score: 0.9187
6. Doc 23389795 - Score: 0.9057
7. Doc 14717500 - Score: 0.8955
8. Doc 13519661 - Score: 0.8141
9. Doc 19497526 - Score: 0.8118
10. Doc 19058822 - Score: 0.7785

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

1. Title Only vs. Full Text Comparison:
There is a significant performance gap between indexing only the titles (MAP 0.2981) and indexing the full 
abstract (MAP 0.6310). This is expected because scientific titles are often concise and may not contain the specific 
natural language keywords used in a query. The abstract provides necessary context and a larger vocabulary, 
allowing the BM25 algorithm to find more relevant matches that would otherwise be missed.

2. Comparison to Baseline:
Our best run (Full Text) achieved a MAP score of 0.6310. This slightly outperforms the BM25 baseline 
of 0.6012 in the provided "previous student report". This validates that our preprocessing pipeline and our 
BM25 implementation are functioning correctly and efficiently.

3. Algorithms and Optimizations:
As detailed in the algorithms section, we optimized our index size 
by applying stemming, which helped the system match words even if they had different endings. 
This kept our index size manageable and made our search results more accurate. We also chose BM25 
instead of standard TF-IDF because it handles long documents better, it stops long abstracts from ranking 
too high just because they repeat a word, ensuring that the top results are actually the most relevant.
-----------------------------------------------------------------------------------------------------------------------------