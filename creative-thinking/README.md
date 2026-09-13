# Creative thinking

Creative thinking helps an AI agent explore design, writing, and other creative tasks when you haven't chosen a direction or want alternatives. It uses randomly sampled words to introduce unexpected associations, then turns those associations into a direction that serves your task.

## Try it

With the skill installed, give your agent a request like this:

```text
Use $creative-thinking to explore three directions for a neighborhood library website. Help first-time visitors find events and opening hours. Keep it readable and easy to navigate.
```

Include your purpose, constraints, and any decisions you've already made. Ask for alternatives to compare or for a finished result, depending on what you need.

The skill is also configured for automatic selection when a design or creative task has an open direction, when you request creative alternatives, or when you explicitly ask for creativity or imagination.

## How it works

1. A Python helper samples seven distinct words from a broad, cleaned vocabulary of noun, adjective, and adverb spellings. You can supply your own seed instead.
2. The agent treats the seed as a secret code to decrypt and draw inspiration from, looking beyond the surface for subpatterns.
3. It develops the requested work from useful associations while preserving your purpose and constraints. Unusual words can contribute through their form alone.

You receive the work itself. Ask the agent to explain the seed's influence if you want to inspect the connection.

The vocabulary removes capitalized-only names and acronyms, single letters, a small set of grammatical filler, and redundant regional spellings. Unusual and technical words remain eligible. These rules remove identifiable dictionary clutter; they do not rank words by creative potential.

## Requirements and limits

The bundled scripts use Python 3.9 or later and the standard library. Word sampling runs locally and offline; the vocabulary is included with the skill. If the agent cannot execute the helper, it reports that limitation and continues from your brief.

Results vary with the task, seed, and model. Judge the result by whether it helps your task.

## Sources and maintenance

The method adapts [Anshu Chimala's article on AI-assisted design](https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world). This skill uses seven randomly sampled words as its seed and combines the secret-code prompt with an invitation to explore subpatterns.

See [sources and vocabulary documentation](references/wordlist.md) for dictionary provenance, licensing, and rebuilding instructions. The agent's operating instructions are in [SKILL.md](SKILL.md).
