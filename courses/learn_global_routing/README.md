# learn_global_routing

[![GitHub](https://img.shields.io/badge/github-learning-monorepo-blank)](https://github.com/universal-verification-methodology)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)
[![Role](https://img.shields.io/badge/role-course-blue)](../../eda.md)
[![Parent](https://img.shields.io/badge/parent-eda__learning-informational)](../../README.md)
[![Labs](https://img.shields.io/badge/labs-platform%20tools-success)](https://universal-verification-methodology.github.io/learning/tools/)
[![Domain](https://img.shields.io/badge/domain-global--routing-orange)](docs/MODULES.md)

**learn_global_routing** is the open learning path for *global routing on GCell graphs* with pattern, maze, and rip-up algorithms.

Readers follow module READMEs. Authors rebuild clips with module-slides. This tree may be consumed from the parent monorepo or as a submodule later.

## Table of contents

- [Contents](#contents)
- [Browse or clone](#browse-or-clone)
- [Consume from the parent](#consume-from-the-parent)
- [Author: publish or update](#author-publish-or-update)
- [Two learning tracks](#two-learning-tracks)
- [Module landings](#module-landings)
- [Browser labs](#browser-labs)
- [License](#license)

## Contents

```
learn_global_routing/
├── README.md
├── LICENSE
├── common/         # Track A: tiny_gr.json, solvers, tests
├── docs/           # MODULES, SCOPE, TWO_TRACKS, WALKTHROUGHS
├── scripts/        # scaffold_course.py, build_all_media.sh, …
└── moduleSS-AA-slug/
    ├── README.md · CHECKLIST.md · EXAMPLES.md
    ├── transcript.md · outline.yaml · quiz.json
    └── (optional) examples/ · assets/ · slides · audio · video
```

Optional per-module media (pptx/pdf/audio/video) is produced by [module-slides](../../.cursor/skills/module-slides/SKILL.md).

## Browse or clone

From the monorepo root:

```bash
cd courses/learn_global_routing
```

## Consume from the parent

Prereq: [learn_congestion](../learn_congestion/README.md) / [learn_legalization](../learn_legalization/README.md).  
Next: [learn_routing](../learn_routing/README.md) or [learn_clock_tree](../learn_clock_tree/README.md).  
Lane map: [`eda.md`](../../eda.md). Scope: [docs/SCOPE.md](docs/SCOPE.md).

## Author: publish or update

```bash
# WSL / Linux — from monorepo root
python3 courses/learn_global_routing/scripts/scaffold_course.py   # regenerate stubs carefully
bash courses/learn_global_routing/scripts/build_all_media.sh
python3 platform/scripts/publish_course_platform.py learn_global_routing
python3 .cursor/skills/module-slides/scripts/verify_course_readme.py \
  courses/learn_global_routing --modules
```

## Two learning tracks

| Track | Where | Doc |
|-------|-------|-----|
| **A — Implement** | `common/` + `examples/` | [TWO_TRACKS.md](docs/TWO_TRACKS.md) |
| **B — Browser lab** | platform tools | [TWO_TRACKS.md](docs/TWO_TRACKS.md) |

## Module landings

Full table: [docs/MODULES.md](docs/MODULES.md).

| Key | Module | Kind |
|-----|--------|------|
| `00-00` | [Welcome to global routing for EDA](module00-00-intro/README.md) | `intro` |
| `01-01` | [GCell routing graph](module01-01-routing-graph/README.md) | `lab` |
| `01-03` | [Pin terminals on GCells](module01-03-terminal-gcells/README.md) | `lab` |
| `02-01` | [L-shape pattern routes](module02-01-pattern-l-route/README.md) | `lab` |
| `02-03` | [Z-shape pattern routes](module02-03-pattern-z-route/README.md) | `lab` |
| `02-05` | [Maze routing on GCells](module02-05-maze-gcell-route/README.md) | `lab` |
| `02-07` | [Multi-pin tree (Steiner-lite)](module02-07-multipin-tree/README.md) | `lab` |
| `03-01` | [Edge overflow metrics](module03-01-edge-overflow/README.md) | `lab` |
| `03-03` | [Rip-up and reroute](module03-03-ripup-reroute/README.md) | `lab` |
| `04-01` | [Sequential global route](module04-01-sequential-global/README.md) | `lab` |
| `05-01` | [Offline benchmark compare](module05-01-offline-benchmark-compare/README.md) | `offline` |
| `99-00` | [Global routing path complete](module99-00-wrap/README.md) | `wrap` |

## Browser labs

By workflow (Track B): `routing-graph`, `terminal-gcells`, `pattern-l-route`, `pattern-z-route`, `maze-gcell-route`, `multipin-tree`, `edge-overflow`, `ripup-reroute`, `sequential-global`. See [all tools](https://universal-verification-methodology.github.io/learning/tools/) and each module README. Walkthroughs: [docs/WALKTHROUGHS.md](docs/WALKTHROUGHS.md).

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — see [`LICENSE`](LICENSE).
