# Welcome to static timing analysis

**Module id:** module00-00-intro
**Lab:** none (intro)
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Welcome to static timing analysis

Digital chips must meet clock constraints without simulating every vector. Static timing analysis builds a timing graph, propagates arrival and required times, and reports slack—so designers know which paths fail and where to fix. This course teaches those algorithms as full implementations on tiny netlists.

## Slide 2 — What you’ll build

You’ll start with the timing graph and levelization, then propagate arrival forward and required backward. Slack, setup, and hold follow, then critical-path traceback. Later labs cover incremental updates after a local delay edit, and false-path or multicycle exceptions as data the engine consumes—not a full SDC authoring course. One idea per lab. Full implementations at course scale—not foundry throughput, but complete and correct on the scoped instances.

## Slide 3 — Stable module ids

Module folders use hierarchical ids: section, then algorithm slot—like module two dash zero one for slack. That way we can add algorithms later without renumbering everything. Odd slots leave room for inserts. Treat published ids as stable keys; display order lives in the module index.

## Slide 4 — Two tracks

Every lab module offers two practice tracks. Track A is implement: code the algorithm, run tiny netlists, report metrics. Track B is the browser lab shelf for visual intuition. A good rhythm is browser first for the idea, then implement to harden it. Intro and wrap modules have no lab. Heavy constraint authoring lives next door in learn SDC.

## Slide 5 — How to move

For each module, read the README for outcomes, pick a track—or both—then work the checklist. Keep arrival, required, and slack as your habit. When this intro checklist is done, continue to the timing graph—the shared language every later algorithm will use.
