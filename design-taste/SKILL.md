---
name: design-taste
description: Aesthetic judgment for visual artifacts — web UI, slides, posters, dashboards, charts, documents, diagrams. Use when visual styling or critique is part of the requested outcome — requests to make something look better, more professional, less generic, or more polished; restyling or theming existing work; design reviews and feedback ("why does this look off?"); or creating an artifact whose appearance matters to the ask. Acts as the judgment layer on top of medium-specific skills (slides, docs, charts, frontend), which keep owning mechanics and output format. Skip it for content-only or purely functional edits where appearance isn't in question.
---

# Design Taste

Taste feels like mystique, but it decomposes into three learnable moves:

1. **Commit** to one clear direction instead of averaging safe defaults.
2. **Execute** with a small, consistent system — few typefaces, few colors, one spacing scale.
3. **Diagnose** — look at the result, name what is off, and fix the biggest lever first.

Most bad design is not a wrong direction; it is the *absence* of one, plus inconsistency in the fundamentals. Fix those two things and almost any artifact looks intentional.

## Scope and routing

This skill judges and shapes; it does not replace medium expertise.

- **Medium-specific skills lead the build.** Slide, document, spreadsheet, chart, and frontend skills own structure, mechanics, and output format. Run them for the build; apply this skill as the pass over direction, system, and the four checks. For web UI specifically, let a frontend-design skill (when available) drive ideation and direction — this skill supplies the craft rules and the critique.
- **Specifications beat heuristics.** An explicit design system, brand guide, or template in the request overrides every default and preference here. Taste fills the gaps a specification leaves open; it never overrules one. The only thing that outranks a specification is an accessibility requirement — see Fallbacks.
- **Stay out of non-visual work.** Do not activate for content-only or correctness edits — fixing a formula, editing copy for meaning, refactoring logic — where nothing about appearance is in question.

## Workflow when creating something visual

Use this workflow for a new artifact or broad redesign. For a local styling change, inherit the existing direction and tokens, then change and inspect only the affected area.

**1. Direction — before any pixels or code.**
Name the direction in 2–3 adjectives ("warm, editorial, unhurried" / "dense, technical, precise") plus one reference world the subject actually lives in (lab notebooks, transit signage, vinyl sleeves, terminal UIs). If you cannot state the direction in one sentence, you do not have one yet — and no amount of styling will hide that. Derive it from the subject and audience, not from what is easy to render.

**2. System — tokens before layout.**
Commit to: 1–2 typefaces with a type scale ratio, a palette of neutrals + one accent (two max), one spacing scale, one corner radius pair (small + large), one separation strategy (borders OR shadows OR background shifts). Writing these down first is what prevents drift — every later decision becomes a lookup instead of a fresh choice.

**3. Execute.**
Build with the system. When a value is not on the scale, that is a bug, not an adjustment. For detailed decisions (pairing type, tuning shadows, chart styling, per-medium rules for slides vs posters vs documents), read `references/fundamentals.md`.

**4. Check the requested result.**
For a local change, inspect the affected area and relevant requirements. For a new artifact or broad redesign, use the four checks below. Fix and re-check only unresolved requirements or defects that affect the requested outcome; do not restart a full critique for each small adjustment.

A condensed end-to-end pass of this workflow — and of the critique protocol — is in `references/worked-examples.md`.

## The four checks

**Squint test.** Blur the artifact (mentally, or actually screenshot and blur). Does exactly one thing dominate? Do related items still read as groups? If everything blurs into even gray noise, hierarchy is missing; if three things fight for attention, de-emphasize two — muting the losers works better than amplifying the winner.

**Inventory count.** Count distinct typefaces, text sizes, colors, spacing values, corner radii, icon styles. Refined work uses startlingly few of each (often 2 faces, 4–5 sizes, 5–6 colors, 6–8 spacing values, 2 radii). High counts predict the vague "something's off" feeling more reliably than any single flaw, because every extra value is a small broken promise of consistency.

**Alignment sweep.** Trace the left edges, top edges, and baselines. Fewer alignment lines = calmer page. Anything off by a few pixels, or centered while its neighbors are left-aligned, gets snapped to the grid. Check optical alignment for icons and asymmetric shapes — visually centered beats mathematically centered.

