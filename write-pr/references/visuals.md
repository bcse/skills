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

Mermaid, Graphviz, or a diagram editor can all work. Prefer the format that stays readable in the PR. Use short labels, explicit before/after headings, and only the nodes needed to explain the behavior. Keep meaningful failure paths visible in the diagram or its caption.

Follow the render-and-inspect step in `SKILL.md` for every diagram. In Mermaid, use `#35;` for a literal `#` in a label. GitHub's Mermaid version can differ from the local renderer.

## Custom images

Use images for architecture, process boundaries, memory ownership, data transformations, performance charts, annotated traces, or any explanation that benefits from precise layout. They are not limited to UI screenshots.

When Mermaid creates cramped labels, awkward routing, or a weak before/after comparison, use Graphviz, a diagram editor, or a custom SVG/HTML drawing exported as an image. Choose the tool for layout control and legibility. Follow the same accuracy and render checks as for inline diagrams.

Give the image a clear reading order, short labels, and a caption stating the main result. Use consistent scales and comparable states in before/after charts. Include useful alt text and retain editable source when it helps later updates.

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
