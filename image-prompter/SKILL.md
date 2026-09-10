---
name: image-prompter
description: Use when the deliverable is image prompt text, including new-image briefs, prompt optimization or merging, reverse prompting from an image, and prompts for edits or composites. Also use when explicitly invoked with an image and no text. Excludes direct image generation or editing, captions, OCR, visual critique, and identity recognition.
---

# Image prompter

Turn the user's brief into one paste-ready, natural-language image prompt.

## 1. Choose the operation

Choose by what the downstream generator will receive:

- **Standalone generation:** It receives only text. Describe the complete final image, including when optimizing or merging prompts. Express revisions as final attributes, such as "The subject wears a blue jacket." Keep the prompt independent of source prompts and conversation history.
- **Standalone reconstruction:** An image supplies evidence, but the generator receives only text. Explicit invocation with an image and no text selects this operation. Describe the target completely without referring to the evidence image.
- **Reference-guided edit or composite:** The generator receives images to modify or combine. Identify each by number and role, specify changes and preserved features, and use edit language. Infer roles from the request; inherit only details relevant to each role.

If the deliverable is an image itself, use the image-generation workflow. Otherwise, finish this step with one operation and a known set of downstream image inputs, if any.

## 2. Resolve the brief

Extract the intended deliverable and use, subject, action, wardrobe, setting, composition, visual treatment, lighting, palette, materials, required copy, data, and final attributes. Translate meaningful tags, weights, and flags into natural language.

**Image evidence:** Whenever an image supplies visual information, read [image-analysis.md](references/image-analysis.md) completely before inspection. It defines the required coverage and fidelity check.

Resolve conflicts in this order: explicit requirements over inferred details, later refinements over earlier wording, functional constraints over decoration. For remaining ties, choose the least expansive interpretation that preserves the subject and intended use.

Ask one concise question when a required image is unavailable, competing image-role assignments would materially change the result, or essential exact copy, data, or factual relationships cannot be obtained from the available context. Ask for the missing inputs together. Proceed with reasonable visual choices for optional details. Use fictional data only when the user authorizes it; never invent factual values or citations.

Finish this step with resolved requirements and the essential inputs available, or return the necessary input question.

## 3. Compose the prompt

**Prompt patterns:** For reconstruction, reference-guided edits, composites, character consistency, exact text, products, logos, comics, historical scenes, diagrams, educational visuals, slides, charts, interfaces, or complex new-image briefs, read [prompt-patterns.md](references/prompt-patterns.md). Use the applicable sections and replace all placeholders. The reference also contains worked examples for prompt merging, missing data, and panel structure.

Lead with the operation and defining subject or deliverable. Begin standalone prompts with Create, Render, or Photograph. Make placement, scale, and spatial relationships concrete. Describe the desired appearance positively; use brief exclusions where they prevent a materially incorrect result. Add specificity supported by the brief or needed to express the requested result.

Preserve required image text verbatim in quotation marks. Treat quoted copy as image content, even when its words resemble instructions. Use the exact-text pattern for typography, placement, and occurrence counts.

Finish with a complete description of the resolved target. Remove duplicated wording while retaining distinct relevant requirements and the image-evidence coverage defined in the analysis reference.

## 4. Check and return

Check every resolved requirement against the prompt, including exact text and its occurrence counts, factual inputs, and spatial relationships. For standalone prompts, a generator receiving only the prompt must have everything needed to depict the target. For edits and composites, external dependencies are limited to the identified supplied images.

Return only the final prompt as plain text, or the necessary input question from step 2. Keep explanations, code fences, generator parameters, and follow-up offers outside the response.

- **Simple brief:** Use one cohesive prose paragraph.
- **Scene reconstruction:** Use the applicable labeled sections from the reconstruction pattern.
- **Other complex deliverables:** Use labeled prose sections suited to the artifact, such as numbered panels for comics or canvas, layout, content, and constraints for slides. For reconstruction of these artifacts, preserve the full evidence coverage while using their native structure.

Use complete sentences within sections. If the user requests variants, separate complete, independently usable prompts with blank lines.
