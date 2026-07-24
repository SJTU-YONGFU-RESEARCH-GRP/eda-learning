# Rip-up and reroute (detailed)

**Module id:** module03-03-ripup-detailed
**Lab:** ripup-detailed
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Relieve track hotspots

When track overflow appears, detailed routers rip up contributing nets and reroute around congested tracks. Our toy pass picks the net whose route contributes the most overflow, removes its usage, then A*-reroutes.

## Slide 2 — The idea

Score each net by track overflow on its segments. Subtract its route from usage. Run astar_route between its pins with the remaining usage map. Add the new segment track usage back. Total overflow should not rise; ideally it drops versus the pre-rip state.

<!-- algorithm-walkthrough -->

## Slide 3 — Sequential first

![Sequential first](assets/steps/01-seq.png)

Route layered; tracks exceed Cap.

## Slide 4 — Pick hot net

![Pick hot net](assets/steps/02-pick.png)

Find net with worst overflow contribution.

## Slide 5 — Rip segments

![Rip segments](assets/steps/03-rip.png)

Subtract ripped net from track usage.

## Slide 6 — A* reroute

![A* reroute](assets/steps/04-astar-r.png)

Reroute ripped net with A* on updated usage.

## Slide 7 — Iterate

![Iterate](assets/steps/05-loop.png)

Real detailed routers loop route→DRC→rip until clean.

<!-- /algorithm-walkthrough -->

## Slide 8 — Browser lab track

![Browser lab starter](assets/lab-starter.png)

Open **ripup-detailed**. Run sequential L to create overflow, then one rip-up pass. Watch total overflow fall on the metrics panel.

## Slide 9 — Implement track

Implement `ripup_detailed(routes, usage, cap, terminals_map, nets, nx, ny, blocks)`. Assert total overflow after is less than or equal to before on tiny_dr sequential L seed.

## Slide 10 — Pitfalls

Ripping a net but leaving ghost usage on its old tracks. Rerouting with pattern L through the same hot track. Picking the wrong net to rip—use overflow contribution not HPWL.

## Slide 11 — Your turn

Clear rip-up challenges. Next: tie it together with full sequential detailed routing.
