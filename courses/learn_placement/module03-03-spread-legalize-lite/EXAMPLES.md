# Examples — Spreading / overlap relief

Track A (implement). Use the tiny 6-cell placement first.

## Algorithm

**pairwise spread / overlap relief**

## Starter prompts

1. Restate the algorithm in five bullets (inputs → loop → stop → output).
2. Run it on `examples/tiny_place.json` (same instance as the browser starter).
3. Compute total HPWL after the run (and density overflow when relevant).
4. Change one parameter (seed, iters, pad fix, capacity) and report what moved.
5. Name one failure mode (overlap collapse, ignored pads, metric mismatch, …).

## Expected artifacts

- Cell coordinates (or assignment) after the run
- HPWL before and after (plus density / overflow when used)
- Short note: why this algorithm belongs on the placement shelf

## Stretch

Scale to ~100 cells; keep the same API as the tiny case.
