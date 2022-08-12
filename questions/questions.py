import nltk 
import os
import math
import string
import sys

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
    
    data = dict()
    #gets a list of all files (and directories) in the corpus
    for filename in os.listdir(directory):
        #opens and reads th file as a string
        #using the encoding key to avoid UnicodeErrors because of the weird horizontal bits in text
        with open(os.path.join(directory, filename), encoding= "UTF-8") as file:
            # Extract text
            data[filename] = file.read()

    return data

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    #tokenizes document
    split_raw = nltk.word_tokenize(document.lower())

    split_text = []
    for word in split_raw:
        #if it is a stopword
        if word in nltk.corpus.stopwords.words("english"):
            continue
        #filters punctuation
        for char in word:
            if char in string.punctuation:
                word = word.replace(char, "")

        if word != "":
                split_text.append(word)
    
    return split_text
    #raise NotImplementedError

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()
    for file in documents:
        #calculates the idf of words 
        for word in documents[file]:
            #counts the number of files in which word appears
            inclusive_files = 0
            for wordlist in documents:
                if word in documents[wordlist]:
                    inclusive_files += 1
            
            #calculates the idf using the natural logarithm
            idf = math.log(len(documents) / inclusive_files)
            idfs[word] = idf

    return idfs
    #raise NotImplementedError


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    values = dict()
    for file in files:
        tf_idf = 0
        for Qword in query:
            #calcs term frequency of word for this file
            tf = files[file].count(Qword)
            #sum of tf-idfs of each word in Q to calc rank of doc
            try:
                tf_idf += tf * idfs[Qword]
            except KeyError:
                print(f"{Qword} not found in {file} check the spelling, or add to database\n")
        values[file] = tf_idf

    #sorts values by the tf-idf value
    ranks_sorted = list(sorted(values.keys(), key=lambda key: values[key], reverse=True))
    return ranks_sorted[:n]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    values = dict()
    for sentence in sentences:
        mwm = 0
        overlap = 0
        for Qword in query:
            #counts how many words overlap and adds to the matching word measure
            if Qword in sentences[sentence]:
                overlap += 1
                mwm += idfs[Qword]

        #calculates the query term frequency
        frequency = overlap / len(sentences[sentence])
        values[sentence] = (mwm, frequency)

    #sorts values by mwm and if needed by term frequency
    ranks_sorted = list(sorted(values.keys(), key=lambda key: (values[key][0], values[key][1]), reverse=True))
    return ranks_sorted[:n]

if __name__ == "__main__":
    main()
