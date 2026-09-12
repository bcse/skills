# Auditing and migrating prompts to GPT-5.6

Use the relevant sections when auditing or migrating an existing prompt to GPT-5.6. For a text-only revision, perform the audit and return the requested text. Run empirical evaluation only when requested, with available and authorized tools, data, and budget.

Contents:
1. The audit pass
2. The removal loop
3. Migrating from GPT-5.4 / 5.5
4. Migrating from Claude- or Gemini-shaped prompts
5. What to measure
6. Reporting the result

---

## 1. The audit pass

Read the prompt once and tag every line into one of four buckets.

**Keep** — domain context the model can't infer, hard constraints, approval boundaries, success criteria, output schema, examples that encode a real product requirement.

**Move to a parameter** — anything trying to control reasoning depth, global verbosity, or cross-turn memory with words. See `api-parameters.md`.

**Consolidate** — rules stated in more than one place. Pick the section that owns the rule; delete the other instances. Duplicates cost tokens and create contradiction risk.

**Cut** — decorative identity ("world-class," "expert"), step-by-step recipes for tasks the model can infer, tools exposed just in case, redundant few-shot examples, scattered "be concise," scattered "ask first," persistence boilerplate ("keep going until the query is fully resolved") that 5.6 no longer needs to be told.

Flag two things specifically, because they're the most common 5.5 holdovers that actively hurt:

- **Brevity instructions.** GPT-5.6 is terser by default than 5.5. "Be concise" may now be unnecessary, and in some tasks pushes output past useful. Test removing it; if the output goes long, replace it with `text.verbosity` plus a statement of what a short answer must preserve.
- **Repeated approval language.** "Ask first," "do not mutate," "wait for approval" scattered across sections is the documented cause of nuisance approval requests on safe, expected actions. Consolidate into one autonomy policy that names the safe actions explicitly.

---

## 2. The removal loop

For requested empirical optimization, use a fixed set of representative evaluations and the agreed scope or budget:

1. Start from a prompt and tool set that already works. Never rewrite from scratch and hope.
2. Remove **one group** of instructions, examples, or tools.
3. Rerun the **same** evals.
4. Keep the removal if scores hold; restore the group if they drop.
5. Repeat only within the agreed scope or budget. Stop when the requested quality criteria hold or the budget is reached, and report any remaining uncertainty.

One group at a time is the whole point — batch removals tell you the prompt got worse but not which cut did it.

Track context at the start of a run *and* as the conversation grows. A prompt that looks lean at turn one can be heavy by turn twenty once repeated tool descriptions and re-injected content accumulate.

---

## 3. Migrating from GPT-5.4 / 5.5

Order of operations:

1. **Choose the tier.** `sol` for frontier capability, `terra` for balanced cost, `luna` for high volume. Don't assume the top tier.
2. **Baseline the reasoning effort** at your current setting, then test one level lower. GPT-5.6 often matches or beats the old quality with fewer tokens.
3. **Check whether `max` helps** if you're on `xhigh`.
4. **Run the audit pass** above. Use the removal loop only for requested empirical optimization.
5. **Re-examine brevity instructions** — the single highest-yield check on this migration.
6. **Confirm persisted reasoning.** The default flipped to `all_turns`. If your app manually manages history, make sure you're resending every response output item, and replaying encrypted reasoning items under ZDR or `store: false`.
7. **Review caching economics.** Writes now cost 1.25× uncached input. Track `cached_tokens` and `cache_write_tokens`; switch to explicit breakpoints if you're writing prefixes you rarely reuse. Replace `prompt_cache_retention` with `prompt_cache_options.ttl`.
8. **Consider pro mode** only for tasks where a marginal quality gain materially changes the outcome — and only if evals show a real gain.
9. **Consider PTC** only for bounded stages that reduce large intermediate outputs to a small structured result.

Codex can apply much of this mechanically via OpenAI's `openai-docs` skill (`openai-docs migrate this project to the GPT-5.6 model family`), downloadable from the OpenAI skills repository for other agents. Mention it when the user is migrating a whole codebase rather than a single prompt.

---

## 4. Migrating from Claude- or Gemini-shaped prompts

Common cross-family habits that misfire on GPT-5.6:

| Habit from elsewhere | What to do instead |
|---|---|
| Heavy XML scaffolding around every section | Markdown headers for sections; reserve XML for delineating injected content |
| Long explicit reasoning scaffolds ("first do X, then Y, then verify Z") | Success criteria plus `reasoning.effort` |
| Extensive persona and tone preamble | Identity only where it constrains behavior; tone as concrete writing choices |
| `system` role assumptions | OpenAI uses `developer` (app rules, higher priority) and `user` (inputs). Think function definition vs. arguments |
| Many-shot example blocks | One or two examples, only where they encode a requirement |
| Politeness/framing padding | Cut; it's pure token cost |

---

## 5. What to measure

When running requested evaluations, use representative tasks from the actual application. Capture:

- Task success rate
- Answer completeness, and whether required evidence or citations survived
- Total tokens (input, output, cached, cache-write)
- Latency
- Cost
- For agents: number of calls, turns, retries, and unnecessary approval requests

The rule that keeps this honest: lower resource use counts as an improvement **only** when the response still passes your existing evals. A cheaper prompt that drops a required caveat is a regression.

For PTC specifically, test the `program_output` item and the final assistant message separately — they're distinct outputs, and a correct program can still be followed by a message that omits a required field.

---

## 6. Reporting the result

Follow the requested output format. Return only the prompt when that is the requested deliverable. For an audit, include relevant items below; parameters apply only to API usage, and empirical results require actual evaluation:

1. **The revised prompt**, in one copy-pasteable block.
2. **A removal table** — what was cut, which group it belonged to, and why. Grouping matters: it lets them restore a specific group if their evals disagree with the audit.
3. **Parameter changes**, with a one-line rationale each.
4. **A test plan** — which representative tasks to run, what to measure, and which single change to revert first if quality drops.

Present the token/cost figures from OpenAI's evals as directional context, never as a prediction of what this particular prompt will achieve. The user's own evals are the arbiter.
