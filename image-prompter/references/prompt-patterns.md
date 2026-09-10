# Natural-Language Prompt Patterns

Use the applicable patterns below to organize the resolved brief. Bracketed fields are placeholders and code fences mark examples in this reference. Apply the output contract in SKILL.md to the final answer.

## New image

```text
Create a [orientation and use-case] image of [specific subject] [action or state] in [setting]. Frame the scene with [composition, viewpoint, placement, and depth]. Render it as [medium and visual treatment], lit by [lighting] with [palette, material, texture, and atmosphere]. Include [essential details] while keeping [critical exclusion] out of the scene.
```

Use one primary visual language and only a few supporting cues. Resolve incompatible style requests instead of stacking them.

## Standalone reconstruction from image evidence

For scene reconstruction, organize the evidence collected with image-analysis.md into these sections. For a comic, slide, diagram, or interface, organize the same evidence by panels or layout regions instead.

```text
Create a [orientation and aspect ratio] [medium or deliverable] showing [one-sentence subject, action, setting, and style gist].

Subject: [Complete appearance or physical construction, including distinctive geometry, surface, face, eyes, hair, skin, expression, and condition where applicable.]

Wardrobe and accessories: [Every visible garment, material, fit, construction detail, wear pattern, accessory, and carried object.]

Pose and gesture: [Torso, head, gaze, shoulders, each visible limb and hand, stance, weight, movement, interaction, and occlusion.]

Environment: [Setting, architecture, materials, wear, foreground, middle ground, background, repeated structures, openings, and distinctive secondary objects.]

Composition and camera: [Crop, shot type, camera height and angle, subject placement, negative space, framing, visual rhythm, perspective, focus plane, depth of field, and aspect ratio.]

Lighting: [Source, direction, softness, temperature, highlight and shadow placement, material response, background exposure, and subject-background separation.]

Mood and style: [Atmosphere, palette, medium, realism, texture, grading, contrast, grain, and finish.]

Constraints: [Only evidence-based exclusions that prevent a known failure.]
```

Use the applicable sections and adapt person-specific fields to the subject.

## Image edit

```text
Edit the supplied image by changing only [target] to [requested result]. Preserve [identity or form, pose, composition, background, viewpoint, lighting, palette, layout, text, and surrounding objects]. Integrate the change with matching scale, perspective, focus, material texture, reflections, and shadows so it belongs naturally in the original image.
```

Name both the change and the important invariants. Avoid vague instructions such as “keep everything the same” when drift would be costly.

## Multiple-reference composite

```text
Use the first image as the base [scene or composition], the second as the reference for [subject or object], and the third as the reference for [visual role]. Create [desired result] by placing [element] at [location and scale], preserving [base invariants] and matching perspective, lighting, shadows, color, focus, and texture across the composite.
```

Assign each reference one clear role by default. If the user explicitly assigns a reference multiple roles, honor them without inheriting unrelated content.

## Exact text or localization

```text
Create a [poster, package, sign, diagram, or interface] featuring the exact text “[TEXT]” [occurrence count] with [typographic character, weight, case, color, and scale] at [precise placement]. Preserve the wording, spelling, punctuation, hierarchy, alignment, and spacing exactly, with no added copy. [For localization: Replace only “[SOURCE TEXT]” with “[TARGET TEXT]” while preserving every other visual element and the original layout.]
```

Specify the occurrence count for each required string. Use the requested or visibly supported count; otherwise use once for a standalone headline or tagline. For repeated labels or patterns, define the repetition by region or element. For multiple strings, give each string, count, and placement in a separate prose sentence. Include only the applicable localization sentence. For dense or production-critical copy, keep text large and visually distinct enough to verify in the generated result.

## Product or branded object

```text
Create a [use-case] image of [product] shown [position and angle] on [surface or setting]. Preserve [shape, proportions, packaging geometry, label, and exact text]. Use [lighting setup] to reveal [materials, texture, transparency, reflections, and contact shadows], with [background and palette] and enough negative space for [intended layout need]. Add no unrequested branding or copy.
```

