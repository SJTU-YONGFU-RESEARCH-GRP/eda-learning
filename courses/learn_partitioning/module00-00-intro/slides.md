---
marp: true
title: Welcome to partitioning for EDA
paginate: true
---

# Welcome to partitioning for EDA

Physical design repeatedly asks: how do we cut a design into balanced pieces with few wires between them?

---

## What you’ll build
- You’ll start with cutsize and balance, then form an initial legal bipartition
- Classic methods follow
- Then multiway, terminal propagation, hypergraph cuts, and a multilevel V-cycle
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
- Track A is implement: code the algorithm, run tiny graphs, report metrics
- Track B is the browser lab shelf for visual intuition
- A good rhythm is browser first for the idea, then implement to harden it
- Intro and wrap modules have no lab

---

## How to move
- For each module
- Keep cutsize and balance as your habit
- When this intro checklist is done

