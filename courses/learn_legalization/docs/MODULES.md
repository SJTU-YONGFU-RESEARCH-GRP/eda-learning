# learn_legalization — module index

Lab-driven syllabus with **hierarchical module ids** (`moduleSS-AA-slug`).
Odd `AA` slots are preferred so new algorithms can be inserted without renumbering.
Published ids are **stable keys**; order below is the teaching path.

Status: **ref** = reference / lab id reserved for `platform/tools/` (algorithm modules).

| Id | Kind | Module | Lab / activity | Status |
|----|------|--------|----------------|--------|
| `module00-00-intro` | `intro` | [Welcome to legalization for EDA](../module00-00-intro/README.md) | — | — |
| `module01-01-site-row-model` | `lab` | [Site and row model](../module01-01-site-row-model/README.md) | `site-row-model` | **ref** |
| `module01-03-legality-metrics` | `lab` | [Legality metrics](../module01-03-legality-metrics/README.md) | `legality-metrics` | **ref** |
| `module02-01-greedy-snap` | `lab` | [Greedy site/row snap](../module02-01-greedy-snap/README.md) | `greedy-snap` | **ref** |
| `module02-03-overlap-removal` | `lab` | [Overlap removal in rows](../module02-03-overlap-removal/README.md) | `overlap-removal` | **ref** |
| `module02-05-abacus-row-pack` | `lab` | [Abacus row packing](../module02-05-abacus-row-pack/README.md) | `abacus-row-pack` | **ref** |
| `module02-07-tetris-row-pack` | `lab` | [Tetris-style row packing](../module02-07-tetris-row-pack/README.md) | `tetris-row-pack` | **ref** |
| `module03-01-fixed-macros` | `lab` | [Fixed macros during legalization](../module03-01-fixed-macros/README.md) | `fixed-macros` | **ref** |
| `module03-03-displacement-hpwl` | `lab` | [Displacement vs HPWL tradeoff](../module03-03-displacement-hpwl/README.md) | `displacement-hpwl` | **ref** |
| `module04-01-detailed-vs-global` | `lab` | [Detailed vs global legalize](../module04-01-detailed-vs-global/README.md) | `detailed-vs-global` | **ref** |
| `module05-01-offline-benchmark-compare` | `offline` | [Offline benchmark compare](../module05-01-offline-benchmark-compare/README.md) | offline harness | P |
| `module99-00-wrap` | `wrap` | [Legalization path complete](../module99-00-wrap/README.md) | — | — |

## Sections

| Section | Focus |
|---------|--------|
| `00` | Intro |
| `01` | Foundations (site/row model, legality metrics) |
| `02` | Snap & row pack (greedy snap, overlap, Abacus, Tetris) |
| `03` | Macros & objectives (fixed macros, displacement vs HPWL) |
| `04` | Global vs detailed legalize |
| `05` | Offline evidence |
| `99` | Wrap |

## Dual tracks

See [TWO_TRACKS.md](TWO_TRACKS.md).

## Algorithm walkthroughs (PPT / transcript)

When walkthrough frames exist: each lab module may have `assets/STEPS.md` and `assets/steps/*.png`. Map: [WALKTHROUGHS.md](WALKTHROUGHS.md).

**Build media in WSL** (LibreOffice + edge-tts + ffmpeg):

```bash
cd /mnt/d/proj/designs/eda_learning
bash courses/learn_legalization/scripts/build_all_media.sh
```
