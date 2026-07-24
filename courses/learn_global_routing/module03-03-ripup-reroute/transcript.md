# Rip-up and reroute

**Module id:** module03-03-ripup-reroute
**Lab:** ripup-reroute
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Relieve hotspots

When overflow appears, global routers rip up contributing nets and reroute around congested edges. Our toy pass picks the net whose edges contribute the most overflow, removes its usage, then maze-reroutes.

## Slide 2 — The idea

Score each net by overflow on its edges. Subtract its route from usage. Run maze_route between its pins with the remaining usage map. Add the new edges back. Total overflow should not rise; ideally it drops versus the pre-rip state.

<!-- algorithm-walkthrough -->

## Slide 3 — Sequential L first

![Sequential L first](assets/steps/01-seq.png)

Route L-HV; some edges exceed Cap.

## Slide 4 — Pick hot edge

![Pick hot edge](assets/steps/02-pick.png)

Find worst overflowing edge; mark nets using it.

## Slide 5 — Rip nets

![Rip nets](assets/steps/03-rip.png)

Remove those nets from usage.

## Slide 6 — Maze reroute

![Maze reroute](assets/steps/04-maze-r.png)

Ripped nets maze-route with updated usage.

## Slide 7 — Iterate

![Iterate](assets/steps/05-loop.png)

Real routers loop estimate→route→rip until clean or budget.

<!-- /algorithm-walkthrough -->

## Slide 8 — Browser lab track

![Browser lab starter](assets/lab-starter.png)

Open **ripup-reroute**. Run sequential L to create overflow, then one rip-up pass. Watch total overflow fall on the metrics panel.

## Slide 9 — Implement track

Implement `ripup_reroute(routes, usage, capacity, nets, term, nx, ny)`. Assert total overflow after is less than or equal to before on tiny_gr sequential L seed.

## Slide 10 — Pitfalls

Ripping a net but leaving ghost usage on its old edges. Rerouting with pattern L through the same hot edge. Picking the wrong net to rip—use overflow contribution not HPWL.

## Slide 11 — Your turn

Clear rip-up challenges. Next: tie it together with full sequential global routing.
