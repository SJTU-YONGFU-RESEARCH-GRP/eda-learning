# Algorithm walkthroughs — learn_sta

Interactive viewer:
`http://127.0.0.1:8080/tools/algorithm-walkthrough/?algo=<lab-id>&step=1`

| Lab id | Module | Frames |
|--------|--------|--------|
| `timing-graph` | Timing graph | 5 PNGs |
| `arrival-required` | Arrival and required times | 5 PNGs |
| `slack-setup-hold` | Slack, setup, and hold | 5 PNGs |
| `critical-path` | Critical path | 5 PNGs |
| `incremental-update` | Incremental timing update | 5 PNGs |
| `false-multicycle-lite` | False and multicycle paths | 5 PNGs |

Each lab module has `assets/STEPS.md`, `assets/steps/*.png`, and full media (`slides.pptx` / `.pdf` / `audio/` / `video.mp4`).

**Rebuild media in WSL:**

```bash
cd /mnt/d/proj/designs/eda_learning
bash courses/learn_sta/scripts/build_all_media.sh
python3 platform/scripts/publish_course_platform.py learn_sta
```
