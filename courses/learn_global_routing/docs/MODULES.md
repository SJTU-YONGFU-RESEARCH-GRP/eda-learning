# learn_global_routing — module index

Lab-driven syllabus with **hierarchical module ids** (`moduleSS-AA-slug`).
Odd `AA` slots are preferred so new algorithms can be inserted without renumbering.

| Id | Kind | Module | Lab / activity | Status |
|----|------|--------|----------------|--------|
| `module00-00-intro` | `intro` | [Welcome to global routing for EDA](../module00-00-intro/README.md) | — | — |
| `module01-01-routing-graph` | `lab` | [GCell routing graph](../module01-01-routing-graph/README.md) | `routing-graph` | **ref** |
| `module01-03-terminal-gcells` | `lab` | [Pin terminals on GCells](../module01-03-terminal-gcells/README.md) | `terminal-gcells` | **ref** |
| `module02-01-pattern-l-route` | `lab` | [L-shape pattern routes](../module02-01-pattern-l-route/README.md) | `pattern-l-route` | **ref** |
| `module02-03-pattern-z-route` | `lab` | [Z-shape pattern routes](../module02-03-pattern-z-route/README.md) | `pattern-z-route` | **ref** |
| `module02-05-maze-gcell-route` | `lab` | [Maze routing on GCells](../module02-05-maze-gcell-route/README.md) | `maze-gcell-route` | **ref** |
| `module02-07-multipin-tree` | `lab` | [Multi-pin tree (Steiner-lite)](../module02-07-multipin-tree/README.md) | `multipin-tree` | **ref** |
| `module03-01-edge-overflow` | `lab` | [Edge overflow metrics](../module03-01-edge-overflow/README.md) | `edge-overflow` | **ref** |
| `module03-03-ripup-reroute` | `lab` | [Rip-up and reroute](../module03-03-ripup-reroute/README.md) | `ripup-reroute` | **ref** |
| `module04-01-sequential-global` | `lab` | [Sequential global route](../module04-01-sequential-global/README.md) | `sequential-global` | **ref** |
| `module05-01-offline-benchmark-compare` | `offline` | [Offline benchmark compare](../module05-01-offline-benchmark-compare/README.md) | offline harness | P |
| `module99-00-wrap` | `wrap` | [Global routing path complete](../module99-00-wrap/README.md) | — | — |

## Sections

| Section | Focus |
|---------|--------|
| `00` | Intro |
| `01` | Foundations (routing graph, terminals) |
| `02` | Pattern routing (L, Z, maze, multipin) |
| `03` | Overflow and rip-up |
| `04` | Sequential global route |
| `05` | Offline evidence |
| `99` | Wrap |

## Dual tracks

See [TWO_TRACKS.md](TWO_TRACKS.md).

## Algorithm walkthroughs

Map: [WALKTHROUGHS.md](WALKTHROUGHS.md).

```bash
cd /mnt/d/proj/designs/eda_learning
bash courses/learn_global_routing/scripts/build_all_media.sh
```
