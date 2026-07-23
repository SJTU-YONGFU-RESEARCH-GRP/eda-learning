# Detailed versus global legalize

**Module id:** module04-01-detailed-vs-global
**Lab:** detailed-vs-global
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Detailed versus global legalize

Global legalize lite maps to Tetris shelf pack—displacement six, HPWL thirty-two. Detailed legalize lite maps to Abacus—displacement four, HPWL thirty-eight. Both are legal on the overlap seed; metrics pick the winner.

## Slide 2 — The idea

Pick global Tetris when you want a fast pass and can afford extra movement. Pick detailed Abacus when displacement budget is tight. Report both pipelines side by side in regressions—legal first, then disp and HPWL.





## Slide 3 — Pseudocode

Here the sketch is two named pipelines on the same seed. Global legalize lite means Tetris. Detailed legalize lite means Abacus. Pseudocode names both so regressions do not mix the labels.

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

## Slide 4 — Algorithm sketch

Both pipelines must end legal. Then compare displacement six versus four and HPWL thirty-two versus thirty-eight. Pick detailed when movement budget is tight; pick global when speed matters more.

```text
INPUT: illegal / global positions
global:   TetrisLite → disp=6 HPWL=32
detailed: AbacusLite → disp=4 HPWL=38
both must report legal=true
CHOOSE detailed when disp budget is tight
CHOOSE global when a fast shelf pack is enough
```


<!-- algorithm-walkthrough -->

## Slide 5 — Global = Tetris, disp 6

![Global = Tetris, disp 6](assets/steps/01-global-tetris.png)

Global legalize lite maps to Tetris-style nearest-row shelf pack. On the overlap seed it legalizes with displacement six and HPWL thirty-two.

## Slide 6 — Detailed = Abacus, disp 4

![Detailed = Abacus, disp 4](assets/steps/02-detailed-abacus.png)

Detailed legalize lite maps to Abacus row trial. Same seed, both legal—but displacement drops to four by spreading A, B, C across rows.

## Slide 7 — Both pipelines legal

![Both pipelines legal](assets/steps/03-both-legal.png)

Global and detailed both pass legality on the overlap seed. The difference is how far cells move and how HPWL shifts—thirty-two versus thirty-eight here.

## Slide 8 — Side-by-side metrics

![Side-by-side metrics](assets/steps/04-side-by-side.png)

Global Tetris: disp six, HPWL thirty-two. Detailed Abacus: disp four, HPWL thirty-eight. Neither dominates on both axes—pick by your displacement budget.

## Slide 9 — Pick detailed when displacement is tight

![Pick detailed when displacement is tight](assets/steps/05-pick-detailed.png)

Production flows often run a fast global legalize, then a detailed pass when timing or continuity needs cells near global targets. On this toy, that is Abacus over Tetris.

<!-- /algorithm-walkthrough -->


## Slide 10 — Browser lab track

In the browser lab track, open the **detailed-vs-global** lab from the tools shelf. Open the interactive lab, place or snap cells on the site and row grid—or use an Apply helper—then Check. Reveal golden is study-only. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 11 — Implement track

In the implement track, open this module's EXAMPLES.md Pseudocode section and the course common solvers. Parse `tiny_legal.json`, run the algorithm with deterministic coordinates, and print legality, displacement, and HPWL. Match the browser goldens before you claim the checklist.

## Slide 12 — Pitfalls

Common traps: assuming snap alone legalizes; forgetting site width when checking overlap; ignoring fixed macro D at (8, 4); reporting HPWL without legality; and comparing Abacus and Tetris without naming displacement versus wirelength tradeoffs.

## Slide 13 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you're ready, take the short quiz, then continue to the next module.
