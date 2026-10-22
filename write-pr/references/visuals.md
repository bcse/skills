# Visual reference

Use the format that answers the reviewer's question. Keep names consistent with the patch and put each view beside the explanation it supports.

## Decisions and small transformations

A conceptual diff makes a changed condition easy to see:

```diff
 on save(content)
-  persist content
+  if content equals stored content
+    return existing result
+  persist content
+  clear cached content
   return saved result
```

For mostly new logic, show the complete decision path in pseudocode. Include inputs, branches, effects, and results. Exact source is useful only when its implementation details are the review question.

## Calls, components, and files

Use a call tree for a simple sequence:

```text
submitForm
  createSession
    persistPrompt
    launchAgent
  navigateToSession
```

Use a component tree to show ownership:

```text
SessionPage (owns session state)
  useSessionEvents()
  SessionToolbar
    RunSkillButton
  SessionTimeline
```

Use a shallow file tree when responsibilities move:

```diff
 src/
 ├── commands/       # parses user actions
 ├── sessions/       # owns session state
-└── transport.ts    # sends requests and receives events
+└── transport/
+    ├── client.ts   # sends requests
+    └── stream.ts   # receives events
```

Trees cannot show every branch or asynchronous interaction. Use a sequence or flow diagram when timing, decisions, or failure paths matter.

## Diagrams

| Reviewer question | Mermaid view |
| --- | --- |
| What moves where, or which decision selects a path? | `flowchart` |
| Who calls whom, and in what order? | `sequenceDiagram` |
| Which states and transitions change? | `stateDiagram-v2` |

Mermaid, Graphviz, or a diagram editor can all work. Prefer the format that stays readable in the PR; a flow with stages reads best as a fixed SVG (see Custom images). Use short labels, explicit before/after headings, and only the nodes needed to explain the behavior. Keep meaningful failure paths visible in the diagram or its caption.

Follow the render-and-inspect step in `SKILL.md` for every diagram. In Mermaid, use `#35;` for a literal `#` in a label. GitHub's Mermaid version can differ from the local renderer.

## Custom images

Use images for architecture, process boundaries, memory ownership, data transformations, performance charts, annotated traces, or any explanation that benefits from precise layout. They are not limited to UI screenshots.

When Mermaid creates cramped labels, awkward routing, or a weak before/after comparison, use Graphviz, a diagram editor, or a custom SVG/HTML drawing exported as an image. Choose the tool for layout control and legibility. Follow the same accuracy and render checks as for inline diagrams.

Give the image a clear reading order, short labels, and a caption stating the main result. Use consistent scales and comparable states in before/after charts. Include useful alt text and retain editable source when it helps later updates.

### Fixed SVG

A fixed SVG suits a multi-stage flow. Mermaid lays a long chain out as one tall column; an SVG puts the stages side by side and looks the same in every theme.

- **Panel:** draw on its own opaque background, with a thin border and rounded corners, so the image reads the same on a light or a dark page.
- **Size:** set a `viewBox` about 1100 to 1200 units wide with matching `width` and `height`, and keep text at 13 units or larger so it stays readable at the PR's content width.
- **Fonts:** use system stacks, such as `-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif`, and a monospace stack for code. GitHub shows the file as an image, which cannot load web fonts.
- **Layout:** one labelled panel per stage, left to right, with the boxes top to bottom inside it. Put the arrow between stages on the header row, where it reads as stage to stage.
- **Meaning:** tell steps from checks with colour and a legend that states what a failed check does.
- **Accessibility:** add `<title>` and `<desc>` inside the SVG, and alt text on the Markdown image.
- **Source:** the SVG is its own source. Write it by hand, or with a throwaway generator in the scratch directory.

Show it with `scripts/rasterize_svg.mjs` and open the light and the dark PNG. Check the order, every label, and that no text touches a box edge. Keep the SVG out of the repository unless the user asks for it there; the attachment is the published copy.

## Videos and animated sequences

Use a short video or GIF when timing or change over time carries the explanation: a worker starts and exits, memory falls, retries recover, a migration progresses, or a CLI workflow completes. An annotated sequence of still frames is useful when the reader needs to compare stages.

Show one scenario, trim waiting time, label important events, and make the explanation understandable without sound. Give the clip a short caption with the outcome so the PR remains useful at a glance. Watch the full exported clip to check timing, labels, and the final state.

## Evidence and illustrations

Use actual captures or recordings when claiming observed behavior, whether from a UI, terminal, trace, or profiling tool. Label explanatory animations, mockups, and conceptual diagrams as illustrations; they explain a model but do not prove the implementation works. Keep measured values traceable to their source.

For UI changes, capture comparable before/after states and focus the viewport on the changed behavior.

## Attachments

When uploading an attachment, check GitHub's current attachment documentation for supported formats, size limits, and upload contexts. A supported file type may still need a separate image preview to be readable inline.

Upload through the available GitHub attachment control or a supported CLI capability. Use the returned URL and verify access. A local file path is not an uploaded attachment. For draft-only requests, provide local artifacts and mark their intended positions.

Embed the uploaded main image or video beside its explanation in the PR body, with a caption or static preview. Use supplementary attachments for larger views and editable source files. Public-repository attachments can be public, so preserve the repository's intended audience.

### Attach an image with `gh`

`gh pr edit` uploads images and rewrites the body's reference to the upload. SVG files upload as images.

1. Put the image next to the body file and reference it as `![alt text](./diagram.svg)`. A `#` in the body reference stops the rewrite, and `gh` then appends a duplicate image.
2. Publish with the alt text on the flag: `gh pr edit N --body-file body.md --attach './diagram.svg#alt text'`. Run it from the body file's directory.
3. Read the body back with `gh pr view N --json body`. It holds one `user-attachments` URL per image, no `./` paths, no appended duplicates, and unchanged text elsewhere.
4. Download the asset to confirm it. The first request, sent with the `gh auth token`, answers with a redirect. Fetch the `Location` URL without the token, because forwarding it makes the storage host answer 403. Expect `image/svg+xml` and a file that `cmp` matches to the source.
