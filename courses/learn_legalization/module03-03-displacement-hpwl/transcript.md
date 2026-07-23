# Displacement versus HPWL

**Module id:** module03-03-displacement-hpwl
**Lab:** displacement-hpwl
**Tracks:** A (implement) · B (browser lab)

## Slide 1 — Displacement versus HPWL

Legalization cost combines HPWL and displacement: cost equals HPWL plus lambda times displacement from the pre-legalize layout. Abacus on the overlap seed reports HPWL thirty-eight and displacement four.

## Slide 2 — The idea

Lambda one gives cost forty-two; lambda five gives cost fifty-eight on the same legal Abacus result. Higher lambda favors staying near global placement even when wirelength could be slightly better under a different packer.





## Slide 3 — Pseudocode

This module’s pseudocode is a cost function, not a packer. After you have a legal layout, compute displacement and HPWL, then combine them with lambda.

Open this module's examples file and find the Pseudocode section. That written sketch is what you implement on the implement track and what the browser challenges measure.

## Slide 4 — Algorithm sketch

Plug in the Abacus goldens: thirty-eight plus lambda times four. Lambda one costs forty-two; lambda five costs fifty-eight. Higher lambda means the sketch favors staying near the global place.

```text
INPUT: legal positions, origin, nets, λ≥0
OUTPUT: cost, HPWL, disp
disp ← Σ|Δx|+|Δy| vs origin
HPWL ← Σ net bbox (cell centers)
cost ← HPWL + λ · disp
GOLDEN Abacus: HPWL=38 disp=4
  λ=1 → 42;  λ=5 → 58
```


<!-- algorithm-walkthrough -->

## Slide 5 — Cost = HPWL + λ · displacement

![Cost = HPWL + λ · displacement](assets/steps/01-cost-formula.png)

Legalization objectives often combine wirelength with a displacement penalty from the pre-legalize layout. Lambda controls how hard you resist moving cells away from global placement.

## Slide 6 — Abacus vs overlap origin

![Abacus vs overlap origin](assets/steps/02-abacus-metrics.png)

Abacus on the overlap seed yields HPWL thirty-eight and displacement four versus the illegal starter. That is the Pareto point with lower movement.

## Slide 7 — λ = 1 → cost 42

![λ = 1 → cost 42](assets/steps/03-lambda-1.png)

With lambda one, cost equals thirty-eight plus four equals forty-two. Displacement is cheap—one HPWL point buys one unit of movement in the objective.

## Slide 8 — λ = 5 → cost 58

![λ = 5 → cost 58](assets/steps/04-lambda-5.png)

Raise lambda to five: cost becomes thirty-eight plus five times four equals fifty-eight. The same legal layout looks expensive when you punish displacement heavily.

## Slide 9 — Higher λ favors staying put

![Higher λ favors staying put](assets/steps/05-lambda-tradeoff.png)

When lambda is large, algorithms that minimize displacement—Abacus over Tetris—win the combined cost even if HPWL is slightly worse. Quote λ whenever you compare legalizers.

<!-- /algorithm-walkthrough -->


## Slide 10 — Browser lab track

In the browser lab track, open the **displacement-hpwl** lab from the tools shelf. Open the interactive lab, place or snap cells on the site and row grid—or use an Apply helper—then Check. Reveal golden is study-only. Work the challenges that lock the goldens, then come back to implement the same loop yourself.

## Slide 11 — Implement track

In the implement track, open this module's EXAMPLES.md Pseudocode section and the course common solvers. Parse `tiny_legal.json`, run the algorithm with deterministic coordinates, and print legality, displacement, and HPWL. Match the browser goldens before you claim the checklist.

## Slide 12 — Pitfalls

Common traps: assuming snap alone legalizes; forgetting site width when checking overlap; ignoring fixed macro D at (8, 4); reporting HPWL without legality; and comparing Abacus and Tetris without naming displacement versus wirelength tradeoffs.

## Slide 13 — Your turn

Complete the checklist for at least one track—preferably both. Implement until your metrics match the starter goldens. When you're ready, take the short quiz, then continue to the next module.
