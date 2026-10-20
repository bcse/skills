---
name: write-pr
description: Write or revise PR titles and descriptions. Use when creating a PR, updating its description after code changes, or improving its explanation and visuals.
---

# Write a PR for reviewers

Make the change easy to understand at a glance: the problem, the new behavior, the main tradeoff, and the evidence. Describe the final patch for someone who has not seen the conversation.

## 1. Inspect the change and the existing explanation

Read the diff against the intended base, the repository's PR template, and the available validation results. For an existing PR, read its current body before drafting.

Apply `writing-for-human` for plain technical English. Its local guidance is sufficient for routine PR writing. Use familiar words, accurate software terms, and short labels; preserve code, commands, identifiers, and quoted output exactly. Formal ASD-STE100 certification or dictionary verification is outside this workflow unless the user requests it.

When updating a PR, carry forward each useful diagram, chart, table, image, and video. Update affected labels and values in place. Move supporting detail into an expandable section when it interrupts the main explanation. Replace an obsolete visual with one that answers the same reviewer question. Remove a visual only when it is incorrect, redundant, or the user requests removal; record the specific reason. Reduce repeated prose before removing useful visual information.

**Done when:** the final scope and evidence limits are known, and every existing visual has a disposition: keep, update, move, replace, or remove with a reason. A request to add results should preserve unaffected explanation and layout.

## 2. Choose what the reviewer should see

Choose the view before writing the long explanation. Images and videos are available for any PR, including backend, infrastructure, data, and tooling changes. Images need not be screenshots: draw a diagram, chart, or annotated trace as an image when precise layout matters more than inline editability. Choose the medium for what it explains, rather than the type of code changed. Follow explicit requests for visuals.

| What the change needs to explain | View to include |
| --- | --- |
| A lifecycle, ownership boundary, interaction, or data flow | Before/after diagram, sequence diagram, or flow sketch; draw it as a custom image (Graphviz, SVG, or HTML export) when layout matters |
| Measured benefits and costs | Before/after table with units, workload, and limits; add a generated chart image when the pattern matters |
| Branches, decisions, or a small code transformation | Pseudocode or a conceptual diff |
| Behavior over time, such as memory release, retries, a migration, or a CLI workflow | Short video, GIF, or annotated sequence of frames |
| UI appearance or interaction | Screenshot comparison or a short recording |
| One simple behavior that a sentence fully explains | A short sentence; add a visual only if it adds information |

Use the smallest view that answers the question. Different views should explain different things. For example, a process diagram explains memory ownership; a measurement table shows memory and latency.

For tree examples, custom diagram images, videos, screenshots, or attachment handling, read [Visual reference](references/visuals.md) when using that format.

**Done when:** each main behavior change has a clear explanation format, and measured benefits appear beside their costs and uncertainty.

## 3. Draft the visible explanation first

Follow the repository's template. Otherwise use this reading order:

1. **Summary:** one short paragraph stating the concrete problem and resulting behavior. Start the body here; the PR page already shows the title, draft state, and size, so do not put a summary table before it. Link related issues with closing keywords such as `Fixes #123`, and include the context a reader needs without opening them.
2. **What changes:** the main visual with a short caption. Let it carry the flow or structure; use prose for decisions and facts it cannot show.
3. **Results and tradeoffs:** a compact comparison when measurements exist. Keep operational changes, breaking changes, and material limits visible.
4. **Validation:** commands actually run, observed results, and relevant environment or revision. Distinguish completed checks from proposed work.

Omit sections that add nothing: a small fix may need only Summary and Validation. Keep the core diagram, when the change needs one, and the key results visible. Put long reviewer guides, secondary diagrams, raw measurements, and extended rationale in `<details>` sections or linked references. Use named table headers and short cells. Use prose for reasoning rather than putting paragraphs into table cells.

Use a Conventional Commit title: `type(scope): Imperative description`, as in the `conventional-commits` skill. Scope is optional; mark breaking changes with `!`. Match the final scope, keep it near 50 characters, start the description with a capital letter, and omit the final period.

Keep validation claims tied to evidence. Mock tests, live tests, and production observations are distinct. Mark checklist items complete only after the work is complete; omit empty boilerplate.

Claim TDD only when execution records establish the sequence. Report the test and command run before the implementation with the failure that shows the missing behavior (an unrelated setup failure does not count), then the same test passing afterward, then any refactor with the checks that passed after it. Describe tests added after the implementation as regression coverage. If the sequence is unknown, say it is unverified. Do not invent earlier failures, logs, or test counts.

**Done when:** the summary, the main visual (if the change needs one), and the key results explain the change without opening supplementary sections or reading the authoring conversation.

## 4. Render and inspect

Check every visual against the final diff: before/after labels, arrows, order, ownership, values, units, and failure paths. Label simplified views as conceptual.

Choose a renderer that preserves readability. Mermaid suits simple flows and stays editable in the PR. When the layout is dense or the explanation needs charts or precise grouping, draw a custom image instead.

When using Mermaid, render every block with the skill's `scripts/render_mermaid.mjs`, from a repository with `@playwright/test`:

```sh
node <write-pr-skill-directory>/scripts/render_mermaid.mjs <body.md> [output-directory]
```

Open every rendered PNG. Inspect it at the width it will occupy in the PR. Fix tiny text, overly wide flows, clipped labels, and unclear grouping, then render and inspect again. Use compact before/after columns or separate views when a long row becomes unreadable. Syntax success alone does not complete this step. For other formats, inspect the actual image, recording, or rendered preview.

Run a glance check on the body: from the headings, visible visuals, and short captions, can a reviewer identify what changed, why it matters, its main cost, and what was tested? Put missing answers in the visible explanation and remove repeated prose.

**Done when:** every visual is both accurate and readable, and the glance check passes. If rendering is unavailable, preserve the visual source and state that visual verification is incomplete; resolve the rendering blocker before presenting it as verified.

## 5. Deliver or publish the requested update

For a draft-only request, return the draft and local artifacts. For an authorized PR update, publish the revised title and body, then read them back to confirm the visuals, tables, results, and limitations survived the update.

**Done when:** the delivered draft or saved PR matches the inspected version. Report the link and any material verification gap briefly.
