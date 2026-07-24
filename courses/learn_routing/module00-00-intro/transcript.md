# Welcome to detailed routing for EDA

**Module id:** module00-00-intro
**Lab:** none
**Tracks:** intro (dual-track welcome)

## Slide 1 — Detailed routing in the stack

You committed coarse paths in global routing. Detailed routing assigns tracks on M1 and M2, places vias, and chases DRC-clean geometry before compaction or signoff. This course teaches that grid, maze, A*, track usage, vias, spacing, and rip-up on a tiny chip.

## Slide 2 — Two tracks

![Tools index](assets/tools-index.png)

Track B is the browser lab: route nets, watch track heat, inspect vias, clear challenges. Track A is implement: Python solvers on tiny_dr.json. Use either or both. Browser first for intuition is fine.

## Slide 3 — Course map

Foundations cover the routing grid and pin access. Algorithms cover Lee maze, A*, track usage, and via assignment. DRC and rip-up cover spacing lite and detailed rip-up. Sequential detailed ties the flow together. Offline compare and wrap close the path.

## Slide 4 — Prerequisites

Finish learn_global_routing so GCell graphs and edge usage deposits already make sense. Directed track usage is finer-grained—not the same keys as GCell edges.

## Slide 5 — How to move

Read each module README, pick a track, check the checklist, then skim the clip when media is available. Odd module slots leave room to insert algorithms later without renumbering.

## Slide 6 — Next

Open the routing grid graph and enumerate M1 and M2 tracks on the twelve-by-eight grid.
