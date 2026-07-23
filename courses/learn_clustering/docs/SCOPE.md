# Scope — learn_clustering

## In scope

- Full implementations of clustering / coarsening / refinement algorithms on tiny-to-medium instances
- Graph and hypergraph models used in EDA multilevel flows
- Metrics: cutsize (or hyperedge cut), balance/capacity, objective, runtime
- Offline compare habits against open tools when available

## Out of scope (v1)

- Drop-in replacement for commercial physical design tools
- Foundry PDK certification or production sign-off
- Research ML-EDA as the spine of this course
- Vendor GUI workflows

## “Full implementation” means

Complete and correct for the **scoped problem size** (tens to low hundreds of nodes/nets): parse input, run the algorithm, emit assignment + metrics, with tests—not a production-scale engine.