**Swap test.** Could this artifact belong to any other product, topic, or company with only the logo changed? If yes, the direction never made it into the work. The fix is rarely "add more decoration" — it is pulling one signature element from the subject's own world and letting everything else stay quiet.

## Requirements, defaults, and preferences

Three strengths of rule live in this skill, and confusing them is itself a taste failure: treating a preference as law produces rigidity; treating a requirement as taste produces harm.

**Requirements — verify these, never trade them away**

| Check | Bar |
|---|---|
| Text contrast | 4.5:1 body · 3:1 large text & UI elements — computed, not eyeballed |
| Motion | reduced-motion preference respected |
| State encoding | never by color alone — pair with label, icon, or weight |
| Chart honesty | bar axes start at zero; a zoomed line axis is disclosed |

**Defaults — start here, adapt to context**

| Decision | Default |
|---|---|
| Type scale ratio | 1.2 dense UI · 1.25–1.333 editorial · ~1.4+ slides |
| Body text | ≥16px web · line-height 1.5–1.7 · 45–75 char measure |
| Headings | line-height 1.1–1.25 · letter-spacing −1% to −3% when large |
| All-caps labels | letter-spacing +4% to +10% · never loosen lowercase body |
| Spacing scale | 4/8/12/16/24/32/48/64 (double it for slides & posters) |
| Grouping | gap inside a group ≤ ½ the gap between groups |
| Palette | neutrals do the work · ~60/30/10 · accent only on what matters most |
| Shadows | small y-offset · blur ≈ 2–3× offset · ≤10% opacity · one light source |
| Motion | 120–250ms micro · 250–400ms transitions · ease-out in, ease-in out |

**Preferences — house style; a stated direction or brand system wins**

| Preference | Instead of |
|---|---|
| Near-black on near-white (≈#1A1A1A on ≈#FAFAF8) | pure black on pure white |
| Temperature-tinted neutrals | pure grays |
| One small + one large corner radius | per-component radii |

## Fallbacks and limits

- **Judge rendered output whenever the environment allows** — render or screenshot before critiquing. Rendering catches what markup review cannot: optical alignment, typographic texture, trapped whitespace, real color interaction.
- **When only code or markup is available**, critique what the code determines (scale consistency, token counts, spacing values, structure), say plainly that the review is code-level, and name what still needs a visual pass.
- **Never state a measurement you did not take.** Compute contrast ratios (or run a checker) before citing one; otherwise write "verify contrast," not "passes contrast." The same discipline applies to any pixel, ratio, or size claim.
- **When brand conflicts with accessibility, accessibility wins** — but by changing usage (a darker shade of the brand hue for text, the pure brand color for fills and graphics) and flagging the conflict, never by silently redesigning the brand or silently shipping the failure.
- **Missing context is not a blocker.** Unknown audience, medium, or stage: state the assumption being judged against in one line, then proceed.

## When critiquing someone else's design

Do not free-associate observations. For a broad critique, read `references/critique.md` and follow its protocol: context first, first-impression capture, the four checks, then leverage-ordered passes, then at most three prioritized fixes phrased as observation → effect → cause → concrete change. For a focused question, inspect only the affected area and relevant checks; stop when the question is answered with evidence. Feedback that cannot be acted on without a follow-up question is not finished.

## When something "looks AI-generated" or amateur

Read `references/anti-patterns.md`. It is a diagnostic table of the recognizable tells — the default-gradient hero, the identical card grid, emoji-as-icons, uniform 16px gaps, rainbow charts — each with why it fails and the specific fix. Use it both to repair existing work and as a final scan of your own output.

## Reference files

- `references/fundamentals.md` — the craft layer: hierarchy, typography, spacing, color, depth, motion, charts, and per-medium rules with concrete numbers. Read when making detailed styling decisions or when a check fails and you need the underlying rule.
- `references/anti-patterns.md` — recognizable failure patterns and their fixes. Read when diagnosing work that feels generic, cluttered, or off.
- `references/critique.md` — the review protocol, critique vocabulary, and how to phrase feedback. Read for a broad critique, or consult relevant sections when needed for a focused design question.
- `references/worked-examples.md` — one complete creation pass and one complete critique pass. Read to calibrate how the workflow, checks, and three-fix limit compose end to end.
