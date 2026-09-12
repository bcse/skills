# Critique

How to review a design so the feedback is diagnostic and actionable rather than a pile of observations. Sections: Protocol · Phrasing feedback · Vocabulary · Calibration.

## Protocol

For a broad critique, run the steps in order: early steps capture what real viewers experience, and later steps explain it. For a focused question, inspect only the affected area and relevant checks; stop when the question is answered with evidence.

**0. Context first.** Ask or infer: purpose, audience, medium, constraints, and *stage* — concept, working draft, or final polish. Feedback must match the stage: do not kern a wireframe; do not propose restructuring a page that ships tomorrow. If the goal is unknown, say so and critique against a stated assumption.

Also establish *what* you are judging. Prefer rendered output — render or screenshot when the environment allows. If only code or markup is available, say so, critique what the code determines (scale, token counts, structure), and name what still needs a visual pass. And cite only measurements you actually took: compute a contrast ratio before quoting one; otherwise write "verify contrast."

**1. First impression, five seconds.** Before analyzing, record the raw read: what mood does it give, where did the eye land first, what was confusing? This is the only moment you get an honest sample of what every real viewer gets — protect it by writing it down before the analytical passes contaminate it.

**2. Squint test.** Blur it. Does the intended focal point survive? Do groups still read as groups? A design that fails blurred fails at a glance, whatever its details.

**3. Inventory.** Count typefaces, text sizes, colors, spacing values, radii, icon styles. High counts are the usual cause of an unarticulated "something's off" — and counting turns that feeling into a fixable list.

**4. Leverage-ordered passes.** Examine in this order, and stop going deeper once a higher layer is broken — polishing color on top of broken hierarchy is wasted effort and wasted feedback:
1. Hierarchy — one focal point? Three levels or fewer, consistently treated?
2. Spacing & alignment — proximity grouping present? Edges shared? Scale consistent?
3. Typography — pairing, scale, measure, line-height, letter-spacing.
4. Color — palette size, accent discipline, contrast floors, consistent meaning.
5. Depth & ornament — one separation strategy? Effects earning their place?
6. Content & copy — do the words carry the design's job, or placeholder-speak?
7. Consistency details — radii, icon set, capitalization, punctuation.

**5. Distinctiveness.** The swap test: change only the logo or topic — could this belong to anyone else? Name who else looks like this. Generic is a diagnosis, not an insult, and it has a specific fix (a signature element from the subject's world, everything else quiet).

**6. Deliver.** Lead with what works and must be preserved — this is calibration, not politeness; the author needs to know what *not* to break while fixing the rest. Then at most **three** prioritized fixes (the biggest levers), each fully phrased per below. Minor issues go in a separate take-or-leave list at the end, if at all.

## Phrasing feedback

Every substantive note carries four parts — observation → effect → cause → fix — with numbers in the fix:

> The three buttons compete (observation), so nothing reads as the next step (effect on viewer). They share size, weight, and color (cause). Keep one filled accent button, drop the other two to text links in gray-600 (fix).

> The slide holds four ideas (observation), so the audience reads instead of listening (effect). There is no primary level — everything is 20pt bold (cause). One claim at 40pt, one supporting visual, the rest to speaker notes (fix).

Rules of the form: a note that cannot be acted on without a follow-up question is not finished ("make it pop" is a request for a critique, not a critique). Critique the work, never the author ("the hierarchy is flat," not "you didn't think about hierarchy"). Where possible, tie the fix back to the maker's own stated direction — "you said calm and premium; the six saturated colors are what's fighting that" lands better than any external rule.

## Vocabulary

Precise words let you name what the eye already caught.

- **Visual weight** — how strongly an element attracts the eye (size × contrast × saturation × isolation).
- **Focal point** — the single element with the most visual weight; the answer to "where do I look first."
- **Hierarchy** — the intended reading order, expressed through consistent level treatments.
- **Rhythm** — the repetition pattern of spacing and alignment down the page; broken rhythm is felt as "messy."
- **Typographic color / texture** — the evenness of gray a block of text makes when squinted at; blotchy texture means erratic spacing or weights.
- **Measure** — line length in characters.
- **Tension / balance** — asymmetry that feels deliberate vs. resolved; zero tension reads inert, unmanaged tension reads broken.
- **Negative space** — the shaped emptiness that defines groups and importance; "trapped" negative space is a gap with no job.
- **Optical alignment** — aligned to the eye rather than the bounding box.
- **Register** — the voice of the copy (formal ↔ casual, warm ↔ technical); mismatched register is a design flaw, not just a writing flaw.

## Calibration

**Principle vs. preference.** Separate "this violates a principle — fix it" (contrast below 4.5:1, no focal point) from "I would have chosen differently — consider it" (this serif vs. that serif). Deliver them with different confidence, explicitly.

**Judge within the direction.** Evaluate maximalist work by maximalist standards — is the chaos controlled, is there still a reading order? — not by minimalist ones. The question is never "is this the style I'd choose," it is "does this execute its own stated direction well."

**Praise specifically.** "The single accent used only on the CTA is exactly right — keep that discipline" teaches; "looks nice" doesn't. Specific praise is how taste transfers to the person receiving the critique.
