# learn_clustering

[![GitHub](https://img.shields.io/badge/GitHub-learn__clustering-181717?logo=github)](https://github.com/universal-verification-methodology/learn_clustering)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-green?logo=creativecommons&logoColor=white)](LICENSE)
[![Role](https://img.shields.io/badge/role-course-orange)](../../syllabus.md)
[![Parent](https://img.shields.io/badge/parent-learning%20monorepo-0A9EDC)](https://github.com/universal-verification-methodology/learning)
[![Labs](https://img.shields.io/badge/labs-GitHub%20Pages-222?logo=githubpages)](https://universal-verification-methodology.github.io/learning/tools/)
[![Domain](https://img.shields.io/badge/domain-EDA%20clustering%20%7C%20multilevel%20%7C%20cutsize-purple)](docs/MODULES.md)

**learn_clustering** is the open learning path for *clustering / coarsening algorithms used in EDA physical design*—one full algorithm per lab, on tiny instances.

Readers and students usually **open a module README** (or the live tools) or work from the parent monorepo checkout. Authors edit content here, rebuild slides/audio with **module-slides** in the parent, and publish platform shells when tools + media are ready.

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

```text
learn_clustering/
├── README.md
├── LICENSE              # CC BY 4.0 (add when publishing standalone)
├── common/              # graph I/O, metrics, reference solvers
├── docs/
│   ├── MODULES.md       # full module index
│   ├── TWO_TRACKS.md    # Track A (implement) vs Track B (browser)
│   ├── SCOPE.md
│   └── WALKTHROUGHS.md  # algorithm walkthrough map
├── scripts/
│   ├── module.sh
│   └── build_all_media.sh
├── module00-00-intro/
├── module01-01-affinity-metrics/
│   ├── README.md
│   ├── CHECKLIST.md
│   ├── EXAMPLES.md
│   ├── outline.yaml
│   ├── transcript.md
│   ├── examples/        # Track A
│   └── (optional) slides.pptx / slides.pdf / video.mp4 / assets/
├── …
└── module99-00-wrap/
```

Module folders use **hierarchical ids** `moduleSS-AA-slug` so algorithms can be added later without renumbering.

Videos and decks are optional per module. Generate with the **module-slides** skill (`.cursor/skills/module-slides/`) in the parent monorepo when ready.

## Browse or clone

- **Browser labs:** [https://universal-verification-methodology.github.io/learning/tools/](https://universal-verification-methodology.github.io/learning/tools/)
- **Syllabus (parent):** [`syllabus.md` § learn_clustering](../../syllabus.md)
- **Scope:** [docs/SCOPE.md](docs/SCOPE.md)
- **From the monorepo:** open `courses/learn_clustering/` (this tree).

Then open [module00-00-intro/README.md](module00-00-intro/README.md).

## Consume from the parent

From a clone of the **learning** monorepo:

```bash
git clone --recurse-submodules \
  git@github.com:universal-verification-methodology/learning.git
# or, if already cloned without submodules:
git submodule update --init --recursive

ls courses/learn_clustering
```

Working tree path in the parent: `courses/learn_clustering/`.

## Author: publish or update

Edit inside the parent monorepo (recommended).

```bash
# from the learning monorepo checkout
cd courses/learn_clustering
# … edit module README / CHECKLIST / EXAMPLES / transcript …

# rebuild media from the parent (one module at a time; Unix/WSL):
cd ../..
# revise transcript.md, then:
python3 .cursor/skills/module-slides/scripts/transcript_to_outline.py \
  courses/learn_clustering/module01-01-affinity-metrics
bash .cursor/skills/module-slides/scripts/narrate_clips.sh \
  courses/learn_clustering/module01-01-affinity-metrics

# bulk (when asked):
# bash courses/learn_clustering/scripts/build_all_media.sh
python3 platform/scripts/publish_course_platform.py learn_clustering
```

Verify README consistency:

```bash
python3 .cursor/skills/module-slides/scripts/verify_course_readme.py \
  courses/learn_clustering --modules
```

See the skill `SKILL.md` for dual-track narration, algorithm walkthrough frames, and the full PPTX → PDF → TTS → MP4 pipeline.

## Two learning tracks

Every **lab** module documents both tracks. Intro/wrap modules have no lab. Details: [docs/TWO_TRACKS.md](docs/TWO_TRACKS.md).

| Track | Practice surface | Start here |
|-------|------------------|------------|
| **A — Implement** | Tiny graphs + `EXAMPLES.md` / `examples/` | [docs/TWO_TRACKS.md](docs/TWO_TRACKS.md) · `./scripts/module.sh SS-AA --check` |
| **B — Browser lab** | Platform tools | [local tools](http://127.0.0.1:8080/tools/) · [live](https://universal-verification-methodology.github.io/learning/tools/) |

Recommended path: short Track B starter (if shipped) → Track A implement + checklist → optional quiz / transcript review.

## Module landings

Full status table: **[docs/MODULES.md](docs/MODULES.md)**. Clusters: 00 intro · 01 foundations · 02 classic methods · 03 multilevel/hypergraph · 04 EDA-aware · 05 offline · 99 wrap.

| Module | Landing |
|--------|---------|
| 00-00 — Welcome to clustering for EDA | [module00-00-intro](module00-00-intro/README.md) |
| 01-01 — Affinity metrics | [module01-01-affinity-metrics](module01-01-affinity-metrics/README.md) |
| 01-03 — Greedy pair merge | [module01-03-greedy-pair-merge](module01-03-greedy-pair-merge/README.md) |
| 01-05 — Size-constrained agglomerative | [module01-05-size-constrained-agglomerative](module01-05-size-constrained-agglomerative/README.md) |
| 02-01 — Label propagation | [module02-01-label-propagation](module02-01-label-propagation/README.md) |
| 02-03 — Spectral bisection | [module02-03-spectral-bisection](module02-03-spectral-bisection/README.md) |
| 02-05 — Kernighan–Lin refinement | [module02-05-kernighan-lin](module02-05-kernighan-lin/README.md) |
| 02-07 — Fiduccia–Mattheyses refinement | [module02-07-fiduccia-mattheyses](module02-07-fiduccia-mattheyses/README.md) |
| 03-01 — Multilevel clustering | [module03-01-multilevel-clustering](module03-01-multilevel-clustering/README.md) |
| 03-03 — Hypergraph clustering | [module03-03-hypergraph-clustering](module03-03-hypergraph-clustering/README.md) |
| 04-01 — Congestion-aware clustering | [module04-01-congestion-aware-clustering](module04-01-congestion-aware-clustering/README.md) |
| 04-03 — Timing-aware clustering | [module04-03-timing-aware-clustering](module04-03-timing-aware-clustering/README.md) |
| 05-01 — Offline benchmark compare | [module05-01-offline-benchmark-compare](module05-01-offline-benchmark-compare/README.md) |
| 99-00 — Clustering path complete | [module99-00-wrap](module99-00-wrap/README.md) |

## Browser labs

By workflow (Track B), **shipped:** [affinity-metrics](https://universal-verification-methodology.github.io/learning/tools/affinity-metrics/) · [greedy-pair-merge](https://universal-verification-methodology.github.io/learning/tools/greedy-pair-merge/) · [label-propagation](https://universal-verification-methodology.github.io/learning/tools/label-propagation/) · [kernighan-lin](https://universal-verification-methodology.github.io/learning/tools/kernighan-lin/) · [fiduccia-mattheyses](https://universal-verification-methodology.github.io/learning/tools/fiduccia-mattheyses/). Other lab ids remain planned—use Track A until they ship. See [all tools](https://universal-verification-methodology.github.io/learning/tools/) and each module README for its primary lab id. Algorithm step walkthroughs: [docs/WALKTHROUGHS.md](docs/WALKTHROUGHS.md).

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — add a course-root [`LICENSE`](LICENSE) when publishing this tree as a standalone repo; until then materials are intended for CC BY 4.0 alignment with the digital_learning courses.

Platform tools and the parent monorepo may carry additional notices.
