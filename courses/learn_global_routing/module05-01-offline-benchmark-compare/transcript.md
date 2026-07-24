# Offline benchmark compare

**Module id:** module05-01-offline-benchmark-compare
**Lab:** none
**Tracks:** offline harness

## Slide 1 — Why compare

Toy global routers need a harness: same JSON in, edge overflow and runtime out. Comparing L, maze, and rip-up teaches what better means beyond a pretty heat map.

## Slide 2 — The idea

Fix tiny_gr. Run sequential L-HV, maze mode, and one rip-up pass. Record total overflow, max overflow, wall time. Optionally compare to a reference router. Write one discrepancy hypothesis.

## Slide 3 — Harness shape

A small Python driver loading tiny_gr.json is enough. Print a markdown table. Missing external tools are OK—document blockers and still validate I/O.

## Slide 4 — Pitfalls

Changing edge_capacity between rows. Comparing incompatible route modes without labeling. Optimizing runtime before correctness.

## Slide 5 — Your turn

Fill one comparison table for L versus maze versus rip-up. Then open the wrap.
