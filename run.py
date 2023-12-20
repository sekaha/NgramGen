from ngram_gen import get_grams
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate n-grams from a text corpus and save the results in TSV files."
    )

    parser.add_argument("corpus", help="The path to the corpus file to be parsed.")
    parser.add_argument(
        "save_location",
        nargs="?",
        help="Output directory, defaults to local directory if not specified.",
        default=".",
    )
    parser.add_argument(
        "-vc",
        help="A set of valid characters to consider for n-grams (default is alphanumeric and some special characters).",
        default="abcdefghijklmnopqrstuvwxyz',.-/;",
    )
    parser.add_argument(
        "-rc",
        help="Characters to remove from the text before processing (default is empty).",
        default="",
    )
    parser.add_argument(
        "-o",
        help="(Boolean): sort ngrams thus reducing the storage space.",
        default=False,
    )
    parser.add_argument(
        "-rd",
        help="(Boolean): remove any bigrams that repeat a character twice in a row.",
        default=False,
    )

    args = parser.parse_args()

    get_grams(args.corpus, args.vc, args.rc, args.o, args.rd, args.save_location)
