import os
import random
import re
import sys
import copy
import math

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
    #Starting the transition model dict
    transition_model = {}

    #Getting the number of links
    number_of_links = len(corpus[page])
    number_of_pages = len(corpus)
    #If the page has links to other pages
    if number_of_links:

        
        #Adding this probability to the transition model
        for p in corpus:
            transition_model[p] = (1 - damping_factor)/number_of_pages

        #Defining the probability for clicking on every other page that is linked to the original page
        for p in corpus[page]:
            transition_model[p] += damping_factor/number_of_links

    else:
        n = len(corpus.keys())
        prob = 1/n

        for key in corpus:
            transition_model[key] = prob

    return transition_model

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    samples = []
    pageranks = {}
    page_list = list(corpus.keys())
    page = random.choice(page_list)
    samples.append(page)

    while len(samples) < n:
        model = transition_model(corpus, page, damping_factor)
        page = random.choices(list(model.keys()), list(model.values()), k = 1)[0]
        samples.append(page)
    
    n = len(samples)
    for page in page_list:
        num = samples.count(page)
        pageranks[page] = num/n

    return pageranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pageranks = {}
    N = len(corpus)
    for page in corpus.keys():
        pageranks[page] = (1 - damping_factor)/N
    go = True
    while go:
        go = False
        temp = copy.deepcopy(pageranks)
        for page in corpus.keys():
            pageranks[page] = ((1 - damping_factor) / N) + (damping_factor * iterate_links(corpus, page, pageranks))

        for page in pageranks:
            if not math.isclose(temp[page], pageranks[page], abs_tol=0.001):
                go = True
    return pageranks

def iterate_links(corpus, page, pageranks):
    """
    Get the pages that link to a given page
    """
    result = float(0)
    for p in corpus:
        if page in corpus[p]:
            result += pageranks[p] / len(corpus[p])
        if not corpus[p]:
            result += pageranks[p] / len(corpus)
    return result

if __name__ == "__main__":
    main()
