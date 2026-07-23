# learn_legalization

[![GitHub](https://img.shields.io/badge/GitHub-learn__legalization-181717?logo=github)](https://github.com/universal-verification-methodology/learn_legalization)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-green?logo=creativecommons&logoColor=white)](LICENSE)
[![Role](https://img.shields.io/badge/role-course-orange)](../../eda.md)
[![Parent](https://img.shields.io/badge/parent-learning%20monorepo-0A9EDC)](https://github.com/universal-verification-methodology/learning)
[![Labs](https://img.shields.io/badge/labs-GitHub%20Pages-222?logo=githubpages)](https://universal-verification-methodology.github.io/learning/tools/)
[![Domain](https://img.shields.io/badge/domain-legalization%20%7C%20sites%20%7C%20rows%20%7C%20Abacus-purple)](docs/MODULES.md)

**learn_legalization** is the open learning path for *site/row snapping and overlap removal after global placement*—one full idea per lab, on a tiny site grid.

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
learn_legalization/
├── README.md
├── LICENSE              # CC BY 4.0
├── common/              # tiny_legal.json, legalization helpers
├── docs/
│   ├── MODULES.md       # full module index
│   ├── TWO_TRACKS.md    # Track A (implement) vs Track B (browser)
│   ├── SCOPE.md
│   └── WALKTHROUGHS.md  # algorithm walkthrough map
├── scripts/
│   ├── module.sh
│   ├── scaffold_course.py
│   ├── build_all_media.sh
│   └── capture_all_walkthroughs.sh
├── module00-00-intro/
├── module01-01-site-row-model/
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
- **Syllabus (parent):** [`eda.md` § learn_legalization](../../eda.md)
- **Scope:** [docs/SCOPE.md](docs/SCOPE.md)
- **Prerequisite:** [learn_placement](../learn_placement/README.md)
- **From the monorepo:** open `courses/learn_legalization/` (this tree).

Then open [module00-00-intro/README.md](module00-00-intro/README.md).

## Consume from the parent

From a clone of the **learning** monorepo:

```bash
git clone --recurse-submodules \
  git@github.com:universal-verification-methodology/learning.git
# or, if already cloned without submodules:
git submodule update --init --recursive

ls courses/learn_legalization
```

Working tree path in the parent: `courses/learn_legalization/`.

## Author: publish or update

Edit inside the parent monorepo (recommended).

```bash
# from the learning monorepo checkout
cd courses/learn_legalization
# … edit module README / CHECKLIST / EXAMPLES / transcript …

# rebuild media from the parent (one module at a time; Unix/WSL):
cd ../..
# revise transcript.md, then:
python3 .cursor/skills/module-slides/scripts/transcript_to_outline.py \
  courses/learn_legalization/module01-01-site-row-model
bash .cursor/skills/module-slides/scripts/narrate_clips.sh \
  courses/learn_legalization/module01-01-site-row-model

# bulk (when asked):
# bash courses/learn_legalization/scripts/build_all_media.sh
python3 platform/scripts/publish_course_platform.py learn_legalization
```

Verify README consistency:

```bash
python3 .cursor/skills/module-slides/scripts/verify_course_readme.py \
  courses/learn_legalization --modules
```

See the skill `SKILL.md` for dual-track narration, algorithm walkthrough frames, and the full PPTX → PDF → TTS → MP4 pipeline.

## Two learning tracks

Every **lab** module documents both tracks. Intro/wrap modules have no lab. Details: [docs/TWO_TRACKS.md](docs/TWO_TRACKS.md).

| Track | Practice surface | Start here |
|-------|------------------|------------|
| **A — Implement** | Tiny legal instance + `EXAMPLES.md` / `examples/` | [docs/TWO_TRACKS.md](docs/TWO_TRACKS.md) · `./scripts/module.sh SS-AA --check` |
| **B — Browser lab** | Platform tools | [local tools](http://127.0.0.1:8080/tools/) · [live](https://universal-verification-methodology.github.io/learning/tools/) |

Recommended path: short Track B starter (if shipped) → Track A implement + checklist → optional quiz / transcript review.

## Module landings

Full status table: **[docs/MODULES.md](docs/MODULES.md)**. Clusters: 00 intro · 01 foundations · 02 snap/pack · 03 macros/objectives · 04 global vs detailed · 05 offline · 99 wrap.

| Module | Landing |
|--------|---------|
| 00-00 — Welcome to legalization for EDA | [module00-00-intro](module00-00-intro/README.md) |
| 01-01 — Site and row model | [module01-01-site-row-model](module01-01-site-row-model/README.md) |
| 01-03 — Legality metrics | [module01-03-legality-metrics](module01-03-legality-metrics/README.md) |
| 02-01 — Greedy site/row snap | [module02-01-greedy-snap](module02-01-greedy-snap/README.md) |
| 02-03 — Overlap removal in rows | [module02-03-overlap-removal](module02-03-overlap-removal/README.md) |
| 02-05 — Abacus row packing | [module02-05-abacus-row-pack](module02-05-abacus-row-pack/README.md) |
| 02-07 — Tetris-style row packing | [module02-07-tetris-row-pack](module02-07-tetris-row-pack/README.md) |
| 03-01 — Fixed macros during legalization | [module03-01-fixed-macros](module03-01-fixed-macros/README.md) |
| 03-03 — Displacement vs HPWL tradeoff | [module03-03-displacement-hpwl](module03-03-displacement-hpwl/README.md) |
| 04-01 — Detailed vs global legalize | [module04-01-detailed-vs-global](module04-01-detailed-vs-global/README.md) |
| 05-01 — Offline benchmark compare | [module05-01-offline-benchmark-compare](module05-01-offline-benchmark-compare/README.md) |
| 99-00 — Legalization path complete | [module99-00-wrap](module99-00-wrap/README.md) |

## Browser labs

By workflow (Track B): [site-row-model](https://universal-verification-methodology.github.io/learning/tools/site-row-model/) · [legality-metrics](https://universal-verification-methodology.github.io/learning/tools/legality-metrics/) · [greedy-snap](https://universal-verification-methodology.github.io/learning/tools/greedy-snap/) · [overlap-removal](https://universal-verification-methodology.github.io/learning/tools/overlap-removal/) · [abacus-row-pack](https://universal-verification-methodology.github.io/learning/tools/abacus-row-pack/) · [tetris-row-pack](https://universal-verification-methodology.github.io/learning/tools/tetris-row-pack/) · [fixed-macros](https://universal-verification-methodology.github.io/learning/tools/fixed-macros/) · [displacement-hpwl](https://universal-verification-methodology.github.io/learning/tools/displacement-hpwl/) · [detailed-vs-global](https://universal-verification-methodology.github.io/learning/tools/detailed-vs-global/). Lab tools may still be shipping—use Track A until each id is live. See [all tools](https://universal-verification-methodology.github.io/learning/tools/) and each module README for its primary lab id. Algorithm step walkthroughs: [docs/WALKTHROUGHS.md](docs/WALKTHROUGHS.md).

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — see [`LICENSE`](LICENSE).

Platform tools and the parent monorepo may carry additional notices.
