---
marp: true
title: Why compare
paginate: true
---

# Why compare

Toy estimators need a harness: same JSON in, overflow and runtime out

---

## The idea
- Fix the instance
- Run RUDY and probabilistic
- Record total overflow, max overflow, wall time
- Optionally compare to a reference map
- Write one discrepancy hypothesis

---

## Harness shape
- A small Python driver loading tiny_cong.json is enough
- Print a markdown table
- Missing external tools are OK, document blockers and still validate I/O

---

## Pitfalls
- Changing Cap between rows of the table
- Comparing incompatible demand units
- Optimizing runtime before correctness

---

## Your turn
- Fill one comparison table for spread versus congested seeds
- Then open the wrap

