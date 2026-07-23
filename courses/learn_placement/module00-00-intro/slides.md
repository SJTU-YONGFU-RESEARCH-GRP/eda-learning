---
marp: true
title: Welcome to placement for EDA
paginate: true
---

# Welcome to placement for EDA

Physical design asks: where does each cell go so wires stay short and density stays legal?

---

## What you’ll build
- Simulated-annealing place
- Density bins and spreading teach legality proxies
- Timing-driven place weights critical nets
- One algorithm per lab
- Full implementations at course scale

---

## Stable module ids
- Module folders use hierarchical ids
- That way we can add algorithms later without renumbering everything
- Odd slots leave room for inserts
- Treat published ids as stable keys; display order lives in the module index

---

## Two tracks
- Every lab module offers two practice tracks
- Track A is implement: code the algorithm, run the tiny placement, report metrics
- Track B is the browser lab shelf for visual intuition
- A good rhythm is browser first for the idea, then implement to harden it
- Intro and wrap modules have no lab

---

## How to move
- For each module
- Keep HPWL as your habit
- When this intro checklist is done

