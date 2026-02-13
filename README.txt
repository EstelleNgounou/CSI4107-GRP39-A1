COURSE CODE: CSI4107
STUDENT NAMES: Estelle Ngounou (300269700), Matsuru Hoshi (300228879), Max Wang (300296800), Wanis Hassan (300255946)

TASK DIVISION:
Estelle: Environment setup using Pyserini, Preprocessing, Indexing, Retrieval and Ranking
Matsuru: 
- Set up and devised installation/running instructions.
- Preprocessing - Added support for .tsv files on query input.
- Ranking - Enabled bm25 ranking.
Max: Algorithm explanations
Wanis: MAP scores, Discussion

FUNCTIONALITIES OF THE PROGRAMS:

This program does the following things:
 - Parses the corpus documents
 - Preprocesses the tokenized text
 - Creates an inverted index to allow searching
 - Searches and ranks documents using the invertex index with BM25 ranking

A list compiling results for a given set of queries in TREC format is outputted.

INSTRUCTIONS ON HOW TO RUN THE PROGRAMS:

Dependencies:
- Python (Tested on 3.9.6)
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



ALGORITHMS EXPLANATIONS:

Step 1, Preprocessing: 

To convert the raw text into a list of clean words, we first normalize the text, ensuring that the system is not case-sensitive. We then use NLTK's tokenizer to convert the text into discrete linguistic units. Following this, we use the Porter Stemmer to strip texts of suffixes and reduce words into a common base/root word. We finally filter out specific meta-tokens and placeholders, leaving us with our preprocessed documents/queries containing all the tokens.

Step 2, Indexing:

The algorithm goes through the entire preprocessed list of documents once, and for every word processed, the system will note the document number the word appears in, as well as the frequency of the word. Making use of nested dictionaries, this will allow the system to find any word in constant time. Additionally, added an inverted index for only titles as required.

Step 3, Retrieval and Ranking:

When a query is entered, the system looks at the inverted index and finds only the documents that have at least one of the query's words. For every matching document, we use BM25 to calculate a relevance score by looking at how rare a word is(idf) and how often it appears. Afterwards, we use a min-max normalization algorithm to scale the scores between 0.0 and 1.0 and sort the documents according to their new ranking.


MEAN AVERAGE PRECISION (MAP):


DISCUSSION:


