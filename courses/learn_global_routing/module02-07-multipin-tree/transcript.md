# Multi-pin tree (Steiner-lite)

**Module id:** module02-07-multipin-tree
**Lab:** multipin-tree
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — More than two pins

Real nets have many pins. A full Steiner tree is heavy; our Steiner-lite star picks the bbox-center GCell as a hub and L-routes each pin to that hub. Good enough to teach shared edge usage on the four-pin net A B C D.

## Slide 2 — The idea

Collect terminal GCells for the net. Center is the integer average of min and max column and row. For each pin, add the edges along l_route center to pin with HV unless you choose VH. Union all legs—edges shared by two legs count once in usage when you deposit.

<!-- algorithm-walkthrough -->

## Slide 3 — Four-pin net

![Four-pin net](assets/steps/01-net4.png)

Net [A,B,C,D] needs a tree, not a single two-pin path.

## Slide 4 — Bbox center

![Bbox center](assets/steps/02-center.png)

Star hub at mean GCell of pins (clamped).

## Slide 5 — Four L legs

![Four L legs](assets/steps/03-legs.png)

Each pin gets an L-route from the hub in the full sequential pass.

## Slide 6 — Shared edges

![Shared edges](assets/steps/04-usage.png)

Multi-pin trees reuse edges—overflow adds up.

## Slide 7 — Two-pin nets

![Two-pin nets](assets/steps/05-two.png)

Short nets E–F stay single L paths.

<!-- /algorithm-walkthrough -->

## Slide 8 — Browser lab track

![Browser lab starter](assets/lab-starter.png)

Open **multipin-tree**. Route the four-pin net and highlight the hub near column one row zero. Compare total edges to four separate two-pin L routes.

## Slide 9 — Implement track

Implement `multipin_star` and `multipin_star_edges`. Route net index four on tiny_gr and print hub GCell plus edge count.

## Slide 10 — Pitfalls

Routing pairwise between every pin pair— that explodes edges. Picking chip center instead of bbox center GCell. Double-depositing the same edge when summing legs—usage should increment per net once per edge traversed.

## Slide 11 — Your turn

Complete multipin routing. Next: quantify overflow on those shared edges.
