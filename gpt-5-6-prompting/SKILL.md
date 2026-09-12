---
name: gpt-5-6-prompting
description: Write, audit, or migrate prompts explicitly targeting GPT-5.6 Sol, Terra, or Luna. Do not route unspecified latest-model or other model-family requests here.
---

# Writing prompts for GPT-5.6

Source of truth: OpenAI's model guidance, https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6#prompting-best-practices — verify against it if a detail here seems stale.

## Why GPT-5.6 prompts look different

Four model changes drive every rule below:

- **It infers intent well.** GPT-5.6 reads the user's underlying goal and intended level of work from context, so prescribing every step is wasted budget. Supply what it *can't* infer: domain context, hard constraints, approval boundaries, success criteria.
- **Lean beats thorough.** In OpenAI's internal coding-agent evals, leaner system prompts scored roughly 10–15% higher while cutting tokens 41–66% and cost 33–67%. Those figures are directional, not a promise — but the direction is the point. Removing instructions is a legitimate optimization, not a compromise.
- **It's terser by default than GPT-5.5.** Brevity instructions inherited from older prompts can now over-truncate.
- **It's proactive and persistent.** Left unbounded it keeps going; over-bounded it stops to ask permission for safe, expected actions. The fix is one clear boundary statement, not repeated warnings.

**The governing habit: subtract, don't add.** A GPT-5.6 prompt is finished when removing one more thing would lose a real requirement.

## Step 1 — Collect what you can't infer

Check the conversation first; only ask for what's genuinely missing, and ask in one batch rather than interrogating turn by turn.

| Need | Why it matters |
|---|---|
| Task + what "done well" looks like | Success criteria replace step-by-step instructions |
| Surface: Responses API, ChatGPT, or Codex | Decides whether parameters are available to you at all |
| Domain context the model can't guess | Internal terms, business rules, data shape, house conventions |
| Hard constraints | Never-dos, compliance rules, required libraries/formats |
| Autonomy: what it may do unattended | Prevents both runaway actions and needless approval pauses |
| Output shape | Format, length, required fields, citations |
| Tools available (if agentic) | Drives orchestration and the tool-exposure decision |

If the user gives you a rich brief already, don't re-ask — draft and flag assumptions inline.

## Step 2 — Split prompt from parameters

A common failure is writing config as prose. Put each concern where it belongs:

| Concern | Goes in the API parameter | Goes in the prompt |
|---|---|---|
| How hard to think | `reasoning.effort` (`none`→`max`) | nothing |
| Extra work for reliability | `reasoning.mode: "pro"` | nothing |
| Default detail level | `text.verbosity` (`low`/`medium`/`high`) | task-specific length rules |
| Cross-turn reasoning reuse | `reasoning.context` | nothing |
| Cost/latency of repeated prefixes | prompt caching config | nothing |
| Goal, context, constraints, format, evidence | — | all of it |

Never write "think harder," "use pro mode," or "generate several candidates then pick the best" into the prompt — the same outcome-focused prompt works in both standard and pro mode. See `references/api-parameters.md` for the full parameter surface and how to pick values.

**On ChatGPT or Codex** (no parameter access), fold the intent into plain language instead: state the depth of analysis expected and the target length directly.

## Step 3 — Draft against the skeleton

```
# Identity            (only if role constrains behavior — skip generic "you are world-class")
# Task                (goal + what a good result looks like)
# Context             (domain facts, data shape, house conventions)
# Constraints         (hard limits, never-dos)
# Autonomy            (only for agents/tool use)
# Output              (format, required content, length priority)
# Examples            (only where they encode a requirement or fix a measured gap)
```

Order sections stable-first: reusable content at the top maximizes prompt-cache hits; per-request context goes last. Markdown headers separate sections; XML tags delineate injected content (`<document>`, `<tool_orchestration>`).

Filled examples for coding agents, RAG answering, frontend work, and analysis are in `references/prompt-templates.md`, along with reusable snippets for autonomy, brevity, and tone.

## The four levers

### 1. Leanness

State each instruction exactly once. Expose only tools relevant to the task and keep their descriptions concise and precise. Keep examples and style guidance only when they encode a product requirement or correct a gap you actually measured. Watch context growth across long sessions too — repeated prompt and tool content compounds turn over turn.

### 2. Autonomy and approval boundaries

Give the model a compact policy so it can continue safe in-scope work without pausing, while stopping before external, destructive, costly, or scope-expanding actions:

