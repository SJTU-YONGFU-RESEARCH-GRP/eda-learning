# learn_routing

[![GitHub](https://img.shields.io/badge/github-learning-monorepo-blank)](https://github.com/universal-verification-methodology)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)
[![Role](https://img.shields.io/badge/role-course-blue)](../../eda.md)
[![Parent](https://img.shields.io/badge/parent-eda__learning-informational)](../../README.md)
[![Labs](https://img.shields.io/badge/labs-platform%20tools-success)](https://universal-verification-methodology.github.io/learning/tools/)
[![Domain](https://img.shields.io/badge/domain-detailed--routing-orange)](docs/MODULES.md)

**learn_routing** is the open learning path for *detailed routing on M1/M2 track grids* with Lee, A*, via assignment, DRC lite, and rip-up algorithms.

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
learn_routing/
├── README.md
├── LICENSE
├── common/         # Track A: tiny_dr.json, solvers, tests
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
cd courses/learn_routing
```

## Consume from the parent

Prereq: [learn_global_routing](../learn_global_routing/README.md).  
Next: [learn_compaction](../learn_compaction/README.md) or [learn_pattern_matching](../learn_pattern_matching/README.md).  
Lane map: [`eda.md`](../../eda.md). Scope: [docs/SCOPE.md](docs/SCOPE.md).

## Author: publish or update

```bash
# WSL / Linux — from monorepo root
python3 courses/learn_routing/scripts/scaffold_course.py   # regenerate stubs carefully
bash courses/learn_routing/scripts/build_all_media.sh
python3 platform/scripts/publish_course_platform.py learn_routing
python3 .cursor/skills/module-slides/scripts/verify_course_readme.py \
  courses/learn_routing --modules
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
| `00-00` | [Welcome to detailed routing for EDA](module00-00-intro/README.md) | `intro` |
| `01-01` | [Routing grid graph](module01-01-routing-grid/README.md) | `lab` |
| `01-03` | [Pin access points](module01-03-pin-access/README.md) | `lab` |
| `02-01` | [Lee maze routing](module02-01-lee-maze/README.md) | `lab` |
| `02-03` | [A* detailed routing](module02-03-astar-route/README.md) | `lab` |
| `02-05` | [Track usage and capacity](module02-05-track-usage/README.md) | `lab` |
| `02-07` | [Via assignment (2-layer)](module02-07-via-assignment/README.md) | `lab` |
| `03-01` | [DRC spacing lite](module03-01-drc-spacing/README.md) | `lab` |
| `03-03` | [Rip-up and reroute (detailed)](module03-03-ripup-detailed/README.md) | `lab` |
| `04-01` | [Sequential detailed route](module04-01-sequential-detailed/README.md) | `lab` |
| `05-01` | [Offline benchmark compare](module05-01-offline-benchmark-compare/README.md) | `offline` |
| `99-00` | [Detailed routing path complete](module99-00-wrap/README.md) | `wrap` |

## Browser labs

By workflow (Track B): `routing-grid`, `pin-access`, `lee-maze`, `astar-route`, `track-usage`, `via-assignment`, `drc-spacing`, `ripup-detailed`, `sequential-detailed`. See [all tools](https://universal-verification-methodology.github.io/learning/tools/) and each module README. Walkthroughs: [docs/WALKTHROUGHS.md](docs/WALKTHROUGHS.md).

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — see [`LICENSE`](LICENSE).
