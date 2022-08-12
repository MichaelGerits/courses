import nltk
import sys
import re

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """

S -> NP VP | S Conj S
NP -> Nom | Det Nom | Nom Adv | Det Nom Adv | Det Nom PP | NP Conj NP
VP -> V | V NP | V PP | V NP PP | Adv VP | V Adv | VP Conj VP
PP -> P NP
Nom -> N | Adj Nom
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    #tokenizes using the nltk function
    split_raw = nltk.word_tokenize(sentence)
    split_clean = []
    for word in split_raw:
        for char in word:
            #if there is ay alphabetical character in word, 
            # word gets added and it continues to the next word 
            if char.isalpha():
                split_clean.append(word.lower())
                break

    return split_clean

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_subs = []
    #gets all the subrees with an NP label
    for np in tree.subtrees(lambda tree: tree.label() == "NP"):
        sub2_labels = [sub.label() for sub in np.subtrees()]
        #if it's the only NP/ doesn't contain any others its added to the list
        if sub2_labels.count("NP") == 1:
            np_subs.append(np)

    return np_subs

if __name__ == "__main__":
    main()
