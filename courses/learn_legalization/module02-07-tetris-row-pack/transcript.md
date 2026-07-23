# Tetris row packing

**Module id:** module02-07-tetris-row-pack
**Lab:** tetris-row-pack
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Tetris row packing

Tetris-lite assigns each cell to its nearest row, then left-packs like overlap removal. On the overlap seed the result matches overlap removal: A at four, B at six, C at eight on row two—legal, displacement six, HPWL thirty-two.

## Slide 2 — The idea

Tetris is simpler than Abacus but moves cells farther on this toy. Contrast disp six versus Abacus disp four. Trade simpler control flow against a tighter displacement budget and slightly higher HPWL when Abacus wins movement.

<!-- algorithm-walkthrough -->

## Slide 3 — Same overlap seed

![Same overlap seed](assets/steps/01-overlap-seed.png)

Tetris-lite assigns each cell to its nearest row, then left-packs within the row—same engine as overlap removal. Start from the triple stack at (4, 2).

## Slide 4 — Nearest row, then left pack

![Nearest row, then left pack](assets/steps/02-nearest-row.png)

A, B, and C stay on middle row two after snap. Sort by x and pack: A at four, B at six, C at eight—identical to overlap removal on this instance.

## Slide 5 — Result: disp 6, HPWL 32

![Result: disp 6, HPWL 32](assets/steps/03-tetris-result.png)

Tetris legalizes with displacement six and HPWL thirty-two—the overlap-removal golden. Same coordinates, same metrics: this is the global legalize path in later labs.

## Slide 6 — Contrast Abacus disp 4

![Contrast Abacus disp 4](assets/steps/04-contrast-abacus.png)

Abacus spreads A, B, C across three rows for displacement four. Tetris keeps them on one row and moves farther in x—six total L1 units.

## Slide 7 — Tradeoff: simpler vs better displacement

![Tradeoff: simpler vs better displacement](assets/steps/05-tradeoff.png)

Tetris is easier to implement and slightly better on HPWL for this toy. Abacus is the choice when displacement budget is tight—preview the detailed-vs-global lab.

<!-- /algorithm-walkthrough -->


## Slide 8 — Browser lab track

In the browser lab track, open the **tetris-row-pack** lab from the tools shelf. Load the overlap or float starter, run the legalizer once, and read legality plus displacement and HPWL when the panel shows them. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 9 — Implement track

In the implement track, open this module's examples and the course `common/` solvers. Parse `tiny_legal.json`, run the algorithm with deterministic coordinates, and print legality, displacement, and HPWL. Match the browser goldens before you claim the checklist.

## Slide 10 — Pitfalls

Common traps: assuming snap alone legalizes; forgetting site width when checking overlap; ignoring fixed macro D at (8, 4); reporting HPWL without legality; and comparing Abacus and Tetris without naming displacement versus wirelength tradeoffs.

## Slide 11 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you're ready, take the short quiz, then continue to the next module.
