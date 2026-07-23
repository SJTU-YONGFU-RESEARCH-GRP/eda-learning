# learn_sta — module index

Lab-driven syllabus with **hierarchical module ids** (`moduleSS-AA-slug`).
Odd `AA` slots are preferred so new algorithms can be inserted without renumbering.
Published ids are **stable keys**; order below is the teaching path.

Status: **P** = planned; **ref** = browser lab + `common/` solvers shipped.

| Id | Kind | Module | Lab / activity | Status |
|----|------|--------|----------------|--------|
| `module00-00-intro` | `intro` | [Welcome to static timing analysis](../module00-00-intro/README.md) | — | — |
| `module01-01-timing-graph` | `lab` | [Timing graph](../module01-01-timing-graph/README.md) | `timing-graph` | **ref** |
| `module01-03-arrival-required` | `lab` | [Arrival and required times](../module01-03-arrival-required/README.md) | `arrival-required` | P |
| `module02-01-slack-setup-hold` | `lab` | [Slack, setup, and hold](../module02-01-slack-setup-hold/README.md) | `slack-setup-hold` | P |
| `module02-03-critical-path` | `lab` | [Critical path](../module02-03-critical-path/README.md) | `critical-path` | P |
| `module03-01-incremental-update` | `lab` | [Incremental timing update](../module03-01-incremental-update/README.md) | `incremental-update` | P |
| `module03-03-false-multicycle-lite` | `lab` | [False and multicycle paths (engine view)](../module03-03-false-multicycle-lite/README.md) | `false-multicycle-lite` | P |
| `module05-01-offline-benchmark-compare` | `offline` | [Offline benchmark compare](../module05-01-offline-benchmark-compare/README.md) | offline harness | P |
| `module99-00-wrap` | `wrap` | [STA path complete](../module99-00-wrap/README.md) | — | — |

## Sections

| Section | Focus |
|---------|--------|
| `00` | Intro |
| `01` | Foundations (timing graph, arrival / required) |
| `02` | Slack and critical path |
| `03` | Incremental update + engine-facing exceptions |
| `05` | Offline evidence |
| `99` | Wrap |

## Dual tracks

See [TWO_TRACKS.md](TWO_TRACKS.md).

## Algorithm walkthroughs (PPT / transcript)

When walkthrough frames exist: [WALKTHROUGHS.md](WALKTHROUGHS.md).
Each lab module may have `assets/STEPS.md` and `assets/steps/*.png`.

**Build media in WSL** (LibreOffice + edge-tts + ffmpeg):

```bash
cd /mnt/d/proj/designs/eda_learning
bash courses/learn_sta/scripts/build_all_media.sh
```
