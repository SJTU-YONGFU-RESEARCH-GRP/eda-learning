# learn_global_routing — scope

## In scope

- GCell routing graph and pin terminals on a tiny chip (4×2 over 12×8)
- L-shape and Z-shape pattern routing
- Maze routing with edge capacity (BFS)
- Multipin star tree (Steiner-lite)
- Edge overflow metrics (total, max, count)
- Rip-up and maze reroute
- Sequential global routing with ordered net deposit
- Offline compare harness on shared JSON

## Out of scope (v1)

- Production global routers / OpenROAD as the syllabus spine
- Layer assignment, via rules, and detailed DRC (see `learn_routing`)
- Vendor GUI certification
- Foundry PDK edge capacity tables

## Shared instance

`common/tiny_gr.json` — see `common/README.md`.
