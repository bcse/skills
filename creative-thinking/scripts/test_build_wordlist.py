#!/usr/bin/env python3
"""Offline regression tests for vocabulary cleanup and seed generation."""

import gzip
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parent


def entry(word, pos="n", synsets=(), spelling=None):
    element = ET.Element("LexicalEntry")
    ET.SubElement(element, "Lemma", writtenForm=word, partOfSpeech=pos)
    for synset in synsets or (word,):
        sense = ET.SubElement(element, "Sense", synset=synset)
        if spelling:
            ET.SubElement(
                sense, "SenseRelation", relType="exemplifies", target=spelling
            )
    return element


AMERICAN = "oewn-american_spelling__1.10.01.."
BRITISH = "oewn-british_spelling__1.10.01.."


class WordlistTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def build(self, entries):
        root = ET.Element("LexicalResource")
        lexicon = ET.SubElement(root, "Lexicon")
        lexicon.extend(entries)
        source = self.root / "source.xml.gz"
        with gzip.open(source, "wb") as stream:
            stream.write(ET.tostring(root, encoding="utf-8"))
        output = self.root / "words.txt"
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "build_wordlist.py"), str(source), str(output)],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return output.read_text(encoding="utf-8").splitlines()

    def test_names_acronyms_and_lowercase_homographs(self):
        words = self.build([
            entry("NASA"), entry("Berlin"), entry("ID"), entry("id"),
            entry("Atlas"), entry("atlas"), entry("Hermes"), entry("hermes", "v"),
        ])
        self.assertEqual(words, ["atlas", "id"])

    def test_single_letters_filler_and_meaningful_short_words(self):
        words = self.build([
            entry(word) for word in
            ("a", "x", "the", "and", "but", "on", "in", "at", "are", "qi", "ox", "id", "root", "other",
             "being", "over", "under")
        ])
        self.assertEqual(set(words), {
            "qi", "ox", "id", "root", "other", "being", "over", "under"
        })

    def test_rare_words_unicode_and_part_of_speech(self):
        words = self.build([
            entry("tomentum"), entry("siloxane"), entry("éclair"), entry("e\u0301clair"),
            entry("森林"),
            entry("radiant", "a"), entry("angular", "s"), entry("obliquely", "r"),
            entry("defraud", "v"), entry("with", "p"), entry("and", "c"),
            entry("ice cream"), entry("self-aware", "a"), entry("word8"),
        ])
        self.assertEqual(words, [
            "angular", "obliquely", "radiant", "siloxane", "tomentum", "éclair", "森林"
        ])

    def test_pure_spelling_variants_collapse_across_all_eligible_parts_of_speech(self):
        entries = []
        for word, spelling in (("colour", BRITISH), ("color", AMERICAN)):
            entries.extend([
                entry(word, "n", ("pigment", "appearance"), spelling),
                entry(word, "a", ("chromatic",), spelling),
            ])
        entries.append(entry("color", "v", ("extra-verb",)))
        self.assertEqual(self.build(entries), ["color"])
        self.assertEqual(self.build(list(reversed(entries))), ["color"])

    def test_unique_sense_or_part_of_speech_preserves_spelling(self):
        words = self.build([
            entry("metre", "n", ("length",), BRITISH),
            entry("meter", "n", ("length", "instrument"), AMERICAN),
            entry("licence", "n", ("permission",), BRITISH),
            entry("license", "n", ("permission",), AMERICAN),
            entry("license", "a", ("extra",)),
            entry("centre", "n", ("middle",), BRITISH),
            entry("center", "n", ("middle",), AMERICAN),
            entry("Center", "n", ("named-place",)),
        ])
        self.assertEqual(words, ["center", "centre", "licence", "license", "meter", "metre"])

    def test_generic_synonyms_and_derived_words_are_retained(self):
        words = self.build([
            entry("feline", "n", ("cat",)), entry("cat", "n", ("cat",)),
            entry("coloration", "n", ("color",)),
            entry("color", "n", ("color",), AMERICAN),
            entry("colour", "n", ("color",), BRITISH),
            entry("local", "a", ("nearby",), "oewn-british_english__1.10.00.."),
            entry("nearby", "a", ("nearby",)),
        ])
        self.assertEqual(words, ["cat", "color", "coloration", "feline", "local", "nearby"])

    def test_spelling_labels_do_not_merge_different_word_families(self):
        words = self.build([
            entry("synchronisation", "n", ("coordination",), BRITISH),
            entry("synchronization", "n", ("coordination",), AMERICAN),
            entry("synchronizing", "n", ("coordination",), AMERICAN),
            entry("synchronising", "n", ("coordination",), BRITISH),
            entry("niter", "n", ("mineral",), AMERICAN),
            entry("nitre", "n", ("mineral",), BRITISH),
            entry("saltpeter", "n", ("mineral",), AMERICAN),
            entry("saltpetre", "n", ("mineral",), BRITISH),
        ])
        self.assertEqual(words, [
            "niter", "saltpeter", "synchronisation", "synchronising"
        ])

    def test_sampler_reads_bundled_vocabulary_from_another_directory(self):
        words = self.build([
            entry(word) for word in
            ("qi", "ox", "id", "tomentum", "siloxane", "éclair", "root", "over")
        ])
        scripts = self.root / "skill" / "scripts"
        scripts.mkdir(parents=True)
        data = scripts.parent / "data"
        data.mkdir()
        shutil.copyfile(self.root / "words.txt", data / "words.txt")
        sampler = scripts / "generate_seed.py"
        shutil.copyfile(SCRIPTS / sampler.name, sampler)
        result = subprocess.run(
            [sys.executable, str(sampler)], cwd=self.root,
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        draw = result.stdout.split()
        self.assertEqual(len(draw), 7)
        self.assertEqual(len(set(draw)), 7)
        self.assertLessEqual(set(draw), set(words))


if __name__ == "__main__":
    unittest.main()
