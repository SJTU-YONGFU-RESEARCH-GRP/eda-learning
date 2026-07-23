# Scope — learn_placement

## In scope

- Full implementations of global placement algorithms on a tiny-to-medium instance
- Metrics: HPWL (bbox), clique/star net models, density bins / overflow
- Fixed pads, analytical density spreading, timing-weighted objectives
- Offline compare habits against open tools when available

## Out of scope (v1)

- Drop-in replacement for commercial or OpenROAD production placers
- Foundry PDK certification or production sign-off
- Detailed legalization / row-site snapping as the spine (see `learn_legalization`)
- Vendor GUI workflows

## “Full implementation” means

Complete and correct for the **scoped problem size** (handful of cells/nets → low hundreds): parse input, run the algorithm, emit coordinates + metrics, with tests—not a production-scale engine.
