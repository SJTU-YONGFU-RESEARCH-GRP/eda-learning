# learn_congestion — scope

## In scope

- GCell grid model on a tiny chip (4×2 over 12×8)
- Capacity vs demand literacy
- RUDY and probabilistic L-shape demand estimates
- Congestion heat maps and overflow metrics (total, max, count)
- Cell inflation and congestion-aware net weighting
- One-pass placement feedback (estimate → inflate → push)
- Offline compare harness on shared JSON

## Out of scope (v1)

- Production global routers / OpenROAD congestion reports as the syllabus spine
- Full rip-up-and-reroute detailed routing (see `learn_routing`)
- Vendor GUI certification
- Foundry PDK capacity tables

## Shared instance

`common/tiny_cong.json` — see `common/README.md`.
