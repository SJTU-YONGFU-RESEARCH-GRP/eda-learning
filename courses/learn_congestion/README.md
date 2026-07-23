# learn_congestion

[![GitHub](https://img.shields.io/badge/github-learning-monorepo-blank)](https://github.com/universal-verification-methodology)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)
[![Role](https://img.shields.io/badge/role-course-blue)](../../eda.md)
[![Parent](https://img.shields.io/badge/parent-eda__learning-informational)](../../README.md)
[![Labs](https://img.shields.io/badge/labs-platform%20tools-success)](https://universal-verification-methodology.github.io/learning/tools/)
[![Domain](https://img.shields.io/badge/domain-congestion-orange)](docs/MODULES.md)

**learn_congestion** is the open learning path for *routing congestion estimation and placement feedback* on tiny GCell grids.

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
learn_congestion/
├── README.md
├── LICENSE
├── common/         # Track A: tiny_cong.json, solvers, tests
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
cd courses/learn_congestion
```

## Consume from the parent

Prereq: [learn_placement](../learn_placement/README.md) / [learn_legalization](../learn_legalization/README.md).  
Next: [learn_global_routing](../learn_global_routing/README.md) or [learn_clock_tree](../learn_clock_tree/README.md).  
Lane map: [`eda.md`](../../eda.md). Scope: [docs/SCOPE.md](docs/SCOPE.md).

## Author: publish or update

```bash
# WSL / Linux — from monorepo root
python3 courses/learn_congestion/scripts/scaffold_course.py   # regenerate stubs carefully
bash courses/learn_congestion/scripts/build_all_media.sh
python3 platform/scripts/publish_course_platform.py learn_congestion
python3 .cursor/skills/module-slides/scripts/verify_course_readme.py \
  courses/learn_congestion --modules
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
| `00-00` | [Welcome to congestion for EDA](module00-00-intro/README.md) | `intro` |
| `01-01` | [GCell grid model](module01-01-gcell-grid/README.md) | `lab` |
| `01-03` | [Capacity vs demand](module01-03-capacity-demand/README.md) | `lab` |
| `02-01` | [RUDY congestion estimate](module02-01-rudy-estimate/README.md) | `lab` |
| `02-03` | [Probabilistic routing demand](module02-03-probabilistic-demand/README.md) | `lab` |
| `02-05` | [Congestion heat map](module02-05-congestion-map/README.md) | `lab` |
| `02-07` | [Overflow metrics](module02-07-overflow-metrics/README.md) | `lab` |
| `03-01` | [Cell inflation](module03-01-cell-inflator/README.md) | `lab` |
| `03-03` | [Congestion-aware net weighting](module03-03-net-weighting/README.md) | `lab` |
| `04-01` | [Placement feedback loop](module04-01-placement-feedback/README.md) | `lab` |
| `05-01` | [Offline benchmark compare](module05-01-offline-benchmark-compare/README.md) | `offline` |
| `99-00` | [Congestion path complete](module99-00-wrap/README.md) | `wrap` |

## Browser labs

By workflow (Track B): `gcell-grid`, `capacity-demand`, `rudy-estimate`, `probabilistic-demand`, `congestion-map`, `overflow-metrics`, `cell-inflator`, `net-weighting`, `placement-feedback`. See [all tools](https://universal-verification-methodology.github.io/learning/tools/) and each module README. Walkthroughs: [docs/WALKTHROUGHS.md](docs/WALKTHROUGHS.md).

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — see [`LICENSE`](LICENSE).
