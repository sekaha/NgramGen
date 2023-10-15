import concurrent.futures
from math import floor, ceil
from collections import Counter


def get_grams(
    corpus, valid=set("abcdefghijklmnopqrstuvwxyz[];',./`1234567890-=\\ "), remove=""
):
    """
    Generate n-grams from a text corpus and save the results in TSV files.

    Parameters:
        corpus (str): The path to the input text file.
        valid_chars (set, optional): A set of valid characters to consider for n-grams (default is alphanumeric and some special characters).
        remove_chars (str, optional): Characters to remove from the text before processing (default is empty).
    """

    DATA_TYPES = {
        "characters": (1, 0),
        "bigrams": (2, 0),
        "trigrams": (3, 0),
        "quadrigram": (4, 0),
        "1-skip": (2, 1),
        "2-skip": (2, 2),
        "3-skip": (2, 3),
        "4-skip": (2, 4),
        "5-skip": (2, 5),
        "6-skip": (2, 6),
        "7-skip": (2, 7),
    }

    unshift = str.maketrans('!@#$%^&*()_+:{}:<>|?"', "1234567890-=;[];,.\/'", remove)
    text = open(corpus, "r").read().lower().translate(unshift)

    def create(alias, size, skip):
        grams = Counter()

        for i in range(len(text) - size - skip + 1):
            window = text[i : i + size + skip]

            # make an n-gram that skips letters between
            gram = window[: floor(size / 2)] + window[-ceil(size / 2) :]

            # only accept valid characters
            if all(char in valid for char in gram):
                grams[gram] += 1

        # Output a TSV file of this data subtype
        with open(f"output/{alias}.txt", "w") as f:
            for chars, count in sorted(grams.items(), key=lambda x: -x[1]):
                f.write(f"{chars}\t{count}\n")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(create, alias, size, skip)
            for alias, (size, skip) in DATA_TYPES.items()
        ]
        concurrent.futures.wait(futures)
