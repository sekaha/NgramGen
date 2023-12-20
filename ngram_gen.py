import concurrent.futures
from collections import Counter


def get_grams(
    corpus,
    valid_chars=None,
    removed="",
    ordered=False,
    remove_duplicates=False,
    save_location="",
):
    """
    Generate n-grams from a text corpus and save the results in TSV files.

    Parameters:
        corpus (str): The path to the corpus file to be parsed.
        valid_chars (set, optional): A set of valid characters to consider for n-grams (default is alphanumeric and some special characters).
        ordered (boolean, optional): Sort ngrams thus reducing the storage space.
        removed (str, optional): Characters to remove from the text before processing (default is empty).
        remove_duplicates (boolean, optional): Remove any bigrams that repeat a character twice in a row.
        save_location (str, optional): Output directory, defaults to local directory.
    """
    if not valid_chars:
        valid_chars = "abcdefghijklmnopqrstuvwxyz[];',./`1234567890-=\\ "
    valid_chars = set(valid_chars)

    DATA_TYPES = {
        "characters": (1, 0),
        "bigrams": (2, 0),
        "trigrams": (3, 0),
        "quadrigram": (4, 0),
        "1-skip": (2, 1),
        # "2-skip": (2, 2),
        # "3-skip": (2, 3),
        # "4-skip": (2, 4),
        # "5-skip": (2, 5),
        # "6-skip": (2, 6),
        # "7-skip": (2, 7),
    }

    unshift = str.maketrans('!@#$%^&*()_+:{}:<>|?"', "1234567890-=;[];,.\/'", removed)
    text = open(corpus, "r").read().lower().translate(unshift)

    def create(alias, size, skip):
        grams = Counter()

        for i in range(len(text) - size - skip + 1):
            window = text[i : i + size + skip]

            # make an n-gram that skips letters between
            gram = window[: int(size / 2)] + window[-int(size / 2 + 0.5) :]

            if ordered:
                gram = "".join(sorted(gram))

            # only accept substrings with valid characters and filter duplicates
            if not (remove_duplicates and size == 2 and gram[0] == gram[1]):
                if all(c in valid_chars for c in gram):
                    grams[gram] += 1

        # Output a TSV file of this data subtype
        with open(save_location + f"/output/{alias}.txt", "w") as f:
            for chars, count in sorted(grams.items(), key=lambda x: -x[1]):
                f.write(f"{chars}\t{count}\n")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(create, alias, size, skip)
            for alias, (size, skip) in DATA_TYPES.items()
        ]
        concurrent.futures.wait(futures)
