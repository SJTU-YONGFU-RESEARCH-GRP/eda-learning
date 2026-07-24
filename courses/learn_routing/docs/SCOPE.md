# learn_routing — scope

## In scope

- M1/M2 routing grid and pin access on a tiny chip (12×8)
- Lee maze routing around blockages (BFS on cells)
- A* detailed routing with track capacity penalties
- Track usage and overflow metrics (total, max, count)
- Two-layer via assignment on L-shaped paths
- DRC spacing lite (parallel same-layer distance)
- Rip-up and A* reroute on track usage
- Sequential detailed routing with ordered net deposit
- Offline compare harness on shared JSON

## Out of scope (v1)

- Production detailed routers / OpenROAD as the syllabus spine
- Full foundry DRC decks and antenna rules
- Vendor GUI certification
- Multi-cut via rules and advanced layer stacks

## Shared instance

`common/tiny_dr.json` — see `common/README.md`.
