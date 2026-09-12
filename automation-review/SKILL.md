---
name: automation-review
description: Identify repeated workflows worth automating or packaging when the user asks for automation opportunities. Use work-summary for ordinary activity summaries.
---

Inspect work within the requested scope and period to identify repeated manual workflows worth packaging. If no period is specified, use the last 30 days or all available history if shorter.

Use available evidence in this order:
- Recent Codex sessions and task summaries.
- Codex Memories and rollout summaries to find patterns repeated across sessions.
- Chronicle, if enabled, to spot repeated work outside Codex. Use Chronicle for discovery only; confirm important details in the relevant source system when possible.
- Existing skills, custom agents, and automations, so you reuse or extend what already exists instead of duplicating it.

Look broadly for work that is repeated, time-consuming, error-prone, context-heavy, or benefits from a consistent process. Include workflows across coding, research, writing, planning, communication, operations, analysis, and personal administration.

Only act on a candidate when it:
- occurred at least twice, or is clearly likely to recur and costly to repeat;
- has stable inputs, a repeatable procedure, and a clear output or stopping condition;
- would materially improve speed, quality, consistency, or reliability;
- is not already adequately covered.

Choose the smallest appropriate form:
- Skill: a reusable workflow or playbook.
- Custom subagent: a bounded specialist role or investigation task suitable for delegation.
- Automation: a scheduled or recurring check, report, reminder, or monitor.
- Skip: work that is too one-off, ambiguous, sensitive, or poorly evidenced to package.

First produce a compact shortlist with:
- repeated workflow
- supporting evidence and dates
- frequency/confidence
- recommended form: skill, subagent, automation, extend existing, or skip
- why it is or is not worth creating

If the request includes creating or implementing these assets, create only the high-confidence missing items within that authorization. Otherwise, the shortlist is the completed deliverable. Keep created assets narrow, practical, source-aware, and easy to validate; do not create speculative or overlapping assets.

Finish with:
- recommendations, or what you created or extended when implementation was requested
- what you deliberately skipped
- what needs more evidence before packaging