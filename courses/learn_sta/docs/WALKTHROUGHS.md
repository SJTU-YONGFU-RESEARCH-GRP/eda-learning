# Algorithm walkthroughs — learn_sta

Step frames for PPT / transcript live under each lab’s `assets/steps/` once captured.

Interactive viewer:
`http://127.0.0.1:8080/tools/algorithm-walkthrough/?algo=<lab-id>&step=1`

| Lab id | Module | Status |
|--------|--------|--------|
| `timing-graph` | Timing graph | **ALGOS ready** (5 steps) |
| `arrival-required` | Arrival and required times | planned |
| `slack-setup-hold` | Slack, setup, and hold | planned |
| `critical-path` | Critical path | planned |
| `incremental-update` | Incremental timing update | planned |
| `false-multicycle-lite` | False and multicycle paths (engine view) | planned |

Capture (WSL, with platform server up):

```bash
python3 .cursor/skills/module-slides/scripts/capture_algorithm_walkthrough.py \
  courses/learn_sta/module01-01-timing-graph \
  --inject-transcript
```
