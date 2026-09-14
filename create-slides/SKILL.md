---
name: create-slides
description: Use when asked to create slides, a deck, a presentation, or a talk, or to present work to a team, whether the deliverable is projected in a room or shared as a link.
---

# Create slides

A deck is not a document with borders. Its unit is the **slide face**: what a
person reads from the back of a room in a few seconds. Everything else belongs
in the **notes strip** beneath it.

Build it as one HTML file, publish it with the Artifact tool, and keep the
scrolling page and the projected view as the same artifact.

## The afar test

The one rule the whole skill serves: **a slide face must be readable from across
a room.** It binds every slide.

- One claim per face, in a headline of ten words or fewer.
- Under the headline, at most **three or four short lines, or one diagram**.
  Never both a full list and a full diagram.
- Aim for **forty words or fewer** on the face. Count them.
- Headline near `3.6rem` at the top of the clamp, bullets near `1.7rem`.
  Web-page type is too small for a deck by roughly a factor of two.
- Diagram labels at **15px at the drawn scale**, not 11px. A diagram that reads
  fine in a browser tab is illegible on a projector.

Everything cut by this test goes into the notes strip, which is where the detail
was always supposed to live. Nothing is lost, so cut without hesitation.

## Steps

1. **Settle the read.** Who is in the room, and is the deliverable projected,
   read alone as a link, or both? Both is the common answer and is what the
   scaffold is built for. Ask only if the answer changes the slide count.

2. **Source the content from the material, not from memory.** For an engineering
   talk that means reading the code, the ADRs and the git log for the period,
   not summarising what you recall. Quote real values: model ids, timeouts,
   limits, the actual step count.

3. **Plan one claim per slide** before writing any HTML. Write the claim list
   first and check it reads as an argument in order. Twelve to fourteen slides
   is a comfortable length for a half-hour talk.

4. **Load `artifact-design` and, for diagrams, `artifact-diagramming`.** They own
   palette, typography and figure craft. This skill owns deck shape only.

5. **Build from the scaffold.** Copy
   [references/deck-scaffold.html](references/deck-scaffold.html) and replace the
   palette, the faces and the notes. It carries the slide and notes structure,
   present mode, keyboard paging and the progress bar, all verified.

6. **Render-check once before publishing.** See below. Read the screenshot; do
   not skip to publishing on the assumption that careful writing settled it.

7. **Audit the wording.** See [references/deck-craft.md](references/deck-craft.md)
   for the grep commands and the plain-English rules.

8. **Publish, and republish to the same file path.** Covered below.

A slide plan is done when every slide has one claim and every face passes the
afar test. The deck is done when the render-check is clean, the wording audit
returns zero, and the artifact URL is in the user's hands.

## Two faces, split by reading distance

Set anything read from across the room in the display face: headlines, bullets,
tile titles, chat mockups, figure captions. Set the notes strip in the body face
at ordinary size. The split is deliberate, and it is what keeps a deck from
reading like a web page at large sizes.

## The notes strip

Put every slide's detail in an `<aside class="notes">` **outside** the slide
panel, so it reads as annotation rather than content. Give the page a toggle
that hides all of them at once, and hide them automatically in present mode.

This is what makes one artifact serve both jobs. The projected view is clean;
the person reading the link alone still gets the substance.

## Present mode

Keep the **document** as the scroll container. Add `data-present` to `<html>`,
and let CSS do the rest:

```css
html[data-present]{ scroll-snap-type:y mandatory }
html[data-present] .unit{ scroll-snap-align:start; scroll-snap-stop:always }
html[data-present] .slide{ min-height:100dvh; scroll-margin-top:0 }
html[data-present] .notes, html[data-present] #controls{ display:none !important }
```

Request fullscreen but do not require it: an artifact runs in an iframe that may
refuse the API, and present mode must still snap one slide per screen so the
button never appears to do nothing. Bind `Esc` manually as well as listening for
`fullscreenchange`, because the no-fullscreen path gets no event.

Working implementation in the scaffold.

## Render-check

One screenshot, read once, before publishing.

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --hide-scrollbars \
  --screenshot=shot.png --window-size=1400,2400 --virtual-time-budget=4000 \
  "file://$PWD/deck.html"
```

Then Read `shot.png`. Also verify the script separately, since a syntax error
renders as a silently dead page:

```bash
python3 -c "s=open('deck.html').read(); print(s[s.index('<script>')+8:s.index('</script>')])" | node --check /dev/stdin
```

This step is not ceremony. In the session this skill came from it caught a
ghosted diagram that no amount of re-reading the source would have revealed.

## Publishing

The Artifact tool keys the URL to the **file path**. Republishing the same path
updates the deck in place; writing to a different path silently creates a second
artifact and strands the link already shared.

So: pick the path once, keep editing that file, and republish it. If you have
already written to a new path, move the file back to the original path before
publishing rather than publishing the new one.

Pass `favicon` only on the first publish. Omit it on every redeploy so the tab
icon stays stable.

## What did not work

| Approach | Why it failed |
|---|---|
| `filter: drop-shadow()` on SVG elements for a glow | On a tall scrolling page the filtered element composites at the wrong vertical offset and ghosts onto another slide. Get emphasis from accent colour and stroke weight instead. |
| A wrapper element as the present-mode scroll container | The existing `window` scroll listener stops firing, so the progress bar and slide counter die. Keep the document as the scroller. |
| `height: 100dvh` on a slide in present mode | Clips a dense slide on a short window. `min-height` lets it grow and snapping still lands correctly. |
| Nested `@media` inside a selector for the dark-theme tokens | Modern CSS nesting is not safe to rely on here. Write the media query as a separate top-level block. |
| Leading with commit counts, line counts and file counts | An internal audience wants the mechanism, not the metrics. Include volume numbers only when asked for them. |
| Naming an internal decision record on a slide | It means nothing to the audience. State the principle in plain words and leave the document reference to the notes, or drop it. |

## Common mistakes

- **Writing the deck as a document and shrinking it afterwards.** The face and
  the notes are different material with different word budgets. Draft them apart.
- **A diagram carrying every box in the system.** Draw only what the claim turns
  on. If the slide's claim is about fallback, the retry logic is not in the picture.
- **Numbered markers on content that is not a sequence.** Number a real order and
  nothing else.
- **Publishing without reading a screenshot**, on the grounds that the HTML is
  obviously correct.
