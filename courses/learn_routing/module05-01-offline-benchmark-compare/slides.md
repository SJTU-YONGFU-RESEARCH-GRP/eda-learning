---
marp: true
title: Why compare
paginate: true
---

# Why compare

Toy detailed routers need a harness: same JSON in, track overflow and runtime out

---

## The idea
- Fix tiny_dr
- Run sequential L-HV, Lee mode, A* mode, and one rip-up pass
- Record total overflow, max overflow, wall time
- Optionally compare to a reference router
- Write one discrepancy hypothesis

---

## Harness shape
- A small Python driver loading tiny_dr.json is enough
- Print a markdown table
- Missing external tools are OK, document blockers and still validate I/O

---

## Pitfalls
- Changing track_capacity between rows
- Comparing incompatible route modes without labeling
- Optimizing runtime before correctness

---

## Your turn
- Fill one comparison table for Lee versus A* versus rip-up
- Then open the wrap

