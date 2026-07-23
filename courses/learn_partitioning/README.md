# learn_partitioning

[![GitHub](https://img.shields.io/badge/GitHub-learn__partitioning-181717?logo=github)](https://github.com/universal-verification-methodology/learn_partitioning)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-green?logo=creativecommons&logoColor=white)](LICENSE)
[![Role](https://img.shields.io/badge/role-course-orange)](../../syllabus.md)
[![Parent](https://img.shields.io/badge/parent-learning%20monorepo-0A9EDC)](https://github.com/universal-verification-methodology/learning)
[![Labs](https://img.shields.io/badge/labs-GitHub%20Pages-222?logo=githubpages)](https://universal-verification-methodology.github.io/learning/tools/)
[![Domain](https://img.shields.io/badge/domain-EDA%20partitioning%20%7C%20cutsize%20%7C%20KL%2FFM-purple)](docs/MODULES.md)

**learn_partitioning** is the open learning path for *bipartition and multiway partitioning algorithms used in EDA physical design*—one full algorithm per lab, on tiny instances.

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
learn_partitioning/
├── README.md
├── LICENSE              # CC BY 4.0 (add when publishing standalone)
├── common/              # graph I/O, metrics, reference helpers
├── docs/
│   ├── MODULES.md       # full module index
│   ├── TWO_TRACKS.md    # Track A (implement) vs Track B (browser)
│   ├── SCOPE.md
│   └── WALKTHROUGHS.md  # algorithm walkthrough map
├── scripts/
│   ├── scaffold_course.py
│   └── build_all_media.sh
├── module00-00-intro/
├── module01-01-cutsize-balance/
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
- **Syllabus (parent):** [`syllabus.md` § learn_partitioning](../../syllabus.md)
- **Scope:** [docs/SCOPE.md](docs/SCOPE.md)
- **From the monorepo:** open `courses/learn_partitioning/` (this tree).

Then open [module00-00-intro/README.md](module00-00-intro/README.md).

## Consume from the parent

From a clone of the **learning** monorepo:

```bash
git clone --recurse-submodules \
  git@github.com:universal-verification-methodology/learning.git
# or, if already cloned without submodules:
git submodule update --init --recursive

ls courses/learn_partitioning
```

Working tree path in the parent: `courses/learn_partitioning/`.

## Author: publish or update

Edit inside the parent monorepo (recommended).

```bash
# from the learning monorepo checkout
cd courses/learn_partitioning
# … edit module README / CHECKLIST / EXAMPLES / transcript …

# rebuild media from the parent (one module at a time; Unix/WSL):
cd ../..
# revise transcript.md, then:
python3 .cursor/skills/module-slides/scripts/transcript_to_outline.py \
  courses/learn_partitioning/module01-01-cutsize-balance
bash .cursor/skills/module-slides/scripts/narrate_clips.sh \
  courses/learn_partitioning/module01-01-cutsize-balance

# bulk (when asked):
# bash courses/learn_partitioning/scripts/build_all_media.sh
python3 platform/scripts/publish_course_platform.py learn_partitioning
```

Verify README consistency:

```bash
python3 .cursor/skills/module-slides/scripts/verify_course_readme.py \
  courses/learn_partitioning --modules
```

See the skill `SKILL.md` for dual-track narration, algorithm walkthrough frames, and the full PPTX → PDF → TTS → MP4 pipeline.

## Two learning tracks

Every **lab** module documents both tracks. Intro/wrap modules have no lab. Details: [docs/TWO_TRACKS.md](docs/TWO_TRACKS.md).

| Track | Practice surface | Start here |
|-------|------------------|------------|
| **A — Implement** | Tiny graphs + `EXAMPLES.md` / `examples/` | [docs/TWO_TRACKS.md](docs/TWO_TRACKS.md) |
| **B — Browser lab** | Platform tools | [local tools](http://127.0.0.1:8080/tools/) · [live](https://universal-verification-methodology.github.io/learning/tools/) |

Recommended path: short Track B starter (if shipped) → Track A implement + checklist → optional quiz / transcript review.

## Module landings

Full status table: **[docs/MODULES.md](docs/MODULES.md)**. Clusters: 00 intro · 01 foundations · 02 classic bipartition · 03 multiway/terminals/hypergraph · 04 multilevel · 05 offline · 99 wrap.

| Module | Landing |
|--------|---------|
| 00-00 — Welcome to partitioning for EDA | [module00-00-intro](module00-00-intro/README.md) |
| 01-01 — Cutsize and balance | [module01-01-cutsize-balance](module01-01-cutsize-balance/README.md) |
| 01-03 — Initial bipartition | [module01-03-initial-bipartition](module01-03-initial-bipartition/README.md) |
| 02-01 — Kernighan–Lin bipartition | [module02-01-kl-partition](module02-01-kl-partition/README.md) |
| 02-03 — Fiduccia–Mattheyses bipartition | [module02-03-fm-partition](module02-03-fm-partition/README.md) |
| 02-05 — Spectral bipartition | [module02-05-spectral-partition](module02-05-spectral-partition/README.md) |
| 02-07 — Recursive bisection | [module02-07-recursive-bisection](module02-07-recursive-bisection/README.md) |
| 03-01 — Multiway partitioning | [module03-01-multiway-partition](module03-01-multiway-partition/README.md) |
| 03-03 — Terminal propagation | [module03-03-terminal-propagation](module03-03-terminal-propagation/README.md) |
| 03-05 — Hypergraph partitioning | [module03-05-hypergraph-partition](module03-05-hypergraph-partition/README.md) |
| 04-01 — Multilevel partitioning | [module04-01-multilevel-partition](module04-01-multilevel-partition/README.md) |
| 05-01 — Offline benchmark compare | [module05-01-offline-benchmark-compare](module05-01-offline-benchmark-compare/README.md) |
| 99-00 — Partitioning path complete | [module99-00-wrap](module99-00-wrap/README.md) |

## Browser labs

By workflow (Track B), **shipped:** [cutsize-balance](https://universal-verification-methodology.github.io/learning/tools/cutsize-balance/) · [initial-bipartition](https://universal-verification-methodology.github.io/learning/tools/initial-bipartition/) · [kl-partition](https://universal-verification-methodology.github.io/learning/tools/kl-partition/) · [fm-partition](https://universal-verification-methodology.github.io/learning/tools/fm-partition/) · [spectral-partition](https://universal-verification-methodology.github.io/learning/tools/spectral-partition/) · [recursive-bisection](https://universal-verification-methodology.github.io/learning/tools/recursive-bisection/) · [multiway-partition](https://universal-verification-methodology.github.io/learning/tools/multiway-partition/) · [terminal-propagation](https://universal-verification-methodology.github.io/learning/tools/terminal-propagation/) · [hypergraph-partition](https://universal-verification-methodology.github.io/learning/tools/hypergraph-partition/) · [multilevel-partition](https://universal-verification-methodology.github.io/learning/tools/multilevel-partition/). Offline compare remains Track A / harness only. See [all tools](https://universal-verification-methodology.github.io/learning/tools/) and each module README for its primary lab id. Algorithm step walkthroughs: [docs/WALKTHROUGHS.md](docs/WALKTHROUGHS.md).

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — add a course-root [`LICENSE`](LICENSE) when publishing this tree as a standalone repo; until then materials are intended for CC BY 4.0 alignment with the digital_learning courses.

Platform tools and the parent monorepo may carry additional notices.
