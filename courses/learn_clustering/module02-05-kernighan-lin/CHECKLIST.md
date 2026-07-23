# Checklist — Kernighan–Lin refinement

## Track A — Implement

- [ ] Computed seed cutsize **12** from `examples/seed_partition.json`
- [ ] Implemented (or ran) full KL with D-values, locking, and **rollback**
- [ ] Matched golden: swap **(A, D)**, cut **12 → 3**, clusters {A,B,C}/{D,E}
- [ ] `python -m unittest common.test_solvers.TestKL -v` passes (from course root)

## Track B — Browser lab (`kernighan-lin`)

- [ ] Opened the lab (local or live) — or noted Coming soon and used Track A
- [ ] Watched cumulative gain / rollback behavior (when shipped)

## Done when

- [ ] I can explain why rollback exists, and I reproduced the 12→3 golden