```
For requests to answer, explain, review, diagnose, or plan, inspect the relevant
materials and report the result. Do not implement changes unless the request also
asks for them.

For requests to change, build, or fix, make the requested in-scope local changes
and run relevant non-destructive validation without asking first.

Require confirmation for external writes, destructive actions, purchases, or a
material expansion of scope only when that action is not already authorized.
Existing authorization remains valid within its scope; respect tool permissions.
```

Name the safe local actions explicitly — reading files, inspecting logs, editing in-scope code, running tests. Keep the whole policy in one place. Sprinkling "ask first" or "wait for approval" across sections is the main cause of nuisance approval requests.

### 3. Length, style, and tone

Broad brevity instructions are now suspect. When migrating, test whether "Be concise" still earns its place — GPT-5.6 may already be short enough, and the instruction can push it past useful.

Instead of trimming by adjective, give a priority order for what survives:

```
Lead with the conclusion. Include the evidence needed to support it, any material
caveat, and the next action. Omit secondary detail and repetition.
```

For tone, describe writing choices rather than labels. "Friendly" and "empathetic" are ambiguous; "state the answer directly, acknowledge the specific problem before giving the next step, use reassurance only when relevant, omit generic praise and sign-offs" is executable.

### 4. Tool orchestration (agentic prompts only)

Programmatic Tool Calling (PTC) fits bounded stages where code processes several tool results or large intermediate outputs into a much smaller structured result — filtering, joining, ranking, deduplication, aggregation, validation.

Prefer direct tool calls when one call suffices, intermediate outputs are already small, each result may change the next decision, an action needs approval, or the output must preserve citations or native artifacts. Multiple or parallel calls alone don't justify PTC.

Generic instructions like "use Programmatic Tool Calling efficiently" don't route anything. Be specific:

```
<tool_orchestration>
Use Programmatic Tool Calling for [bounded stage] using only [eligible tools].
Run independent calls concurrently when safe. Use only documented tool input
and output fields.

Process and reduce the intermediate results, then emit exactly [output schema],
including the evidence needed for the final answer.

Stop when [condition] is met. Retry transient failures at most [R] times.
Do not repeat completed calls or perform side-effecting actions. If a required
result is still missing, return a clear structured failure.

Use direct tool calls for [semantic judgment, approval, or final validation].
</tool_orchestration>
```

If the model can't know a tool's return shape before writing the program, route it to direct calling so it can inspect the result first. When both routes are needed, define one handoff and tell it not to switch routes or repeat completed work.

## Anti-patterns — delete on sight

| In the prompt | Why it hurts on 5.6 | Replace with |
|---|---|---|
| Same rule restated in three sections | Tokens plus contradiction risk | State once, in the section that owns it |
| "Be concise" everywhere | Already terse; can over-truncate | `text.verbosity` + what a short answer must preserve |
| "Always ask before acting," repeated | Nuisance approvals on safe actions | One autonomy policy naming safe actions |
| "Think step by step" / "think harder" | Reasoning is a parameter | `reasoning.effort`, `reasoning.mode` |
| Eight few-shot examples for a simple format | Bloat; the model infers the pattern | One or two, only where they encode a requirement |
| Every tool exposed "just in case" | Descriptions crowd context, routing degrades | Expose only task-relevant tools |
| "Use PTC efficiently" | Doesn't route anything | Named stage, tools, schema, limits |
| "You are a world-class expert…" | Decorative, constrains nothing | Identity only when it changes behavior |
| Step-by-step recipe for an inferable task | Wastes the intent-understanding gain | Goal + constraints + success criteria |

## Deliverable format

Return the requested deliverable. If the user asks only for a paste-ready prompt, return only the prompt in their requested format.

- Include recommended parameters only for API usage, with a brief rationale when useful.
- Include change explanations or a validation plan when requested or useful to an audit, rather than appending them to every prompt.
- Run the removal/evaluation loop in `references/migration-audit.md` only when empirical optimization is requested and the required data, tools, and budget are available and authorized. A text-only revision ends with the revised prompt; do not imply measured improvement without evidence.

## References

- `references/prompt-templates.md` — annotated skeleton, four filled examples, reusable policy snippets
- `references/api-parameters.md` — model tiers, reasoning effort ladder, pro mode, persisted reasoning, verbosity, caching, PTC wiring, safeguards
- `references/migration-audit.md` — auditing an existing prompt, the removal loop, migrating from 5.4/5.5 and from other model families
