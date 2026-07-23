---
marp: true
title: Welcome to clustering for EDA
paginate: true
---

# Welcome to clustering for EDA

Physical design engines almost never optimize a flat million-cell problem in one shot

---

## What you’ll build
- Fiduccia–Mattheyses
- Then multilevel and hypergraph models, then congestion- and timing-aware objectives
- One algorithm per lab
- Full implementations at course scale

---

## Stable module ids
- Module folders use hierarchical ids
- That way we can add algorithms later without renumbering everything
- Odd slots are reserved so inserts stay clean
- Treat published ids as stable keys; display order lives in the module index

---

## Two tracks
- Every lab module offers two practice tracks
- Track A is implement: code the algorithm, run tiny graphs, report metrics
- Track B is the browser lab shelf
- A good rhythm is browser first for the idea, then implement to harden it
- Intro and wrap modules have no lab

---

## How to move
- For each module
- Keep cutsize, balance, and objective as your habit
- When this intro checklist is done

