#!/usr/bin/env python3
"""Print seven distinct words from the bundled offline vocabulary."""

import argparse
import random
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    wordlist = Path(__file__).resolve().parents[1] / "data" / "words.txt"
    try:
        words = wordlist.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        parser.exit(1, f"Cannot read bundled vocabulary: {error}\n")
    if len(words) < 7:
        parser.exit(1, "Bundled vocabulary must contain at least seven words.\n")
    print(" ".join(random.sample(words, 7)))


if __name__ == "__main__":
    main()
