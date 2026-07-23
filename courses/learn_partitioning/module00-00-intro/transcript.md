# Welcome to partitioning for EDA

**Module id:** module00-00-intro
**Lab:** none (intro)
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Welcome to partitioning for EDA

Physical design repeatedly asks: how do we cut a design into balanced pieces with few wires between them? That is partitioning. This course teaches bipartition and multiway algorithms as full implementations on tiny graphs—so you build literacy for floorplanning, placement multilevel, and FPGA packing later.

## Slide 2 — What you’ll build

You’ll start with cutsize and balance, then form an initial legal bipartition. Classic methods follow: Kernighan–Lin, Fiduccia–Mattheyses, spectral bipartition, and recursive bisection. Then multiway, terminal propagation, hypergraph cuts, and a multilevel V-cycle. One algorithm per lab. Full implementations at course scale—not production throughput, but complete and correct on the scoped instances.

## Slide 3 — Stable module ids

Module folders use hierarchical ids: section, then algorithm slot—like module two dash zero one for Kernighan–Lin. That way we can add algorithms later without renumbering everything. Odd slots leave room for inserts. Treat published ids as stable keys; display order lives in the module index.

## Slide 4 — Two tracks

Every lab module offers two practice tracks. Track A is implement: code the algorithm, run tiny graphs, report metrics. Track B is the browser lab shelf for visual intuition. A good rhythm is browser first for the idea, then implement to harden it. Intro and wrap modules have no lab.

## Slide 5 — How to move

For each module, read the README for outcomes, pick a track—or both—then work the checklist. Keep cutsize and balance as your habit. When this intro checklist is done, continue to cutsize and balance—the shared language every later algorithm will use.
