# Detailed Image Analysis for Prompt Synthesis

Collect visual evidence internally for the resolved operation from SKILL.md. This reference defines fidelity and inspection coverage; SKILL.md defines conflict resolution, input questions, and final output.

## Fidelity before brevity

The goal is reproducibility. Capture every unique, visually supported detail that materially controls whether a generated result resembles the source. Salience determines ordering and emphasis, not permission to discard evidence. Optimization may merge duplicated wording, but it must not silently delete distinct subject, wardrobe, pose, environment, composition, lighting, palette, text, or style information merely to make the prompt shorter.

For a complex image, expect a detailed prompt with multiple labeled prose sections. A substantially shorter prompt is a warning sign unless the source itself is visually simple.

## Confirm visual access

- Verify that the actual image is viewable. A filename, inaccessible link, alt text, placeholder, or mention of an image is not visual access.
- Inspect the rendered image at the highest useful detail. Zoom into faces, hands, clothing construction, accessories, text, products, interfaces, and small background elements.
- If the required image is unavailable, follow the missing-input rule in SKILL.md.
- If blur, crop, or resolution hides a detail, use the broadest supported description or omit that single uncertain attribute. Do not let one unclear detail reduce coverage elsewhere.
- Record the visible orientation and aspect ratio accurately. State pixel dimensions only when known from the file.

## Build a complete visual brief

Cover every applicable category below. Adapt person-specific fields to the equivalent properties of products, animals, food, landscapes, illustrations, diagrams, or interfaces.

### 1. Subject or primary object

- Count, category, apparent age range, physique or overall form, proportions, scale cues, and distinguishing silhouette.
- Face shape, jawline, cheekbones, nose, mouth, lips, brows, and other prominent geometry.
- Eye color when supported, eye shape, gaze direction, eyelid tension, and focal target.
- Hair color, length, cut, texture, parting, direction, dampness, flyaways, and styling.
- Skin tone, undertone, texture, perspiration, dirt, freckles, makeup, scars, abrasions, or other visible marks.
- Expression and emotional read, described through visible facial evidence rather than generic mood words alone.

For objects, replace facial fields with geometry, construction, material, surface finish, wear, labels, controls, and distinctive components.

### 2. Wardrobe and accessories

Describe every visible garment separately: type, color, material, weight, pattern, fit, neckline, sleeve and hem treatment, seams, panels, pockets, fasteners, hardware, wrinkles, damage, dirt, and placement. Describe each accessory or carried object with its material, shape, color, construction, exact location, attachment, and visible interaction with the subject. Include small identity-bearing details such as watch cases, straps, bracelets, eyewear, jewelry, bags, holsters, tools, or weapon components when visible.

### 3. Pose, gesture, and action

Describe torso direction, head turn, eyeline, shoulder tension, spine angle, hip height, stance, weight distribution, knee bend, and direction of movement. Account for each visible arm, hand, and leg separately: joint angles, hand shape, contact points, what is obscured, and what the body appears ready to do. Preserve awkward, transitional, or asymmetrical poses instead of normalizing them into a generic stance.

### 4. Scene and environment

Describe the setting, architecture, terrain, surfaces, furniture, props, structures, openings, and small background objects. Record materials, construction, wear, grain, cracks, stains, grime, moisture, reflections, and weather. Preserve foreground, middle-ground, and background layers, plus object counts and spatial relationships. Include distinctive secondary evidence—such as a rope entering a corner, repeated windows, a dark doorway, or a blurred stool—when it helps reconstruct the same frame.

### 5. Composition and camera

Record orientation, apparent aspect ratio, shot type, crop boundaries, camera height and angle, subject placement, relative scale, symmetry or imbalance, negative space, leading lines, repetition, framing devices, overlap, occlusion, and tonal separation. Describe what is sharp and what is blurred, the apparent depth of field, perspective character, and any lens-like visual cue. Use numerical lens or aperture values only when the user supplies them or the value is necessary as a creative translation; do not present guessed numbers as observed fact.

Describe composition as relationships, not an unordered object list. Preserve unusual crops, empty space, and visual imbalance when they define the source.

### 6. Lighting

Describe source type, direction, height, softness, diffusion, intensity, color temperature, contrast ratio, highlight placement, shadow placement, edge hardness, reflections, rim light, and background exposure. State how light behaves separately on skin, fabric, metal, glass, wood, and other important materials. Preserve relationships such as a bright subject against a substantially darker background.

### 7. Color, mood, and atmosphere

Describe the dominant palette, accent colors, saturation, contrast, color distribution, haze, dust, weather, and atmospheric depth. Ground mood in visible evidence: pose, light, environment, texture, and color.

### 8. Medium and finish

Name the visual medium and production character: natural photograph, cinematic still, editorial image, product photograph, 3D render, flat illustration, painting, print, collage, interface, or another form. Capture filmic contrast, grain, bokeh, line weight, shading, rendering quality, post-processing, surface texture, believable imperfections, or other finish cues that distinguish the image.

### 9. Text, graphics, and interfaces

Transcribe clearly legible text exactly, including spelling, case, punctuation, and line breaks. Record typography, hierarchy, alignment, spacing, placement, signage, labels, icons, and graphic shapes. Do not invent unreadable copy. For interfaces, include the screen type, regions, navigation, panels, active controls, selected or error states, density, spacing, and component relationships.

Do not identify an unknown real person. Do not infer a franchise, named location, occupation, character role, story context, or specific kind of place from recognition alone. Describe only visible evidence needed for the target image; when context is uncertain, prefer neutral wording such as “weathered timber structure” over an unsupported label such as “ship.”

## Apply the resolved operation

Use image evidence for details the user leaves unspecified, within each image's assigned role. For edits, build explicit change and preserve sets. Carry preserved identity, geometry, pose, layout, viewpoint, lighting, palette, text, and environment into the prompt at their original level of detail.

## Fidelity transfer check

Before writing the answer, make a private coverage pass across all applicable categories. Every unique high-confidence observation must be carried into the prompt, deliberately merged with an equivalent phrase, or omitted for a specific reason such as irrelevance to the requested change. Never drop a detail solely because the prompt is already long.

Finish when every applicable category is accounted for. Organize the checked evidence using the output structure selected in SKILL.md.
