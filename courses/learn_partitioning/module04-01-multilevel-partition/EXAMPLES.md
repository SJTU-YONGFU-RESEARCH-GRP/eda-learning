# Examples — Multilevel partitioning

Track A (implement). Use tiny graphs first (8–30 nodes).

## Algorithm

**multilevel coarsen / initial / uncoarsen / refine**

## Starter prompts

1. Restate the algorithm in five bullets (inputs → loop → stop → output).
2. Run it on the 5-node weighted graph in `examples/tiny_graph.json` (create if missing).
3. Compute cutsize and balance after the run.
4. Change one parameter (seed, k, balance tolerance) and report what moved.
5. Name one failure mode (imbalance, local minimum, ignored terminals, …).

## Expected artifacts

- Partition assignment per node
- Cutsize and balance before and after
- Short note: why this algorithm belongs on the partitioning shelf

## Stretch

Scale to ~100 nodes; keep the same API as the tiny case.
