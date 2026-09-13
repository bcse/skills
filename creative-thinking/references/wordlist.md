# Sources and offline vocabulary

## Creative method

The method is inspired by [Anshu Chimala's design process](https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world). This skill uses seven randomly sampled words with a secret-code prompt and an invitation to explore subpatterns. This combination has not been shown to outperform the article's alphanumeric seed.

## Vocabulary

The bundled `data/words.txt` contains **60,219 distinct words** derived from the Open English WordNet team's **Open English WordNet 2025** core release, which builds on Princeton University's WordNet. The vocabulary preserves unusual words and scientific terms. It removes identifiable dictionary clutter without a frequency, familiarity, or subject filter.

## Source and attribution

- Project: [Open English WordNet](https://github.com/globalwordnet/english-wordnet).
- Release file: [english-wordnet-2025.xml.gz](https://en-word.net/static/english-wordnet-2025.xml.gz), downloaded September 13, 2026. Its `Lexicon` metadata identifies version `2025`.
- Compressed source SHA-256: `9ca6d1dcb75f822fdd66617f7d9da48142ace38dd544d6ad5e2feca1674ad3fe`.
- Vocabulary SHA-256: `04b89b2946bc4ca6bfd0a7291dd6cef7232e155f13c22177afda051959420393`.
- Open English WordNet license and notices: [data/LICENSE.md](../data/LICENSE.md).
- Princeton WordNet license and notices: [data/WNDB_License.txt](../data/WNDB_License.txt).

This vocabulary is a transformed subset of that source, not the complete dictionary. The transformation described below constitutes the changes made for this skill. Preserve both bundled license files when redistributing the vocabulary.

## Transformation

1. Collect lemmas tagged noun (`n`), adjective (`a`), adjective satellite (`s`), or adverb (`r`), along with their complete eligible part-of-speech and synset coverage. A synset identifies a dictionary meaning.
2. Normalize spellings to lowercase Unicode NFC and retain alphabetic single words. Whitespace, digits, punctuation, hyphens, apostrophes, and multiword phrases are excluded. Deduplicate spellings across entries and senses.
3. Require an eligible source spelling that is already lowercase or uncased. This removes entries recorded only with capitals, including many names and acronyms. A lowercase homograph such as `id` survives its separate `ID` entry.
4. Remove single letters and the small explicit grammatical-filler set in `CLOSED_CLASS_WORDS` in the builder. Short words such as `qi` and `ox` remain eligible.
5. Consolidate regional spellings only when both words have explicit spelling metadata, identical complete eligible part-of-speech and synset coverage, and a recognized spelling correspondence. Keep the shortest spelling, breaking ties alphabetically. This is a deterministic choice, not a locale preference.
6. Sort the remaining words and write one per line as UTF-8 with a final newline.

The recognized spelling correspondences are deliberately limited: `iz/is`, `our/or`, `ae/e`, `oe/e`, doubled `ll/l`, final `re/er`, and final `ence/ense`, including final plural `s` for the last two. General synonyms and derived word families are retained. For example, `synchronisation` and `synchronising` remain separate even though their dictionary meanings overlap. A spelling with a unique eligible sense also survives.

| Cleanup stage | Words removed |
| --- | ---: |
| Capitalized-only spellings | 3,932 |
| Single letters | 26 |
| Explicit grammatical filler | 5 |
| Redundant regional spellings | 356 |
| Total | 4,319 |

The initial eligible pool contains 64,538 spellings. Cleanup leaves **60,219 words**, stored in **587,739 bytes**. Sense counts do not increase a word's sampling probability.

These rules are conservative and do not measure inspiration. Some capitalized-only entries are useful cultural terms or associated adjectives; some retained words are narrow technical labels or ordinary vocabulary. No entire scientific category is excluded. Words such as `tomentum`, `siloxane`, `luculent`, and `merlon` remain eligible. Some spellings can function as prepositions, conjunctions, or verbs in other contexts because the source also gives them an eligible meaning.

## Rebuilding

Download the exact release file linked above and verify its SHA-256 before rebuilding. From this skill's directory, run:

```sh
python3 scripts/build_wordlist.py /absolute/path/to/english-wordnet-2025.xml.gz data/words.txt
```

The builder uses Python 3.9 or later and the standard library only. It accepts a local `.xml.gz` file and an output path; it performs no network requests. Rebuilding from the verified source produces the vocabulary SHA-256 recorded above.

Run the offline regression checks from the skill's directory:

```sh
python3 scripts/test_build_wordlist.py
```

The fixtures cover casing and homographs, Unicode, grammatical categories, rare and short words, spelling consolidation, preservation of distinct meanings, and sampling from another working directory.

## Sampling

```sh
python3 /absolute/path/to/creative-thinking/scripts/generate_seed.py
```

The generator resolves the bundled vocabulary relative to its own file, so it works from any current directory. It samples seven distinct spellings without replacement using Python's automatically seeded `random.sample`, then prints exactly one space-separated line. No corpus download, external dependency, API, or network connection is needed at runtime. Sampling is uniform over spellings in the combined pool; it does not balance the parts of speech or favor familiar words.
