import nltk
import sys
import os
import string
import math
from operator import itemgetter

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    rtn = {}

    # make sure the given `directory` is a valid directory
    if not os.path.isdir(directory):
        return rtn

    for name in os.listdir(directory):

        # make sure the `name` found is a valid file
        f = os.path.join(directory, name)
        if not os.path.isfile(f):
            continue

        # read the file content as a string
        with open(f, encoding="utf8") as fp:
            rtn[name] = fp.read()

    return rtn


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    punctuations = string.punctuation
    stopwords = nltk.corpus.stopwords.words("english")
    return [word for word in nltk.word_tokenize(document.lower())
            if not word in punctuations and not word in stopwords]


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    word_sets = [set(doc) for doc in documents.values()]
    word_in_doc_count = {word: sum(1 for ws in word_sets if word in ws)
                         for word in set().union(*word_sets)}
    return {word: math.log(len(word_sets)/count)
            for word, count in word_in_doc_count.items()}


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idfs = {f: sum(files[f].count(q) * idfs.get(q, 0) for q in query)
               for f in files}
    return sorted(tf_idfs, key=tf_idfs.__getitem__, reverse=True)[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    data = [(s, 
             sum(idfs[q] for q in query if q in sentences[s]),
             sum(1 for w in sentences[s] if w in query) / len(sentences[s])
             ) for s in sentences]
    return [d[0] for d in sorted(data, key=itemgetter(1,2), reverse=True)][:n]


if __name__ == "__main__":
    main()
