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
    distribution = {p: 0.0 for p in corpus.keys()}

    # with probability `damping_factor`, the surfer randomly choose one of the
    # linked pages with equal probability
    linkTo = corpus[page] if len(corpus[page]) > 0 else corpus.keys()
    for p in linkTo:
        distribution[p] += damping_factor / len(linkTo)

    # with probability 1 - `damping_factor`, the surfer randomly choose one
    # of all pages with equal probability
    for p in corpus.keys():
        distribution[p] += (1 - damping_factor) / len(corpus)

    assert (-0.001 <= 1 - sum(d for d in distribution.values()) <= 0.001), (
            "transition_model(): distribution should sum to 1.")

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    samples = {p: 0.0 for p in corpus.keys()}

    page = None
    for i in range(n):
        if page is None:
            # Condition for the first sample. `weights` = None means the
            # probabilities are equal among all populations.
            population, weights = list(corpus.keys()), None
        else:
            # While we're on a randomly chosen page, randomly choose another
            # one according to the corresponding transition model
            population, weights = zip(
                *transition_model(corpus, page, damping_factor).items()
                )
        page = random.choices(population, weights=weights)[0]
        samples[page] += 1

    # Normalize as probability distribution (sample / total samples)
    distribution = {page: sample/n for page, sample in samples.items()}

    assert (-0.001 <= 1 - sum(d for d in distribution.values()) <= 0.001), (
            "sample_pagerank(): distribution should sum to 1")

    return distribution


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    DELTA_THRESHOLD = 0.001
    MAX_ITERATION = 10000

    distribution = {p: 1.0/len(corpus) for p in corpus.keys()}

    iteration = 0
    max_delta = 1.0
    while max_delta >= DELTA_THRESHOLD:

        if iteration >= MAX_ITERATION:
            raise RecursionError(
                "Process exceeds its maximum allowed iteration (%d). "
                "Please make sure the input corpus condition is convergent."
                % MAX_ITERATION)

        # With probability 1 - d, the surfer chose a page at random and ended
        # up on page p
        new_distribution = {p: (1-damping_factor)/len(corpus) 
                            for p in corpus.keys()}

        # With probability d, the surfer followed a link from a page i to
        # page p
        for i in corpus.keys():
            linkTo = corpus[i] if len(corpus[i]) > 0 else corpus.keys()
            for p in linkTo:
                new_distribution[p] += (damping_factor * distribution[i] / 
                                        len(linkTo))

        max_delta = max(abs(new_distribution[p] - distribution[p]) 
                        for p in corpus.keys())
        distribution = new_distribution
        iteration += 1

    assert (-0.001 <= 1 - sum(d for d in distribution.values()) <= 0.001), (
            "iterate_pagerank(): distribution should sum to 1")

    return distribution

def print_rank_table(corpus, smp_ranks, iter_ranks, samples, max_error):
    """
    Print a table of comparison of the given generated pageranks.

    Args:
        corpus (:obj:`dict`): A dict of corpus queried from `crawl()`.
        smp_ranks (:obj:`dict`): A dict queried from `sample_pagerank()`.
        iter_ranks (:obj:`dict`): A dict queried from `iterate_pagerank()`.
        samples (int): Number of samples for `sample_pagerank` algorithm.
        max_error (float): Maximum absolute error allowed for the difference.
    """
    
    # column widths
    widths = [20, 20, 10, 10]

    # formatted string of a row
    template = " | ".join(f"{{{i}:{{aligns[{i}]}}{{widths[{i}]}}}}" 
                          for i in range(len(widths)))

    separator = " | ".join("-" * w for w in widths)
    print(separator)

    headers = ["Page", f"PR_smp (n={samples})", "PR_iter", "Delta"]
    print(template.format(*headers, aligns="^^^^", widths=widths))

    print(separator)

    for page in corpus.keys():
        delta = abs(smp_ranks[page] - iter_ranks[page])
        row = [page, 
               f"{smp_ranks[page]:.4f}", 
               f"{iter_ranks[page]:.4f}", 
               ("* " if delta > max_error else "") + f"{delta:.4f}"
        ]
        print(template.format(*row, aligns="^^^>", widths=widths))
    

def test_ranks(corpus, samples=SAMPLES, iteration=50, max_error=0.01):
    """
    Test the correctness of the pagerank algorithms by iterating the procedures
    for a given number of times (`iteration`) and check the absolute difference.
    Display the details if the difference is larger than the given `max_error`.

    Args:
        corpus (:obj:`dict`): A dict of corpus queried from `crawl()`.
        samples (int): Number of samples for `sample_pagerank` algorithm.
        iteration (int): Number of iterations to test.
        max_error (float): Maximum absolute error allowed for the difference.
    """

    err_msg = None
    print("Loop", end="", flush=True)
    for i in range(iteration):
        print(".", end="", flush=True)
        smp_ranks = sample_pagerank(corpus, DAMPING, samples)
        iter_ranks = iterate_pagerank(corpus, DAMPING)
        if ((set(smp_ranks.keys()) != set(corpus.keys())) or 
            (set(iter_ranks.keys()) != set(corpus.keys()))
            ):
            err_msg = "Key set does not match"
        else:
            for k in smp_ranks.keys():
                err = abs(smp_ranks[k] - iter_ranks[k])
                if err > max_error:
                    err_msg = f"Rank of {k} ({err:.4}) exceeds maximum error"
                    break
        if err_msg:
            print("")
            print(f"Error is found after the {i+1}th try:")
            print(f"\t{err_msg}")
            print_rank_table(corpus, smp_ranks, iter_ranks, samples, max_error)
            break
    else:
        print("")
        print(f"Finish a {iteration}-iteration pagerank comparison with "
                f"{samples} samples")


if __name__ == "__main__":
    main()
