import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    paths = corpus[page]
    result = dict()
    #checks if the page has any links and handles if that's not the case
    if len(paths) == 0:
        for link in corpus:
            result[link] = 1/len(corpus)
        return result
    else:
        #adds the random propability for all pages
        for page in corpus:
            result[page] = ((1 - damping_factor)/len(corpus))
        #adds the propability of the possible paths/links
        for link in paths:
            result[link] += (damping_factor/len(paths))
        return result
    #raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #gets the first sample randomly and initiates the dictionaries
    sample = random.choice(list(corpus.copy().keys()))
    state = dict()
    Pr = dict()
    #executes the chain n times
    for i in range(n):
        #counts the amount of times the page has been sampled.
        if sample not in Pr:
            Pr[sample] = 1
        else:
            Pr[sample] += 1

        #gets the state of this iteration
        state = transition_model(corpus, sample, damping_factor)

        #gets the weights for the next sample choice
        weights = list(state.values())
        #gets the next sample from a weighted choice
        sample = random.choices(list(state.keys()), weights, k=1)[0]
        
    #divides the sample amount by the amount of iterations to get the relative proportion
    for page in Pr:
        Pr[page] = Pr[page]/n
    return Pr

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    Pr = dict()
    n = len(corpus)
    #initiates the original/equal pagerank
    for page in corpus:
        Pr[page] = 1/n
    new_corpus = edit_corpus(corpus)

    #keeps calculating untill the diffrence is max 0.001
    cycles = 0
    while True:
        new_Pr = dict.fromkeys(new_corpus.keys(), 0)
        high_difference = -1

        #calculates the new Pr for each page 
        for page in corpus:
            new_Pr[page] = calculate_pr(Pr, page, damping_factor, new_corpus)
            #calculates the diffrence between new and old 
            if abs(new_Pr[page] - Pr[page]) > high_difference:
                high_difference = abs(new_Pr[page] - Pr[page])

        Pr = new_Pr
        #if there is no diffrence higher than 0.001 it quits the loop
        if high_difference <= 0.001:
            break
    return Pr

def edit_corpus(corpus):
    '''handles the case that if a page has no links, every page becomes its link'''
    new_corpus = dict()
    for page in corpus:
        if len(corpus[page]) == 0:
            new_corpus[page] = corpus.keys()
        else: 
            new_corpus[page] = corpus[page]
    return new_corpus

def calculate_pr(Pr, page, damping_factor, corpus):
    '''
    this function calculates the new pagerank 
    using the formula that we've seen in background
    '''
    n = len(corpus)

    parents = []
    #finds  all the pages that link to our specific page
    for parent in corpus:
        if page in corpus[parent]:
            parents.append(parent)

    #adds the first term of the formulas
    term1 = 1/n
    #calculates the summation of the formula
    summation = 0
    for parent in parents:
        summation += (Pr[parent]/len(corpus[parent]))
    return (1-damping_factor) * term1 + damping_factor * summation




if __name__ == "__main__":
    main()
