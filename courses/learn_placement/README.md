# learn_placement

[![Role](https://img.shields.io/badge/role-course%20scaffold-orange)](../../eda.md)
[![Domain](https://img.shields.io/badge/domain-EDA%20placement%20%7C%20HPWL%20%7C%20density-purple)](docs/MODULES.md)

**learn_placement** is the open learning path for *global placement algorithms used in EDA physical design*—one full algorithm per lab, on a tiny instance.

- Scope: [docs/SCOPE.md](docs/SCOPE.md)
- Modules: [docs/MODULES.md](docs/MODULES.md)
- Tracks: [docs/TWO_TRACKS.md](docs/TWO_TRACKS.md)
- Walkthroughs: [docs/WALKTHROUGHS.md](docs/WALKTHROUGHS.md)

## Contents

```text
learn_placement/
├── README.md
├── common/         # placement I/O, HPWL, reference solvers
├── docs/           # MODULES, TWO_TRACKS, SCOPE, WALKTHROUGHS
├── scripts/        # scaffold_course.py, enrich_transcripts.py, build_all_media.sh
├── module00-00-intro/
├── …
└── module99-00-wrap/
```

Module folders use **hierarchical ids** `moduleSS-AA-slug` so algorithms can be added later without renumbering.

## Two learning tracks

| Track | Practice surface |
|-------|------------------|
| **A** | Implement full algorithms on the tiny placement (`EXAMPLES.md`) |
| **B** | Browser labs under `platform/tools/` |

## Module landings

Full table: **[docs/MODULES.md](docs/MODULES.md)**.

| Module | Landing |
|--------|---------|
| module00-00-intro — Welcome to placement for EDA | [module00-00-intro](module00-00-intro/README.md) |
| module01-01-hpwl-metrics — Half-perimeter wirelength | [module01-01-hpwl-metrics](module01-01-hpwl-metrics/README.md) |
| module01-03-net-models — Net models for wirelength | [module01-03-net-models](module01-03-net-models/README.md) |
| module02-01-force-directed-place — Force-directed placement | [module02-01-force-directed-place](module02-01-force-directed-place/README.md) |
| module02-03-quadratic-place — Quadratic placement | [module02-03-quadratic-place](module02-03-quadratic-place/README.md) |
| module02-05-analytical-place — Analytical / density-aware place | [module02-05-analytical-place](module02-05-analytical-place/README.md) |
| module02-07-sa-placement — Simulated annealing placement | [module02-07-sa-placement](module02-07-sa-placement/README.md) |
| module03-01-density-bins — Density bins and overflow | [module03-01-density-bins](module03-01-density-bins/README.md) |
| module03-03-spread-legalize-lite — Spreading / overlap relief | [module03-03-spread-legalize-lite](module03-03-spread-legalize-lite/README.md) |
| module04-01-timing-driven-place — Timing-driven placement | [module04-01-timing-driven-place](module04-01-timing-driven-place/README.md) |
| module05-01-offline-benchmark-compare — Offline benchmark compare | [module05-01-offline-benchmark-compare](module05-01-offline-benchmark-compare/README.md) |
| module99-00-wrap — Placement path complete | [module99-00-wrap](module99-00-wrap/README.md) |

## Author: module-slides

From the monorepo root (WSL):

```bash
python3 .cursor/skills/module-slides/scripts/transcript_to_outline.py \
  courses/learn_placement/module01-01-hpwl-metrics
python3 .cursor/skills/module-slides/scripts/build_pptx.py \
  courses/learn_placement/module01-01-hpwl-metrics
bash courses/learn_placement/scripts/build_all_media.sh
```

## License

Course materials intended for CC BY 4.0 alignment with the digital_learning courses (add `LICENSE` when publishing).
