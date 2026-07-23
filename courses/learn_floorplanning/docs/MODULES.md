# learn_floorplanning — module index

Lab-driven syllabus with **hierarchical module ids** (`moduleSS-AA-slug`).
Odd `AA` slots are preferred so new algorithms can be inserted without renumbering.
Published ids are **stable keys**; order below is the teaching path.

Status: **ref** = reference / lab id reserved for `platform/tools/` (algorithm modules).

| Id | Kind | Module | Lab / activity | Status |
|----|------|--------|----------------|--------|
| `module00-00-intro` | `intro` | [Welcome to floorplanning for EDA](../module00-00-intro/README.md) | — | — |
| `module01-01-fixed-outline` | `lab` | [Fixed-outline constraints](../module01-01-fixed-outline/README.md) | `fixed-outline` | **ref** |
| `module01-03-area-deadspace` | `lab` | [Area, packing density, whitespace/deadspace](../module01-03-area-deadspace/README.md) | `area-deadspace` | **ref** |
| `module02-01-slicing-floorplan` | `lab` | [Slicing tree / polish expression packing](../module02-01-slicing-floorplan/README.md) | `slicing-floorplan` | **ref** |
| `module02-03-bstar-tree` | `lab` | [B*-tree floorplan representation](../module02-03-bstar-tree/README.md) | `bstar-tree` | **ref** |
| `module02-05-sequence-pair` | `lab` | [Sequence-pair representation](../module02-05-sequence-pair/README.md) | `sequence-pair` | **ref** |
| `module03-01-simulated-annealing-fp` | `lab` | [Simulated annealing floorplan search](../module03-01-simulated-annealing-fp/README.md) | `simulated-annealing-fp` | **ref** |
| `module03-03-soft-module-sizing` | `lab` | [Soft module aspect sizing](../module03-03-soft-module-sizing/README.md) | `soft-module-sizing` | **ref** |
| `module03-05-macro-placement` | `lab` | [Hard macro / fixed-block placement](../module03-05-macro-placement/README.md) | `macro-placement` | **ref** |
| `module04-01-hierarchical-floorplan` | `lab` | [Hierarchical floorplanning](../module04-01-hierarchical-floorplan/README.md) | `hierarchical-floorplan` | **ref** |
| `module04-03-pin-assignment` | `lab` | [Boundary pin / I/O assignment](../module04-03-pin-assignment/README.md) | `pin-assignment` | **ref** |
| `module05-01-offline-benchmark-compare` | `offline` | [Offline benchmark compare](../module05-01-offline-benchmark-compare/README.md) | offline harness | P |
| `module99-00-wrap` | `wrap` | [Floorplanning path complete](../module99-00-wrap/README.md) | — | — |

## Sections

| Section | Focus |
|---------|--------|
| `00` | Intro |
| `01` | Foundations (fixed outline, area / deadspace) |
| `02` | Representations (slicing, B*-tree, sequence pair) |
| `03` | Search & blocks (SA, soft modules, macros) |
| `04` | Hierarchy & pins |
| `05` | Offline evidence |
| `99` | Wrap |

## Dual tracks

See [TWO_TRACKS.md](TWO_TRACKS.md).

## Algorithm walkthroughs (PPT / transcript)

When walkthrough frames exist: each lab module may have `assets/STEPS.md` and `assets/steps/*.png`. Map: [WALKTHROUGHS.md](WALKTHROUGHS.md).

**Build media in WSL** (LibreOffice + edge-tts + ffmpeg):

```bash
cd /mnt/d/proj/designs/eda_learning
bash courses/learn_floorplanning/scripts/build_all_media.sh
```
