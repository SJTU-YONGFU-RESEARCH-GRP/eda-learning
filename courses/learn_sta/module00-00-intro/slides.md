---
marp: true
title: Welcome to static timing analysis
paginate: true
---

# Welcome to static timing analysis

Digital chips must meet clock constraints without simulating every vector

---

## What you’ll build
- You’ll start with the timing graph and levelization
- Slack, setup, and hold follow, then critical-path traceback
- Later labs cover incremental updates after a local delay edit
- One idea per lab
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
- Track A is implement: code the algorithm, run tiny netlists, report metrics
- Track B is the browser lab shelf for visual intuition
- A good rhythm is browser first for the idea, then implement to harden it
- Intro and wrap modules have no lab
- Heavy constraint authoring lives next door in learn SDC

---

## How to move
- For each module
- Keep arrival, required, and slack as your habit
- When this intro checklist is done

