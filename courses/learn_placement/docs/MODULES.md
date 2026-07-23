# learn_placement — module index

Lab-driven syllabus with **hierarchical module ids** (`moduleSS-AA-slug`).
Odd `AA` slots are preferred so new algorithms can be inserted without renumbering.
Published ids are **stable keys**; order below is the teaching path.

Status: **ref** = browser lab shipped under `platform/tools/` (algorithm modules).

| Id | Kind | Module | Lab / activity | Status |
|----|------|--------|----------------|--------|
| `module00-00-intro` | `intro` | [Welcome to placement for EDA](../module00-00-intro/README.md) | — | — |
| `module01-01-hpwl-metrics` | `lab` | [Half-perimeter wirelength](../module01-01-hpwl-metrics/README.md) | `hpwl-metrics` | **ref** |
| `module01-03-net-models` | `lab` | [Net models for wirelength](../module01-03-net-models/README.md) | `net-models` | **ref** |
| `module02-01-force-directed-place` | `lab` | [Force-directed placement](../module02-01-force-directed-place/README.md) | `force-directed-place` | **ref** |
| `module02-03-quadratic-place` | `lab` | [Quadratic placement](../module02-03-quadratic-place/README.md) | `quadratic-place` | **ref** |
| `module02-05-analytical-place` | `lab` | [Analytical / density-aware place](../module02-05-analytical-place/README.md) | `analytical-place` | **ref** |
| `module02-07-sa-placement` | `lab` | [Simulated annealing placement](../module02-07-sa-placement/README.md) | `sa-placement` | **ref** |
| `module03-01-density-bins` | `lab` | [Density bins and overflow](../module03-01-density-bins/README.md) | `density-bins` | **ref** |
| `module03-03-spread-legalize-lite` | `lab` | [Spreading / overlap relief](../module03-03-spread-legalize-lite/README.md) | `spread-legalize-lite` | **ref** |
| `module04-01-timing-driven-place` | `lab` | [Timing-driven placement](../module04-01-timing-driven-place/README.md) | `timing-driven-place` | **ref** |
| `module05-01-offline-benchmark-compare` | `offline` | [Offline benchmark compare](../module05-01-offline-benchmark-compare/README.md) | offline harness | P |
| `module99-00-wrap` | `wrap` | [Placement path complete](../module99-00-wrap/README.md) | — | — |

## Sections

| Section | Focus |
|---------|--------|
| `00` | Intro |
| `01` | Foundations (HPWL, net models) |
| `02` | Global place (force, quadratic, analytical, SA) |
| `03` | Density and spreading |
| `04` | Timing-driven place |
| `05` | Offline evidence |
| `99` | Wrap |

## Dual tracks

See [TWO_TRACKS.md](TWO_TRACKS.md).

## Algorithm walkthroughs (PPT / transcript)

When walkthrough frames exist: each lab module may have `assets/STEPS.md` and `assets/steps/*.png`. Map: [WALKTHROUGHS.md](WALKTHROUGHS.md).

**Build media in WSL** (LibreOffice + edge-tts + ffmpeg):

```bash
cd /mnt/d/proj/designs/eda_learning
bash courses/learn_placement/scripts/build_all_media.sh
```
