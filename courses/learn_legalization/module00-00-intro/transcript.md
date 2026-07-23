# Welcome to legalization for EDA

**Module id:** module00-00-intro
**Lab:** none (intro)
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Welcome to legalization

Global placement spreads cells for wirelength and density—but coordinates float freely. Legalization snaps them to rows and sites, removes overlaps, and respects fixed macros before routing. This course teaches that transition on a tiny twelve-site grid so detailed routing has a legal canvas.

## Slide 2 — What you'll build

You'll model sites and rows, check legality, greedy-snap floats, remove overlaps, and pack rows with Abacus and Tetris-style algorithms. Then legalize around fixed macros, measure displacement versus HPWL, and contrast global versus detailed passes. Nine browser labs have step-by-step algorithm walkthroughs with verified goldens.

## Slide 3 — Prerequisite path

Finish **learn_placement** first: you need global-place floats and HPWL intuition. Floorplanning and clustering further upstream set the outline; legalization assumes cells already have rough (x, y) targets.

## Slide 4 — Two tracks

Every lab offers Track A—implement on `tiny_legal.json`—and Track B—browser labs with interactive walkthroughs. Good rhythm: browser for row/site intuition, implement to harden checkers and packers.

## Slide 5 — How to move

Read each README, pick a track, work the checklist. Keep legality, displacement, and HPWL as habits. When intro checklist is done, continue to site and row model—the geometry contract for every later algorithm.
