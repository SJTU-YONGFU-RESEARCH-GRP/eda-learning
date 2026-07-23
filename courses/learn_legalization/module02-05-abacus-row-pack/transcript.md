# Abacus row packing

**Module id:** module02-05-abacus-row-pack
**Lab:** abacus-row-pack
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Abacus row packing

Abacus-lite processes cells by increasing x and tries every row. For each trial it finds the leftmost legal site and picks the row with minimum L1 displacement from the origin. On the overlap seed: A at (4, 2), B at (4, 0), C at (4, 4).

## Slide 2 — The idea

Cross-row spread beats single-row shelf pack on displacement—four versus six here—with HPWL thirty-eight versus thirty-two for Tetris. Abacus is the detailed legalizer in this course: more search, less movement.

<!-- algorithm-walkthrough -->

## Slide 3 — Start from overlap seed

![Start from overlap seed](assets/steps/01-overlap-seed.png)

Abacus-lite processes movables by increasing original x. From the same overlap seed as overlap removal, it tries each row and picks the placement with minimum L1 displacement.

## Slide 4 — Process by x: try each row

![Process by x: try each row](assets/steps/02-try-rows.png)

Cell A tries rows zero, two, four—picks row two at x four (zero displacement). B chooses row zero at x four. C chooses row four at x four. Cross-row spread beats single-row pack.

## Slide 5 — Result: A@4,2 B@4,0 C@4,4

![Result: A@4,2 B@4,0 C@4,4](assets/steps/03-abacus-result.png)

Final Abacus layout: A on middle row, B on bottom, C on top—all at x equals four but on different rows. D, E, F stay at their seed coordinates.

## Slide 6 — Lower displacement than Tetris

![Lower displacement than Tetris](assets/steps/04-vs-overlap-removal.png)

Abacus displacement is four versus six for overlap removal / Tetris on this seed. You pay three HPWL points—thirty-eight versus thirty-two—for staying closer to global targets.

## Slide 7 — Abacus minimizes movement

![Abacus minimizes movement](assets/steps/05-takeaway.png)

Abacus is the detailed legalizer in this course: try rows, pick min displacement. Use it when staying near global coordinates matters more than the last HPWL point.

<!-- /algorithm-walkthrough -->


## Slide 8 — Browser lab track

In the browser lab track, open the **abacus-row-pack** lab from the tools shelf. Load the overlap or float starter, run the legalizer once, and read legality plus displacement and HPWL when the panel shows them. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 9 — Implement track

In the implement track, open this module's examples and the course `common/` solvers. Parse `tiny_legal.json`, run the algorithm with deterministic coordinates, and print legality, displacement, and HPWL. Match the browser goldens before you claim the checklist.

## Slide 10 — Pitfalls

Common traps: assuming snap alone legalizes; forgetting site width when checking overlap; ignoring fixed macro D at (8, 4); reporting HPWL without legality; and comparing Abacus and Tetris without naming displacement versus wirelength tradeoffs.

## Slide 11 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you're ready, take the short quiz, then continue to the next module.
