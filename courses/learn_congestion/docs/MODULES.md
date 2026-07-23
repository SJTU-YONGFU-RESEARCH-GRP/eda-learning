# learn_congestion — module index

Lab-driven syllabus with **hierarchical module ids** (`moduleSS-AA-slug`).
Odd `AA` slots are preferred so new algorithms can be inserted without renumbering.

| Id | Kind | Module | Lab / activity | Status |
|----|------|--------|----------------|--------|
| `module00-00-intro` | `intro` | [Welcome to congestion for EDA](../module00-00-intro/README.md) | — | — |
| `module01-01-gcell-grid` | `lab` | [GCell grid model](../module01-01-gcell-grid/README.md) | `gcell-grid` | **ref** |
| `module01-03-capacity-demand` | `lab` | [Capacity vs demand](../module01-03-capacity-demand/README.md) | `capacity-demand` | **ref** |
| `module02-01-rudy-estimate` | `lab` | [RUDY congestion estimate](../module02-01-rudy-estimate/README.md) | `rudy-estimate` | **ref** |
| `module02-03-probabilistic-demand` | `lab` | [Probabilistic routing demand](../module02-03-probabilistic-demand/README.md) | `probabilistic-demand` | **ref** |
| `module02-05-congestion-map` | `lab` | [Congestion heat map](../module02-05-congestion-map/README.md) | `congestion-map` | **ref** |
| `module02-07-overflow-metrics` | `lab` | [Overflow metrics](../module02-07-overflow-metrics/README.md) | `overflow-metrics` | **ref** |
| `module03-01-cell-inflator` | `lab` | [Cell inflation](../module03-01-cell-inflator/README.md) | `cell-inflator` | **ref** |
| `module03-03-net-weighting` | `lab` | [Congestion-aware net weighting](../module03-03-net-weighting/README.md) | `net-weighting` | **ref** |
| `module04-01-placement-feedback` | `lab` | [Placement feedback loop](../module04-01-placement-feedback/README.md) | `placement-feedback` | **ref** |
| `module05-01-offline-benchmark-compare` | `offline` | [Offline benchmark compare](../module05-01-offline-benchmark-compare/README.md) | offline harness | P |
| `module99-00-wrap` | `wrap` | [Congestion path complete](../module99-00-wrap/README.md) | — | — |

## Sections

| Section | Focus |
|---------|--------|
| `00` | Intro |
| `01` | Foundations (GCell grid, capacity vs demand) |
| `02` | Estimation (RUDY, probabilistic, map, overflow) |
| `03` | Feedback knobs (inflator, net weighting) |
| `04` | Placement feedback loop |
| `05` | Offline evidence |
| `99` | Wrap |

## Dual tracks

See [TWO_TRACKS.md](TWO_TRACKS.md).

## Algorithm walkthroughs

Map: [WALKTHROUGHS.md](WALKTHROUGHS.md).

```bash
cd /mnt/d/proj/designs/eda_learning
bash courses/learn_congestion/scripts/build_all_media.sh
```
