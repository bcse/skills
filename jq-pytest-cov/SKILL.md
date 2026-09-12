---
name: jq-pytest-cov
description: Query pytest-cov coverage.json reports with jq for coverage summaries, uncovered lines, and file or function statistics.
---

# jq + pytest-cov JSON Coverage Reports

A reference guide for querying `coverage.json` (produced by `pytest --cov --cov-report=json`)
using `jq`.

## JSON Structure

```
coverage.json
├── meta                    # Report metadata
│   ├── format              # Report format version (int)
│   ├── version             # pytest-cov version string
│   ├── timestamp           # ISO-8601 generation time
│   ├── branch_coverage     # bool
│   └── show_contexts       # bool
├── totals                  # Aggregate across all files
│   ├── covered_lines       # int
│   ├── num_statements      # int
│   ├── percent_covered     # float
│   ├── percent_covered_display  # string (rounded)
│   ├── missing_lines       # int
│   └── excluded_lines      # int
└── files                   # Object keyed by file path (relative)
    └── "<path>"
        ├── executed_lines  # [int, ...]  line numbers hit
        ├── missing_lines   # [int, ...]  line numbers NOT hit
        ├── excluded_lines  # [int, ...]  lines excluded via pragmas
        ├── summary         # Same shape as totals, for this file
        ├── functions       # Object keyed by "ClassName.method" or "fn_name"
        │   └── "<name>"
        │       ├── executed_lines, missing_lines, excluded_lines
        │       ├── summary
        │       └── start_line  # int
        └── classes         # Same shape as functions, keyed by class name
```

---

## Common Recipes

### Overall summary

```bash
jq '.totals' coverage.json
```

```bash
# One-liner
jq '"Coverage: \(.totals.percent_covered_display)% (\(.totals.covered_lines)/\(.totals.num_statements) lines)"' coverage.json
```

---

### List all tracked files

```bash
jq '.files | keys[]' coverage.json
```

---

### Per-file coverage table (sorted ascending)

```bash
jq -r '
  .files
  | to_entries[]
  | [.key, .value.summary.percent_covered_display, .value.summary.covered_lines, .value.summary.num_statements]
  | @tsv
' coverage.json | sort -t$'\t' -k2 -n | column -t -s $'\t'
```

---

### Files BELOW a coverage threshold (e.g. < 50%)

```bash
jq -r '
  .files
  | to_entries[]
  | select(.value.summary.percent_covered < 50)
  | "\(.value.summary.percent_covered_display)%\t\(.key)"
' coverage.json | sort -k1 -n
```

Change `50` to any threshold you need.

---

### Files with ZERO coverage

```bash
jq -r '
  .files
  | to_entries[]
  | select(.value.summary.covered_lines == 0 and .value.summary.num_statements > 0)
  | .key
' coverage.json
```

---

### Missing lines for a specific file

```bash
jq '.files["path/to/module.py"].missing_lines' coverage.json
```

---

### All functions below a threshold in a specific file

```bash
jq -r '
  .files["path/to/module.py"].functions
  | to_entries[]
  | select(.value.summary.percent_covered < 80)
  | "\(.value.summary.percent_covered_display)%\t\(.key)\t(line \(.value.start_line))"
' coverage.json | sort -k1 -n
```

---

### All uncovered functions across the entire project

```bash
jq -r '
  .files
  | to_entries[]
  | .key as $file
  | .value.functions
  | to_entries[]
  | select(.value.summary.covered_lines == 0 and .value.summary.num_statements > 0)
  | "\($file)\t\(.key)\t(line \(.value.start_line))"
' coverage.json
```

---

### Top N least-covered files

```bash
N=10
jq -r '
  .files
  | to_entries[]
  | select(.value.summary.num_statements > 0)
  | "\(.value.summary.percent_covered)\t\(.value.summary.percent_covered_display)%\t\(.key)"
' coverage.json | sort -k1 -n | head -"$N" | cut -f2- | column -t -s $'\t'
```

---

### Coverage by directory/module (aggregate)

```bash
jq -r '
  .files
  | to_entries[]
  | {
      dir: (.key | split("/") | .[:-1] | join("/")),
      covered: .value.summary.covered_lines,
      total:   .value.summary.num_statements
    }
' coverage.json \
| jq -rs '
  group_by(.dir)[]
  | {
      dir:     .[0].dir,
      covered: map(.covered) | add,
      total:   map(.total)   | add
    }
  | select(.total > 0)
  | "\( (.covered / .total * 100) | round )%\t\(.dir)\t(\(.covered)/\(.total))"
' | sort -k1 -rn | column -t -s $'\t'
```

---

### Count total uncovered functions

```bash
jq '
  [.files[].functions[]
   | select(.summary.covered_lines == 0 and .summary.num_statements > 0)]
  | length
' coverage.json
```

---

### Missing lines formatted as ranges (for editor navigation)

```bash
jq -r '
  .files["path/to/module.py"].missing_lines
  | reduce .[] as $n (
      [];
      if length == 0 then [[[$n,$n]]]
      elif $n == (last | last) + 1 then .[:-1] + [[(last | first), $n]]
      else . + [[$n,$n]]
      end
    )
  | .[]
  | if .[0] == .[1] then "\(.[0])" else "\(.[0])-\(.[1])" end
' coverage.json | paste -sd','
```

---

### Report metadata

```bash
jq '.meta' coverage.json
```

---

## Tips

- **File paths** in `.files` are relative to the project root (where `pytest` ran). Use the exact
  string shown by `jq '.files | keys[]' coverage.json` when filtering a specific file.
- **`percent_covered` vs `percent_covered_display`** — the float field is precise; the display
  field is a rounded string (e.g. `"55"`). Use the float for numeric comparisons in `select()`.
- **`num_statements == 0`** files (e.g. `__init__.py`) show 100% by convention; filter them with
  `select(.value.summary.num_statements > 0)` to avoid false positives.
- **Branch coverage** — when `meta.branch_coverage` is `true`, the report gains additional
  `covered_branches` / `num_branches` fields in each summary. All line-based queries still work.
- **Pretty-print a single file's full data**:
  ```bash
  jq '.files["path/to/module.py"]' coverage.json
  ```
- **Raw output for shell pipelines**: use `jq -r` when you want plain strings without JSON quotes.
