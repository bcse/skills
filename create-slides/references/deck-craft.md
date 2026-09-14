# Deck craft

Load when writing or auditing the words and figures of a deck. `SKILL.md` owns
the shape; this file owns the finishing.

## Word budget per face

| Slide kind | Face carries |
|---|---|
| Title | Deck name, one line of what it is, a few chips naming the parts |
| Claim | Headline plus three or four short lines |
| Figure | Headline plus one diagram plus a one-line caption |
| Comparison | Headline plus a row of three to five tiles, a phrase each |
| Ladder or sequence | Headline plus up to six rows of a few words each |
| Recap | Headline plus one diagram that replays the whole argument |

A face that needs more than this is two slides, or its detail belongs in notes.

## Plain English

Decks are read fast and often by people outside the team, so write to a plain
technical English bar. These come from ASD-STE100, ISO 24495-1 plain language,
and an anti-slop pass.

- One idea per sentence. Active voice, and name the actor.
- Define a term the first time it carries weight, then reuse that exact term.
- Common words over fancy ones: *use* not *leverage*, *help* not *facilitate*.
- Start from the audience's problem, not from your architecture.
- No em dashes and no en dashes. End the sentence, or use a comma.
- Straight quotes only.
- Sentence case headings. No decorative emoji.
- No "not just X, but Y", no forced groups of three, no vague attributions.
- Say what a thing does, not how it feels. If a sentence could sit unchanged in
  another project's deck, it says nothing about this one. Cut it.

### Audit commands

Run these before publishing. All should return zero.

```bash
f=deck.html
grep -c '—' "$f"                       # em dashes
grep -c '–' "$f"                       # en dashes
grep -o '[“”‘’]' "$f" | wc -l          # curly quotes
grep -ocirE '\b(crucial|delve|enhance|fostering|garner|intricate|pivotal|showcase|tapestry|testament|underscore|leverage|utilize|seamless|robust|comprehensive|additionally)\b' "$f"
grep -ocirE '\b(substrate|nexus|scaffolding|paradigm|flywheel|bedrock|north star)\b' "$f"
```

Read every hit rather than trusting the count. A word can appear legitimately
inside quoted user speech or a product name.

## Diagrams

Load the `artifact-diagramming` skill for figure craft. Deck-specific additions:

- **15px text at the drawn scale**, small labels at 12.5px. Size the `viewBox` so
  that holds, rather than shrinking the type to fit a chosen canvas.
- **Two arrow markers per figure**, one in `currentColor` for ordinary edges and
  one in the accent for the path the claim is about. Set `color` on the `<svg>`
  to the same value as the ordinary stroke so an arrowhead never outshines its
  own line.
- **Check label collisions by arithmetic**, not by eye. A mono label is roughly
  `0.6em` per character wide; compute where it ends and compare against the next
  element's x. Stacked fallback arrows with labels are the usual offender.
- **Two arrows beat five.** Collapse "timeout", "error" and "unparseable" into one
  dashed edge labelled with all three.
- Give every `<svg>` `role="img"` and an `aria-label` that states the same claim
  as the caption.

## Mock interfaces

A three-turn chat mockup often explains a conversational product faster than a
diagram. Build it from plain divs: a user bubble aligned right in accent wash, an
assistant bubble aligned left on the lifted surface, a tiny mono role label above
each, and a row of pill-shaped chips for tappable answers. Set the bubble text in
the display face so it survives the afar test.

## Publishing checklist

- Title is a short noun phrase that names the deck, with no appended explainer.
- `favicon` on the first publish only.
- `description` is one sentence, since it becomes the gallery subtitle.
- Republished to the same file path, so the URL held.
- Screenshot read, and any defect it revealed fixed and re-rendered.
