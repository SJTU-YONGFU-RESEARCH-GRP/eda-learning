# learn_routing — module index

Lab-driven syllabus with **hierarchical module ids** (`moduleSS-AA-slug`).
Odd `AA` slots are preferred so new algorithms can be inserted without renumbering.

| Id | Kind | Module | Lab / activity | Status |
|----|------|--------|----------------|--------|
| `module00-00-intro` | `intro` | [Welcome to detailed routing for EDA](../module00-00-intro/README.md) | — | — |
| `module01-01-routing-grid` | `lab` | [Routing grid graph](../module01-01-routing-grid/README.md) | `routing-grid` | **ref** |
| `module01-03-pin-access` | `lab` | [Pin access points](../module01-03-pin-access/README.md) | `pin-access` | **ref** |
| `module02-01-lee-maze` | `lab` | [Lee maze routing](../module02-01-lee-maze/README.md) | `lee-maze` | **ref** |
| `module02-03-astar-route` | `lab` | [A* detailed routing](../module02-03-astar-route/README.md) | `astar-route` | **ref** |
| `module02-05-track-usage` | `lab` | [Track usage and capacity](../module02-05-track-usage/README.md) | `track-usage` | **ref** |
| `module02-07-via-assignment` | `lab` | [Via assignment (2-layer)](../module02-07-via-assignment/README.md) | `via-assignment` | **ref** |
| `module03-01-drc-spacing` | `lab` | [DRC spacing lite](../module03-01-drc-spacing/README.md) | `drc-spacing` | **ref** |
| `module03-03-ripup-detailed` | `lab` | [Rip-up and reroute (detailed)](../module03-03-ripup-detailed/README.md) | `ripup-detailed` | **ref** |
| `module04-01-sequential-detailed` | `lab` | [Sequential detailed route](../module04-01-sequential-detailed/README.md) | `sequential-detailed` | **ref** |
| `module05-01-offline-benchmark-compare` | `offline` | [Offline benchmark compare](../module05-01-offline-benchmark-compare/README.md) | offline harness | P |
| `module99-00-wrap` | `wrap` | [Detailed routing path complete](../module99-00-wrap/README.md) | — | — |

## Sections

| Section | Focus |
|---------|--------|
| `00` | Intro |
| `01` | Foundations (routing grid, pin access) |
| `02` | Algorithms (Lee, A*, track usage, vias) |
| `03` | DRC spacing and rip-up |
| `04` | Sequential detailed route |
| `05` | Offline evidence |
| `99` | Wrap |

## Dual tracks

See [TWO_TRACKS.md](TWO_TRACKS.md).

## Algorithm walkthroughs

Map: [WALKTHROUGHS.md](WALKTHROUGHS.md).

```bash
cd /mnt/d/proj/designs/eda_learning
bash courses/learn_routing/scripts/build_all_media.sh
```
