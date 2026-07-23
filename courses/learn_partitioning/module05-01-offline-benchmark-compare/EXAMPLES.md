# Examples — Offline benchmark compare

1. Export the same graph/netlist used in multilevel / hypergraph modules.
2. Run your toy partitioner; record cutsize, balance, wall time.
3. If available, run an open tool (e.g. KaHyPar / Metis-style flow) on the same instance.
4. Fill a comparison table: quality, balance, runtime, notes.
5. If the external tool is missing, document install blockers and still validate your harness I/O.
