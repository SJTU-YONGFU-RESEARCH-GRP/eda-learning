# Welcome to floorplanning for EDA

**Module id:** module00-00-intro
**Lab:** none (intro)
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Welcome to floorplanning for EDA

After clustering and partitioning, physical design asks a geometric question: how do we pack blocks into a fixed chip outline? That is floorplanning. This course teaches fixed-outline packing, classic representations, and search—as full implementations on tiny modules—so placement and legalization make sense later.

## Slide 2 — What you’ll build

You’ll start with outline legality, area, density, and deadspace. Then slicing trees and polish expressions, B*-trees, and sequence pairs. Simulated annealing searches those encodings. Soft modules change aspect; hard macros stay fixed; hierarchy nests sub-floorplans; pins land on chip edges. One idea per lab. Complete and correct on scoped instances—not a production P&R engine.

## Slide 3 — Stable module ids

Module folders use hierarchical ids: section, then algorithm slot—like module two dash zero three for B*-tree. Odd slots leave room for inserts. Treat published ids as stable keys; display order lives in the module index.

## Slide 4 — Two tracks

Every lab offers Track A—implement packing and metrics on tiny modules—and Track B—browser labs for visual intuition when shipped. A good rhythm is browser first for the geometry, then implement to harden it. Intro and wrap have no lab.

## Slide 5 — How to move

Read each README for outcomes, pick a track—or both—then work the checklist. Keep legality, deadspace, and density as your habit. When this intro checklist is done, continue to fixed-outline constraints—the gate every later packing must pass.
