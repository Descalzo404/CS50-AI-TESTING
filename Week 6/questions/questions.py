import nltk
from nltk.tokenize import word_tokenize
import string
import sys
import os
import math

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
    file_dict = dict()
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), "r", encoding='utf8') as f:
            file_dict[filename] = f.read()  
    return file_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    text = word_tokenize(document.lower())
    return [word for word in text if word not in nltk.corpus.stopwords.words("english") and word not in string.punctuation]


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    idf_values = dict()
    
    for name in documents:
        list_words = list()
        for word in documents[name]:
            if word not in list_words:
                list_words.append(word)
                if word not in idf_values:
                    idf_values[word] = 1
                else:
                    idf_values[word] += 1

    for word in idf_values:
        temp = math.log(len(documents) / idf_values[word])
        idf_values[word] = temp

    return idf_values



def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    file_ranks = dict()
    for file in files:
        tf_idf = 0
        for word in query:
            times = files[file].count(word)
            tf_idf += idfs[word] * times

        file_ranks[file] = tf_idf
    ranks = dict(sorted(file_ranks.items(), key=lambda item: item[1], reverse=True))
    ranks_list = list(ranks.keys())
    return (ranks_list[:n])


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    ranks = []
    for sentence in sentences:
        sentence_ranks = [sentence, 0, 0]

        for term in query:
            if term in sentences[sentence]:
                sentence_ranks[1] += idfs[term]
                sentence_ranks[2] += sentences[sentence].count(term) / len(sentences[sentence])

        ranks.append(sentence_ranks)

    ranks_sorted = [sentence for sentence, idf_sum, term_density in sorted(ranks, key=lambda item: (item[1], item[2]), reverse=True)]
    return (ranks_sorted[:n])            


if __name__ == "__main__":
    main()
