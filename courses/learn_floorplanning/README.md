# learn_floorplanning

[![GitHub](https://img.shields.io/badge/GitHub-learn__floorplanning-181717?logo=github)](https://github.com/universal-verification-methodology/learn_floorplanning)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-green?logo=creativecommons&logoColor=white)](LICENSE)
[![Role](https://img.shields.io/badge/role-course-orange)](../../syllabus.md)
[![Parent](https://img.shields.io/badge/parent-learning%20monorepo-0A9EDC)](https://github.com/universal-verification-methodology/learning)
[![Labs](https://img.shields.io/badge/labs-GitHub%20Pages-222?logo=githubpages)](https://universal-verification-methodology.github.io/learning/tools/)
[![Domain](https://img.shields.io/badge/domain-floorplanning-purple)](docs/MODULES.md)

**learn_floorplanning** is the open learning path for *fixed-outline floorplanning representations and search used in EDA physical design*—one full idea per lab, on tiny modules.

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
learn_floorplanning/
├── README.md
├── LICENSE              # CC BY 4.0
├── common/              # tiny_modules.json, shared helpers
├── docs/
│   ├── MODULES.md       # full module index
│   ├── TWO_TRACKS.md    # Track A (implement) vs Track B (browser)
│   ├── SCOPE.md
│   └── WALKTHROUGHS.md  # algorithm walkthrough map
├── scripts/
│   ├── module.sh
│   ├── scaffold_course.py
│   └── build_all_media.sh
├── module00-00-intro/
├── module01-01-fixed-outline/
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
- **Syllabus (parent):** [`syllabus.md` § learn_floorplanning](../../syllabus.md)
- **Scope:** [docs/SCOPE.md](docs/SCOPE.md)
- **From the monorepo:** open `courses/learn_floorplanning/` (this tree).

Then open [module00-00-intro/README.md](module00-00-intro/README.md).

## Consume from the parent

From a clone of the **learning** monorepo:

```bash
git clone --recurse-submodules \
  git@github.com:universal-verification-methodology/learning.git
# or, if already cloned without submodules:
git submodule update --init --recursive

ls courses/learn_floorplanning
```

Working tree path in the parent: `courses/learn_floorplanning/`.

## Author: publish or update

Edit inside the parent monorepo (recommended).

```bash
# from the learning monorepo checkout
cd courses/learn_floorplanning
# … edit module README / CHECKLIST / EXAMPLES / transcript …

# rebuild media from the parent (one module at a time; Unix/WSL):
cd ../..
# revise transcript.md, then:
python3 .cursor/skills/module-slides/scripts/transcript_to_outline.py \
  courses/learn_floorplanning/module01-01-fixed-outline
bash .cursor/skills/module-slides/scripts/narrate_clips.sh \
  courses/learn_floorplanning/module01-01-fixed-outline

# bulk (when asked):
# bash courses/learn_floorplanning/scripts/build_all_media.sh
python3 platform/scripts/publish_course_platform.py learn_floorplanning
```

Verify README consistency:

```bash
python3 .cursor/skills/module-slides/scripts/verify_course_readme.py \
  courses/learn_floorplanning --modules
```

See the skill `SKILL.md` for dual-track narration, algorithm walkthrough frames, and the full PPTX → PDF → TTS → MP4 pipeline.

## Two learning tracks

Every **lab** module documents both tracks. Intro/wrap modules have no lab. Details: [docs/TWO_TRACKS.md](docs/TWO_TRACKS.md).

| Track | Practice surface | Start here |
|-------|------------------|------------|
| **A — Implement** | Tiny modules + `EXAMPLES.md` / `examples/` | [docs/TWO_TRACKS.md](docs/TWO_TRACKS.md) · `./scripts/module.sh SS-AA --check` |
| **B — Browser lab** | Platform tools | [local tools](http://127.0.0.1:8080/tools/) · [live](https://universal-verification-methodology.github.io/learning/tools/) |

Recommended path: short Track B starter (if shipped) → Track A implement + checklist → optional quiz / transcript review.

## Module landings

Full status table: **[docs/MODULES.md](docs/MODULES.md)**. Clusters: 00 intro · 01 foundations · 02 representations · 03 search/blocks · 04 hierarchy/pins · 05 offline · 99 wrap.

| Module | Landing |
|--------|---------|
| 00-00 — Welcome to floorplanning for EDA | [module00-00-intro](module00-00-intro/README.md) |
| 01-01 — Fixed-outline constraints | [module01-01-fixed-outline](module01-01-fixed-outline/README.md) |
| 01-03 — Area, packing density, whitespace/deadspace | [module01-03-area-deadspace](module01-03-area-deadspace/README.md) |
| 02-01 — Slicing tree / polish expression packing | [module02-01-slicing-floorplan](module02-01-slicing-floorplan/README.md) |
| 02-03 — B*-tree floorplan representation | [module02-03-bstar-tree](module02-03-bstar-tree/README.md) |
| 02-05 — Sequence-pair representation | [module02-05-sequence-pair](module02-05-sequence-pair/README.md) |
| 03-01 — Simulated annealing floorplan search | [module03-01-simulated-annealing-fp](module03-01-simulated-annealing-fp/README.md) |
| 03-03 — Soft module aspect sizing | [module03-03-soft-module-sizing](module03-03-soft-module-sizing/README.md) |
| 03-05 — Hard macro / fixed-block placement | [module03-05-macro-placement](module03-05-macro-placement/README.md) |
| 04-01 — Hierarchical floorplanning | [module04-01-hierarchical-floorplan](module04-01-hierarchical-floorplan/README.md) |
| 04-03 — Boundary pin / I/O assignment | [module04-03-pin-assignment](module04-03-pin-assignment/README.md) |
| 05-01 — Offline benchmark compare | [module05-01-offline-benchmark-compare](module05-01-offline-benchmark-compare/README.md) |
| 99-00 — Floorplanning path complete | [module99-00-wrap](module99-00-wrap/README.md) |

## Browser labs

By workflow (Track B): [fixed-outline](https://universal-verification-methodology.github.io/learning/tools/fixed-outline/) · [area-deadspace](https://universal-verification-methodology.github.io/learning/tools/area-deadspace/) · [slicing-floorplan](https://universal-verification-methodology.github.io/learning/tools/slicing-floorplan/) · [bstar-tree](https://universal-verification-methodology.github.io/learning/tools/bstar-tree/) · [sequence-pair](https://universal-verification-methodology.github.io/learning/tools/sequence-pair/) · [simulated-annealing-fp](https://universal-verification-methodology.github.io/learning/tools/simulated-annealing-fp/) · [soft-module-sizing](https://universal-verification-methodology.github.io/learning/tools/soft-module-sizing/) · [macro-placement](https://universal-verification-methodology.github.io/learning/tools/macro-placement/) · [hierarchical-floorplan](https://universal-verification-methodology.github.io/learning/tools/hierarchical-floorplan/) · [pin-assignment](https://universal-verification-methodology.github.io/learning/tools/pin-assignment/). Lab tools may still be shipping—use Track A until each id is live. See [all tools](https://universal-verification-methodology.github.io/learning/tools/) and each module README for its primary lab id. Algorithm step walkthroughs: [docs/WALKTHROUGHS.md](docs/WALKTHROUGHS.md).

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — see [`LICENSE`](LICENSE).

Platform tools and the parent monorepo may carry additional notices.
