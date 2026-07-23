# Simulated annealing placement

**Module id:** module02-07-sa-placement
**Lab:** sa-placement
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Simulated annealing placement

Simulated annealing jogs one cell at a time under an HPWL cost. With seed forty-two and sixty moves on the starter, best HPWL lands near forty-nine point six—modest improvement over fifty-two, not a force-style collapse.

## Slide 2 — The idea

Propose a small axis move, accept improvements always, and accept worsenings with temperature probability. Keep the best iterate, not only the final temperature. Fix the seed so your golden stays stable across runs.


## Slide 3 — Pseudocode

Placement annealing jogs one cell per move under HPWL cost, accepts by Metropolis, and keeps the best iterate—not only the final temperature.

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

## Slide 4 — Algorithm sketch

Seed forty-two with sixty moves yields best HPWL near forty-nine point six from fifty-two. Lock the seed so goldens stay stable.

```text
INPUT: positions, seed, moves, T0
OUTPUT: best positions + best HPWL
for i in 1..moves:
  jog one cell on one axis
  accept if ΔHPWL<0 or rand<e^(−Δ/T)
  keep best; cool T
GOLDEN seed=42, 60 moves → best≈49.6
accepted≈44 rejected≈16
```


<!-- algorithm-walkthrough -->

## Slide 5 — Anneal from HPWL fifty-two

![Anneal from HPWL fifty-two](assets/steps/01-starter-sa.png)

Simulated annealing jogs one cell at a time under an HPWL cost. Seed forty-two and sixty moves on the starter—deterministic teaching run.

## Slide 6 — Accept improvements; maybe worsenings

![Accept improvements; maybe worsenings](assets/steps/02-accept-reject.png)

Improvements always accept. Worsenings accept with probability exp(−Δ/T). Temperature cools each move so late stages get pickier.

## Slide 7 — Best HPWL near forty-nine point six

![Best HPWL near forty-nine point six](assets/steps/03-best-not-final.png)

With seed forty-two the best HPWL lands near forty-nine point six—modest gain over fifty-two. Report best, not only the final temperature.

## Slide 8 — Fix the seed for goldens

![Fix the seed for goldens](assets/steps/04-seed-lock.png)

Change the seed and accept/reject counts drift. Teaching labs lock seed forty-two so forty-nine point six stays a stable challenge.

## Slide 9 — SA is a stochastic local search

![SA is a stochastic local search](assets/steps/05-takeaway.png)

Propose, score, accept or reject, cool, and remember the best. On this instance expect about forty-nine point six—not a force-style collapse.

<!-- /algorithm-walkthrough -->


## Slide 10 — Browser lab track

In the browser lab track, open the **sa-placement** lab from the tools shelf. Load the starter placement, run the algorithm once, and read HPWL—and density when the panel shows it. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 11 — Implement track

In the implement track, open this module's EXAMPLES.md Pseudocode section and the course common solvers. Parse `tiny_place.json`, run the algorithm with a deterministic seed, and print coordinates plus HPWL. Match the browser goldens before you claim the checklist.

## Slide 12 — Pitfalls

Common traps: celebrating HPWL while cells pile into one bin; ignoring fixed pads A and D; mixing bbox and clique models in one report; keeping only the final SA iterate instead of the best; and forgetting that timing weights change the objective, not just the label.

## Slide 13 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you’re ready, take the short quiz, then continue to the next module.
