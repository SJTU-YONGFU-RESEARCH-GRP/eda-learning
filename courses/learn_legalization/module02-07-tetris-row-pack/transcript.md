# Tetris row packing

**Module id:** module02-07-tetris-row-pack
**Lab:** tetris-row-pack
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Tetris row packing

Tetris-lite assigns each cell to its nearest row, then left-packs like overlap removal. On the overlap seed the result matches overlap removal: A at four, B at six, C at eight on row two—legal, displacement six, HPWL thirty-two.

## Slide 2 — The idea

Tetris is simpler than Abacus but moves cells farther on this toy. Contrast disp six versus Abacus disp four. Trade simpler control flow against a tighter displacement budget and slightly higher HPWL when Abacus wins movement.





## Slide 3 — Pseudocode

Tetris pseudocode is shorter than Abacus on purpose. First assign each cell to its nearest row and freeze that choice. Then reuse the per-row left pack from overlap removal.

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

## Slide 4 — Algorithm sketch

Same teaching seed, same numbers as overlap removal: displacement six, HPWL thirty-two. Write the compare line in the sketch so you remember Abacus spends search to cut displacement to four.

```text
INPUT: positions, widths, rows Y[], fixed macros
OUTPUT: legal packing (shelf / Tetris-lite)
for each movable c: y ← nearest row (freeze)
then per-row left pack (see overlap removal)
GOLDEN: A@4 B@6 C@8 on y=2; disp=6; HPWL=32
COMPARE: Abacus disp=4 (more search)
```


<!-- algorithm-walkthrough -->

## Slide 5 — Same overlap seed

![Same overlap seed](assets/steps/01-overlap-seed.png)

Tetris-lite assigns each cell to its nearest row, then left-packs within the row—same engine as overlap removal. Start from the triple stack at (4, 2).

## Slide 6 — Nearest row, then left pack

![Nearest row, then left pack](assets/steps/02-nearest-row.png)

A, B, and C stay on middle row two after snap. Sort by x and pack: A at four, B at six, C at eight—identical to overlap removal on this instance.

## Slide 7 — Result: disp 6, HPWL 32

![Result: disp 6, HPWL 32](assets/steps/03-tetris-result.png)

Tetris legalizes with displacement six and HPWL thirty-two—the overlap-removal golden. Same coordinates, same metrics: this is the global legalize path in later labs.

## Slide 8 — Contrast Abacus disp 4

![Contrast Abacus disp 4](assets/steps/04-contrast-abacus.png)

Abacus spreads A, B, C across three rows for displacement four. Tetris keeps them on one row and moves farther in x—six total L1 units.

## Slide 9 — Tradeoff: simpler vs better displacement

![Tradeoff: simpler vs better displacement](assets/steps/05-tradeoff.png)

Tetris is easier to implement and slightly better on HPWL for this toy. Abacus is the choice when displacement budget is tight—preview the detailed-vs-global lab.

<!-- /algorithm-walkthrough -->


## Slide 10 — Browser lab track

In the browser lab track, open the **tetris-row-pack** lab from the tools shelf. Open the interactive lab, place or snap cells on the site and row grid—or use an Apply helper—then Check. Reveal golden is study-only. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 11 — Implement track

In the implement track, open this module's EXAMPLES.md Pseudocode section and the course common solvers. Parse `tiny_legal.json`, run the algorithm with deterministic coordinates, and print legality, displacement, and HPWL. Match the browser goldens before you claim the checklist.

## Slide 12 — Pitfalls

Common traps: assuming snap alone legalizes; forgetting site width when checking overlap; ignoring fixed macro D at (8, 4); reporting HPWL without legality; and comparing Abacus and Tetris without naming displacement versus wirelength tradeoffs.

## Slide 13 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you're ready, take the short quiz, then continue to the next module.
