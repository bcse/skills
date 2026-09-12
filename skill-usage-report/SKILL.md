---
name: skill-usage-report
description: Generate Codex skill-usage statistics and reports from local session logs for a requested period. Excludes general activity reports and unrelated session-log analysis.
---

# Skill usage report

Generate the report with `scripts/skill_usage.py`. The default request means the six calendar months ending today. Do not ask for dates, paths, hostname, or timezone unless the user wants to override them.

## Generate the default report

Resolve the script relative to this skill directory. Compute today's ISO date and use literal output paths in the current workspace:

```sh
python3 <skill-dir>/scripts/skill_usage.py extract --logs ~/.codex --months 6 --output outputs/skill-usage-data-YYYY-MM-DD.json
python3 <skill-dir>/scripts/skill_usage.py validate outputs/skill-usage-data-YYYY-MM-DD.json
python3 <skill-dir>/scripts/skill_usage.py dashboard outputs/skill-usage-data-YYYY-MM-DD.json --output outputs/skill-usage-dashboard-YYYY-MM-DD.html
```

Create `outputs/` if needed. Return links to both files and a short factual readout from `combined.totals`. Do not replace the JSON with a summary.

The JSON is the complete report dataset, not a copy of private session-log text. It includes every detected qualified skill name, every host export, corpus counters, totals, and daily usage breakdowns. It contains no skill file paths. Hostname identifies the machine but is not part of skill identity.

## Date overrides and merging

Use `--months N`, `--days N`, or `--since YYYY-MM-DD` with optional `--until YYYY-MM-DD` when the user specifies another period. Run `extract --help` rather than guessing additional flags.

For independent-machine exports, merge exact qualified names with:

```sh
python3 <skill-dir>/scripts/skill_usage.py merge machine-a.json machine-b.json --output outputs/skill-usage-merged.json
python3 <skill-dir>/scripts/skill_usage.py validate outputs/skill-usage-merged.json
python3 <skill-dir>/scripts/skill_usage.py dashboard outputs/skill-usage-merged.json --output outputs/skill-usage-merged.html
```

Matching qualified names are the same skill across machines. Duplicate hostnames are rejected to prevent importing one machine twice. The portable JSON Schema is at [references/skill-usage.schema.json](references/skill-usage.schema.json) for external validators.