## Diagram, infographic, or educational visual

```text
Create a [diagram or infographic] for [audience and purpose] on a [orientation] canvas. Organize it into [sections or regions] with [hierarchy, flow, axes, arrows, or legends]. Use the exact labels and data “[CONTENT]”, readable typography, consistent spacing, clear alignment, and [visual system]. Depict only the supplied facts and keep relationships unambiguous.
```

Include the lesson objective, required components, and factual relationships. For educational visuals, favor consistent icons, clear arrows, readable labels, and enough white space to scan the concept. Put the resolved facts, labels, and numbers directly in the prompt. Resolve missing factual inputs through step 2 of SKILL.md.

## Interface mockup

```text
Create a realistic interface mockup for [product and platform] showing [specific screen or workflow]. Arrange [navigation, content regions, controls, and actions] with [density, hierarchy, spacing, and alignment], and show [realistic labels, data, and the relevant empty, loading, error, or success state]. Use [typographic, color, and component treatment] so the interface is coherent, readable, and ready for production rather than decorative concept art.
```

## Character consistency

```text
Use the supplied character as the visual anchor, preserving [face and body proportions, hairstyle, age range, outfit, palette, and distinctive traits]. Show the same character [new action] in [new setting], changing only [pose, action, expression, or environment] while keeping the character immediately recognizable. Match the established [medium, line treatment, lighting, and rendering finish].
```

Describe visible identity traits without trying to identify an unknown real person.

## Reusable logo

Describe the brand, audience, and defining shapes. Specify a strong silhouette, balanced negative space, and legibility at small and large sizes. Prefer simple shapes and minimal strokes when the brief calls for a reusable mark. Define placement and padding. For a transparent logo, request a fully transparent background with clean edges and no solid backdrop or drawn checkerboard. Apply the exact-text pattern to a wordmark. Describe vector-like appearance when appropriate without promising a vector file.

## Historical scene

Use the supplied place and date as context, with period-appropriate clothing, staging, and surroundings. Distinguish user-supplied context from visual evidence; image reconstruction alone does not establish an event or location. Resolve essential factual uncertainties through step 2 of SKILL.md.

## Comic or storyboard

Specify the panel count, arrangement, and reading order. Give each numbered panel one concrete visual beat with its action, framing, setting, and any exact dialogue. State recurring character traits once for the whole strip, then describe each panel's changes. Preserve the supplied narrative sequence.

## Slide or chart

Name the deliverable and define its canvas, layout regions, hierarchy, and visual system. Place the resolved title, labels, numbers, units, and supplied source notes directly in their regions. For charts, specify chart type, axes, series, and value-to-label mapping. For slides, specify orientation and reading order. Require readable type and spacing appropriate to the intended display size. Resolve missing factual inputs through step 2 of SKILL.md.

## Worked examples

### Merge revisions into final attributes

Input: "A red mug on a wood table, morning window light. Update the mug to blue and use a square crop. Return the prompt."

Output:

Create a square photograph of a blue mug on a wooden table, lit by morning light from a window.

### Request essential data

Input: "Write an image prompt for a chart of our quarterly revenue this year." No revenue data is available in the context.

Output:

What revenue figures, currency, and year should the chart show for each quarter?

### Organize a comic by panels

Input: "Write a prompt for a vertical three-panel comic. A child plants a seed, waters it, then sees a sprout. Red overalls throughout. No dialogue."

Output:

Create a vertical three-panel comic read from top to bottom. Show the same child wearing red overalls in every panel, with no dialogue or captions.

Panel 1: The child places a seed into a small hole in the soil of a flowerpot.

Panel 2: The child gently waters the soil in the same flowerpot.

Panel 3: The child looks at a small green sprout emerging from the soil in the flowerpot.

## Generation guidance source

The generation patterns draw on the [Generate images section of OpenAI's image prompting guide](https://developers.openai.com/api/docs/guides/image-prompting#generate-images). API settings and output inspection belong to the downstream generation workflow.
