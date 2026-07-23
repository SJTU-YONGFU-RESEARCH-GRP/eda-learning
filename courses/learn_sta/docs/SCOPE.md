# Scope — learn_sta

## In scope

- Full implementations of core STA algorithms on tiny-to-small netlists
- Timing graph construction and levelization
- Forward arrival and backward required propagation
- Setup / hold slack and critical-path traceback
- Incremental invalidate / recompute after a local delay edit
- False-path and multicycle exceptions as **engine-facing data** (lite)
- Offline compare habits against open timers when available

## Out of scope (v1)

- Drop-in replacement for commercial or production OpenSTA flows
- Foundry PDK / liberty / SPEF sign-off certification
- Full SDC authoring and constraint methodology (see `learn_sdc`)
- Crosstalk / noise-on-timing deep dive (see `learn_si`)
- Vendor GUI workflows

## “Full implementation” means

Complete and correct for the **scoped problem size** (tens of cells / pins): parse input, build the graph, propagate tags, emit slack / paths, with tests—not a production-scale timer.
