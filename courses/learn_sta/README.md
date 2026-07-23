# learn_sta

[![GitHub](https://img.shields.io/badge/GitHub-learn__sta-181717?logo=github)](https://github.com/universal-verification-methodology/learn_sta)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-green?logo=creativecommons&logoColor=white)](LICENSE)
[![Role](https://img.shields.io/badge/role-course-orange)](../../eda.md)
[![Parent](https://img.shields.io/badge/parent-learning%20monorepo-0A9EDC)](https://github.com/universal-verification-methodology/learning)
[![Labs](https://img.shields.io/badge/labs-GitHub%20Pages-222?logo=githubpages)](https://universal-verification-methodology.github.io/learning/tools/)
[![Domain](https://img.shields.io/badge/domain-EDA%20STA%20%7C%20timing%20graph%20%7C%20slack-purple)](docs/MODULES.md)

**learn_sta** is the open learning path for *static timing analysis algorithms used in digital design*—timing graph, arrival/required, slack, critical path, and incremental update on tiny netlists.

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
learn_sta/
├── README.md
├── LICENSE              # CC BY 4.0 (add when publishing standalone)
├── common/              # netlist I/O, propagation helpers, goldens
├── docs/
│   ├── MODULES.md       # full module index
│   ├── TWO_TRACKS.md    # Track A (implement) vs Track B (browser)
│   ├── SCOPE.md
│   └── WALKTHROUGHS.md  # algorithm walkthrough map
├── scripts/
│   ├── scaffold_course.py
│   └── build_all_media.sh
├── module00-00-intro/
├── module01-01-timing-graph/
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
- **Syllabus (parent):** [`eda.md` § learn_sta](../../eda.md)
- **Scope:** [docs/SCOPE.md](docs/SCOPE.md)
- **From the monorepo:** open `courses/learn_sta/` (this tree).

Then open [module00-00-intro/README.md](module00-00-intro/README.md).

## Consume from the parent

From a clone of the **learning** monorepo:

```bash
git clone --recurse-submodules \
  git@github.com:universal-verification-methodology/learning.git
# or, if already cloned without submodules:
git submodule update --init --recursive

ls courses/learn_sta
```

Working tree path in the parent: `courses/learn_sta/`.

## Author: publish or update

Edit inside the parent monorepo (recommended).

```bash
# from the learning monorepo checkout
cd courses/learn_sta
# … edit module README / CHECKLIST / EXAMPLES / transcript …

# rebuild media from the parent (one module at a time; Unix/WSL):
cd ../..
# revise transcript.md, then:
python3 .cursor/skills/module-slides/scripts/transcript_to_outline.py \
  courses/learn_sta/module01-01-timing-graph
bash .cursor/skills/module-slides/scripts/narrate_clips.sh \
  courses/learn_sta/module01-01-timing-graph

# bulk (when asked):
# bash courses/learn_sta/scripts/build_all_media.sh
python3 platform/scripts/publish_course_platform.py learn_sta
```

Verify README consistency:

```bash
python3 .cursor/skills/module-slides/scripts/verify_course_readme.py \
  courses/learn_sta --modules
```

See the skill `SKILL.md` for dual-track narration, algorithm walkthrough frames, and the full PPTX → PDF → TTS → MP4 pipeline.

## Two learning tracks

Every **lab** module documents both tracks. Intro/wrap modules have no lab. Details: [docs/TWO_TRACKS.md](docs/TWO_TRACKS.md).

| Track | Practice surface | Start here |
|-------|------------------|------------|
| **A — Implement** | Tiny netlists + `EXAMPLES.md` / `examples/` | [docs/TWO_TRACKS.md](docs/TWO_TRACKS.md) |
| **B — Browser lab** | Platform tools | [local tools](http://127.0.0.1:8080/tools/) · [live](https://universal-verification-methodology.github.io/learning/tools/) |

Recommended path: short Track B starter → Track A implement + checklist → optional quiz / transcript review.

## Module landings

Full status table: **[docs/MODULES.md](docs/MODULES.md)**. Clusters: 00 intro · 01 foundations · 02 slack/critical path · 03 incremental + exceptions · 05 offline · 99 wrap.

| Module | Landing |
|--------|---------|
| 00-00 — Welcome to static timing analysis | [module00-00-intro](module00-00-intro/README.md) |
| 01-01 — Timing graph | [module01-01-timing-graph](module01-01-timing-graph/README.md) |
| 01-03 — Arrival and required times | [module01-03-arrival-required](module01-03-arrival-required/README.md) |
| 02-01 — Slack, setup, and hold | [module02-01-slack-setup-hold](module02-01-slack-setup-hold/README.md) |
| 02-03 — Critical path | [module02-03-critical-path](module02-03-critical-path/README.md) |
| 03-01 — Incremental timing update | [module03-01-incremental-update](module03-01-incremental-update/README.md) |
| 03-03 — False and multicycle paths (engine view) | [module03-03-false-multicycle-lite](module03-03-false-multicycle-lite/README.md) |
| 05-01 — Offline benchmark compare | [module05-01-offline-benchmark-compare](module05-01-offline-benchmark-compare/README.md) |
| 99-00 — STA path complete | [module99-00-wrap](module99-00-wrap/README.md) |

## Browser labs

By workflow (Track B), **shipped:** [timing-graph](https://universal-verification-methodology.github.io/learning/tools/timing-graph/) · [arrival-required](https://universal-verification-methodology.github.io/learning/tools/arrival-required/) · [slack-setup-hold](https://universal-verification-methodology.github.io/learning/tools/slack-setup-hold/) · [critical-path](https://universal-verification-methodology.github.io/learning/tools/critical-path/) · [incremental-update](https://universal-verification-methodology.github.io/learning/tools/incremental-update/) · [false-multicycle-lite](https://universal-verification-methodology.github.io/learning/tools/false-multicycle-lite/). Offline compare remains Track A / harness only. See [all tools](https://universal-verification-methodology.github.io/learning/tools/) and each module README for its primary lab id. Algorithm step walkthroughs: [docs/WALKTHROUGHS.md](docs/WALKTHROUGHS.md).

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — add a course-root [`LICENSE`](LICENSE) when publishing this tree as a standalone repo; until then materials are intended for CC BY 4.0 alignment with the digital_learning courses.

Platform tools and the parent monorepo may carry additional notices.
