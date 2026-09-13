#!/usr/bin/env python3
"""Build the vocabulary from a local gzipped Open English WordNet LMF file."""

import argparse
import gzip
import re
import unicodedata
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path


# This intentionally small set leaves words with useful conceptual meanings,
# including other, being, over, and under, available for association.
CLOSED_CLASS_WORDS = {
    "an", "and", "are", "at", "but", "if", "in", "nor", "on", "or", "than", "that", "the", "this",
    "whether", "whichever", "whoever",
}
SPELLING_TARGETS = {
    f"oewn-{region}_spelling__1.10.01.."
    for region in ("american", "british", "australian", "canadian")
}


def collect_words(source_path: Path):
    """Collect complete eligible sense coverage before deciding which words survive."""
    coverage = defaultdict(set)
    lowercase = set()
    spellings = set()
    with gzip.open(source_path, "rb") as source:
        for _, element in ET.iterparse(source, events=("end",)):
            if element.tag == "LexicalEntry":
                lemma = element.find("Lemma")
                part_of_speech = lemma.get("partOfSpeech")
                written = unicodedata.normalize("NFC", lemma.attrib["writtenForm"])
                word = unicodedata.normalize("NFC", written.lower())
                if part_of_speech in {"n", "a", "s", "r"} and word.isalpha():
                    coverage[word].update(
                        (part_of_speech, sense.attrib["synset"])
                        for sense in element.findall("Sense")
                    )
                    if written == written.lower():
                        lowercase.add(word)
                    if any(
                        relation.get("relType") == "exemplifies"
                        and relation.get("target") in SPELLING_TARGETS
                        for relation in element.findall("Sense/SenseRelation")
                    ):
                        spellings.add(word)
                element.clear()
            elif element.tag == "Synset":
                element.clear()
    return coverage, lowercase, spellings


def spelling_key(word: str) -> str:
    """Recognize a small set of regional spelling correspondences, not synonyms."""
    for original, replacement in (
        ("iz", "is"), ("our", "or"), ("ae", "e"), ("oe", "e"), ("ll", "l")
    ):
        word = word.replace(original, replacement)
    word = re.sub(r"re(s?)$", r"er\1", word)
    return re.sub(r"ence(s?)$", r"ense\1", word)


def clean_words(coverage, lowercase, spellings):
    """Remove dictionary clutter without ranking familiarity or subject matter."""
    removed = {
        "capitalized_only": set(coverage) - lowercase,
        "single_letter": {word for word in lowercase if len(word) == 1},
        "closed_class": lowercase & CLOSED_CLASS_WORDS,
    }
    words = lowercase - set().union(*removed.values())
    spelling_groups = defaultdict(list)
    for word in words & spellings:
        if coverage[word]:
            key = (frozenset(coverage[word]), spelling_key(word))
            spelling_groups[key].append(word)
    replacements = {}
    for variants in spelling_groups.values():
        preferred = min(variants, key=lambda word: (len(word), word))
        replacements.update((word, preferred) for word in variants if word != preferred)
    removed["spelling_variant"] = set(replacements)
    return words - replacements.keys(), removed, replacements


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Downloaded WordNet .xml.gz file")
    parser.add_argument("output", type=Path, help="Destination words.txt file")
    args = parser.parse_args()
    coverage, lowercase, spellings = collect_words(args.source)
    words, removed, _ = clean_words(coverage, lowercase, spellings)
    if not words:
        parser.error("Source contains no words after vocabulary cleanup.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(("\n".join(sorted(words)) + "\n").encode("utf-8"))
    print(f"Read {len(coverage):,} distinct eligible alphabetic words")
    for reason, exclusions in removed.items():
        print(f"Removed {len(exclusions):,}: {reason}")
    print(f"Wrote {len(words):,} distinct words to {args.output}")


if __name__ == "__main__":
    main()
