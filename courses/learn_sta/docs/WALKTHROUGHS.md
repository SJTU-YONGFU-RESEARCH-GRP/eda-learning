# Algorithm walkthroughs — learn_sta

Interactive viewer:
`http://127.0.0.1:8080/tools/algorithm-walkthrough/?algo=<lab-id>&step=1`

| Lab id | Module | Status |
|--------|--------|--------|
| `timing-graph` | Timing graph | **ALGOS ready** (5 steps) |
| `arrival-required` | Arrival and required times | **ALGOS ready** (5 steps) |
| `slack-setup-hold` | Slack, setup, and hold | **ALGOS ready** (5 steps) |
| `critical-path` | Critical path | **ALGOS ready** (5 steps) |
| `incremental-update` | Incremental timing update | **ALGOS ready** (5 steps) |
| `false-multicycle-lite` | False and multicycle paths | **ALGOS ready** (5 steps) |

Capture (WSL, platform server on :8080):

```bash
for m in module01-01-timing-graph module01-03-arrival-required \
  module02-01-slack-setup-hold module02-03-critical-path \
  module03-01-incremental-update module03-03-false-multicycle-lite; do
  python3 .cursor/skills/module-slides/scripts/capture_algorithm_walkthrough.py \
    courses/learn_sta/$m --inject-transcript
done
```
