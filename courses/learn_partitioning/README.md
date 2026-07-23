# learn_partitioning

[![Role](https://img.shields.io/badge/role-course%20scaffold-orange)](../../eda.md)
[![Domain](https://img.shields.io/badge/domain-EDA%20partitioning%20%7C%20cutsize%20%7C%20KL%2FFM-purple)](docs/MODULES.md)

**learn_partitioning** is the open learning path for *bipartition and multiway partitioning algorithms used in EDA physical design*—one full algorithm per lab, on tiny instances.

- Scope: [docs/SCOPE.md](docs/SCOPE.md)
- Modules: [docs/MODULES.md](docs/MODULES.md)
- Tracks: [docs/TWO_TRACKS.md](docs/TWO_TRACKS.md)

## Contents

```text
learn_partitioning/
├── README.md
├── common/         # graph I/O, metrics, reference helpers
├── docs/           # MODULES, TWO_TRACKS, SCOPE
├── scripts/        # scaffold_course.py, build_all_media.sh
├── module00-00-intro/
├── …
└── module99-00-wrap/
```

Module folders use **hierarchical ids** `moduleSS-AA-slug` so algorithms can be added later without renumbering.

## Two learning tracks

| Track | Practice surface |
|-------|------------------|
| **A** | Implement full algorithms on tiny graphs (`EXAMPLES.md`) |
| **B** | Browser labs under `platform/tools/` |

## Module landings

Full table: **[docs/MODULES.md](docs/MODULES.md)**.

| Module | Landing |
|--------|---------|
| module00-00-intro — Welcome to partitioning for EDA | [module00-00-intro](module00-00-intro/README.md) |
| module01-01-cutsize-balance — Cutsize and balance | [module01-01-cutsize-balance](module01-01-cutsize-balance/README.md) |
| module01-03-initial-bipartition — Initial bipartition | [module01-03-initial-bipartition](module01-03-initial-bipartition/README.md) |
| module02-01-kl-partition — Kernighan–Lin bipartition | [module02-01-kl-partition](module02-01-kl-partition/README.md) |
| module02-03-fm-partition — Fiduccia–Mattheyses bipartition | [module02-03-fm-partition](module02-03-fm-partition/README.md) |
| module02-05-spectral-partition — Spectral bipartition | [module02-05-spectral-partition](module02-05-spectral-partition/README.md) |
| module02-07-recursive-bisection — Recursive bisection | [module02-07-recursive-bisection](module02-07-recursive-bisection/README.md) |
| module03-01-multiway-partition — Multiway partitioning | [module03-01-multiway-partition](module03-01-multiway-partition/README.md) |
| module03-03-terminal-propagation — Terminal propagation | [module03-03-terminal-propagation](module03-03-terminal-propagation/README.md) |
| module03-05-hypergraph-partition — Hypergraph partitioning | [module03-05-hypergraph-partition](module03-05-hypergraph-partition/README.md) |
| module04-01-multilevel-partition — Multilevel partitioning | [module04-01-multilevel-partition](module04-01-multilevel-partition/README.md) |
| module05-01-offline-benchmark-compare — Offline benchmark compare | [module05-01-offline-benchmark-compare](module05-01-offline-benchmark-compare/README.md) |
| module99-00-wrap — Partitioning path complete | [module99-00-wrap](module99-00-wrap/README.md) |

## Author: module-slides

From the monorepo root (WSL):

```bash
python3 .cursor/skills/module-slides/scripts/transcript_to_outline.py \
  courses/learn_partitioning/module01-01-cutsize-balance
python3 .cursor/skills/module-slides/scripts/build_pptx.py \
  courses/learn_partitioning/module01-01-cutsize-balance
bash courses/learn_partitioning/scripts/build_all_media.sh
```

## License

Course materials intended for CC BY 4.0 alignment with the digital_learning courses (add `LICENSE` when publishing).
