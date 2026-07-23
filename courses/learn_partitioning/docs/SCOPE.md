# Scope — learn_partitioning

## In scope

- Full implementations of bipartition and multiway partitioning algorithms on tiny-to-medium instances
- Metrics: edge cutsize, hyperedge cut, balance / part sizes
- Terminal / fixed-node constraints and multilevel V-cycles
- Offline compare habits against open tools when available

## Out of scope (v1)

- Drop-in replacement for commercial partitioners (hMETIS / KaHyPar production)
- Foundry PDK certification or production sign-off
- Clustering affinities as the spine (see `learn_clustering`)
- Vendor GUI workflows

## “Full implementation” means

Complete and correct for the **scoped problem size** (tens to low hundreds of nodes/nets): parse input, run the algorithm, emit assignment + metrics, with tests—not a production-scale engine.
