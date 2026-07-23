# Scope — learn_floorplanning

## In scope

- Fixed-outline floorplanning (W×H chip) and legal packing checks
- Area, packing density, and deadspace (= outlineArea − Σ module areas)
- Slicing tree / polish expression packing
- B*-tree and sequence-pair representations
- Simulated annealing search over floorplan moves
- Soft module aspect sizing and hard macro / fixed-block constraints
- Hierarchical sub-floorplans and boundary pin / I/O assignment
- Offline compare habits on shared tiny instances

## Out of scope (v1)

- Production place-and-route engines or foundry sign-off
- Vendor GUI workflows (Innovus / ICC2 click-paths)
- Detailed standard-cell placement and row legalization (see `learn_placement`, `learn_legalization`)
- Full chip packaging / substrate codesign

## “Full implementation” means

Complete and correct for the **scoped problem size** (a handful of modules on a tiny outline): parse input, pack or search, emit coordinates + metrics—not a production-scale floorplanner.
