COURSE CODE: CSI4107
STUDENT NAMES: Estelle Ngounou (300269700), Matsuru Hoshi (300228879), Max Wang (300296800), Wanis Hassan (300255946)

TASK DIVISION:
Estelle: Environment setup using Pyserini, Preprocessing, Indexing, Retrieval and Ranking
Matsuru:
Max:
Wanis: MAP scores, Algorithm explanations, Discussion

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


MEAN AVERAGE PRECISION (MAP):


DISCUSSION:


